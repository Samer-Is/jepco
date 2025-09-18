"""
JEPCO Customer Support Chatbot - Main Streamlit Application
Official customer service chatbot for Jordan Electric Power Company (JEPCO)
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Import custom modules
from utils.chatbot import get_chatbot_instance
from utils.languages import (
    detect_language, get_language_name, get_rtl_direction,
    format_message_for_display, get_welcome_message, get_error_message
)

# Load environment variables
load_dotenv(override=True)  # Force override system environment variables


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None
    
    if "chatbot_initialized" not in st.session_state:
        st.session_state.chatbot_initialized = False


def setup_page_config():
    """Configure Streamlit page settings"""
    
    st.set_page_config(
        page_title="JEPCO Customer Support",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def display_header():
    """Display JEPCO header and branding"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("⚡ JEPCO Customer Support")
        st.markdown(
            """
            <div style='text-align: center; color: #666; margin-bottom: 2rem;'>
                <h4>شركة الكهرباء الأردنية | Jordan Electric Power Company</h4>
                <p>Official AI-Powered Customer Service Assistant</p>
            </div>
            """, 
            unsafe_allow_html=True
        )


def setup_sidebar():
    """Setup sidebar with information (no language selector)"""
    
    with st.sidebar:
        st.header("ℹ️ معلومات | Information")
        
        # Remove language selector - automatic detection only
        # Set default language to English for initial welcome message
        if "selected_language" not in st.session_state:
            st.session_state.selected_language = "english"
        
        # Bilingual information section
        st.markdown("""
        **About this service | حول هذه الخدمة:**
        - Official JEPCO customer support | خدمة عملاء جيبكو الرسمية
        - AI-powered assistance 24/7 | مساعدة بالذكاء الاصطناعي 24 ساعة
        - Information from JEPCO website | معلومات من موقع جيبكو
        - Automatic language detection | كشف اللغة التلقائي
        
        **For urgent issues | للقضايا العاجلة:**
        - Contact JEPCO directly | اتصل بجيبكو مباشرة
        - Hotline: **116** | الخط الساخن: **116**
        - Visit nearest JEPCO office | زيارة أقرب مكتب جيبكو
        """)
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat | مسح المحادثة"):
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant",
                "content": get_welcome_message("english"),  # Default welcome in English
                "timestamp": datetime.now(),
                "language": "english"
            })
            st.rerun()


def initialize_chatbot():
    """Initialize the JEPCO chatbot"""
    
    if not st.session_state.chatbot_initialized:
        with st.spinner("Initializing JEPCO Customer Support..."):
            st.session_state.chatbot = get_chatbot_instance()
            
            if st.session_state.chatbot:
                st.session_state.chatbot_initialized = True
                # Add welcome message in English by default
                welcome_msg = get_welcome_message("english")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": welcome_msg,
                    "timestamp": datetime.now(),
                    "language": "english"
                })
                st.success("✅ JEPCO Customer Support is ready!")
            else:
                st.error("❌ Failed to initialize customer support. Please check your OpenAI API key configuration.")
                st.info("""
                **To fix this issue:**
                1. Make sure you have set the `OPENAI_API_KEY` in your environment
                2. For Streamlit Cloud: Add the API key to your app secrets
                3. For local development: Create a `.env` file with your API key
                
                **Without the API key, the chatbot cannot function.**
                """)
                st.stop()


def display_chat_messages():
    """Display chat message history"""
    
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        msg_language = message.get("language", st.session_state.selected_language)
        
        # Format content for display
        formatted_content = format_message_for_display(content, msg_language)
        
        with st.chat_message(role):
            # Add RTL styling for Arabic messages
            if get_rtl_direction(msg_language):
                st.markdown(
                    f'<div style="direction: rtl; text-align: right;">{formatted_content}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(formatted_content)
            
            # Show timestamp
            if "timestamp" in message:
                timestamp = message["timestamp"].strftime("%H:%M")
                st.caption(f"⏰ {timestamp}")


def handle_user_input():
    """Handle user input and generate AI response"""
    
    # Get user input with bilingual placeholder
    user_input = st.chat_input("Type your message here | اكتب رسالتك هنا")
    
    if user_input:
        # Detect language of user input
        detected_lang = detect_language(user_input)
        
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now(),
            "language": detected_lang
        })
        
        # Display user message immediately
        with st.chat_message("user"):
            if get_rtl_direction(detected_lang):
                st.markdown(
                    f'<div style="direction: rtl; text-align: right;">{format_message_for_display(user_input, detected_lang)}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(user_input)
        
        # Generate AI response
        if st.session_state.chatbot:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Prepare chat history for context
                    chat_history = []
                    for msg in st.session_state.messages[-10:]:  # Last 10 messages for context
                        if msg["role"] in ["user", "assistant"]:
                            chat_history.append({
                                "role": msg["role"],
                                "content": msg["content"]
                            })
                    
                    # Get AI response
                    ai_response = st.session_state.chatbot.get_gpt_response(
                        user_input, 
                        detected_lang, 
                        chat_history[:-1]  # Exclude current message
                    )
                    
                    # Display AI response
                    if get_rtl_direction(detected_lang):
                        st.markdown(
                            f'<div style="direction: rtl; text-align: right;">{format_message_for_display(ai_response, detected_lang)}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(ai_response)
                    
                    # Add AI response to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_response,
                        "timestamp": datetime.now(),
                        "language": detected_lang
                    })
        else:
            # Chatbot not available
            error_msg = get_error_message(detected_lang)
            with st.chat_message("assistant"):
                st.error(error_msg)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "timestamp": datetime.now(),
                "language": detected_lang
            })


def check_environment():
    """Check if required environment variables are set"""
    
    if not os.getenv('OPENAI_API_KEY'):
        st.error("❌ **Missing OpenAI API Key**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **For Streamlit Cloud:**
            1. Go to your app settings ⚙️
            2. Click on "Secrets" 
            3. Add: `OPENAI_API_KEY = "your_key_here"`
            4. Restart the app
            """)
        
        with col2:
            st.markdown("""
            **For Local Development:**
            1. Create a `.env` file
            2. Add: `OPENAI_API_KEY=your_key_here`
            3. Restart the app
            """)
        
        st.info("💡 **Get your API key from:** https://platform.openai.com/api-keys")
        st.warning("⚠️ **The chatbot cannot function without a valid OpenAI API key.**")
        st.stop()


def main():
    """Main application function"""
    
    # Setup page configuration
    setup_page_config()
    
    # Check environment
    check_environment()
    
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Setup sidebar
    setup_sidebar()
    
    # Initialize chatbot
    initialize_chatbot()
    
    # Display chat messages
    display_chat_messages()
    
    # Handle user input
    handle_user_input()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888; font-size: 0.8em;'>
            Powered by OpenAI GPT-4o | Built for JEPCO Customer Service<br>
            For official inquiries, visit <a href="https://www.jepco.com.jo" target="_blank">www.jepco.com.jo</a>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
