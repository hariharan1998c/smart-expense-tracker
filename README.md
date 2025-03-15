# Smart Expense Tracker with WhatsApp Integration

## 📌 Introduction
Managing expenses can be challenging. **Smart Expense Tracker** is a powerful yet simple web app that helps users efficiently track their spending through two modes:

✅ **Web Interface** for direct expense input and visualization.  
✅ **WhatsApp Bot Integration** for fast expense logging and instant report delivery.

Using **Google Gemini API**, the system extracts structured financial data from natural language inputs like:  
> *"I spent ₹100 on groceries"*  

All expenses are stored in an **SQLite database** and visualized with **bar and pie charts** for clear insights.

### 🌐 Live Demo: [Smart Expense Tracker](https://smart-expense-tracker-7xwa.onrender.com/) 
(Wait ~30 sec for initial load as Render may take time after inactivity.)

---

## 2. Key Features
✅ **Easy Expense Logging:** Enter expenses using natural language.  
✅ **WhatsApp Bot Integration:** Log expenses and receive summary reports directly on WhatsApp.  
✅ **Visual Reports:** Bar and pie charts provide clear insights into spending patterns.  
✅ **Database Storage:** All data is securely stored in an **SQLite database**.  
✅ **AI Integration:** Uses **Google Gemini API** for accurate expense extraction.  
✅ **Cloud Deployment:** Hosted on **Render** for real-time accessibility.  

---

## 3. User Interface Screenshots

### 🔹 Web Interface for Logging Expenses
<p align="center">
  <img src="https://github.com/user-attachments/assets/10a0c5dd-4250-49d9-8d17-4c1b4388d12f" width="400px">
</p>

### 🔹 WhatsApp Bot for Quick Expense Logging
<p align="center">
  <img src="https://github.com/user-attachments/assets/fa53cfca-4fe8-4881-8702-7ca737ad20e1" width="400px">
</p>
---

## 4. How to Use the WhatsApp Bot

1️⃣ Send a WhatsApp message to: **+1 415 523 8886**  
2️⃣ In the message body, type:  
```
join tall-across
```
3️⃣ Once connected, log expenses by messaging text like:  
```
I spent 50rs on coffee
```
4️⃣ Receive a confirmation message and a visual expense summary (bar and pie chart) in return.  

---
## 5. How to Use the Web App

1️⃣ Visit the web app.

2️⃣ Enter your expense in the input field (e.g., "I spent 50rs on coffee").

3️⃣ Click the **Submit** button to log the expense.

4️⃣ The **bar chart and pie chart** will update automatically.

## 6. Tools & Technologies Used
- **Programming Languages:** Python, JavaScript  
- **Frameworks & Libraries:** Flask, SQLite, Matplotlib  
- **API Integration:** Google Gemini API for NLP  
- **WhatsApp Integration:** Twilio API  
- **Deployment:** Render (for web hosting)  

---

## 7. Installation & Setup

### 🔹 Prerequisites
- **Python 3+**  
- **pip** (Python package manager)  
- **Git**  

### 🔹 Steps to Set Up the Project Locally

1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/your-repo/smart-expense-tracker.git
cd smart-expense-tracker
```

2️⃣ **Install Dependencies**  
```bash
pip install -r requirements.txt
```

3️⃣ **Set Up API Keys**  
- Go to [AI Studio](https://aistudio.google.com/) and generate a Google Gemini API key.  
- Sign up at [Twilio](https://www.twilio.com/) and get your **Account SID**, **Auth Token**, and **WhatsApp Number**.  
- Store these keys in a `.env` file:  
```bash
GEMINI_API_KEY=your_gemini_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:your_twilio_whatsapp_number
```

4️⃣ **Run the Application Locally**  
```bash
python app.py
```
The server should start at: **http://127.0.0.1:5000/**  

5️⃣ **Running on Render (Cloud Deployment)**  
Ensure your Flask app listens on the correct port:
```python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
```

---


## 8. API Endpoints

| **Endpoint**        | **Method** | **Description** |
|---------------------|------------|---------------|
| `/`                | GET        | Loads the homepage (index.html). |
| `/add_expense`     | POST       | Takes user input, processes it with Gemini API, and stores the structured data in the database. |
| `/expense_chart`   | GET        | Generates a bar chart and pie chart of expenses. |
| `/whatsapp`        | POST       | Handles WhatsApp messages, adds expenses, and sends back a summary. |

---

## 9. Future Enhancements
🔹 **AI-driven Insights:** Personalized financial advice based on spending habits.  
🔹 **Multi-User Support:** Users can create accounts and manage expenses individually.  
🔹 **Advanced Analytics:** Detailed reports for improved financial planning.  

---

## 10. Conclusion
The **Smart Expense Tracker** combines web and WhatsApp functionality to simplify expense management. With AI-powered data extraction, secure database storage, and visual insights, it empowers users to manage their money effectively. Future enhancements aim to provide personalized insights, making it a comprehensive financial assistant.

---

## 📌 Final Notes
- Contributions are welcome!  
- Feel free to submit issues or feature requests.  
- Feedback is highly appreciated. 🚀

