# Smart Expense Tracker

## 📌 Introduction
Smart Expense Tracker is a web-based application that helps users track their daily expenses effortlessly. It utilizes **Google Gemini API** to extract structured financial data from natural language inputs (e.g., *"I spent ₹100 on lunch"*). The application stores expense details in an **SQLite database** and provides **visual insights** through **bar and pie charts**.

### 🖥 Live Demo: [Smart Expense Tracker](https://smart-expense-tracker-7xwa.onrender.com/)

---

## 2. Features
✔ **Expense Logging:** Enter expenses in natural language, and the system extracts the details automatically.  
✔ **Database Storage:** Expenses are categorized and stored in an **SQLite database**.  
✔ **Visual Reports:** Bar and pie charts help users analyze spending habits.  
✔ **User-Friendly Interface:** A simple and interactive web UI for managing expenses.  
✔ **Deployment:** Hosted on **Render** for real-time accessibility.  
✔ **Future Enhancement:** Integration of a **WhatsApp bot** for seamless expense tracking via chat.  

---

## 3. User Interface
Below is a screenshot of the web interface:

<p align="center">
  <img src="https://github.com/user-attachments/assets/e5a525fb-d1fb-4d62-92d3-7d8f10f50a70" width="400px">
</p>


The UI consists of:  
✅ **Input Field:** Users enter expenses in natural language.  
✅ **Submit Button:** Processes the expense and saves it.  
✅ **Expense Chart:** Displays spending distribution using **bar and pie charts**.  

---

## 4. Tools & Technologies Used
- **Programming Languages:** Python, JavaScript  
- **Frameworks & Libraries:** Flask, SQLite, Matplotlib, Chart.js  
- **API Integration:** Google Gemini API for text processing  
- **Frontend:** HTML, CSS, JavaScript  
- **Deployment:** Render (for cloud hosting)  

---

## 5. Installation & Setup

### 🔹 Prerequisites
Ensure you have the following installed on your system:  
- **Python 3+**  
- **pip (Python package manager)**  
- **Git**  

### 🔹 Steps to Set Up the Project Locally

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/smart-expense-tracker.git
cd smart-expense-tracker
```

#### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3️⃣ Set Up API Key (Google Gemini API)
- Go to [AI Studio](https://aistudio.google.com/) and generate an API key.  
- Store it as an **environment variable** in a `.env` file:
  ```
  GEMINI_API_KEY=your_api_key_here
  ```

#### 4️⃣ Run the Application Locally
```bash
python app.py
```
The server should start at: **http://127.0.0.1:5000/**  

#### 5️⃣ Running on Render (Cloud Deployment)
Render assigns a dynamic port, so ensure your Flask app is set up to listen on the correct port:
```python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
```

---


## 6. Usage Guide

### 🔹 Adding an Expense
1. Open the web app.  
2. Enter your expense in natural language (e.g., *"I spent ₹50 on coffee"*).  
3. Click **Submit**, and the expense is added to the database.  

### 🔹 Viewing Expense Reports
- The **bar chart and pie chart** automatically update based on stored expenses.  
- You can analyze spending patterns visually.  

---

## 7. API Endpoints

| **Endpoint**        | **Method** | **Description** |
|---------------------|------------|---------------|
| `/`                | GET        | Loads the homepage (index.html). |
| `/add_expense`     | POST       | Takes user input, processes it with Gemini API, and stores the structured data in the database. |
| `/expense_chart`   | GET        | Generates a bar chart and pie chart of expenses. |

---

## 8. Future Enhancements
🔹 **WhatsApp Bot Integration:** Users can send expenses via WhatsApp, and the system will log them automatically.  
🔹 **AI-driven Spending Insights:** The app will provide personalized financial suggestions based on spending habits.  
🔹 **Multi-User Support:** Users can create accounts and manage expenses individually.  

---

## 9. Conclusion
The **Smart Expense Tracker** simplifies financial management by allowing users to log expenses in natural language and track spending visually. With **AI-powered data extraction, database storage, and interactive charts**, it provides a seamless expense-tracking experience. Future improvements will further enhance usability, making it a complete financial assistant.  

---

## 📌 Final Notes
- Feel free to contribute and improve the project.  
- Suggestions and feedback are always welcome! 😊🚀  
