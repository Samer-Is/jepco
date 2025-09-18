# JEPCO Customer Support Chatbot

Official AI-powered customer service chatbot for Jordan Electric Power Company (JEPCO).

## 🌟 Features

- **Multi-language Support**: English, Formal Arabic, and Jordanian Arabic
- **Real JEPCO Data**: Information extracted from official JEPCO website
- **AI-Powered**: Uses OpenAI GPT-4o for intelligent responses
- **24/7 Availability**: Always available customer support
- **Streamlit Interface**: Clean, user-friendly web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (GPT-4o access)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Samer-Is/jepco.git
   cd jepco
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_gpt4o_api_key_here
   ```

4. **Scrape JEPCO content (first time only):**
   ```bash
   python utils/scraper.py
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser:**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
jepco/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── utils/
│   ├── scraper.py           # Website content extraction
│   ├── chatbot.py           # GPT-4o integration
│   └── languages.py        # Language detection and handling
├── data/
│   └── jepco_content.json   # Scraped website content
├── TODO.md                  # Task tracking file
├── ACTIVITY.md              # Development log
├── README.md                # This file
└── .gitignore               # Git ignore file
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key with GPT-4o access

### Streamlit Configuration

The app uses custom Streamlit configuration in `.streamlit/config.toml`:
- JEPCO brand colors
- Optimized for customer service interface

## 🌍 Language Support

### Supported Languages

1. **English**: Full customer service support
2. **Formal Arabic (العربية الفصحى)**: Professional Arabic responses
3. **Jordanian Arabic (العربية الأردنية)**: Local dialect support

### Language Detection

The system automatically detects the user's language and responds accordingly:
- Automatic language detection from user input
- Manual language selection in sidebar
- Right-to-left (RTL) text support for Arabic

## 📊 Data Sources

All information is extracted from official JEPCO websites:
- Arabic content: https://www.jepco.com.jo/ar/Home
- English content: https://www.jepco.com.jo/en

### Content Categories

- Customer services information
- Billing procedures
- Contact information
- Emergency procedures
- Service areas

## 🚀 Deployment

### Streamlit Cloud

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Add `OPENAI_API_KEY` to secrets
   - Deploy the app

3. **Set Secrets:**
   In Streamlit Cloud app settings, add:
   ```toml
   OPENAI_API_KEY = "your_api_key_here"
   ```

### Local Development

For development, use:
```bash
streamlit run app.py --server.port 8501
```

## 🧪 Testing

### Test Components

1. **Scraper Testing:**
   ```bash
   python utils/scraper.py
   ```

2. **Language Detection:**
   ```bash
   python utils/languages.py
   ```

3. **Chatbot Integration:**
   ```bash
   python utils/chatbot.py
   ```

### Manual Testing

1. Test all three languages
2. Verify Arabic RTL display
3. Test different query types:
   - Billing questions
   - Service inquiries
   - Contact requests
   - Emergency procedures

## 📱 WhatsApp Integration Assessment

Future integration possibilities:
- WhatsApp Business API integration
- Webhook setup for message handling
- Multi-platform support
- Enhanced customer reach

## 🛠️ Development

### Adding New Features

1. Update `TODO.md` with new tasks
2. Log activities in `ACTIVITY.md`
3. Follow existing code patterns
4. Test thoroughly before deployment

### Code Structure

- `app.py`: Main Streamlit interface
- `utils/chatbot.py`: AI integration logic
- `utils/languages.py`: Language handling
- `utils/scraper.py`: Content extraction

## 📞 Support

For technical issues or questions:
- Check the `ACTIVITY.md` file for development history
- Review `TODO.md` for known issues
- Contact JEPCO directly for service-related queries

## 📄 License

This project is developed for Jordan Electric Power Company (JEPCO) customer service purposes.

## 🔗 Links

- **JEPCO Official Website**: https://www.jepco.com.jo
- **Repository**: https://github.com/Samer-Is/jepco
- **Streamlit**: https://streamlit.io

---

**Built with ❤️ for JEPCO customers**
