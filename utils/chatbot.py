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
        """Initialize JEPCO chatbot with comprehensive knowledge base"""
        
        load_dotenv(override=True)  # Ensure .env overrides system environment variables
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = openai.OpenAI(api_key=api_key)
        
        # Load comprehensive JEPCO content
        self.jepco_content = self._load_comprehensive_jepco_content()
        
        # Initialize web searcher for real-time information
        self.web_searcher = JEPCOWebSearcher()
        
        print("✅ JEPCO Chatbot initialized with comprehensive knowledge base")
    
    def _load_comprehensive_jepco_content(self) -> Dict:
        """Load comprehensive JEPCO content from JSON file"""
        
        try:
            with open('data/jepco_content.json', 'r', encoding='utf-8') as f:
                content = json.load(f)
                
                # Check if it's comprehensive content
                if 'extraction_metadata' in content:
                    pages_scraped = len(content['extraction_metadata'].get('pages_scraped', []))
                    content_sections = content['extraction_metadata'].get('total_content_sections', 0)
                    print(f"✅ Comprehensive JEPCO content loaded successfully")
                    print(f"📄 {pages_scraped} pages | 📋 {content_sections} sections")
                    return content
                else:
                    # Legacy content format
                    print("⚠️  Legacy content format detected. Using as-is.")
                    return content
                    
        except FileNotFoundError:
            print("⚠️  JEPCO content file not found. Running comprehensive extraction...")
            return self._extract_and_save_comprehensive_content()
        except Exception as e:
            print(f"❌ Error loading JEPCO content: {str(e)}")
            return self._create_fallback_content()
    
    def _extract_and_save_comprehensive_content(self) -> Dict:
        """Extract comprehensive content if not available"""
        
        try:
            from utils.scraper import scrape_complete_jepco_website, save_complete_content_to_json
            
            print("🚀 Starting comprehensive JEPCO website extraction...")
            comprehensive_content = scrape_complete_jepco_website()
            save_complete_content_to_json(comprehensive_content)
            
            return comprehensive_content
            
        except Exception as e:
            print(f"❌ Error during comprehensive extraction: {str(e)}")
            return self._create_fallback_content()
    
    def load_jepco_content(self) -> Dict:
        """Legacy method - redirects to comprehensive loader"""
        return self._load_comprehensive_jepco_content()
    
    def find_relevant_content(self, query: str, language: str = 'english') -> str:
        """
        Search for relevant information using real-time web search + static content
        Return: Most relevant content snippets
        """
        
        print(f"🔍 Comprehensive search for: {query} (Language: {language})")
        
        # Check if this is a calculation/pricing query
        if self._is_calculation_query(query):
            try:
                calculation_result = self._handle_calculation_query(query, language)
                if calculation_result:
                    print("✅ Using calculation with live pricing data")
                    return calculation_result
            except Exception as e:
                print(f"⚠️ Calculation failed: {str(e)}")
        
        # First, search comprehensive knowledge base
        knowledge_base_results = self._search_comprehensive_knowledge_base(query, language)
        
        # Then, try real-time web search for current information
        web_search_results = ""
        try:
            web_results = search_jepco_website(query, language)
            if web_results and "Unable to search website" not in web_results and "No current information found" not in web_results:
                print("✅ Using real-time web search results")
                web_search_results = web_results
        except Exception as e:
            print(f"⚠️ Web search failed: {str(e)}")
        
        # Combine comprehensive knowledge base with real-time results
        combined_results = []
        
        if knowledge_base_results:
            combined_results.append("📚 From JEPCO Comprehensive Knowledge Base:")
            combined_results.append(knowledge_base_results)
        
        if web_search_results:
            combined_results.append("\n🌐 Current Information from JEPCO Website:")
            combined_results.append(web_search_results)
        
        if combined_results:
            return "\n".join(combined_results)
        
        # Fallback to static content if everything fails
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
    
    def _is_calculation_query(self, query: str) -> bool:
        """Check if the query is asking for cost calculation"""
        
        calculation_keywords = [
            'احسب', 'calculate', 'حساب', 'كم', 'how much', 'cost', 'تكلفة', 
            'فاتورة', 'bill', 'كيلو واط', 'kwh', 'سعر', 'price'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in calculation_keywords)
    
    def _handle_calculation_query(self, query: str, language: str) -> str:
        """Handle calculation queries with live pricing data"""
        
        print("🧮 Processing calculation query...")
        
        # Extract kWh value from query
        import re
        numbers = re.findall(r'\d+(?:\.\d+)?', query)
        
        if not numbers:
            return None
        
        try:
            # Get the consumption value (assuming first number is kWh)
            daily_kwh = float(numbers[0])
            print(f"📊 Extracted consumption: {daily_kwh} kWh daily")
            
            # Get live tariff information
            tariff_info = self.web_searcher.get_electricity_tariffs(language)
            
            # Calculate costs
            calculation = self.web_searcher.calculate_electricity_cost(daily_kwh, tariff_info)
            
            # Format response based on language
            if language in ['arabic', 'jordanian']:
                return self._format_calculation_arabic(calculation, tariff_info)
            else:
                return self._format_calculation_english(calculation, tariff_info)
                
        except Exception as e:
            print(f"❌ Calculation error: {str(e)}")
            return None
    
    def _format_calculation_arabic(self, calculation: Dict, tariff_info: Dict) -> str:
        """Format calculation results in Arabic"""
        
        daily_kwh = calculation['daily_kwh']
        monthly_kwh = calculation['monthly_kwh']
        costs = calculation['estimated_costs']
        
        if not costs:
            return f"🌐 معلومات حية من موقع جيبكو:\n\nلحساب تكلفة استهلاك {daily_kwh} كيلو واط يوميًا، أحتاج للوصول إلى جدول التعرفة الحالي. يرجى الاتصال بجيبكو على 116 للحصول على التعرفة الدقيقة."
        
        result = f"🧮 حساب فاتورة الكهرباء - معلومات من موقع جيبكو:\n\n"
        result += f"📊 **الاستهلاك:**\n"
        result += f"• يوميًا: {daily_kwh} كيلو واط ساعة\n"
        result += f"• شهريًا: {monthly_kwh} كيلو واط ساعة\n\n"
        
        if 'daily' in costs and costs['daily'] > 0:
            result += f"💰 **التكلفة المقدرة:**\n"
            result += f"• يوميًا: {costs['daily']:.3f} دينار أردني\n"
            result += f"• شهريًا: {costs['monthly']:.2f} دينار أردني\n"
            result += f"• سنويًا: {costs['yearly']:.2f} دينار أردني\n\n"
            
            if 'rate_used' in costs:
                result += f"📋 **السعر المستخدم:** {costs['rate_used']:.3f} دينار/كيلو واط ساعة\n\n"
        
        if calculation['calculation_method'] == 'estimated':
            result += f"⚠️ **ملاحظة:** هذه أسعار تقديرية. للحصول على التعرفة الدقيقة والحالية:\n"
            result += f"• اتصل بجيبكو على الرقم 116\n"
            result += f"• زر الموقع الرسمي www.jepco.com.jo\n\n"
        
        # Add tariff information if found
        if tariff_info.get('tariffs'):
            result += f"📈 **معلومات التعرفة من الموقع:**\n"
            for i, tariff in enumerate(tariff_info['tariffs'][:3]):
                result += f"• {tariff.get('additional_info', 'معلومات تعرفة')}\n"
        
        result += f"\n🔍 **المصدر:** البحث المباشر في موقع جيبكو الرسمي\n"
        result += f"⏰ **وقت البحث:** {calculation['timestamp']}"
        
        return result
    
    def _format_calculation_english(self, calculation: Dict, tariff_info: Dict) -> str:
        """Format calculation results in English"""
        
        daily_kwh = calculation['daily_kwh']
        monthly_kwh = calculation['monthly_kwh']
        costs = calculation['estimated_costs']
        
        if not costs:
            return f"🌐 Live information from JEPCO website:\n\nTo calculate the cost for {daily_kwh} kWh daily consumption, I need access to the current tariff schedule. Please contact JEPCO at 116 for exact current rates."
        
        result = f"🧮 Electricity Bill Calculation - Live JEPCO Data:\n\n"
        result += f"📊 **Consumption:**\n"
        result += f"• Daily: {daily_kwh} kWh\n"
        result += f"• Monthly: {monthly_kwh} kWh\n\n"
        
        if 'daily' in costs and costs['daily'] > 0:
            result += f"💰 **Estimated Costs:**\n"
            result += f"• Daily: {costs['daily']:.3f} JOD\n"
            result += f"• Monthly: {costs['monthly']:.2f} JOD\n"
            result += f"• Yearly: {costs['yearly']:.2f} JOD\n\n"
            
            if 'rate_used' in costs:
                result += f"📋 **Rate Used:** {costs['rate_used']:.3f} JOD/kWh\n\n"
        
        if calculation['calculation_method'] == 'estimated':
            result += f"⚠️ **Note:** These are estimated rates. For exact current tariffs:\n"
            result += f"• Call JEPCO at 116\n"
            result += f"• Visit www.jepco.com.jo\n\n"
        
        # Add tariff information if found
        if tariff_info.get('tariffs'):
            result += f"📈 **Tariff Information from Website:**\n"
            for i, tariff in enumerate(tariff_info['tariffs'][:3]):
                result += f"• {tariff.get('additional_info', 'Tariff information')}\n"
        
        result += f"\n🔍 **Source:** Live search of official JEPCO website\n"
        result += f"⏰ **Search Time:** {calculation['timestamp']}"
        
        return result
    
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
    
    def _search_comprehensive_knowledge_base(self, query: str, language: str) -> str:
        """Search through the comprehensive knowledge base"""
        
        if not self.jepco_content or 'extraction_metadata' not in self.jepco_content:
            return ""
        
        # Determine language key
        lang_key = 'arabic' if language in ['arabic', 'jordanian'] else 'english'
        
        if lang_key not in self.jepco_content:
            return ""
        
        query_lower = query.lower()
        relevant_content = []
        
        # Search through all content categories
        content_categories = [
            ('company_info', 'Company Information'),
            ('services', 'Customer Services'),
            ('billing', 'Billing Information'),
            ('technical_services', 'Technical Services'),
            ('contact_info', 'Contact Information'),
            ('safety_regulations', 'Safety & Regulations'),
            ('faq', 'Frequently Asked Questions'),
            ('additional_content', 'Additional Information')
        ]
        
        for category_key, category_name in content_categories:
            if category_key in self.jepco_content[lang_key]:
                category_content = self.jepco_content[lang_key][category_key]
                
                # Search through category content
                category_matches = self._search_category_content(query_lower, category_content)
                
                if category_matches:
                    relevant_content.append(f"\n📋 {category_name}:")
                    relevant_content.extend(category_matches[:2])  # Top 2 matches per category
        
        return "\n".join(relevant_content) if relevant_content else ""
    
    def _search_category_content(self, query_lower: str, category_content: Dict) -> List[str]:
        """Search within a specific content category"""
        
        matches = []
        
        if not isinstance(category_content, dict):
            return matches
        
        for key, value in category_content.items():
            if isinstance(value, str):
                if any(word in value.lower() for word in query_lower.split() if len(word) > 2):
                    matches.append(f"• {value[:300]}...")
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        if any(word in item.lower() for word in query_lower.split() if len(word) > 2):
                            matches.append(f"• {item[:300]}...")
                    elif isinstance(item, dict):
                        # Handle structured content
                        item_text = str(item.get('text', item.get('title', str(item))))
                        if any(word in item_text.lower() for word in query_lower.split() if len(word) > 2):
                            matches.append(f"• {item_text[:300]}...")
            elif isinstance(value, dict):
                # Handle nested dictionary content
                nested_matches = self._search_category_content(query_lower, value)
                matches.extend(nested_matches)
        
        return matches


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
