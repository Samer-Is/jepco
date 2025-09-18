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
        'english': """You are a customer service representative for JEPCO (Jordan Electric Power Company). Answer questions about electricity services, billing, outages, and general inquiries using only the provided JEPCO website information. Be professional and helpful. If information is not available in the provided context, direct customers to contact JEPCO directly.

Key guidelines:
- Only use information from the provided JEPCO website content
- Be professional and courteous
- Provide specific contact information when available
- If you don't have specific information, direct to JEPCO customer service
- Keep responses concise but informative""",

        'arabic': """أنت ممثل خدمة العملاء في شركة الكهرباء الأردنية (جيبكو). أجب على الأسئلة حول خدمات الكهرباء والفواتير وانقطاع التيار والاستفسارات العامة باستخدام معلومات موقع جيبكو المقدمة فقط. كن مهنياً ومفيداً. إذا لم تكن المعلومات متوفرة في السياق المقدم، وجه العملاء للاتصال بجيبكو مباشرة.

الإرشادات الأساسية:
- استخدم فقط المعلومات المتوفرة من محتوى موقع جيبكو المقدم
- كن مهنياً ومهذباً
- قدم معلومات الاتصال المحددة عند توفرها
- إذا لم تكن لديك معلومات محددة، وجه إلى خدمة عملاء جيبكو
- اجعل الردود مختصرة ولكن مفيدة""",

        'jordanian': """إنت موظف خدمة عملاء في شركة الكهربا الأردنية (جيبكو). جاوب على أسئلة العملاء عن خدمات الكهربا والفواتير وقطع الكهربا والاستفسارات العامة بس من معلومات موقع جيبكو اللي معطاة لك. كن مهني ومفيد. إذا ما في معلومات في السياق المعطى، قلهم يتصلوا مع جيبكو مباشرة.

الإرشادات المهمة:
- استخدم بس المعلومات الموجودة من موقع جيبكو
- كن مهني ومحترم
- اعطي معلومات الاتصال لما تكون موجودة
- إذا ما عندك معلومات محددة، وجههم لخدمة عملاء جيبكو
- خلي الردود مختصرة بس مفيدة
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
        'english': "Welcome to JEPCO Customer Support! How can I help you today?",
        'arabic': "مرحباً بكم في خدمة عملاء شركة الكهرباء الأردنية (جيبكو)! كيف يمكنني مساعدتكم اليوم؟",
        'jordanian': "أهلاً وسهلاً في خدمة عملاء جيبكو! شو بقدر أساعدك اليوم؟"
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
