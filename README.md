
# EcoStep 🌱 – Carbon Footprint from Receipts, Made Easy

**EcoStep** is a multi-functional platform that lets users:
- Analyze receipts to calculate carbon footprints
- Interact with a smart chatbot for environmental queries
- Generate professional monthly CO₂ reports using AI and cloud tools

---

## 🚀 Features

- 📸 **OCR Analyzer**: Upload receipt images and extract product details with estimated carbon footprint.
- 🤖 **AI Chatbot**: Ask sustainability questions powered by LLM (Groq).
- 📊 **Monthly Report Generator**: Creates Word reports, graphs, and AI-generated suggestions.
- 📱 **WhatsApp Alerts**: Sends report links directly via WhatsApp using Twilio.
- ☁️ **Google Drive Upload**: Uploads reports to Google Drive and returns a public download link.

---

## 🗂️ Project Structure

```
project/
├── .env                  # API credentials (never push to GitHub)
├── chatbot_app.py         # Streamlit chatbot app
├── ocr_app.py             # Streamlit OCR receipt app
├── config.py              # Loads credentials from .env
├── chatbot/
│   ├── __init__.py
│   ├── llm_utils.py
│   └── database.py
├── ocr/
│   ├── __init__.py
│   ├── ocr_utils.py
│   └── database.py
├── reports/
│   ├── __init__.py
│   └── report_generator.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/DPRASAD-dp/EcoStep.git
cd ecostep
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory and fill in your actual keys.

---

## 🔑 Environment Variables

Example structure for `.env`:

```
# === GROQ AI ===
GROQ_API_KEY=your_groq_api_key_here

# === Twilio WhatsApp Integration ===
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_TO=whatsapp:+91xxxxxxxxxx

# === Google Drive OAuth (for uploading reports) ===
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

---

## 💻 How to Run

### Run the OCR App
```bash
streamlit run ocr_app.py
```

### Run the Chatbot
```bash
streamlit run chatbot_app.py
```

### Generate the Monthly Report
```bash
python -m reports.report_generator
```

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 👥 Contributing

Contributions are welcome! Feel free to submit a Pull Request.

### How to contribute:

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

---

## 📜 Code of Conduct

When contributing, please:

- Write clean, maintainable code
- Add appropriate comments and documentation
- Follow the existing coding style
- Test your changes thoroughly
- Be respectful and constructive in code reviews

---

## 📬 Contact

For any queries, contact: **kdurgaprasadkavali@gmail.com**
