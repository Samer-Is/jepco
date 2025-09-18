"""
GPT-4o Integration for JEPCO Customer Support Chatbot
Handles AI responses using OpenAI's GPT-4o model
"""

import openai
import json
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from .languages import get_system_prompt, detect_language
from .web_search import search_jepco_website, JEPCOWebSearcher

# Force load environment variables with override
load_dotenv(override=True)


class JEPCOChatbot:
    """JEPCO Customer Support Chatbot using GPT-4o"""
    
    def __init__(self):
        """Initialize the chatbot with OpenAI API key"""
        
        # Get API key from environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key)
        
        # Load JEPCO content
        self.jepco_content = self.load_jepco_content()
        
        # Initialize web searcher for real-time information
        self.web_searcher = JEPCOWebSearcher()
        
        print("✅ JEPCO Chatbot initialized successfully")
    
    def load_jepco_content(self) -> Dict:
        """Load JEPCO content from JSON file"""
        
        try:
            with open('data/jepco_content.json', 'r', encoding='utf-8') as f:
                content = json.load(f)
                print("✅ JEPCO content loaded successfully")
                return content
        except FileNotFoundError:
            print("⚠️  JEPCO content file not found. Please run scraper first.")
            return {}
        except Exception as e:
            print(f"❌ Error loading JEPCO content: {str(e)}")
            return {}
    
    def find_relevant_content(self, query: str, language: str = 'english') -> str:
        """
        Search for relevant information using real-time web search + static content
        Return: Most relevant content snippets
        """
        
        print(f"🔍 Searching for: {query} (Language: {language})")
        
        # First, try real-time web search
        try:
            web_results = search_jepco_website(query, language)
            if web_results and "Unable to search website" not in web_results and "No current information found" not in web_results:
                print("✅ Using real-time web search results")
                return f"🌐 Current information from JEPCO website:\n\n{web_results}"
        except Exception as e:
            print(f"⚠️ Web search failed: {str(e)}")
        
        # Fallback to static content if web search fails
        print("📁 Using static content as fallback")
        
        if not self.jepco_content:
            return "Please contact JEPCO customer service directly at 116 for the most current information."
        
        # Determine which language content to search
        content_lang = 'arabic' if language in ['arabic', 'jordanian'] else 'english'
        
        if content_lang not in self.jepco_content:
            content_lang = 'english' if 'english' in self.jepco_content else 'arabic'
        
        if content_lang not in self.jepco_content:
            return "Please contact JEPCO customer service directly at 116 for the most current information."
        
        lang_content = self.jepco_content[content_lang]
        
        # Search keywords based on query
        query_lower = query.lower()
        relevant_content = []
        
        # Define search categories and their keywords
        search_categories = {
            'billing': ['bill', 'فاتورة', 'payment', 'دفع', 'pay', 'cost', 'تكلفة'],
            'services': ['service', 'خدمة', 'خدمات', 'help', 'مساعدة'],
            'contact': ['contact', 'phone', 'اتصال', 'هاتف', 'تواصل'],
            'emergency': ['emergency', 'طوارئ', 'urgent', 'عاجل', 'outage', 'انقطاع'],
            'areas': ['area', 'منطقة', 'location', 'موقع']
        }
        
        # Find relevant categories
        relevant_categories = []
        for category, keywords in search_categories.items():
            if any(keyword in query_lower for keyword in keywords):
                relevant_categories.append(category)
        
        # If no specific categories found, search all
        if not relevant_categories:
            relevant_categories = list(search_categories.keys())
        
        # Extract relevant content
        for category in relevant_categories:
            category_mapping = {
                'billing': 'billing_procedures',
                'services': 'customer_services', 
                'contact': 'contact_information',
                'emergency': 'emergency_procedures',
                'areas': 'service_areas'
            }
            
            mapped_category = category_mapping.get(category, category)
            
            if mapped_category in lang_content:
                items = lang_content[mapped_category]
                if isinstance(items, list):
                    for item in items[:2]:  # Limit to 2 items per category
                        if isinstance(item, dict) and 'text' in item:
                            relevant_content.append(f"[{category.title()}] {item['text']}")
                        elif isinstance(item, str):
                            relevant_content.append(f"[{category.title()}] {item}")
        
        # Add general info if no specific content found
        if not relevant_content and 'general_info' in lang_content:
            general_items = lang_content['general_info']
            if isinstance(general_items, list):
                for item in general_items[:2]:
                    if isinstance(item, dict) and 'text' in item:
                        relevant_content.append(f"[General] {item['text']}")
        
        # Combine relevant content with disclaimer
        if relevant_content:
            static_content = "\n\n".join(relevant_content[:3])  # Limit total content
            return f"📋 Available information:\n\n{static_content}\n\n⚠️ For the most current information, please contact JEPCO at 116 or visit www.jepco.com.jo"
        else:
            return "Please contact JEPCO customer service at 116 for detailed assistance, or visit www.jepco.com.jo for current information."
    
    def get_gpt_response(self, user_message: str, language: str = None, chat_history: List = None) -> str:
        """
        Send request to GPT-4o with:
        - User message
        - Selected language
        - Relevant JEPCO content as context
        Return: AI response in requested language
        """
        
        try:
            # Detect language if not provided
            if not language:
                language = detect_language(user_message)
            
            # Get relevant JEPCO content
            context = self.find_relevant_content(user_message, language)
            
            # Get system prompt for the language
            system_prompt = get_system_prompt(language)
            
            # Prepare messages
            messages = [
                {
                    "role": "system",
                    "content": f"""{system_prompt}

JEPCO WEBSITE CONTEXT:
{context}

Instructions:
- Use ONLY the information provided in the JEPCO website context above
- If the information is not in the context, direct the customer to contact JEPCO directly
- Be helpful and professional
- Respond in {language} language
- Keep responses concise but informative"""
                }
            ]
            
            # Add chat history if provided (last 6 messages to stay within token limits)
            if chat_history:
                recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
                for msg in recent_history:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call GPT-4o
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Extract response
            ai_response = response.choices[0].message.content.strip()
            
            return ai_response
            
        except openai.AuthenticationError:
            return self._get_error_message(language, "Authentication error. Please check API key configuration.")
        
        except openai.RateLimitError:
            return self._get_error_message(language, "Service temporarily unavailable due to high demand. Please try again shortly.")
        
        except openai.APIError as e:
            return self._get_error_message(language, f"Service error: {str(e)}")
        
        except Exception as e:
            print(f"❌ Unexpected error in get_gpt_response: {str(e)}")
            return self._get_error_message(language, "Technical difficulties encountered.")
    
    def _get_error_message(self, language: str, error_detail: str = "") -> str:
        """Get appropriate error message based on language"""
        
        error_messages = {
            'english': f"I apologize, but I'm experiencing technical difficulties. {error_detail} Please contact JEPCO customer service directly at their official phone numbers.",
            
            'arabic': f"أعتذر، ولكنني أواجه صعوبات تقنية. {error_detail} يرجى الاتصال بخدمة عملاء جيبكو مباشرة على أرقام الهواتف الرسمية.",
            
            'jordanian': f"بعتذر، بس في مشكلة تقنية. {error_detail} أرجو تتصلوا مع خدمة عملاء جيبكو مباشرة على الأرقام الرسمية."
        }
        
        return error_messages.get(language, error_messages['english'])
    
    def test_connection(self) -> bool:
        """Test OpenAI API connection"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            print("✅ OpenAI API connection successful")
            return True
            
        except Exception as e:
            print(f"❌ OpenAI API connection failed: {str(e)}")
            return False


# Utility functions for standalone usage
def get_chatbot_instance() -> Optional[JEPCOChatbot]:
    """Get a chatbot instance, handling errors gracefully"""
    
    try:
        return JEPCOChatbot()
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {str(e)}")
        return None


if __name__ == "__main__":
    """Test the chatbot functionality"""
    
    print("🧪 Testing JEPCO Chatbot...")
    
    # Test initialization
    chatbot = get_chatbot_instance()
    if not chatbot:
        print("❌ Chatbot initialization failed")
        exit(1)
    
    # Test API connection
    if not chatbot.test_connection():
        print("❌ API connection test failed")
        exit(1)
    
    # Test sample queries
    test_queries = [
        ("Hello, how can I pay my electricity bill?", "english"),
        ("مرحباً، كيف يمكنني دفع فاتورة الكهرباء؟", "arabic"),
        ("شو بقدر أدفع فاتورة الكهربا؟", "jordanian")
    ]
    
    print("\n🧪 Testing sample queries:")
    for query, lang in test_queries:
        print(f"\nQuery ({lang}): {query}")
        response = chatbot.get_gpt_response(query, lang)
        print(f"Response: {response[:100]}...")
    
    print("\n✅ Chatbot testing completed!")
