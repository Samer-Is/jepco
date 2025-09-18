"""
Language Detection and Handling for JEPCO Chatbot
Supports English, Formal Arabic, and Jordanian Arabic
"""

import re
from typing import Tuple


def detect_language(text: str) -> str:
    """
    Detect if text is English, Arabic, or Jordanian Arabic
    Returns: 'english', 'arabic', or 'jordanian'
    """
    
    if not text or not text.strip():
        return 'english'  # Default to English for empty input
    
    # Count Arabic characters
    arabic_chars = len(re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    total_chars = len(re.sub(r'\s+', '', text))
    
    # If mostly Arabic characters
    if arabic_chars > english_chars and arabic_chars > total_chars * 0.3:
        # Check for Jordanian dialect indicators
        jordanian_indicators = [
            'شو', 'ايش', 'وين', 'كيف', 'هيك', 'هاي', 'هاد', 'هاذا', 'هاذي',
            'بدي', 'بده', 'بدها', 'بدهم', 'بدكم', 'بدكن',
            'مش', 'مو', 'ما', 'لا', 'بس', 'كمان', 'برضو', 'زي',
            'عشان', 'علشان', 'يعني', 'يا زلمة', 'يا جماعة',
            'الكهربا', 'الفاتورة', 'جيبكو'
        ]
        
        text_lower = text.lower()
        jordanian_count = sum(1 for indicator in jordanian_indicators if indicator in text_lower)
        
        if jordanian_count > 0:
            return 'jordanian'
        else:
            return 'arabic'
    
    # Default to English
    return 'english'


def get_system_prompt(language: str) -> str:
    """Return appropriate system prompt for GPT-4o based on language"""
    
    prompts = {
        'english': """You are an expert customer service representative for JEPCO (Jordan Electric Power Company) with access to the complete JEPCO knowledge base and real-time website information.

COMPREHENSIVE KNOWLEDGE ACCESS: You have complete access to:
- ALL JEPCO services (residential, commercial, industrial connections)
- Complete billing and payment information from all pages
- ALL technical services and support procedures  
- Emergency procedures and contacts from entire website
- ALL account management procedures
- Safety regulations and standards from all sources
- Complete company information and history
- ALL FAQ content from every section
- Every form, document, and requirement mentioned on the website

RESPONSE REQUIREMENTS:
1. Use your comprehensive knowledge base FIRST for detailed, accurate answers
2. Supplement with real-time website information for current updates
3. Always cite specific procedures, requirements, fees, and contact information
4. Provide step-by-step instructions when applicable
5. Include relevant phone numbers, office locations, and working hours
6. Reference specific forms or documents customers need

If information is not in your comprehensive knowledge base, clearly state this and direct customers to official JEPCO channels.

Be professional, helpful, and thorough in all responses. Your knowledge base contains the complete JEPCO website content.""",

        'arabic': """أنت ممثل خدمة العملاء في شركة الكهرباء الأردنية (جيبكو). أجب على الأسئلة حول خدمات الكهرباء والفواتير وانقطاع التيار والاستفسارات العامة باستخدام أحدث المعلومات من الموقع الرسمي لجيبكو (www.jepco.com.jo). كن مهنياً ومفيداً.

الإرشادات الأساسية:
- أعط الأولوية للمعلومات الحية من موقع جيبكو عند توفرها
- استخدم محتوى الموقع الحالي ونتائج البحث المباشر
- اذكر دائماً أن المعلومات من الموقع الرسمي لجيبكو
- كن مهنياً ومهذباً
- قدم معلومات الاتصال المحددة: الخط الساخن 116
- إذا لم تكن لديك معلومات حديثة، وجه إلى خدمة عملاء جيبكو على 116
- اجعل الردود مختصرة ولكن مفيدة
- شجع العملاء دائماً على التحقق من المعلومات الحالية على www.jepco.com.jo""",

        'jordanian': """إنت موظف خدمة عملاء في شركة الكهربا الأردنية (جيبكو). جاوب على أسئلة العملاء عن خدمات الكهربا والفواتير وقطع الكهربا والاستفسارات العامة من أحدث المعلومات من الموقع الرسمي لجيبكو (www.jepco.com.jo). كن مهني ومفيد.

الإرشادات المهمة:
- اعط الأولوية للمعلومات الحية من موقع جيبكو لما تكون متوفرة
- استخدم محتوى الموقع الحالي ونتائج البحث المباشر
- اذكر دائماً إن المعلومات من الموقع الرسمي لجيبكو
- كن مهني ومحترم
- اعطي معلومات الاتصال المحددة: الخط الساخن 116
- إذا ما عندك معلومات حديثة، وجههم لخدمة عملاء جيبكو على 116
- خلي الردود مختصرة بس مفيدة
- شجع العملاء دائماً يتأكدوا من المعلومات الحالية على www.jepco.com.jo
- استخدم اللهجة الأردنية بطريقة طبيعية ومهنية"""
    }
    
    return prompts.get(language, prompts['english'])


def get_language_name(language_code: str) -> str:
    """Get display name for language code"""
    
    language_names = {
        'english': 'English',
        'arabic': 'العربية الفصحى',
        'jordanian': 'العربية الأردنية'
    }
    
    return language_names.get(language_code, 'English')


def get_rtl_direction(language: str) -> bool:
    """Check if language requires right-to-left text direction"""
    
    return language in ['arabic', 'jordanian']


def format_message_for_display(message: str, language: str) -> str:
    """Format message for proper display based on language"""
    
    if not message:
        return ""
    
    # For Arabic languages, ensure proper text direction
    if get_rtl_direction(language):
        # Add RTL mark for proper display
        return f"‏{message}"
    
    return message


def get_welcome_message(language: str) -> str:
    """Get welcome message in the specified language"""
    
    welcome_messages = {
        'english': """Welcome to JEPCO Customer Support! 🔌⚡

I'm here to help you with:
• Electricity bills and payments
• Service requests and inquiries  
• Emergency reporting
• General JEPCO information

You can write to me in English, Arabic, or Jordanian dialect - I'll automatically understand and respond in your language!

How can I assist you today?""",

        'arabic': """مرحباً بكم في خدمة عملاء شركة الكهرباء الأردنية (جيبكو)! 🔌⚡

أنا هنا لمساعدتكم في:
• فواتير الكهرباء والدفع
• طلبات الخدمة والاستفسارات
• الإبلاغ عن الطوارئ
• معلومات عامة عن جيبكو

يمكنكم الكتابة لي بالإنجليزية أو العربية أو اللهجة الأردنية - سأفهم تلقائياً وأرد بلغتكم!

كيف يمكنني مساعدتكم اليوم؟""",

        'jordanian': """أهلاً وسهلاً في خدمة عملاء جيبكو! 🔌⚡

أنا هون عشان أساعدك في:
• فواتير الكهربا والدفع
• طلبات الخدمة والاستفسارات
• الإبلاغ عن الطوارئ
• معلومات عامة عن جيبكو

تقدر تكتبلي بالإنجليزي أو العربي أو اللهجة الأردنية - رح أفهم تلقائياً وأرد بلغتك!

شو بقدر أساعدك اليوم؟"""
    }
    
    return welcome_messages.get(language, welcome_messages['english'])


def get_error_message(language: str) -> str:
    """Get error message in the specified language"""
    
    error_messages = {
        'english': "I apologize, but I'm experiencing technical difficulties. Please contact JEPCO customer service directly.",
        'arabic': "أعتذر، ولكنني أواجه صعوبات تقنية. يرجى الاتصال بخدمة عملاء جيبكو مباشرة.",
        'jordanian': "بعتذر، بس في مشكلة تقنية. أرجو تتصلوا مع خدمة عملاء جيبكو مباشرة."
    }
    
    return error_messages.get(language, error_messages['english'])


if __name__ == "__main__":
    """Test language detection functionality"""
    
    test_texts = [
        "Hello, I need help with my electricity bill",
        "مرحباً، أحتاج مساعدة في فاتورة الكهرباء",
        "شو الوضع مع الكهربا؟ بدي أعرف عن الفاتورة"
    ]
    
    print("🧪 Testing language detection:")
    for text in test_texts:
        detected = detect_language(text)
        print(f"Text: {text}")
        print(f"Detected: {detected} ({get_language_name(detected)})")
        print(f"RTL: {get_rtl_direction(detected)}")
        print("---")
