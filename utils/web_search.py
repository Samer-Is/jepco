"""
Real-time Web Search and JEPCO Website Access
Provides live information retrieval from JEPCO website
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from typing import Dict, List, Optional
import warnings
from urllib.parse import urljoin, urlparse
import re

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


class JEPCOWebSearcher:
    """Real-time web searcher for JEPCO information"""
    
    def __init__(self):
        """Initialize the web searcher"""
        self.base_urls = {
            'arabic': 'https://www.jepco.com.jo/ar/Home',
            'english': 'https://www.jepco.com.jo/en'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5,ar;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        print("🔍 JEPCO Web Searcher initialized")
    
    def search_jepco_realtime(self, query: str, language: str = 'arabic') -> Dict:
        """
        Search JEPCO website in real-time based on query
        """
        print(f"🔍 Searching JEPCO website for: {query}")
        
        results = {
            'query': query,
            'language': language,
            'results': [],
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'source': 'live_search'
        }
        
        # Determine which language site to search
        base_url = self.base_urls.get(language, self.base_urls['arabic'])
        
        try:
            # Search main page
            main_page_results = self._search_page(base_url, query, language)
            if main_page_results:
                results['results'].extend(main_page_results)
            
            # Search specific service pages based on query keywords
            service_urls = self._get_relevant_service_urls(query, language)
            for service_url in service_urls:
                try:
                    service_results = self._search_page(service_url, query, language)
                    if service_results:
                        results['results'].extend(service_results)
                    time.sleep(1)  # Be respectful to the server
                except Exception as e:
                    print(f"⚠️ Error searching service page {service_url}: {str(e)}")
                    continue
            
            print(f"✅ Found {len(results['results'])} relevant results")
            
        except Exception as e:
            print(f"❌ Error in real-time search: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _search_page(self, url: str, query: str, language: str) -> List[Dict]:
        """Search a specific page for relevant information"""
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            # Extract relevant content based on query
            relevant_content = []
            query_keywords = self._extract_keywords(query, language)
            
            # Search in different sections
            sections_to_search = [
                soup.find_all(['div', 'section', 'article'], class_=lambda x: x and any(
                    keyword in x.lower() for keyword in ['content', 'main', 'service', 'info', 'text']
                )),
                soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li']),
                soup.find_all(['td', 'th'])  # Table content
            ]
            
            for section_group in sections_to_search:
                for element in section_group:
                    text = element.get_text(separator=' ', strip=True)
                    if text and len(text) > 20:  # Only meaningful content
                        
                        # Check if text contains query-relevant keywords
                        text_lower = text.lower()
                        relevance_score = sum(1 for keyword in query_keywords if keyword in text_lower)
                        
                        if relevance_score > 0:
                            relevant_content.append({
                                'text': text[:800],  # Limit length
                                'relevance_score': relevance_score,
                                'source_url': url,
                                'element_type': element.name,
                                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                            })
            
            # Sort by relevance and return top results
            relevant_content.sort(key=lambda x: x['relevance_score'], reverse=True)
            return relevant_content[:5]  # Top 5 most relevant
            
        except Exception as e:
            print(f"❌ Error searching page {url}: {str(e)}")
            return []
    
    def _extract_keywords(self, query: str, language: str) -> List[str]:
        """Extract search keywords from query based on language"""
        
        # Common service-related keywords by language
        keyword_mappings = {
            'arabic': {
                'billing': ['فاتورة', 'فواتير', 'دفع', 'تسديد', 'حساب'],
                'service': ['خدمة', 'خدمات', 'طلب', 'اشتراك'],
                'contact': ['اتصال', 'تواصل', 'هاتف', 'رقم'],
                'emergency': ['طوارئ', 'عطل', 'انقطاع', 'عاجل'],
                'areas': ['منطقة', 'مناطق', 'موقع', 'عنوان']
            },
            'english': {
                'billing': ['bill', 'payment', 'invoice', 'account', 'pay'],
                'service': ['service', 'request', 'subscription', 'application'],
                'contact': ['contact', 'phone', 'call', 'number'],
                'emergency': ['emergency', 'outage', 'fault', 'urgent'],
                'areas': ['area', 'location', 'address', 'region']
            }
        }
        
        keywords = []
        query_lower = query.lower()
        
        # Add words from query
        query_words = re.findall(r'\b\w+\b', query_lower)
        keywords.extend(query_words)
        
        # Add related keywords based on query content
        lang_keywords = keyword_mappings.get(language, keyword_mappings['arabic'])
        for category, category_keywords in lang_keywords.items():
            if any(keyword in query_lower for keyword in category_keywords):
                keywords.extend(category_keywords)
        
        # Add universal keywords
        universal_keywords = ['جيبكو', 'jepco', 'كهرباء', 'electricity', '116']
        keywords.extend(universal_keywords)
        
        return list(set(keywords))  # Remove duplicates
    
    def _get_relevant_service_urls(self, query: str, language: str) -> List[str]:
        """Get relevant service page URLs based on query"""
        
        base_url = self.base_urls.get(language, self.base_urls['arabic'])
        
        # Common service page patterns for JEPCO
        service_paths = [
            '/ar/Home/ServiceStepPage',  # Service steps
            '/ar/Home/CustomerService',   # Customer service
            '/ar/Home/ElectronicServices', # Electronic services
            '/ar/Home/ContactUs',         # Contact us
            '/ar/Home/EmergencyNumbers',  # Emergency numbers
        ]
        
        # Convert to full URLs
        service_urls = []
        for path in service_paths:
            if language == 'english':
                path = path.replace('/ar/', '/en/')
            
            full_url = urljoin(base_url, path)
            service_urls.append(full_url)
        
        return service_urls
    
    def get_contact_info(self, language: str = 'arabic') -> Dict:
        """Get current JEPCO contact information"""
        
        print("📞 Fetching current JEPCO contact information...")
        
        contact_info = {
            'hotline': '116',
            'emergency': '116', 
            'website': 'www.jepco.com.jo',
            'working_hours': 'Sunday to Thursday, 8:00 AM - 3:00 PM',
            'services': [],
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # Search for contact information
            base_url = self.base_urls.get(language, self.base_urls['arabic'])
            response = requests.get(base_url, headers=self.headers, timeout=10, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for phone numbers
            phone_pattern = r'1\d{2}'  # JEPCO uses 3-digit numbers like 116
            text_content = soup.get_text()
            phone_matches = re.findall(phone_pattern, text_content)
            
            if phone_matches:
                contact_info['found_numbers'] = list(set(phone_matches))
            
            # Look for service information
            service_elements = soup.find_all(text=re.compile(r'خدمة|service|اتصال|contact', re.I))
            for element in service_elements[:3]:  # Limit to prevent too much data
                parent = element.parent
                if parent:
                    service_text = parent.get_text(strip=True)
                    if len(service_text) > 10 and len(service_text) < 200:
                        contact_info['services'].append(service_text)
            
            print("✅ Contact information retrieved successfully")
            
        except Exception as e:
            print(f"❌ Error fetching contact info: {str(e)}")
            contact_info['error'] = str(e)
        
        return contact_info
    
    def search_billing_info(self, language: str = 'arabic') -> Dict:
        """Get current billing and payment information"""
        
        print("💰 Searching for billing and payment information...")
        
        billing_query = "فاتورة دفع تسديد" if language == 'arabic' else "bill payment pay"
        return self.search_jepco_realtime(billing_query, language)


# Utility functions for integration
def search_jepco_website(query: str, language: str = 'arabic') -> str:
    """
    Quick search function for integration with chatbot
    Returns formatted results as string
    """
    
    searcher = JEPCOWebSearcher()
    results = searcher.search_jepco_realtime(query, language)
    
    if 'error' in results:
        return f"Unable to search website at this time: {results['error']}"
    
    if not results['results']:
        return "No current information found on JEPCO website for your query."
    
    # Format results
    formatted_results = []
    formatted_results.append(f"🔍 Live information from JEPCO website ({results['timestamp']}):\n")
    
    for i, result in enumerate(results['results'][:3], 1):  # Top 3 results
        formatted_results.append(f"{i}. {result['text'][:300]}...")
        if result.get('source_url'):
            formatted_results.append(f"   Source: {result['source_url']}\n")
    
    return "\n".join(formatted_results)


if __name__ == "__main__":
    """Test the web searcher"""
    
    print("🧪 Testing JEPCO Web Searcher...")
    
    searcher = JEPCOWebSearcher()
    
    # Test searches
    test_queries = [
        ("كيف أدفع فاتورة الكهرباء؟", "arabic"),
        ("رقم خدمة العملاء", "arabic"),
        ("How to pay electricity bill?", "english")
    ]
    
    for query, lang in test_queries:
        print(f"\n🔍 Testing: {query} ({lang})")
        results = searcher.search_jepco_realtime(query, lang)
        print(f"Found {len(results.get('results', []))} results")
        
        if results.get('results'):
            print(f"Top result: {results['results'][0]['text'][:100]}...")
    
    # Test contact info
    print("\n📞 Testing contact info retrieval...")
    contact = searcher.get_contact_info()
    print(f"Hotline: {contact.get('hotline')}")
    print(f"Found numbers: {contact.get('found_numbers', [])}")
    
    print("\n✅ Web searcher testing completed!")
