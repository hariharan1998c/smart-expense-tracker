from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import sqlite3
import matplotlib.pyplot as plt
import json, re
from flask import send_file

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
    model = genai.GenerativeModel("gemini-pro")
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

    plt.figure(figsize=(8, 5))  # Increase figure size
    plt.bar(categories, amounts, color="skyblue")
    plt.xlabel("Category")
    plt.ylabel("Amount Spent (Rs)")
    plt.title("Expense Analysis")
    
    plt.xticks(rotation=45, ha="right")  # Rotate category labels
    plt.tight_layout()  # Adjust spacing to prevent label cutoff

    plt.savefig("static/expense_chart.png")
    plt.close()

    return send_file("static/expense_chart.png", mimetype="image/png") # jsonify({"success": True, "chart_url": "/static/expense_chart.png"})


# if __name__ == "__main__":
#     app.run(debug=True) # Flask syntax

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Get PORT from Render
    app.run(host="0.0.0.0", port=port)  # Allow external access

