from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import sqlite3
import matplotlib.pyplot as plt
import json, re
from flask import send_file
import os
from twilio.rest import Client
from pymongo import MongoClient

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Configure MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.expense_tracker  # Reference to a database (not created yet for the first time)
expenses_collection = db.expenses # Reference to a collection (not created yet for the first time)


app = Flask(__name__) # Flask syntax

# # Initialize SQLite DB  ==> now using mongoDB for better
# def init_db():
#     conn = sqlite3.connect("expenses.db") # establishing connection wrt database named expense.db
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS expenses (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             phone_number TEXT,
#             description TEXT,
#             price REAL,
#             category TEXT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     ''')
#     conn.commit()
#     conn.close()

# init_db()


# Function to extract structured (dictionary format) expense data from text input
def extract_expense_data(text):
    model = genai.GenerativeModel("gemini-1.5-flash-latest") # API call to gemini
    response = model.generate_content(f"""Extract structured data from the following expense text. Return only a JSON object with:
- "price" (numerical value of the expense in Rupees)
- "category" (best matching category of the expense)

Use predefined standard categories from this list: 
["Food", "Transport", "Groceries", "Utilities", "Entertainment", "Shopping", "Healthcare", "Education", "Miscellaneous"].  
If no suitable category matches, use "Miscellaneous".
                                      
Ensure the response is valid JSON with no extra text.

Expense text: {text}""") # API call to gemini # sending a prompt
    
    print(text, response)
    # Extract the text part from response
    raw_text = response.candidates[0].content.parts[0].text  
    # Remove triple backticks (if present)
    clean_text = re.sub(r"```JSON|```|\bjson\b", "", raw_text, flags=re.IGNORECASE).strip()
    print(clean_text)
    try:
        expense_data = json.loads(clean_text)  # Convert JSON string to dictionary
        print(expense_data)  # Output: {'price': '20', 'category': 'panipuri'}
        return expense_data
    except :
        print("Error: Could not parse JSON")
        return None


# Route: Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Route: Process Expense Input from UI
@app.route("/add_expense", methods=["POST"])
def add_expense(): # handles POST request from url localhost:5000/add_expense
    data = request.json
    text = data.get("text", "") # I spend 20rs on diary milk

    expense_data = extract_expense_data(text) # do api call to gemini and get a dictionary result
    # text is string | Eg. I spend 20rs on diary milk
    # expense_data is dict | Eg. {'price': '20', 'category': 'food'}

    if expense_data:
        expense_data["description"] = text
        expenses_collection.insert_one(expense_data)
        expense_data["_id"] = str(expense_data["_id"])  # Convert ObjectId to string for JSONify
        return jsonify({"success": True, "message": "Expense added!"})
    
    return jsonify({"success": False, "message": "Failed to extract expense data"})



import matplotlib
matplotlib.use('Agg')  # Fixes Tkinter issue
# Route: Generate Expense Analysis Chart
@app.route("/expense_chart")
def expense_chart():
    data = list(expenses_collection.aggregate([
        {"$group": {"_id": "$category", "price_sum": {"$sum": "$price"}}}
    ]))

    if not data:
        return jsonify({"success": False, "message": "No expense data available"})
    
    # Create bar chart
    categories = [row["_id"] for row in data]
    amounts = [row["price_sum"] for row in data]
    # Create figure with 2 subplots
    fig, subplt = plt.subplots(1, 2, figsize=(10, 5))

    # Colors for chart
    colors = ['#02ffdd', '#00ff00', '#0000ff', '#ffff00'] # HEXADECIMAL VALUE FOR COLOR

    # Bar Chart with Price Labels
    bars = subplt[0].bar(categories, amounts, color=colors)
    subplt[0].set_xlabel("Category")
    subplt[0].set_ylabel("Amount Spent (Rs)")
    subplt[0].set_title("Expense Breakdown")
    subplt[0].tick_params(axis='x', rotation=45)

    # Add price labels above bar chart
    for bar in bars:
        height = bar.get_height()  # Get value of each bar
        subplt[0].text(
            bar.get_x() + bar.get_width() / 2,  # Center text above the bar
            height,  
            f"₹{height}", 
            ha='center', va='bottom'
        )

    subplt[1].pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors)
    subplt[1].set_title("Expense Distribution")

    # Add watermark
    fig.text(0.99, 0.01, "Developed by Hariharan C", fontsize=15, color="gray", ha="right", alpha=0.5)
    
    plt.tight_layout()  # Automatically fixes spacing issues

    plt.savefig("static/expense_chart.png")
    plt.close()

    return send_file("static/expense_chart.png", mimetype="image/png")





#### whatsapp integration

# Configure Twilio
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio Sandbox Number

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Function to generate and send the expense chart to the sender
def generate_and_send_chart(user_number):
    data = list(expenses_collection.aggregate([
    {"$match": {"phone_number": user_number}},  # Filter by phone_number
    {"$group": {"_id": "$category", "price_sum": {"$sum": "$price"}}}  # Group by category & sum price
    ]))

    if not data:
        return jsonify({"success": False, "message": "No expense data available"})
    
    # Create bar chart
    categories = [row["_id"] for row in data]
    amounts = [row["price_sum"] for row in data]

    fig, subplt = plt.subplots(1, 2, figsize=(10, 5))
    colors = ['#02ffdd', '#00ff00', '#0000ff', '#ffff00']

    # Bar Chart with Price Labels
    bars = subplt[0].bar(categories, amounts, color=colors)
    subplt[0].set_xlabel("Category")
    subplt[0].set_ylabel("Amount Spent (Rs)")
    subplt[0].set_title("Expense Breakdown")
    subplt[0].tick_params(axis='x', rotation=45)

    # Add price labels above bars
    for bar in bars:
        height = bar.get_height()  # Get value of each bar
        subplt[0].text(
            bar.get_x() + bar.get_width() / 2,  # Center text above the bar
            height,  
            f"₹{height}", 
            ha='center', va='bottom'
        )

    subplt[1].pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors)
    subplt[1].set_title("Expense Distribution")

    # Add watermark
    fig.text(0.99, 0.01, "Developed by Hariharan C", fontsize=15, color="gray", ha="right", alpha=0.5)
    
    plt.tight_layout()
    chart_path = "static/expense_chart.png"
    plt.savefig(chart_path)
    plt.close()

    # Host the image on Render
    hosted_image_url = "https://smart-expense-tracker-production-b185.up.railway.app/static/expense_chart.png"

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
        expense_data["description"] = incoming_msg
        expense_data["phone_number"] = sender_number
        expenses_collection.insert_one(expense_data)

        # Generate and send the expense chart to the sender
        generate_and_send_chart(sender_number)

        return "Expense added! Chart sent to WhatsApp.", 200

    return "Failed to extract expense data.", 400



# if __name__ == "__main__":
#     app.run(debug=True) # Flask syntax

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Get PORT from Render
    app.run(host="0.0.0.0", port=port)  # Allow external access
