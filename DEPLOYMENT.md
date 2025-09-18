# JEPCO Customer Support Chatbot - Deployment Guide

## 🚀 Streamlit Cloud Deployment

The JEPCO Customer Support Chatbot is ready for deployment on Streamlit Cloud. Follow these steps:

### Prerequisites
- ✅ GitHub repository: https://github.com/Samer-Is/jepco
- ✅ OpenAI API key with GPT-4o access
- ✅ Streamlit Cloud account

### Step-by-Step Deployment

#### 1. Access Streamlit Cloud
- Go to [share.streamlit.io](https://share.streamlit.io)
- Sign in with your GitHub account

#### 2. Create New App
- Click "New app"
- Repository: `Samer-Is/jepco`
- Branch: `main`
- Main file path: `app.py`
- App URL: Choose a custom URL (e.g., `jepco-support`)

#### 3. Configure Secrets
In the app settings, add the following secret:

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your_gpt4o_api_key_here"
```

#### 4. Deploy
- Click "Deploy!"
- Wait for deployment to complete
- Your app will be available at: `https://your-app-name.streamlit.app`

### Environment Variables Required

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key with GPT-4o access | ✅ Yes |

### Post-Deployment Verification

After deployment, verify:
- [ ] App loads without errors
- [ ] All three languages work (English, Arabic, Jordanian)
- [ ] Arabic text displays correctly (RTL)
- [ ] Chat interface responds properly
- [ ] Language detection works
- [ ] JEPCO content is available

### Testing the Live App

Test with these sample queries:

**English:**
- "How can I pay my electricity bill?"
- "What is JEPCO's customer service number?"

**Arabic:**
- "كيف يمكنني دفع فاتورة الكهرباء؟"
- "ما هو رقم خدمة العملاء؟"

**Jordanian Arabic:**
- "شو بقدر أدفع فاتورة الكهربا؟"
- "وين بقدر أتصل للشكاوي؟"

## 📱 WhatsApp Integration Assessment

### Current Status: Research Phase

The application is built with a modular architecture that can support WhatsApp integration in the future.

### Integration Requirements:
1. **WhatsApp Business API Account**
   - Meta Business verification
   - WhatsApp Business API access
   - Phone number verification

2. **Technical Requirements**
   - Webhook endpoint for message handling
   - Message formatting for WhatsApp
   - Media handling capabilities
   - Rate limiting compliance

3. **Code Modifications Needed**
   - Webhook handler for incoming messages
   - WhatsApp message formatter
   - Response length optimization (WhatsApp limits)
   - Message threading for context

### Estimated Implementation:
- **Complexity**: Medium to High
- **Timeline**: 2-3 weeks additional development
- **Costs**: WhatsApp Business API fees apply
- **Benefits**: 24/7 customer support via WhatsApp

### Recommended Next Steps:
1. Verify live Streamlit deployment
2. Gather user feedback
3. Assess WhatsApp integration demand
4. Plan WhatsApp Business API setup

## 🔧 Local Development

To run locally for testing:

```bash
# Clone repository
git clone https://github.com/Samer-Is/jepco.git
cd jepco

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.template .env
# Edit .env with your OpenAI API key

# Run application
streamlit run app.py
```

## 🐛 Troubleshooting

### Common Issues:

1. **"Missing OpenAI API Key" Error**
   - Solution: Ensure `OPENAI_API_KEY` is set in Streamlit secrets

2. **Arabic Text Not Displaying Correctly**
   - Solution: Browser should support RTL text (most modern browsers do)

3. **App Loading Slowly**
   - Cause: First-time content scraping or API initialization
   - Solution: Wait for initialization to complete

4. **Empty Responses**
   - Cause: OpenAI API issues or rate limiting
   - Solution: Check API key validity and usage limits

### Support Contacts:
- **Technical Issues**: Check ACTIVITY.md for development history
- **JEPCO Service Issues**: Contact JEPCO directly at 116
- **Repository Issues**: Create GitHub issue

## 📊 Monitoring & Analytics

After deployment, monitor:
- App usage metrics (Streamlit Cloud provides basic analytics)
- Response quality and accuracy
- Language detection accuracy
- User satisfaction feedback

---

**Deployment Status**: ✅ Ready for Streamlit Cloud  
**Last Updated**: 2025-09-18  
**Version**: 1.0.0
