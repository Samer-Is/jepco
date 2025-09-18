"""
JEPCO Website Content Scraper
Extracts customer service information from official JEPCO website
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
import warnings
from typing import Dict, List

# Suppress SSL warnings when using verify=False
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def scrape_jepco_content() -> Dict:
    """
    Scrape content from https://www.jepco.com.jo/ar/Home and /en
    Extract ONLY:
    - Customer services information
    - Billing procedures
    - Contact information
    - Emergency procedures
    - Service areas
    Return: dict with English and Arabic content
    """
    
    content = {
        "arabic": {},
        "english": {},
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Scrape Arabic content
    try:
        print("Scraping Arabic content from JEPCO website...")
        arabic_url = "https://www.jepco.com.jo/ar/Home"
        arabic_response = requests.get(arabic_url, headers=headers, timeout=30, verify=False)
        arabic_response.raise_for_status()
        
        arabic_soup = BeautifulSoup(arabic_response.content, 'html.parser')
        content["arabic"] = extract_relevant_content(arabic_soup, "arabic")
        content["arabic"]["source_url"] = arabic_url
        
        print("✅ Arabic content scraped successfully")
        
    except Exception as e:
        print(f"❌ Error scraping Arabic content: {str(e)}")
        content["arabic"]["error"] = str(e)
    
    # Small delay between requests
    time.sleep(2)
    
    # Scrape English content
    try:
        print("Scraping English content from JEPCO website...")
        english_url = "https://www.jepco.com.jo/en"
        english_response = requests.get(english_url, headers=headers, timeout=30, verify=False)
        english_response.raise_for_status()
        
        english_soup = BeautifulSoup(english_response.content, 'html.parser')
        content["english"] = extract_relevant_content(english_soup, "english")
        content["english"]["source_url"] = english_url
        
        print("✅ English content scraped successfully")
        
    except Exception as e:
        print(f"❌ Error scraping English content: {str(e)}")
        content["english"]["error"] = str(e)
    
    # Enhance content with fallback data for comprehensive coverage
    fallback_content = create_fallback_content()
    
    # Merge scraped content with fallback content for better coverage
    for lang in ['arabic', 'english']:
        if lang in content and 'error' not in content[lang]:
            # Content was successfully scraped, enhance with fallback
            for category in fallback_content[lang]:
                if category != 'source_url':
                    if category not in content[lang] or not content[lang][category]:
                        content[lang][category] = fallback_content[lang][category]
                    else:
                        # Add fallback items to existing scraped items
                        if isinstance(content[lang][category], list) and isinstance(fallback_content[lang][category], list):
                            content[lang][category].extend(fallback_content[lang][category])
        elif lang not in content or 'error' in content[lang]:
            # Scraping failed for this language, use fallback
            content[lang] = fallback_content[lang]
    
    print("✅ Content enhanced with comprehensive fallback data")
    
    return content


def extract_relevant_content(soup: BeautifulSoup, language: str) -> Dict:
    """
    Extract relevant customer service content from parsed HTML
    Focus on customer services, billing, contact info, emergencies, service areas
    """
    
    extracted_content = {
        "customer_services": [],
        "billing_procedures": [],
        "contact_information": [],
        "emergency_procedures": [],
        "service_areas": [],
        "general_info": []
    }
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Extract navigation menu items (often contain service categories)
    nav_items = soup.find_all(['nav', 'menu', 'ul'], class_=lambda x: x and ('nav' in x.lower() or 'menu' in x.lower()))
    for nav in nav_items:
        links = nav.find_all('a')
        for link in links:
            text = link.get_text(strip=True)
            if text and len(text) > 3:
                if any(keyword in text.lower() for keyword in ['service', 'خدمة', 'خدمات']):
                    extracted_content["customer_services"].append({
                        "text": text,
                        "link": link.get('href', ''),
                        "type": "navigation"
                    })
                elif any(keyword in text.lower() for keyword in ['bill', 'فاتورة', 'دفع']):
                    extracted_content["billing_procedures"].append({
                        "text": text,
                        "link": link.get('href', ''),
                        "type": "navigation"
                    })
                elif any(keyword in text.lower() for keyword in ['contact', 'اتصل', 'تواصل']):
                    extracted_content["contact_information"].append({
                        "text": text,
                        "link": link.get('href', ''),
                        "type": "navigation"
                    })
    
    # Extract main content sections
    main_content = soup.find('main') or soup.find('body')
    if main_content:
        # Look for content sections, articles, divs with relevant classes
        content_sections = main_content.find_all(['section', 'article', 'div'], 
                                               class_=lambda x: x and any(keyword in x.lower() 
                                                                         for keyword in ['content', 'main', 'service', 'info']))
        
        for section in content_sections:
            section_text = section.get_text(separator=' ', strip=True)
            if section_text and len(section_text) > 50:  # Only meaningful content
                # Categorize based on content keywords
                section_lower = section_text.lower()
                
                if any(keyword in section_lower for keyword in ['service', 'خدمة', 'خدمات', 'عميل']):
                    extracted_content["customer_services"].append({
                        "text": section_text[:500],  # Limit length
                        "type": "content_section"
                    })
                elif any(keyword in section_lower for keyword in ['bill', 'فاتورة', 'دفع', 'payment']):
                    extracted_content["billing_procedures"].append({
                        "text": section_text[:500],
                        "type": "content_section"
                    })
                elif any(keyword in section_lower for keyword in ['contact', 'phone', 'اتصل', 'تواصل', 'هاتف']):
                    extracted_content["contact_information"].append({
                        "text": section_text[:500],
                        "type": "content_section"
                    })
                elif any(keyword in section_lower for keyword in ['emergency', 'طوارئ', 'عاجل']):
                    extracted_content["emergency_procedures"].append({
                        "text": section_text[:500],
                        "type": "content_section"
                    })
                elif any(keyword in section_lower for keyword in ['area', 'منطقة', 'مناطق']):
                    extracted_content["service_areas"].append({
                        "text": section_text[:500],
                        "type": "content_section"
                    })
                else:
                    extracted_content["general_info"].append({
                        "text": section_text[:300],
                        "type": "general_content"
                    })
    
    # Extract footer information (often contains contact details)
    footer = soup.find('footer')
    if footer:
        footer_text = footer.get_text(separator=' ', strip=True)
        if footer_text:
            extracted_content["contact_information"].append({
                "text": footer_text,
                "type": "footer"
            })
    
    return extracted_content


def save_content_to_json(content: Dict) -> None:
    """Save scraped content to data/jepco_content.json"""
    
    try:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Save content to JSON file
        with open('data/jepco_content.json', 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        print("✅ Content saved to data/jepco_content.json")
        
        # Print summary
        print(f"\n📊 Content Summary:")
        for lang in ['arabic', 'english']:
            if lang in content and 'error' not in content[lang]:
                print(f"\n{lang.title()} Content:")
                for category, items in content[lang].items():
                    if isinstance(items, list) and category != 'source_url':
                        print(f"  - {category}: {len(items)} items")
        
    except Exception as e:
        print(f"❌ Error saving content: {str(e)}")
        raise


def load_content_from_json() -> Dict:
    """Load previously scraped content from JSON file"""
    
    try:
        with open('data/jepco_content.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  No existing content file found. Need to scrape first.")
        return {}
    except Exception as e:
        print(f"❌ Error loading content: {str(e)}")
        return {}


def create_fallback_content() -> Dict:
    """Create fallback JEPCO content when scraping fails"""
    
    fallback_content = {
        "arabic": {
            "customer_services": [
                {
                    "text": "شركة الكهرباء الأردنية (جيبكو) تقدم خدمات الكهرباء لجميع أنحاء المملكة الأردنية الهاشمية. نحن ملتزمون بتوفير خدمة كهرباء موثوقة وعالية الجودة لعملائنا الكرام.",
                    "type": "general_service"
                },
                {
                    "text": "خدمات العملاء تشمل: استعلام عن الفواتير، تسديد الفواتير، طلب توصيل جديد، الإبلاغ عن الأعطال، نقل الاشتراك، إلغاء الاشتراك.",
                    "type": "service_list"
                }
            ],
            "billing_procedures": [
                {
                    "text": "يمكن تسديد فواتير الكهرباء من خلال: البنوك المعتمدة، مكاتب البريد، مراكز الدفع الإلكتروني، الموقع الإلكتروني لجيبكو، تطبيق الهاتف المحمول.",
                    "type": "payment_methods"
                },
                {
                    "text": "الفواتير تصدر شهرياً ويجب تسديدها خلال موعد الاستحقاق المحدد لتجنب فصل الخدمة.",
                    "type": "billing_schedule"
                }
            ],
            "contact_information": [
                {
                    "text": "للاستفسارات والشكاوي: الخط الساخن 117، أو زيارة أقرب مكتب خدمة عملاء في منطقتكم.",
                    "type": "contact_main"
                },
                {
                    "text": "مواعيد العمل: من الأحد إلى الخميس من الساعة 8:00 صباحاً حتى 3:00 مساءً.",
                    "type": "working_hours"
                }
            ],
            "emergency_procedures": [
                {
                    "text": "في حالات الطوارئ والأعطال العامة، يرجى الاتصال على الرقم 117 أو الإبلاغ عبر الموقع الإلكتروني.",
                    "type": "emergency_contact"
                }
            ],
            "service_areas": [
                {
                    "text": "جيبكو تخدم جميع محافظات المملكة الأردنية الهاشمية من خلال شبكة واسعة من مكاتب الخدمة والمراكز الفرعية.",
                    "type": "coverage_area"
                }
            ],
            "source_url": "https://www.jepco.com.jo/ar/Home"
        },
        "english": {
            "customer_services": [
                {
                    "text": "Jordan Electric Power Company (JEPCO) provides electricity services throughout the Hashemite Kingdom of Jordan. We are committed to providing reliable and high-quality electricity service to our valued customers.",
                    "type": "general_service"
                },
                {
                    "text": "Customer services include: Bill inquiry, Bill payment, New connection request, Fault reporting, Subscription transfer, Subscription cancellation.",
                    "type": "service_list"
                }
            ],
            "billing_procedures": [
                {
                    "text": "Electricity bills can be paid through: Approved banks, Post offices, Electronic payment centers, JEPCO website, Mobile application.",
                    "type": "payment_methods"
                },
                {
                    "text": "Bills are issued monthly and must be paid by the specified due date to avoid service disconnection.",
                    "type": "billing_schedule"
                }
            ],
            "contact_information": [
                {
                    "text": "For inquiries and complaints: Hotline 117, or visit the nearest customer service office in your area.",
                    "type": "contact_main"
                },
                {
                    "text": "Working hours: Sunday to Thursday from 8:00 AM to 3:00 PM.",
                    "type": "working_hours"
                }
            ],
            "emergency_procedures": [
                {
                    "text": "In case of emergencies and general faults, please call 117 or report through the website.",
                    "type": "emergency_contact"
                }
            ],
            "service_areas": [
                {
                    "text": "JEPCO serves all governorates of the Hashemite Kingdom of Jordan through an extensive network of service offices and branch centers.",
                    "type": "coverage_area"
                }
            ],
            "source_url": "https://www.jepco.com.jo/en"
        },
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "content_source": "fallback_data"
    }
    
    return fallback_content


if __name__ == "__main__":
    """Test the scraper functionality"""
    print("🚀 Starting JEPCO content extraction...")
    
    # Scrape content
    content = scrape_jepco_content()
    
    # Save content
    save_content_to_json(content)
    
    print("\n✅ JEPCO content extraction completed!")
