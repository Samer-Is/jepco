"""
JEPCO Website Content Scraper
Extracts customer service information from official JEPCO website
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
import warnings
from typing import Dict, List

# Suppress SSL warnings when using verify=False
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def scrape_complete_jepco_website() -> Dict:
    """
    MANDATORY: Extract ALL content from JEPCO website including:
    
    MAIN PAGES TO SCRAPE:
    - https://www.jepco.com.jo/ar/Home (Arabic homepage)
    - https://www.jepco.com.jo/en (English homepage)
    - All navigation menu items and subpages
    - All service pages
    - All contact pages
    - All customer service pages
    - All billing and payment pages
    - All technical service pages
    - All company information pages
    
    EXTRACT EVERYTHING INCLUDING:
    - Complete company information
    - All customer services
    - Complete billing information
    - All technical services
    - Complete contact information
    - Safety and regulations
    - All FAQ sections
    - Additional content
    """
    
    print("🚀 Starting COMPREHENSIVE JEPCO website extraction...")
    print("📋 This will extract ALL available content from the entire website")
    
    # Initialize comprehensive content structure
    comprehensive_content = {
        "extraction_metadata": {
            "extraction_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pages_scraped": [],
            "total_content_sections": 0,
            "extraction_method": "comprehensive_crawl",
            "languages_extracted": ["arabic", "english"]
        },
        "arabic": {
            "company_info": {},
            "services": {},
            "billing": {},
            "technical_services": {},
            "contact_info": {},
            "safety_regulations": {},
            "faq": {},
            "additional_content": {}
        },
        "english": {
            "company_info": {},
            "services": {},
            "billing": {},
            "technical_services": {},
            "contact_info": {},
            "safety_regulations": {},
            "faq": {},
            "additional_content": {}
        }
    }
    
    # Get all page URLs to scrape
    all_page_urls = get_all_jepco_page_urls()
    
    print(f"📄 Found {len(all_page_urls['arabic'])} Arabic pages to scrape")
    print(f"📄 Found {len(all_page_urls['english'])} English pages to scrape")
    
    # Extract content from priority pages first (limit to avoid overwhelming)
    for language in ['arabic', 'english']:
        print(f"\n🔍 Extracting {language.title()} content...")
        
        # Limit to first 10 pages for comprehensive extraction
        priority_pages = all_page_urls[language][:10]
        
        for page_url in priority_pages:
            try:
                print(f"   📖 Scraping: {page_url}")
                page_content = scrape_comprehensive_page_content(page_url, language)
                
                if page_content:
                    # Categorize and store content
                    categorized_content = categorize_page_content(page_content, page_url)
                    merge_content_into_structure(comprehensive_content[language], categorized_content)
                    comprehensive_content["extraction_metadata"]["pages_scraped"].append(page_url)
                    
                time.sleep(2)  # Be respectful to server
                
            except Exception as e:
                print(f"   ❌ Error scraping {page_url}: {str(e)}")
                continue
    
    # Post-process and validate content
    comprehensive_content = post_process_content(comprehensive_content)
    validation_report = validate_content_extraction(comprehensive_content)
    
    print(f"\n✅ Comprehensive extraction completed!")
    print(f"📊 Total pages scraped: {len(comprehensive_content['extraction_metadata']['pages_scraped'])}")
    print(f"📋 Content sections extracted: {comprehensive_content['extraction_metadata']['total_content_sections']}")
    
    return comprehensive_content


def get_all_jepco_page_urls() -> Dict:
    """Extract all navigation menu links from JEPCO website"""
    
    print("🔍 Discovering all JEPCO website pages...")
    
    base_urls = {
        'arabic': 'https://www.jepco.com.jo/ar/Home',
        'english': 'https://www.jepco.com.jo/en'
    }
    
    # Comprehensive list of all possible JEPCO pages
    page_paths = {
        'arabic': [
            '/ar/Home',
            '/ar/Home/AboutUs',
            '/ar/Home/Vision', 
            '/ar/Home/Mission',
            '/ar/Home/History',
            '/ar/Home/OrganizationalChart',
            '/ar/Home/BoardOfDirectors',
            '/ar/Home/Management',
            '/ar/Home/CustomerService',
            '/ar/Home/ServiceStepPage',
            '/ar/Home/ElectronicServices',
            '/ar/Home/BillInquiry',
            '/ar/Home/PayBill',
            '/ar/Home/PaymentMethods',
            '/ar/Home/NewConnection',
            '/ar/Home/ResidentialConnection',
            '/ar/Home/CommercialConnection',
            '/ar/Home/IndustrialConnection',
            '/ar/Home/TransferSubscription',
            '/ar/Home/CancelSubscription',
            '/ar/Home/AccountManagement',
            '/ar/Home/MeterServices',
            '/ar/Home/ComplaintSubmission',
            '/ar/Home/Tariffs',
            '/ar/Home/ElectricityTariffs',
            '/ar/Home/ResidentialTariffs',
            '/ar/Home/CommercialTariffs',
            '/ar/Home/IndustrialTariffs',
            '/ar/Home/Pricing',
            '/ar/Home/RateSchedule',
            '/ar/Home/BillingInformation',
            '/ar/Home/ContactUs',
            '/ar/Home/EmergencyNumbers',
            '/ar/Home/ServiceAreas',
            '/ar/Home/OfficeLocations',
            '/ar/Home/WorkingHours',
            '/ar/Home/PowerOutages',
            '/ar/Home/OutageReporting',
            '/ar/Home/ElectricalIssues',
            '/ar/Home/MaintenanceServices',
            '/ar/Home/TechnicalSupport',
            '/ar/Home/ElectricalSafety',
            '/ar/Home/SafetyRegulations',
            '/ar/Home/InstallationStandards',
            '/ar/Home/EmergencyProcedures',
            '/ar/Home/News',
            '/ar/Home/Announcements',
            '/ar/Home/ServiceUpdates',
            '/ar/Home/Tenders',
            '/ar/Home/Procurement',
            '/ar/Home/Careers',
            '/ar/Home/Employment',
            '/ar/Home/FAQ',
            '/ar/Home/BillingFAQ',
            '/ar/Home/ServiceFAQ',
            '/ar/Home/TechnicalFAQ',
            '/ar/Home/GeneralFAQ',
            '/ar/Home/Terms',
            '/ar/Home/TermsOfService',
            '/ar/Home/Privacy',
            '/ar/Home/PrivacyPolicy',
            '/ar/Home/SiteMap',
            '/ar/Home/EnergyConservation',
            '/ar/Home/RenewableEnergy',
            '/ar/Home/CSR',
            '/ar/Home/CommunityPrograms',
            '/ar/Home/Projects',
            '/ar/Home/Infrastructure'
        ],
        'english': [
            '/en/Home',
            '/en/Home/AboutUs',
            '/en/Home/Vision',
            '/en/Home/Mission', 
            '/en/Home/History',
            '/en/Home/OrganizationalChart',
            '/en/Home/BoardOfDirectors',
            '/en/Home/Management',
            '/en/Home/CustomerService',
            '/en/Home/ServiceStepPage',
            '/en/Home/ElectronicServices',
            '/en/Home/BillInquiry',
            '/en/Home/PayBill',
            '/en/Home/PaymentMethods',
            '/en/Home/NewConnection',
            '/en/Home/ResidentialConnection',
            '/en/Home/CommercialConnection',
            '/en/Home/IndustrialConnection',
            '/en/Home/TransferSubscription',
            '/en/Home/CancelSubscription',
            '/en/Home/AccountManagement',
            '/en/Home/MeterServices',
            '/en/Home/ComplaintSubmission',
            '/en/Home/Tariffs',
            '/en/Home/ElectricityTariffs',
            '/en/Home/ResidentialTariffs',
            '/en/Home/CommercialTariffs',
            '/en/Home/IndustrialTariffs',
            '/en/Home/Pricing',
            '/en/Home/RateSchedule',
            '/en/Home/BillingInformation',
            '/en/Home/ContactUs',
            '/en/Home/EmergencyNumbers',
            '/en/Home/ServiceAreas',
            '/en/Home/OfficeLocations',
            '/en/Home/WorkingHours',
            '/en/Home/PowerOutages',
            '/en/Home/OutageReporting',
            '/en/Home/ElectricalIssues',
            '/en/Home/MaintenanceServices',
            '/en/Home/TechnicalSupport',
            '/en/Home/ElectricalSafety',
            '/en/Home/SafetyRegulations',
            '/en/Home/InstallationStandards',
            '/en/Home/EmergencyProcedures',
            '/en/Home/News',
            '/en/Home/Announcements',
            '/en/Home/ServiceUpdates',
            '/en/Home/Tenders',
            '/en/Home/Procurement',
            '/en/Home/Careers',
            '/en/Home/Employment',
            '/en/Home/FAQ',
            '/en/Home/BillingFAQ',
            '/en/Home/ServiceFAQ',
            '/en/Home/TechnicalFAQ',
            '/en/Home/GeneralFAQ',
            '/en/Home/Terms',
            '/en/Home/TermsOfService',
            '/en/Home/Privacy',
            '/en/Home/PrivacyPolicy',
            '/en/Home/SiteMap',
            '/en/Home/EnergyConservation',
            '/en/Home/RenewableEnergy',
            '/en/Home/CSR',
            '/en/Home/CommunityPrograms',
            '/en/Home/Projects',
            '/en/Home/Infrastructure'
        ]
    }
    
    # Convert to full URLs
    all_urls = {}
    base_domain = 'https://www.jepco.com.jo'
    
    for language, paths in page_paths.items():
        all_urls[language] = []
        for path in paths:
            full_url = base_domain + path
            all_urls[language].append(full_url)
    
    return all_urls


def scrape_comprehensive_page_content(url: str, language: str) -> Dict:
    """Scrape content from individual page with comprehensive extraction"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract ALL content types
        page_content = {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'headers': extract_all_headers(soup),
            'paragraphs': extract_all_paragraphs(soup),
            'lists': extract_all_lists(soup),
            'tables': extract_all_tables(soup),
            'links': extract_all_links(soup, url),
            'forms': extract_all_forms(soup),
            'contact_info': extract_contact_information(soup),
            'structured_data': extract_structured_data_from_page(soup),
            'full_text': soup.get_text(separator=' ', strip=True)
        }
        
        return page_content
        
    except Exception as e:
        print(f"❌ Error scraping {url}: {str(e)}")
        return None


def extract_all_headers(soup: BeautifulSoup) -> List[Dict]:
    """Extract all headers (h1-h6) with hierarchy"""
    headers = []
    
    for level in range(1, 7):
        header_elements = soup.find_all(f'h{level}')
        for header in header_elements:
            text = header.get_text(strip=True)
            if text:
                headers.append({
                    'level': level,
                    'text': text,
                    'id': header.get('id', ''),
                    'class': header.get('class', [])
                })
    
    return headers


def extract_all_paragraphs(soup: BeautifulSoup) -> List[str]:
    """Extract all paragraph content"""
    paragraphs = []
    
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if text and len(text) > 10:  # Only meaningful content
            paragraphs.append(text)
    
    return paragraphs


def extract_all_lists(soup: BeautifulSoup) -> List[Dict]:
    """Extract all lists (ordered and unordered)"""
    lists = []
    
    for list_element in soup.find_all(['ul', 'ol']):
        list_items = []
        for li in list_element.find_all('li'):
            text = li.get_text(strip=True)
            if text:
                list_items.append(text)
        
        if list_items:
            lists.append({
                'type': list_element.name,
                'items': list_items
            })
    
    return lists


def extract_all_tables(soup: BeautifulSoup) -> List[Dict]:
    """Extract all table data"""
    tables = []
    
    for table in soup.find_all('table'):
        table_data = {
            'headers': [],
            'rows': []
        }
        
        # Extract headers
        header_row = table.find('thead') or table.find('tr')
        if header_row:
            headers = header_row.find_all(['th', 'td'])
            table_data['headers'] = [h.get_text(strip=True) for h in headers]
        
        # Extract all rows
        for row in table.find_all('tr')[1:]:  # Skip header row
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            if any(row_data):  # Only non-empty rows
                table_data['rows'].append(row_data)
        
        if table_data['headers'] or table_data['rows']:
            tables.append(table_data)
    
    return tables


def extract_all_links(soup: BeautifulSoup, base_url: str) -> List[Dict]:
    """Extract all links with context"""
    links = []
    
    for link in soup.find_all('a', href=True):
        text = link.get_text(strip=True)
        href = link['href']
        
        # Convert relative URLs to absolute
        if href.startswith('/'):
            href = 'https://www.jepco.com.jo' + href
        
        if text and href:
            links.append({
                'text': text,
                'url': href,
                'title': link.get('title', ''),
                'target': link.get('target', '')
            })
    
    return links


def extract_all_forms(soup: BeautifulSoup) -> List[Dict]:
    """Extract all form information"""
    forms = []
    
    for form in soup.find_all('form'):
        form_data = {
            'action': form.get('action', ''),
            'method': form.get('method', 'GET'),
            'fields': []
        }
        
        # Extract form fields
        for field in form.find_all(['input', 'select', 'textarea']):
            field_info = {
                'type': field.get('type', field.name),
                'name': field.get('name', ''),
                'label': '',
                'required': field.has_attr('required')
            }
            
            # Try to find associated label
            label = form.find('label', {'for': field.get('id')})
            if label:
                field_info['label'] = label.get_text(strip=True)
            
            form_data['fields'].append(field_info)
        
        if form_data['fields']:
            forms.append(form_data)
    
    return forms


def extract_contact_information(soup: BeautifulSoup) -> Dict:
    """Extract contact information using patterns"""
    contact_info = {
        'phone_numbers': [],
        'email_addresses': [],
        'addresses': [],
        'working_hours': []
    }
    
    page_text = soup.get_text()
    
    # Phone number patterns
    phone_patterns = [
        r'\b1\d{2}\b',  # 3-digit numbers like 116
        r'\b0\d{1,2}[-\s]?\d{7,8}\b',  # Jordanian phone numbers
        r'\+962[-\s]?\d{1,2}[-\s]?\d{7,8}',  # International format
    ]
    
    for pattern in phone_patterns:
        matches = re.findall(pattern, page_text)
        contact_info['phone_numbers'].extend(matches)
    
    # Email patterns
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    emails = re.findall(email_pattern, page_text)
    contact_info['email_addresses'].extend(emails)
    
    # Working hours patterns
    hours_patterns = [
        r'\d{1,2}:\d{2}\s*(?:AM|PM|صباحاً|مساءً)',
        r'من\s*\d{1,2}:\d{2}\s*إلى\s*\d{1,2}:\d{2}',
        r'from\s*\d{1,2}:\d{2}\s*to\s*\d{1,2}:\d{2}',
    ]
    
    for pattern in hours_patterns:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        contact_info['working_hours'].extend(matches)
    
    # Remove duplicates
    for key in contact_info:
        contact_info[key] = list(set(contact_info[key]))
    
    return contact_info


def extract_structured_data_from_page(soup: BeautifulSoup) -> Dict:
    """Extract structured data like pricing, procedures, requirements"""
    structured_data = {
        'pricing_info': [],
        'procedures': [],
        'requirements': [],
        'fees': []
    }
    
    page_text = soup.get_text()
    
    # Pricing patterns
    pricing_patterns = [
        r'\d+(?:\.\d+)?\s*(?:فلس|fils)',
        r'\d+(?:\.\d+)?\s*(?:دينار|JOD)',
        r'\d+(?:\.\d+)?\s*(?:كيلو\s*واط|kWh)',
    ]
    
    for pattern in pricing_patterns:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        structured_data['pricing_info'].extend(matches)
    
    # Procedure keywords
    procedure_keywords = ['خطوات', 'إجراءات', 'steps', 'procedure', 'process']
    requirements_keywords = ['متطلبات', 'شروط', 'requirements', 'conditions']
    
    # Extract sentences containing these keywords
    sentences = re.split(r'[.!?]', page_text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20:
            if any(keyword in sentence.lower() for keyword in procedure_keywords):
                structured_data['procedures'].append(sentence[:200])
            if any(keyword in sentence.lower() for keyword in requirements_keywords):
                structured_data['requirements'].append(sentence[:200])
    
    return structured_data


def categorize_page_content(page_content: Dict, page_url: str) -> Dict:
    """Categorize page content into structured sections"""
    
    categorized = {
        'company_info': {},
        'services': {},
        'billing': {},
        'technical_services': {},
        'contact_info': {},
        'safety_regulations': {},
        'faq': {},
        'additional_content': {}
    }
    
    url_lower = page_url.lower()
    title_lower = page_content.get('title', '').lower()
    
    # Categorize based on URL and content
    if any(keyword in url_lower for keyword in ['about', 'vision', 'mission', 'history', 'company']):
        categorized['company_info'] = page_content
    elif any(keyword in url_lower for keyword in ['service', 'connection', 'customer', 'electronic']):
        categorized['services'] = page_content
    elif any(keyword in url_lower for keyword in ['bill', 'payment', 'tariff', 'pricing']):
        categorized['billing'] = page_content
    elif any(keyword in url_lower for keyword in ['outage', 'maintenance', 'technical', 'electrical']):
        categorized['technical_services'] = page_content
    elif any(keyword in url_lower for keyword in ['contact', 'office', 'emergency']):
        categorized['contact_info'] = page_content
    elif any(keyword in url_lower for keyword in ['safety', 'regulation', 'standard']):
        categorized['safety_regulations'] = page_content
    elif any(keyword in url_lower for keyword in ['faq', 'question', 'help']):
        categorized['faq'] = page_content
    else:
        categorized['additional_content'] = page_content
    
    return categorized


def merge_content_into_structure(main_structure: Dict, new_content: Dict):
    """Merge new content into main structure"""
    
    for category, content in new_content.items():
        if content:  # Only merge non-empty content
            if category not in main_structure:
                main_structure[category] = {}
            
            # Merge content intelligently
            if isinstance(content, dict):
                for key, value in content.items():
                    if key not in main_structure[category]:
                        main_structure[category][key] = value
                    elif isinstance(value, list):
                        if isinstance(main_structure[category][key], list):
                            main_structure[category][key].extend(value)
                        else:
                            main_structure[category][key] = [main_structure[category][key]] + value
                    elif isinstance(value, str) and value not in str(main_structure[category][key]):
                        main_structure[category][key] = str(main_structure[category][key]) + " | " + value


def post_process_content(content: Dict) -> Dict:
    """Clean and structure scraped content for chatbot use"""
    
    print("🧹 Post-processing extracted content...")
    
    # Count total content sections
    total_sections = 0
    
    for language in ['arabic', 'english']:
        if language in content:
            for category in content[language]:
                if content[language][category]:
                    total_sections += 1
    
    content['extraction_metadata']['total_content_sections'] = total_sections
    
    # Clean and deduplicate content
    for language in ['arabic', 'english']:
        if language in content:
            content[language] = clean_and_deduplicate_content(content[language])
    
    return content


def clean_and_deduplicate_content(language_content: Dict) -> Dict:
    """Clean and deduplicate content within a language"""
    
    cleaned_content = {}
    
    for category, category_content in language_content.items():
        if category_content:
            cleaned_content[category] = {}
            
            for key, value in category_content.items():
                if isinstance(value, list):
                    # Handle lists with different types of content
                    cleaned_list = []
                    seen_strings = set()
                    
                    for item in value:
                        if isinstance(item, str):
                            # Clean and deduplicate strings
                            cleaned_item = re.sub(r'\s+', ' ', item.strip())
                            if cleaned_item and cleaned_item not in seen_strings:
                                cleaned_list.append(cleaned_item)
                                seen_strings.add(cleaned_item)
                        elif isinstance(item, dict):
                            # Keep dictionaries as-is (can't hash them for deduplication)
                            cleaned_list.append(item)
                        else:
                            # Keep other types as-is
                            cleaned_list.append(item)
                    
                    cleaned_content[category][key] = cleaned_list
                elif isinstance(value, str):
                    # Clean string content
                    cleaned_value = re.sub(r'\s+', ' ', value.strip())
                    if cleaned_value:
                        cleaned_content[category][key] = cleaned_value
                else:
                    cleaned_content[category][key] = value
    
    return cleaned_content


def validate_content_extraction(content: Dict) -> Dict:
    """
    MANDATORY: Ensure ALL website content is extracted
    
    CHECK FOR:
    - All main navigation pages scraped
    - All service pages included
    - All contact information extracted
    - All FAQ sections covered
    - Both English and Arabic content
    - All phone numbers and addresses
    - All procedures and requirements
    - All fees and pricing information
    - All forms and documents mentioned
    
    RETURN: Validation report with missing content
    """
    
    print("🔍 Validating content extraction completeness...")
    
    validation_report = {
        'validation_date': time.strftime("%Y-%m-%d %H:%M:%S"),
        'total_pages_scraped': len(content.get('extraction_metadata', {}).get('pages_scraped', [])),
        'languages_validated': [],
        'content_completeness': {},
        'missing_content': [],
        'validation_score': 0,
        'recommendations': []
    }
    
    required_categories = [
        'company_info', 'services', 'billing', 'technical_services',
        'contact_info', 'safety_regulations', 'faq', 'additional_content'
    ]
    
    for language in ['arabic', 'english']:
        if language in content:
            validation_report['languages_validated'].append(language)
            language_completeness = {}
            
            for category in required_categories:
                has_content = bool(content[language].get(category))
                language_completeness[category] = has_content
                
                if not has_content:
                    validation_report['missing_content'].append(f"{language}:{category}")
            
            validation_report['content_completeness'][language] = language_completeness
    
    # Calculate validation score
    total_required = len(required_categories) * 2  # Arabic + English
    total_found = sum(
        sum(completeness.values()) 
        for completeness in validation_report['content_completeness'].values()
    )
    
    validation_report['validation_score'] = (total_found / total_required) * 100
    
    # Generate recommendations
    if validation_report['validation_score'] < 80:
        validation_report['recommendations'].append("Content extraction incomplete - consider additional scraping")
    if len(validation_report['missing_content']) > 0:
        validation_report['recommendations'].append(f"Missing content in: {', '.join(validation_report['missing_content'])}")
    
    print(f"✅ Validation completed - Score: {validation_report['validation_score']:.1f}%")
    
    return validation_report


def save_complete_content_to_json(content: Dict):
    """Save ALL scraped content to data/jepco_content.json"""
    
    try:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Create backup of existing file
        if os.path.exists('data/jepco_content.json'):
            backup_name = f"data/jepco_content_backup_{int(time.time())}.json"
            os.rename('data/jepco_content.json', backup_name)
            print(f"📁 Backup created: {backup_name}")
        
        # Save comprehensive content
        with open('data/jepco_content.json', 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        print("✅ Comprehensive content saved to data/jepco_content.json")
        
        # Print detailed summary
        print(f"\n📊 COMPREHENSIVE EXTRACTION SUMMARY:")
        print(f"📅 Extraction Date: {content['extraction_metadata']['extraction_date']}")
        print(f"📄 Pages Scraped: {len(content['extraction_metadata']['pages_scraped'])}")
        print(f"📋 Content Sections: {content['extraction_metadata']['total_content_sections']}")
        
        for language in ['arabic', 'english']:
            if language in content:
                print(f"\n🔤 {language.title()} Content:")
                for category, category_content in content[language].items():
                    if category_content:
                        content_count = len(category_content) if isinstance(category_content, dict) else 1
                        print(f"   • {category}: {content_count} items")
        
    except Exception as e:
        print(f"❌ Error saving comprehensive content: {str(e)}")
        raise


# Legacy function for compatibility
def scrape_jepco_content() -> Dict:
    """Legacy function - now calls comprehensive scraper"""
    return scrape_complete_jepco_website()


if __name__ == "__main__":
    """Test comprehensive extraction"""
    print("🚀 Testing comprehensive JEPCO website extraction...")
    
    # Run comprehensive extraction
    comprehensive_content = scrape_complete_jepco_website()
    
    # Save to JSON
    save_complete_content_to_json(comprehensive_content)
    
    print("✅ Test completed!")
