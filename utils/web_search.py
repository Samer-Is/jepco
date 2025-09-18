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
        """Initialize the comprehensive web searcher"""
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
        
        # Comprehensive page discovery - all possible JEPCO pages
        self.all_page_paths = {
            'arabic': [
                '/ar/Home',
                '/ar/Home/AboutUs',
                '/ar/Home/Vision',
                '/ar/Home/Mission', 
                '/ar/Home/History',
                '/ar/Home/OrganizationalChart',
                '/ar/Home/CustomerService',
                '/ar/Home/ServiceStepPage',
                '/ar/Home/ElectronicServices',
                '/ar/Home/BillInquiry',
                '/ar/Home/PayBill',
                '/ar/Home/NewConnection',
                '/ar/Home/TransferSubscription',
                '/ar/Home/CancelSubscription',
                '/ar/Home/ComplaintSubmission',
                '/ar/Home/Tariffs',
                '/ar/Home/ElectricityTariffs',
                '/ar/Home/Pricing',
                '/ar/Home/RateSchedule',
                '/ar/Home/ContactUs',
                '/ar/Home/EmergencyNumbers',
                '/ar/Home/ServiceAreas',
                '/ar/Home/OfficeLocations',
                '/ar/Home/WorkingHours',
                '/ar/Home/News',
                '/ar/Home/Announcements',
                '/ar/Home/Tenders',
                '/ar/Home/Careers',
                '/ar/Home/Safety',
                '/ar/Home/PowerOutages',
                '/ar/Home/Maintenance',
                '/ar/Home/Projects',
                '/ar/Home/FAQ',
                '/ar/Home/Terms',
                '/ar/Home/Privacy',
                '/ar/Home/SiteMap'
            ],
            'english': [
                '/en/Home',
                '/en/Home/AboutUs',
                '/en/Home/Vision',
                '/en/Home/Mission',
                '/en/Home/History',
                '/en/Home/OrganizationalChart',
                '/en/Home/CustomerService',
                '/en/Home/ServiceStepPage',
                '/en/Home/ElectronicServices',
                '/en/Home/BillInquiry',
                '/en/Home/PayBill',
                '/en/Home/NewConnection',
                '/en/Home/TransferSubscription',
                '/en/Home/CancelSubscription',
                '/en/Home/ComplaintSubmission',
                '/en/Home/Tariffs',
                '/en/Home/ElectricityTariffs',
                '/en/Home/Pricing',
                '/en/Home/RateSchedule',
                '/en/Home/ContactUs',
                '/en/Home/EmergencyNumbers',
                '/en/Home/ServiceAreas',
                '/en/Home/OfficeLocations',
                '/en/Home/WorkingHours',
                '/en/Home/News',
                '/en/Home/Announcements',
                '/en/Home/Tenders',
                '/en/Home/Careers',
                '/en/Home/Safety',
                '/en/Home/PowerOutages',
                '/en/Home/Maintenance',
                '/en/Home/Projects',
                '/en/Home/FAQ',
                '/en/Home/Terms',
                '/en/Home/Privacy',
                '/en/Home/SiteMap'
            ]
        }
        
        print("🔍 JEPCO Comprehensive Web Searcher initialized")
        print(f"📄 Ready to search {len(self.all_page_paths['arabic'])} Arabic pages")
        print(f"📄 Ready to search {len(self.all_page_paths['english'])} English pages")
    
    def search_jepco_realtime(self, query: str, language: str = 'arabic') -> Dict:
        """
        Comprehensive search across ALL JEPCO website pages
        """
        print(f"🔍 Comprehensive JEPCO website search for: {query}")
        
        results = {
            'query': query,
            'language': language,
            'results': [],
            'pages_searched': 0,
            'successful_pages': 0,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'source': 'comprehensive_search'
        }
        
        # Get all possible page paths for the language
        page_paths = self.all_page_paths.get(language, self.all_page_paths['arabic'])
        base_domain = 'https://www.jepco.com.jo'
        
        # First, get smart page selection based on query
        priority_pages = self._get_priority_pages(query, language)
        
        # Search priority pages first
        print(f"🎯 Searching {len(priority_pages)} priority pages...")
        for page_path in priority_pages:
            try:
                full_url = base_domain + page_path
                page_results = self._search_page(full_url, query, language)
                results['pages_searched'] += 1
                
                if page_results:
                    results['results'].extend(page_results)
                    results['successful_pages'] += 1
                    print(f"✅ Found {len(page_results)} results on {page_path}")
                
                time.sleep(0.5)  # Be respectful
                
            except Exception as e:
                print(f"⚠️ Error searching {page_path}: {str(e)}")
                continue
        
        # If we have good results from priority pages, return them
        if len(results['results']) >= 10:
            print(f"✅ Found sufficient results ({len(results['results'])}) from priority pages")
            return results
        
        # Otherwise, search additional pages
        print(f"🔍 Expanding search to more pages...")
        remaining_pages = [p for p in page_paths if p not in priority_pages]
        
        for page_path in remaining_pages[:15]:  # Limit to avoid overloading
            try:
                full_url = base_domain + page_path
                page_results = self._search_page(full_url, query, language)
                results['pages_searched'] += 1
                
                if page_results:
                    results['results'].extend(page_results)
                    results['successful_pages'] += 1
                    print(f"✅ Found {len(page_results)} results on {page_path}")
                
                time.sleep(0.5)
                
                # Stop if we have enough results
                if len(results['results']) >= 20:
                    break
                
            except Exception as e:
                print(f"⚠️ Error searching {page_path}: {str(e)}")
                continue
        
        print(f"✅ Comprehensive search complete: {len(results['results'])} total results from {results['successful_pages']}/{results['pages_searched']} pages")
        
        return results
    
    def _get_priority_pages(self, query: str, language: str) -> List[str]:
        """Get priority pages to search based on query content"""
        
        query_lower = query.lower()
        priority_pages = []
        
        # Always include home page
        home_path = '/ar/Home' if language == 'arabic' else '/en/Home'
        priority_pages.append(home_path)
        
        # Categorize query and add relevant pages
        page_categories = {
            # Billing and payments
            'billing': {
                'keywords': ['فاتورة', 'دفع', 'تسديد', 'حساب', 'bill', 'payment', 'pay', 'account'],
                'pages': ['/Home/BillInquiry', '/Home/PayBill', '/Home/ElectronicServices', '/Home/Tariffs', '/Home/Pricing']
            },
            # Services
            'services': {
                'keywords': ['خدمة', 'خدمات', 'طلب', 'اشتراك', 'service', 'request', 'subscription'],
                'pages': ['/Home/CustomerService', '/Home/ServiceStepPage', '/Home/ElectronicServices', '/Home/NewConnection']
            },
            # Contact and support
            'contact': {
                'keywords': ['اتصال', 'تواصل', 'هاتف', 'رقم', 'contact', 'phone', 'call', 'support'],
                'pages': ['/Home/ContactUs', '/Home/EmergencyNumbers', '/Home/CustomerService', '/Home/OfficeLocations']
            },
            # About company
            'about': {
                'keywords': ['عن', 'شركة', 'جيبكو', 'تاريخ', 'about', 'company', 'jepco', 'history'],
                'pages': ['/Home/AboutUs', '/Home/Vision', '/Home/Mission', '/Home/History', '/Home/OrganizationalChart']
            },
            # Technical and maintenance
            'technical': {
                'keywords': ['انقطاع', 'عطل', 'صيانة', 'مشروع', 'outage', 'fault', 'maintenance', 'project'],
                'pages': ['/Home/PowerOutages', '/Home/Maintenance', '/Home/Projects', '/Home/Safety']
            },
            # News and announcements
            'news': {
                'keywords': ['أخبار', 'إعلان', 'مناقصة', 'وظيفة', 'news', 'announcement', 'tender', 'career'],
                'pages': ['/Home/News', '/Home/Announcements', '/Home/Tenders', '/Home/Careers']
            },
            # Areas and locations
            'locations': {
                'keywords': ['منطقة', 'موقع', 'عنوان', 'مكتب', 'area', 'location', 'address', 'office'],
                'pages': ['/Home/ServiceAreas', '/Home/OfficeLocations', '/Home/WorkingHours']
            },
            # Help and FAQ
            'help': {
                'keywords': ['مساعدة', 'سؤال', 'شكوى', 'help', 'question', 'faq', 'complaint'],
                'pages': ['/Home/FAQ', '/Home/ComplaintSubmission', '/Home/CustomerService']
            }
        }
        
        # Add pages based on query content
        for category, info in page_categories.items():
            if any(keyword in query_lower for keyword in info['keywords']):
                for page in info['pages']:
                    full_path = f"/{language[0:2]}{page}" if language == 'english' else f"/ar{page}"
                    if full_path not in priority_pages:
                        priority_pages.append(full_path)
        
        # If no specific category found, add general service pages
        if len(priority_pages) == 1:  # Only home page
            general_pages = [
                '/Home/CustomerService',
                '/Home/ElectronicServices', 
                '/Home/ServiceStepPage',
                '/Home/ContactUs',
                '/Home/FAQ'
            ]
            for page in general_pages:
                full_path = f"/{language[0:2]}{page}" if language == 'english' else f"/ar{page}"
                priority_pages.append(full_path)
        
        print(f"🎯 Selected {len(priority_pages)} priority pages for query: {query}")
        return priority_pages[:10]  # Limit to top 10 priority pages
    
    def _search_page(self, url: str, query: str, language: str) -> List[Dict]:
        """Comprehensive search of a specific page for ALL relevant information"""
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements but keep navigation for links
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract ALL content types
            all_content = []
            query_keywords = self._extract_keywords(query, language)
            
            # 1. Extract ALL text content with structure
            content_elements = [
                # Headers (high priority)
                {'elements': soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']), 'priority': 10, 'type': 'header'},
                # Main content areas
                {'elements': soup.find_all(['div', 'section', 'article', 'main']), 'priority': 8, 'type': 'content'},
                # Paragraphs and text
                {'elements': soup.find_all(['p', 'span', 'li']), 'priority': 6, 'type': 'text'},
                # Tables (important for structured data)
                {'elements': soup.find_all(['table', 'tr', 'td', 'th']), 'priority': 9, 'type': 'table'},
                # Links (for navigation info)
                {'elements': soup.find_all('a'), 'priority': 4, 'type': 'link'},
                # Forms (for service information)
                {'elements': soup.find_all(['form', 'input', 'label']), 'priority': 7, 'type': 'form'}
            ]
            
            for content_group in content_elements:
                for element in content_group['elements']:
                    text = element.get_text(separator=' ', strip=True)
                    
                    # Skip very short or empty content
                    if not text or len(text) < 10:
                        continue
                    
                    # Calculate relevance score
                    text_lower = text.lower()
                    query_lower = query.lower()
                    
                    # Multiple scoring methods
                    keyword_score = sum(1 for keyword in query_keywords if keyword in text_lower)
                    direct_match_score = 5 if query_lower in text_lower else 0
                    priority_score = content_group['priority']
                    
                    total_score = keyword_score + direct_match_score + priority_score
                    
                    # Include content if it has any relevance or if it's important structural content
                    if total_score > 0 or content_group['type'] in ['header', 'table']:
                        
                        # Get additional context
                        parent_text = ""
                        if element.parent and element.parent.name not in ['html', 'body']:
                            parent_text = element.parent.get_text(separator=' ', strip=True)[:200]
                        
                        all_content.append({
                            'text': text[:1000],  # Increased length for more context
                            'relevance_score': total_score,
                            'source_url': url,
                            'element_type': element.name,
                            'content_type': content_group['type'],
                            'priority': content_group['priority'],
                            'parent_context': parent_text,
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                            'page_title': soup.title.string if soup.title else url.split('/')[-1]
                        })
            
            # 2. Extract specific structured data
            structured_data = self._extract_structured_data(soup, url)
            all_content.extend(structured_data)
            
            # 3. Sort by relevance and return comprehensive results
            all_content.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Return more results for comprehensive coverage
            return all_content[:15] if all_content else []
            
        except Exception as e:
            print(f"❌ Error searching page {url}: {str(e)}")
            return []
    
    def _extract_structured_data(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Extract specific structured data like contact info, prices, schedules"""
        
        structured_data = []
        
        # Extract contact information
        contact_patterns = [
            r'\b1\d{2}\b',  # 3-digit numbers like 116
            r'\b0\d{1,2}[-\s]?\d{7,8}\b',  # Phone numbers
            r'[\w\.-]+@[\w\.-]+\.\w+',  # Email addresses
        ]
        
        page_text = soup.get_text()
        for pattern in contact_patterns:
            matches = re.findall(pattern, page_text)
            for match in matches:
                structured_data.append({
                    'text': f"Contact Information: {match}",
                    'relevance_score': 15,  # High priority for contact info
                    'source_url': url,
                    'element_type': 'contact',
                    'content_type': 'structured',
                    'priority': 15,
                    'parent_context': '',
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'page_title': soup.title.string if soup.title else url.split('/')[-1]
                })
        
        # Extract pricing information
        pricing_patterns = [
            r'\d+(?:\.\d+)?\s*(?:فلس|fils)',
            r'\d+(?:\.\d+)?\s*(?:دينار|JOD)',
            r'\d+(?:\.\d+)?\s*(?:كيلو\s*واط|kWh)',
        ]
        
        for pattern in pricing_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            for match in matches:
                structured_data.append({
                    'text': f"Pricing Information: {match}",
                    'relevance_score': 12,
                    'source_url': url,
                    'element_type': 'pricing',
                    'content_type': 'structured',
                    'priority': 12,
                    'parent_context': '',
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'page_title': soup.title.string if soup.title else url.split('/')[-1]
                })
        
        # Extract working hours
        hours_patterns = [
            r'\d{1,2}:\d{2}\s*(?:AM|PM|صباحاً|مساءً)',
            r'من\s*\d{1,2}:\d{2}\s*إلى\s*\d{1,2}:\d{2}',
            r'from\s*\d{1,2}:\d{2}\s*to\s*\d{1,2}:\d{2}',
        ]
        
        for pattern in hours_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            for match in matches:
                structured_data.append({
                    'text': f"Working Hours: {match}",
                    'relevance_score': 10,
                    'source_url': url,
                    'element_type': 'hours',
                    'content_type': 'structured',
                    'priority': 10,
                    'parent_context': '',
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'page_title': soup.title.string if soup.title else url.split('/')[-1]
                })
        
        return structured_data
    
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
    
    def get_electricity_tariffs(self, language: str = 'arabic') -> Dict:
        """Get current electricity pricing and tariff information"""
        
        print("💰 Searching for electricity tariffs and pricing...")
        
        tariff_info = {
            'tariffs': [],
            'pricing_structure': [],
            'calculation_method': '',
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'currency': 'JOD',
            'source': 'live_search'
        }
        
        # Search for tariff-specific pages and keywords
        tariff_keywords = {
            'arabic': ['تعرفة', 'أسعار', 'كيلو واط', 'فلس', 'شريحة', 'استهلاك', 'تسعير'],
            'english': ['tariff', 'price', 'rate', 'kwh', 'kilowatt', 'tier', 'consumption', 'pricing']
        }
        
        # Possible tariff page URLs
        tariff_urls = [
            'https://www.jepco.com.jo/ar/Home/Tariffs',
            'https://www.jepco.com.jo/ar/Home/ElectricityTariffs', 
            'https://www.jepco.com.jo/ar/Home/Pricing',
            'https://www.jepco.com.jo/ar/Home/CustomerService',
            'https://www.jepco.com.jo/ar/Home/ServiceStepPage'
        ]
        
        if language == 'english':
            tariff_urls = [url.replace('/ar/', '/en/') for url in tariff_urls]
        
        base_url = self.base_urls.get(language, self.base_urls['arabic'])
        
        try:
            # Search main page first
            main_response = requests.get(base_url, headers=self.headers, timeout=10, verify=False)
            main_response.raise_for_status()
            main_soup = BeautifulSoup(main_response.content, 'html.parser')
            
            # Look for pricing tables
            pricing_data = self._extract_pricing_tables(main_soup)
            if pricing_data:
                tariff_info['tariffs'].extend(pricing_data)
            
            # Search specific tariff pages
            for tariff_url in tariff_urls:
                try:
                    print(f"🔍 Searching tariff page: {tariff_url}")
                    response = requests.get(tariff_url, headers=self.headers, timeout=10, verify=False)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        pricing_data = self._extract_pricing_tables(soup)
                        if pricing_data:
                            tariff_info['tariffs'].extend(pricing_data)
                        
                        # Look for pricing text
                        pricing_text = self._extract_pricing_text(soup, tariff_keywords[language])
                        if pricing_text:
                            tariff_info['pricing_structure'].extend(pricing_text)
                    
                    time.sleep(1)  # Be respectful
                    
                except Exception as e:
                    print(f"⚠️ Could not access {tariff_url}: {str(e)}")
                    continue
            
            # Search for pricing in general content
            general_pricing = self._search_pricing_in_content(base_url, tariff_keywords[language])
            if general_pricing:
                tariff_info['pricing_structure'].extend(general_pricing)
            
            print(f"✅ Found {len(tariff_info['tariffs'])} tariff entries and {len(tariff_info['pricing_structure'])} pricing details")
            
        except Exception as e:
            print(f"❌ Error searching for tariffs: {str(e)}")
            tariff_info['error'] = str(e)
        
        return tariff_info
    
    def _extract_pricing_tables(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract pricing information from HTML tables"""
        
        pricing_data = []
        
        # Look for tables that might contain pricing
        tables = soup.find_all('table')
        for table in tables:
            table_text = table.get_text().lower()
            
            # Check if table contains pricing keywords
            if any(keyword in table_text for keyword in ['كيلو واط', 'فلس', 'تعرفة', 'kwh', 'price', 'tariff', 'rate']):
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        row_text = [cell.get_text(strip=True) for cell in cells]
                        
                        # Look for patterns like consumption ranges and prices
                        for i, cell_text in enumerate(row_text):
                            if any(keyword in cell_text.lower() for keyword in ['كيلو واط', 'kwh', 'فلس', 'fils']):
                                pricing_data.append({
                                    'consumption_range': row_text[0] if i > 0 else '',
                                    'price': cell_text,
                                    'additional_info': ' | '.join(row_text),
                                    'source': 'table_extraction'
                                })
        
        return pricing_data
    
    def _extract_pricing_text(self, soup: BeautifulSoup, keywords: List[str]) -> List[str]:
        """Extract pricing information from text content"""
        
        pricing_text = []
        
        # Remove navigation, scripts, etc.
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()
        
        # Look for text containing pricing keywords
        all_text = soup.get_text()
        paragraphs = all_text.split('\n')
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if len(paragraph) > 20:  # Meaningful content
                paragraph_lower = paragraph.lower()
                
                # Check if contains pricing keywords
                keyword_count = sum(1 for keyword in keywords if keyword in paragraph_lower)
                
                if keyword_count > 0:
                    # Look for numbers that might be prices
                    import re
                    numbers = re.findall(r'\d+(?:\.\d+)?', paragraph)
                    
                    if numbers and any(keyword in paragraph_lower for keyword in ['فلس', 'fils', 'دينار', 'jod']):
                        pricing_text.append(paragraph[:300])  # Limit length
        
        return pricing_text[:5]  # Top 5 most relevant
    
    def _search_pricing_in_content(self, base_url: str, keywords: List[str]) -> List[str]:
        """Search for pricing information in general website content"""
        
        try:
            response = requests.get(base_url, headers=self.headers, timeout=10, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return self._extract_pricing_text(soup, keywords)
            
        except Exception as e:
            print(f"⚠️ Error searching pricing in content: {str(e)}")
            return []
    
    def calculate_electricity_cost(self, daily_kwh: float, tariff_info: Dict) -> Dict:
        """Calculate electricity cost based on consumption and tariff information"""
        
        calculation = {
            'daily_kwh': daily_kwh,
            'monthly_kwh': daily_kwh * 30,
            'yearly_kwh': daily_kwh * 365,
            'estimated_costs': {},
            'calculation_method': 'estimated',
            'currency': 'JOD',
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Try to extract actual rates from tariff info
        if tariff_info.get('tariffs'):
            rates = self._parse_tariff_rates(tariff_info['tariffs'])
            if rates:
                calculation['estimated_costs'] = self._calculate_with_rates(daily_kwh, rates)
                calculation['calculation_method'] = 'actual_tariffs'
                return calculation
        
        # Fallback to estimated rates if no actual rates found
        # These are approximate JEPCO rates (should be updated with actual rates)
        estimated_rates = [
            {'range': '0-160', 'rate': 0.068, 'description': 'First 160 kWh'},
            {'range': '161-300', 'rate': 0.090, 'description': 'Next 140 kWh (161-300)'},
            {'range': '301-500', 'rate': 0.120, 'description': 'Next 200 kWh (301-500)'},
            {'range': '501+', 'rate': 0.150, 'description': 'Above 500 kWh'}
        ]
        
        calculation['estimated_costs'] = self._calculate_with_rates(daily_kwh, estimated_rates)
        calculation['note'] = 'Estimated rates used. Contact JEPCO for exact current tariffs.'
        
        return calculation
    
    def _parse_tariff_rates(self, tariff_data: List[Dict]) -> List[Dict]:
        """Parse tariff data to extract usable rates"""
        
        rates = []
        import re
        
        for tariff in tariff_data:
            price_text = tariff.get('price', '')
            additional_info = tariff.get('additional_info', '')
            
            # Try to extract numerical rates
            numbers = re.findall(r'\d+(?:\.\d+)?', price_text + ' ' + additional_info)
            
            if numbers:
                try:
                    rate = float(numbers[0]) / 1000  # Convert fils to JOD if needed
                    if rate < 1:  # Reasonable rate range
                        rates.append({
                            'rate': rate,
                            'description': additional_info[:100],
                            'source': 'extracted'
                        })
                except ValueError:
                    continue
        
        return rates
    
    def _calculate_with_rates(self, daily_kwh: float, rates: List[Dict]) -> Dict:
        """Calculate costs using provided rates"""
        
        monthly_kwh = daily_kwh * 30
        
        costs = {
            'daily': 0,
            'monthly': 0,
            'yearly': 0,
            'breakdown': []
        }
        
        if not rates:
            return costs
        
        # Simple calculation with first available rate
        if rates and 'rate' in rates[0]:
            rate = rates[0]['rate']
            costs['daily'] = daily_kwh * rate
            costs['monthly'] = monthly_kwh * rate
            costs['yearly'] = daily_kwh * 365 * rate
            costs['rate_used'] = rate
            costs['breakdown'].append({
                'description': f'{daily_kwh} kWh daily at {rate} JOD/kWh',
                'daily_cost': costs['daily'],
                'monthly_cost': costs['monthly']
            })
        
        return costs


# Utility functions for integration
def search_jepco_website(query: str, language: str = 'arabic') -> str:
    """
    Comprehensive search function for integration with chatbot
    Returns formatted results with complete website information
    """
    
    searcher = JEPCOWebSearcher()
    results = searcher.search_jepco_realtime(query, language)
    
    if 'error' in results:
        return f"Unable to search website at this time: {results['error']}"
    
    if not results['results']:
        return "No current information found on JEPCO website for your query."
    
    # Format comprehensive results
    formatted_results = []
    
    # Header with search statistics
    search_stats = f"🔍 Comprehensive JEPCO Website Search Results ({results['timestamp']})"
    if 'pages_searched' in results:
        search_stats += f"\n📊 Searched {results['successful_pages']}/{results['pages_searched']} pages"
    formatted_results.append(search_stats + "\n")
    
    # Group results by content type for better organization
    content_groups = {
        'contact': [],
        'pricing': [], 
        'header': [],
        'table': [],
        'content': [],
        'other': []
    }
    
    for result in results['results'][:20]:  # More results for comprehensive coverage
        content_type = result.get('content_type', 'other')
        if content_type not in content_groups:
            content_type = 'other'
        content_groups[content_type].append(result)
    
    # Format results by priority groups
    priority_groups = [
        ('📞 Contact Information:', content_groups['contact']),
        ('💰 Pricing Information:', content_groups['pricing']),
        ('📋 Key Information:', content_groups['header']),
        ('📊 Structured Data:', content_groups['table']),
        ('📄 General Content:', content_groups['content'][:5]),  # Limit general content
        ('🔗 Additional Information:', content_groups['other'][:3])  # Limit other content
    ]
    
    for group_title, group_results in priority_groups:
        if group_results:
            formatted_results.append(group_title)
            for i, result in enumerate(group_results[:5], 1):  # Top 5 per group
                # Format based on content type
                text = result['text']
                page_title = result.get('page_title', 'JEPCO Page')
                
                if result.get('content_type') == 'structured':
                    formatted_results.append(f"• {text}")
                else:
                    # Truncate long content but keep important info
                    display_text = text[:400] + "..." if len(text) > 400 else text
                    formatted_results.append(f"• {display_text}")
                
                # Add source info for transparency
                if result.get('source_url'):
                    page_name = result['source_url'].split('/')[-1] or 'Home'
                    formatted_results.append(f"  📍 Source: {page_name}")
            
            formatted_results.append("")  # Add spacing between groups
    
    # Add footer with search summary
    total_results = len(results['results'])
    formatted_results.append(f"📈 Total Results Found: {total_results}")
    formatted_results.append(f"🌐 All information sourced from official JEPCO website")
    formatted_results.append(f"⏰ Search completed at: {results['timestamp']}")
    
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
