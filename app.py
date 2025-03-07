from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import sqlite3
import matplotlib.pyplot as plt
import json, re
from flask import send_file
import os
from twilio.rest import Client

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__) # Flask syntax

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect("expenses.db") # establishing connection wrt database named expense.db
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            price REAL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Function to extract structured expense data
def extract_expense_data(text):
    """Send text to Gemini API and extract structured data."""
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(f"""Extract structured data from the following expense text. Return only a JSON object with:
- "price" (numerical value of the expense)
- "category" (best matching category of the expense)

Ensure the response is valid JSON with no extra text.

Expense text: {text}""") # API call to gemini # sending a prompt
    print(text, response)
    # Extract the text part from response
    raw_text = response.candidates[0].content.parts[0].text  
    # Remove triple backticks (if present)
    clean_text = re.sub(r"```JSON|```|\bjson\b", "", raw_text, flags=re.IGNORECASE).strip()
    # Convert to dictionary
    print(clean_text)
    try:
        expense_data = json.loads(clean_text)  # Convert JSON string to dictionary
        print(expense_data)  # Output: {'price': '20', 'category': 'panipuri'}
        return expense_data
    except :
        print("Error: Could not parse JSON")
        return None
    try:
        data = eval(response.text)  # Convert response to dictionary
        return data
    except:
        return None

# Route: Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Route: Process Expense Input
@app.route("/add_expense", methods=["POST"])
def add_expense(): # handles POST request from url localhost:5000/add_expense
    data = request.json
    text = data.get("text", "") # I spend 20rs on diary milk

    expense_data = extract_expense_data(text) # get api call and get a dictionary result

    if expense_data:
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (description, price, category) VALUES (?, ?, ?)",
                       (text, expense_data["price"], expense_data["category"]))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Expense added!", "data": expense_data})
    
    return jsonify({"success": False, "message": "Failed to extract expense data"})

# Route: Generate Expense Analysis Chart
@app.route("/expense_chart")
def expense_chart():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(price) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data:
        return jsonify({"success": False, "message": "No expense data available"})

    # Create bar chart
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    fig, subplt = plt.subplots(1, 2, figsize=(10, 5))

    # Colors for consistency
    colors = ['#02ffdd', '#00ff00', '#0000ff', '#ffff00']

    # Bar chart
    subplt[0].bar(categories, amounts, color=colors)
    subplt[0].set_xlabel("Category")
    subplt[0].set_ylabel("Amount Spent (Rs)")
    subplt[0].set_title("Expense Breakdown")
    subplt[0].tick_params(axis='x', rotation=45)

    # Pie chart
    subplt[1].pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors)
    subplt[1].set_title("Expense Distribution")
    plt.tight_layout()  # Adjust spacing to prevent label cutoff

    plt.savefig("static/expense_chart.png")
    plt.close()

    return send_file("static/expense_chart.png", mimetype="image/png") # jsonify({"success": True, "chart_url": "/static/expense_chart.png"})







#### whatsapp integration

# Configure Twilio
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio Sandbox Number

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Function to generate and send the expense chart to the sender
def generate_and_send_chart(user_number):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(price) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data:
        return None

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    fig, subplt = plt.subplots(1, 2, figsize=(10, 5))
    colors = ['#02ffdd', '#00ff00', '#0000ff', '#ffff00']

    subplt[0].bar(categories, amounts, color=colors)
    subplt[0].set_xlabel("Category")
    subplt[0].set_ylabel("Amount Spent (Rs)")
    subplt[0].set_title("Expense Breakdown")
    subplt[0].tick_params(axis='x', rotation=45)

    subplt[1].pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors)
    subplt[1].set_title("Expense Distribution")
    
    plt.tight_layout()
    chart_path = "static/expense_chart.png"
    plt.savefig(chart_path)
    plt.close()

    # Host the image on your Render deployment (update the URL accordingly)
    hosted_image_url = "https://smart-expense-tracker-7xwa.onrender.com/static/expense_chart.png"

    # Send the image to the same user who sent the expense message
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=user_number,
        body="📊 Here is your updated expense summary!",
        media_url=hosted_image_url
    )

    return chart_path

# Route: Process Expense Input from WhatsApp user
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip() # I spend 20rs on diary milk
    sender_number = request.values.get("From", "")  # Get sender's WhatsApp number: eg: 824874

    # Extract expense details as dict using gemini API
    expense_data = extract_expense_data(incoming_msg)

    if expense_data:
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (description, price, category) VALUES (?, ?, ?)",
                       (incoming_msg, expense_data["price"], expense_data["category"]))
        conn.commit()
        conn.close()

        # Generate and send the expense chart to the sender
        generate_and_send_chart(sender_number)

        return "Expense added! Chart sent to WhatsApp.", 200

    return "Failed to extract expense data.", 400



# if __name__ == "__main__":
#     app.run(debug=True) # Flask syntax

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Get PORT from Render
    app.run(host="0.0.0.0", port=port)  # Allow external access
