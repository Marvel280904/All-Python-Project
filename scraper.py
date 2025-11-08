# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# import pandas as pd
# import time
# import re
# import random
# from urllib.parse import urljoin

# class WorkNPlaySeleniumScraper:
#     def __init__(self):
#         self.base_url = "https://www.theworknplay.com"
#         self.driver = None
#         self.school_data = []
        
#     def setup_driver(self):
#         """Setup Chrome WebDriver"""
#         print("Setting up Chrome WebDriver...")
        
#         options = webdriver.ChromeOptions()
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
#         service = Service(ChromeDriverManager().install())
#         self.driver = webdriver.Chrome(service=service, options=options)
        
#         # Mask as human
#         self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
#     def wait_for_element(self, by, value, timeout=10):
#         """Wait for element to be present"""
#         return WebDriverWait(self.driver, timeout).until(
#             EC.presence_of_element_located((by, value))
#         )
        
#     def wait_for_elements(self, by, value, timeout=10):
#         """Wait for elements to be present"""
#         return WebDriverWait(self.driver, timeout).until(
#             EC.presence_of_all_elements_located((by, value))
#         )
    
#     def get_all_job_links(self):
#         """Get all job links using Selenium"""
#         print("Mengambil semua link pekerjaan dengan Selenium...")
        
#         job_links = []
        
#         try:
#             # Navigate to jobs page
#             jobs_url = f"{self.base_url}/Work/Search/Job"
#             self.driver.get(jobs_url)
            
#             # Wait for page to load
#             time.sleep(5)
            
#             # Scroll to load all content
#             self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)
            
#             # Cari job listings - coba berbagai kemungkinan selector
#             selectors_to_try = [
#                 "//a[contains(@href, '/Work/Detail/Company/')]",
#                 "//a[contains(@href, 'Company')]",
#                 "//div[contains(@class, 'job')]//a",
#                 "//div[contains(@class, 'listing')]//a", 
#                 "//h4//a",
#                 "//h3//a",
#                 "//*[contains(text(), 'Embark')]//ancestor::a",
#                 "//*[contains(text(), 'SLP')]//ancestor::a"
#             ]
            
#             for selector in selectors_to_try:
#                 try:
#                     links = self.driver.find_elements(By.XPATH, selector)
#                     if links:
#                         print(f"Found {len(links)} elements with: {selector}")
#                         for link in links:
#                             href = link.get_attribute('href')
#                             text = link.text.strip()
#                             if href and '/Work/Detail/Company/' in href:
#                                 job_links.append({
#                                     'url': href,
#                                     'text': text
#                                 })
#                                 print(f"  - {text} -> {href}")
#                 except Exception as e:
#                     continue
            
#             # Jika masih tidak ketemu, coba capture semua links dan filter
#             if not job_links:
#                 print("Mencoba method alternatif: capture semua links...")
#                 all_links = self.driver.find_elements(By.TAG_NAME, "a")
                
#                 for link in all_links:
#                     href = link.get_attribute('href')
#                     text = link.text.strip()
                    
#                     if href and '/Work/Detail/Company/' in href and text:
#                         job_links.append({
#                             'url': href,
#                             'text': text
#                         })
            
#             # Remove duplicates
#             unique_links = []
#             seen_urls = set()
            
#             for job in job_links:
#                 if job['url'] not in seen_urls:
#                     seen_urls.add(job['url'])
#                     unique_links.append(job['url'])
            
#             print(f"Total unique company links found: {len(unique_links)}")
#             return unique_links
            
#         except Exception as e:
#             print(f"Error getting job links: {e}")
#             return []
    
#     def extract_school_info(self, company_url):
#         """Extract school information from company page"""
#         print(f"Scraping: {company_url}")
        
#         school_info = {
#             'school_name': '',
#             'address': '',
#             'phone': '',
#             'email': '',
#             'website': '',
#             'source_url': company_url
#         }
        
#         try:
#             self.driver.get(company_url)
#             time.sleep(3)
            
#             # Extract school name
#             name_selectors = [
#                 "//h1", "//h2", "//h3", "//h4",
#                 "//div[contains(@class, 'company')]",
#                 "//div[contains(@class, 'school')]",
#                 "//div[contains(@class, 'employer')]"
#             ]
            
#             for selector in name_selectors:
#                 try:
#                     name_element = self.driver.find_element(By.XPATH, selector)
#                     name_text = name_element.text.strip()
#                     if name_text and len(name_text) > 2:
#                         school_info['school_name'] = name_text
#                         break
#                 except:
#                     continue
            
#             # Extract address
#             address_selectors = [
#                 "//p[contains(text(), 'Seoul')]",
#                 "//p[contains(text(), 'Korea')]",
#                 "//div[contains(@class, 'address')]",
#                 "//div[contains(@class, 'location')]",
#                 "//p"
#             ]
            
#             for selector in address_selectors:
#                 try:
#                     address_elements = self.driver.find_elements(By.XPATH, selector)
#                     for elem in address_elements:
#                         text = elem.text.strip()
#                         if any(keyword in text for keyword in ['Seoul', 'Korea', '-gu', '-dong']):
#                             if len(text) > 10 and len(text) < 200:
#                                 school_info['address'] = text
#                                 break
#                     if school_info['address']:
#                         break
#                 except:
#                     continue
            
#             # Extract phone and email from page source
#             page_source = self.driver.page_source
            
#             # Phone patterns
#             phone_patterns = [
#                 r'\d{2,4}[-.\s]?\d{3,4}[-.\s]?\d{4}',
#                 r'\+?82[-.\s]?\d{1,2}[-.\s]?\d{3,4}[-.\s]?\d{4}'
#             ]
            
#             for pattern in phone_patterns:
#                 phones = re.findall(pattern, page_source)
#                 if phones:
#                     school_info['phone'] = phones[0]
#                     break
            
#             # Email pattern
#             email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#             emails = re.findall(email_pattern, page_source)
#             if emails:
#                 school_info['email'] = emails[0]
            
#             print(f"✓ Extracted: {school_info['school_name']}")
#             return school_info
            
#         except Exception as e:
#             print(f"✗ Error scraping {company_url}: {e}")
#             return school_info
    
#     def scrape_all_data(self, max_companies=10):
#         """Main scraping function"""
#         print("=== MEMULAI SCRAPING DENGAN SELENIUM ===")
        
#         try:
#             self.setup_driver()
            
#             # Get all company links
#             company_links = self.get_all_job_links()
            
#             if not company_links:
#                 print("Tidak ada company links yang ditemukan!")
#                 return
            
#             print(f"Memproses {len(company_links)} companies...")
            
#             # Process each company (limit for testing)
#             for i, company_url in enumerate(company_links[:max_companies]):
#                 print(f"\n[{i+1}/{min(len(company_links), max_companies)}] ", end="")
                
#                 school_info = self.extract_school_info(company_url)
                
#                 if school_info['school_name']:
#                     self.school_data.append(school_info)
                
#                 # Random delay
#                 time.sleep(random.uniform(2, 4))
            
#             print(f"\nBerhasil mengumpulkan data dari {len(self.school_data)} sekolah")
            
#         except Exception as e:
#             print(f"Error during scraping: {e}")
        
#         finally:
#             if self.driver:
#                 self.driver.quit()
#                 print("Browser closed.")
    
#     def save_to_csv(self, filename="selenium_schools_data.csv"):
#         """Save data to CSV"""
#         if not self.school_data:
#             print("No data to save!")
#             return
        
#         df = pd.DataFrame(self.school_data)
#         df.to_csv(filename, index=False, encoding='utf-8-sig')
#         print(f"Data disimpan ke: {filename}")
        
#         # Show summary
#         print(f"\n=== SUMMARY ===")
#         print(f"Total schools: {len(df)}")
#         print(f"With name: {df['school_name'].notna().sum()}")
#         print(f"With address: {df['address'].notna().sum()}")
#         print(f"With phone: {df['phone'].notna().sum()}")
#         print(f"With email: {df['email'].notna().sum()}")

# # Main execution
# if __name__ == "__main__":
#     scraper = WorkNPlaySeleniumScraper()
    
#     # Scrape data (limit to 10 for testing)
#     scraper.scrape_all_data(max_companies=10)
    
#     # Save to CSV
#     scraper.save_to_csv()
    
#     print("\n🎉 SCRAPING SELESAI! 🎉")



# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# import pandas as pd
# import time
# import re
# import random

# class WorkNPlaySchoolScraper:
#     def __init__(self):
#         self.base_url = "https://www.theworknplay.com"
#         self.driver = None
#         self.school_data = []
        
#     def setup_driver(self):
#         """Setup Chrome WebDriver"""
#         print("Setting up Chrome WebDriver...")
        
#         options = webdriver.ChromeOptions()
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
#         service = Service(ChromeDriverManager().install())
#         self.driver = webdriver.Chrome(service=service, options=options)
#         self.driver.maximize_window()
        
#     def wait_for_element(self, by, value, timeout=10):
#         """Wait for element to be present"""
#         try:
#             return WebDriverWait(self.driver, timeout).until(
#                 EC.presence_of_element_located((by, value))
#             )
#         except:
#             return None
    
#     def scroll_to_load_all_schools(self):
#         """Scroll sampai semua sekolah ter-load di halaman utama"""
#         print("Scrolling to load all schools...")
        
#         last_count = 0
#         no_change_count = 0
#         max_scroll_attempts = 15
        
#         for attempt in range(max_scroll_attempts):
#             # Scroll ke bawah
#             self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2)
            
#             # Hitung berapa banyak sekolah yang terlihat
#             current_schools = self.get_visible_school_count()
            
#             print(f"Scroll {attempt + 1}: Found {current_schools} schools")
            
#             # Cek jika jumlah sekolah bertambah
#             if current_schools == last_count:
#                 no_change_count += 1
#                 if no_change_count >= 3:
#                     print("No new schools loaded. Stopping scroll.")
#                     break
#             else:
#                 no_change_count = 0
#                 last_count = current_schools
            
#             # Jika sudah banyak sekolah, stop
#             if current_schools >= 100:
#                 print(f"Reached {current_schools} schools!")
#                 break
        
#         return last_count
    
#     def get_visible_school_count(self):
#         """Hitung berapa banyak sekolah yang terlihat di halaman"""
#         try:
#             schools = self.driver.find_elements(By.XPATH, "//article[contains(@class, 'media')]//h5/a[contains(@onclick, 'showJobDetail')]")
#             return len(schools)
#         except:
#             return 0
    
#     def get_all_school_job_ids(self):
#         """Dapatkan semua job ID sekolah dari halaman utama"""
#         print("Collecting all school job IDs from main page...")
        
#         job_ids = []
        
#         try:
#             # Cari semua element sekolah di halaman utama
#             school_elements = self.driver.find_elements(By.XPATH, "//article[contains(@class, 'media')]//h5/a[contains(@onclick, 'showJobDetail')]")
            
#             for element in school_elements:
#                 # Dapatkan job ID dari onclick attribute
#                 onclick_text = element.get_attribute('onclick')
#                 job_id_match = re.search(r'showJobDetail\((\d+)\)', onclick_text)
                
#                 if job_id_match:
#                     job_id = job_id_match.group(1)
#                     job_ids.append(job_id)
            
#             print(f"Found {len(job_ids)} school job IDs")
#             return job_ids
            
#         except Exception as e:
#             print(f"Error getting school job IDs: {e}")
#             return []
    
#     def process_school_by_job_id(self, job_id):
#         """Process sekolah berdasarkan job ID"""
#         try:
#             print(f"Processing school with job ID: {job_id}")
            
#             # Step 1: Trigger showJobDetail dengan JavaScript
#             self.driver.execute_script(f"showJobDetail({job_id});")
#             time.sleep(3)  # Tunggu modal load
            
#             # Step 2: Cari dan klik company profile link
#             company_link = self.wait_for_element(By.ID, "companyName")
#             if not company_link:
#                 print("Company link not found, skipping...")
#                 self.close_job_modal()
#                 return None
                
#             company_href = company_link.get_attribute('href')
            
#             if company_href:
#                 print(f"Found company link: {company_href}")
                
#                 # Step 3: Buka tab baru untuk company profile
#                 original_window = self.driver.current_window_handle
#                 self.driver.execute_script("window.open(arguments[0]);", company_href)
#                 time.sleep(3)
                
#                 # Switch ke tab baru
#                 all_windows = self.driver.window_handles
#                 self.driver.switch_to.window(all_windows[-1])
#                 time.sleep(3)
                
#                 # Step 4: Extract data dari profile company (dengan timeout)
#                 school_info = self.extract_school_profile_data()
                
#                 # Step 5: Tutup tab company profile dan kembali ke window utama
#                 self.driver.close()
#                 self.driver.switch_to.window(original_window)
#                 time.sleep(1)
                
#                 # Step 6: Tutup modal job detail
#                 self.close_job_modal()
                
#                 return school_info
#             else:
#                 print("Company href not found")
#                 self.close_job_modal()
#                 return None
                
#         except Exception as e:
#             print(f"Error processing school {job_id}: {e}")
#             # Try to close modal jika ada
#             try:
#                 self.close_job_modal()
#             except:
#                 pass
#             return None
    
#     def close_job_modal(self):
#         """Tutup modal job detail"""
#         try:
#             # Coba berbagai cara untuk tutup modal
#             close_selectors = [
#                 "//button[contains(@class, 'btn-close')]",
#                 "//button[@aria-label='Close']",
#                 "//div[contains(@class, 'modal')]//button[contains(text(), 'Close')]",
#                 "//button[contains(@data-dismiss, 'modal')]"
#             ]
            
#             for selector in close_selectors:
#                 try:
#                     close_btn = self.driver.find_element(By.XPATH, selector)
#                     if close_btn.is_displayed():
#                         self.driver.execute_script("arguments[0].click();", close_btn)
#                         print("Closed job modal")
#                         time.sleep(1)
#                         return True
#                 except:
#                     continue
            
#             # Fallback: click outside modal atau ESC key
#             try:
#                 self.driver.execute_script("document.activeElement.blur();")
#                 self.driver.find_element(By.TAG_NAME, 'body').send_keys('\uE00C')  # ESC key
#                 print("Pressed ESC to close modal")
#                 time.sleep(1)
#             except:
#                 pass
                
#         except Exception as e:
#             print(f"Error closing modal: {e}")
    
#     def extract_school_profile_data(self):
#         """Extract data sekolah dari halaman profile"""
#         school_info = {
#             'school_name': '',
#             'address': '',
#             'phone': '',
#             'email': '',
#             'source_url': self.driver.current_url
#         }
        
#         print("Extracting school profile data...")
        
#         # Step 1: Ambil nama sekolah dari <h4> dengan timeout
#         try:
#             school_name_element = self.wait_for_element(By.XPATH, "//div[@class='card-body']//h4", 5)
#             if school_name_element:
#                 school_info['school_name'] = school_name_element.text.strip()
#                 print(f"School name: {school_info['school_name']}")
#             else:
#                 # Fallback: ambil dari title
#                 school_info['school_name'] = self.driver.title.replace(' | TheWorknPlay', '').strip()
#                 print(f"School name from title: {school_info['school_name']}")
#         except:
#             print("Could not get school name")
#             # Continue anyway, jangan berhenti
        
#         # Step 2: Ambil alamat yang tepat
#         try:
#             # Cari alamat dari element yang tepat (sebelum "View in Google Maps")
#             address_element = self.wait_for_element(By.XPATH, "//h5[contains(text(), 'Location')]/following-sibling::div//p[@class='mb-2']", 3)
            
#             if address_element:
#                 address_text = address_element.text.strip()
#                 # Filter hanya alamat yang meaningful (bukan link atau teks panjang)
#                 if (address_text and 
#                     len(address_text) < 200 and 
#                     not address_text.startswith('http') and
#                     any(keyword in address_text for keyword in ['Seoul', 'Korea', '-gu', '-dong', '-ro', 'Street', 'St', 'Ave', 'Building', 'Bldg', '#'])):
#                     school_info['address'] = address_text
#                     print(f"Address found: {school_info['address']}")
#                 else:
#                     print("Address text not meaningful, skipping...")
#             else:
#                 print("Address element not found")
                
#         except Exception as e:
#             print(f"Error extracting address: {e}")
        
#         # Jika tidak ada alamat yang ditemukan, coba method fallback
#         if not school_info['address']:
#             try:
#                 # Fallback: cari di sekitar Google Maps link
#                 maps_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'maps.google.com') or contains(@href, 'google.co.kr/maps')]")
#                 for maps_link in maps_links:
#                     try:
#                         # Cari sibling atau parent element yang mungkin mengandung alamat
#                         parent_div = maps_link.find_element(By.XPATH, "./ancestor::div[1]")
#                         paragraphs = parent_div.find_elements(By.TAG_NAME, "p")
#                         for p in paragraphs:
#                             text = p.text.strip()
#                             if (text and len(text) < 150 and 
#                                 any(keyword in text for keyword in ['Seoul', 'Korea', '-gu', '-dong', '-ro']) and
#                                 'View in Google Maps' not in text):
#                                 school_info['address'] = text
#                                 print(f"Address found near maps link: {school_info['address']}")
#                                 break
#                         if school_info['address']:
#                             break
#                     except:
#                         continue
#             except:
#                 print("Fallback address extraction failed")
        
#         # Phone dan email tetap kosong sesuai permintaan
        
#         # Cek jika ada data yang berhasil di-extract
#         if school_info['school_name'] or school_info['address']:
#             print(f"✓ Extracted: {school_info['school_name']}")
#             return school_info
#         else:
#             print("✗ No data extracted")
#             return None
    
#     def scrape_all_schools(self, max_schools=20):
#         """Main function untuk scraping semua sekolah"""
#         try:
#             self.setup_driver()
            
#             print("=== WORKNPLAY SCHOOL SCRAPER ===")
#             print("Step 1: Loading main page...")
            
#             # Step 1: Buka halaman utama
#             self.driver.get(f"{self.base_url}/Work/Search/Job")
#             time.sleep(5)
            
#             # Step 2: Scroll sampai semua sekolah ter-load
#             print("Step 2: Scrolling to load all schools...")
#             total_schools = self.scroll_to_load_all_schools()
            
#             # Step 3: Dapatkan semua job IDs
#             print("Step 3: Collecting school job IDs...")
#             job_ids = self.get_all_school_job_ids()
            
#             if not job_ids:
#                 print("No school job IDs found!")
#                 return
            
#             print(f"Step 4: Starting to scrape {min(len(job_ids), max_schools)} schools...")
            
#             # Step 4: Process each school by job ID
#             successful = 0
#             total_to_process = min(len(job_ids), max_schools)
            
#             for i, job_id in enumerate(job_ids[:max_schools]):
#                 print(f"\n[{i+1}/{total_to_process}] ", end="")
                
#                 # Extract school data dengan timeout
#                 start_time = time.time()
#                 school_info = self.process_school_by_job_id(job_id)
#                 processing_time = time.time() - start_time
                
#                 if school_info:
#                     self.school_data.append(school_info)
#                     successful += 1
#                     print(f"✅ Success ({processing_time:.1f}s)")
#                 else:
#                     print(f"❌ Failed ({processing_time:.1f}s)")
                
#                 # Progress tracking
#                 if (i + 1) % 5 == 0:
#                     print(f"\n📊 Progress: {i+1}/{total_to_process} - Successful: {successful}")
                
#                 # Random delay
#                 time.sleep(random.uniform(2, 4))
            
#             # Step 5: Save results
#             if self.school_data:
#                 self.save_results()
            
#             print(f"\n🎉 SCRAPING COMPLETED!")
#             print(f"Total processed: {total_to_process}")
#             print(f"Successfully scraped: {successful}")
            
#         except Exception as e:
#             print(f"Error during scraping: {e}")
#         finally:
#             if self.driver:
#                 self.driver.quit()
#                 print("Browser closed.")
    
#     def save_results(self):
#         """Save data to CSV"""
#         df = pd.DataFrame(self.school_data)
        
#         # Remove duplicates based on school name and URL
#         df = df.drop_duplicates(subset=['school_name', 'source_url'], keep='first')
        
#         filename = f"worknplay_schools_{len(df)}_records.csv"
#         df.to_csv(filename, index=False, encoding='utf-8-sig')
        
#         print(f"\n💾 Saved {len(df)} schools to {filename}")
        
#         # Show summary
#         print(f"\n📈 SUMMARY:")
#         print(f"Total schools: {len(df)}")
#         print(f"With name: {df['school_name'].notna().sum()}")
#         print(f"With address: {df['address'].notna().sum()}")
        
#         # Show sample
#         print(f"\n🎯 SAMPLE DATA (first 5):")
#         for i, row in df.head().iterrows():
#             print(f"{i+1}. {row['school_name']}")
#             print(f"   📍 {row['address']}" if row['address'] else "   📍 No address")
#             print()

# # Run the scraper
# if __name__ == "__main__":
#     scraper = WorkNPlaySchoolScraper()
    
#     # Start with 15 schools for testing
#     scraper.scrape_all_schools(max_schools=15)



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re
import random

class WorkNPlaySchoolScraper:
    def __init__(self):
        self.base_url = "https://www.theworknplay.com"
        self.driver = None
        self.school_data = []
        
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        print("Setting up Chrome WebDriver...")
        
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        
    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to be present"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except:
            return None
    
    def aggressive_scroll_to_load_all_schools(self):
        """Scroll yang lebih agresif untuk memuat SEMUA sekolah"""
        print("🚀 Starting AGGRESSIVE scroll to load ALL 1787 schools...")
        
        all_school_ids = set()
        last_count = 0
        no_progress_count = 0
        max_no_progress = 10
        scroll_attempt = 0
        max_scroll_attempts = 100
        
        while scroll_attempt < max_scroll_attempts and no_progress_count < max_no_progress:
            scroll_attempt += 1
            
            # MULTIPLE SCROLL METHODS
            print(f"\n--- Scroll Attempt {scroll_attempt} ---")
            
            # Method 1: Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            # Method 2: Incremental scroll dengan variasi
            scroll_increments = [300, 500, 800, 1000, 1500]
            for increment in scroll_increments:
                self.driver.execute_script(f"window.scrollBy(0, {increment});")
                time.sleep(1)
            
            # Method 3: Use Page Down key multiple times
            body = self.driver.find_element(By.TAG_NAME, 'body')
            for _ in range(5):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)
            
            # Method 4: Scroll to specific job elements
            try:
                job_elements = self.driver.find_elements(By.XPATH, "//article[contains(@class, 'media')]")
                if job_elements:
                    # Scroll to last job element
                    self.driver.execute_script("arguments[0].scrollIntoView();", job_elements[-1])
                    time.sleep(2)
            except:
                pass
            
            # Method 5: Try to trigger lazy loading dengan scroll random
            current_height = self.driver.execute_script("return document.body.scrollHeight")
            random_scroll = random.randint(500, 1500)
            self.driver.execute_script(f"window.scrollBy(0, {random_scroll});")
            time.sleep(2)
            
            # Collect ALL school IDs after scroll
            current_school_ids = self.get_all_school_job_ids()
            current_count = len(current_school_ids)
            
            # Add to our collection
            previous_count = len(all_school_ids)
            all_school_ids.update(current_school_ids)
            new_count = len(all_school_ids)
            
            print(f"📊 Current page: {current_count} schools")
            print(f"📈 Total collected: {new_count} unique schools")
            
            # Progress check
            if new_count == previous_count:
                no_progress_count += 1
                print(f"⚠️ No new schools ({no_progress_count}/{max_no_progress})")
                
                # Try alternative methods jika stuck
                if no_progress_count >= 3:
                    print("🔄 Trying alternative loading methods...")
                    self.try_alternative_loading_methods()
            else:
                no_progress_count = 0
                new_schools = new_count - previous_count
                print(f"✅ Added {new_schools} new schools!")
            
            # Target check
            if new_count >= 1700:
                print(f"🎯 TARGET REACHED! Found {new_count} schools")
                break
            
            # Jika sudah banyak attempts tapi progress sedikit, coba method extreme
            if scroll_attempt > 30 and new_count < 100:
                print("🚨 Low progress detected, trying extreme methods...")
                self.try_extreme_loading_methods()
            
            # Jika sudah banyak attempts, coba reload
            if scroll_attempt > 50 and new_count < 500:
                print("🔄 Many attempts with low results, trying page reload...")
                self.driver.refresh()
                time.sleep(5)
                # Reset counter setelah reload
                no_progress_count = 0
        
        final_school_ids = list(all_school_ids)
        print(f"\n🎉 FINAL RESULT: {len(final_school_ids)} unique schools collected after {scroll_attempt} scroll attempts")
        return final_school_ids
    
    def try_alternative_loading_methods(self):
        """Coba method alternative untuk load lebih banyak sekolah"""
        print("Trying alternative loading methods...")
        
        # Method 1: Click possible "Load More" buttons
        load_more_selectors = [
            "//button[contains(text(), 'Load')]",
            "//button[contains(text(), 'More')]",
            "//a[contains(text(), 'Load')]",
            "//a[contains(text(), 'More')]",
            "//button[contains(@class, 'load')]",
            "//div[contains(@class, 'load-more')]//button"
        ]
        
        for selector in load_more_selectors:
            try:
                buttons = self.driver.find_elements(By.XPATH, selector)
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        self.driver.execute_script("arguments[0].click();", button)
                        print(f"✅ Clicked: {button.text}")
                        time.sleep(4)
                        return True
            except:
                continue
        
        # Method 2: Try filter buttons untuk trigger reload
        try:
            filter_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'btn')] | //a[contains(@class, 'btn')]")
            for btn in filter_buttons[:5]:
                if btn.is_displayed() and btn.is_enabled():
                    btn_text = btn.text.strip()
                    if btn_text and len(btn_text) < 20:
                        self.driver.execute_script("arguments[0].click();", btn)
                        print(f"✅ Clicked filter: {btn_text}")
                        time.sleep(3)
                        # Click again to reset
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(2)
                        break
        except:
            pass
        
        return False
    
    def try_extreme_loading_methods(self):
        """Method extreme untuk load content"""
        print("Trying EXTREME loading methods...")
        
        # Scroll dari top ke bottom sangat pelan
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        print(f"Total page height: {total_height}")
        
        # Scroll sangat pelan dari atas ke bawah
        for position in range(0, total_height, 100):
            self.driver.execute_script(f"window.scrollTo(0, {position});")
            time.sleep(0.2)
        
        # Scroll sangat pelan dari bawah ke atas
        for position in range(total_height, 0, -100):
            self.driver.execute_script(f"window.scrollTo(0, {position});")
            time.sleep(0.1)
        
        time.sleep(3)
    
    def get_all_school_job_ids(self):
        """Dapatkan semua job ID sekolah dari halaman utama"""
        job_ids = []
        
        try:
            # Cari semua element sekolah di halaman utama
            school_elements = self.driver.find_elements(By.XPATH, "//article[contains(@class, 'media')]//h5/a[contains(@onclick, 'showJobDetail')]")
            
            for element in school_elements:
                # Dapatkan job ID dari onclick attribute
                onclick_text = element.get_attribute('onclick')
                job_id_match = re.search(r'showJobDetail\((\d+)\)', onclick_text)
                
                if job_id_match:
                    job_id = job_id_match.group(1)
                    job_ids.append(job_id)
            
            return job_ids
            
        except Exception as e:
            print(f"Error getting school job IDs: {e}")
            return []
    
    def process_school_by_job_id(self, job_id):
        """Process sekolah berdasarkan job ID"""
        try:
            print(f"Processing school with job ID: {job_id}")
            
            # Step 1: Trigger showJobDetail dengan JavaScript
            self.driver.execute_script(f"showJobDetail({job_id});")
            time.sleep(3)  # Tunggu modal load
            
            # Step 2: Cari dan klik company profile link
            company_link = self.wait_for_element(By.ID, "companyName")
            if not company_link:
                print("Company link not found, skipping...")
                self.close_job_modal()
                return None
                
            company_href = company_link.get_attribute('href')
            
            if company_href:
                print(f"Found company link: {company_href}")
                
                # Step 3: Buka tab baru untuk company profile
                original_window = self.driver.current_window_handle
                self.driver.execute_script("window.open(arguments[0]);", company_href)
                time.sleep(3)
                
                # Switch ke tab baru
                all_windows = self.driver.window_handles
                self.driver.switch_to.window(all_windows[-1])
                time.sleep(3)
                
                # Step 4: Extract data dari profile company (dengan timeout)
                school_info = self.extract_school_profile_data()
                
                # Step 5: Tutup tab company profile dan kembali ke window utama
                self.driver.close()
                self.driver.switch_to.window(original_window)
                time.sleep(1)
                
                # Step 6: Tutup modal job detail
                self.close_job_modal()
                
                return school_info
            else:
                print("Company href not found")
                self.close_job_modal()
                return None
                
        except Exception as e:
            print(f"Error processing school {job_id}: {e}")
            # Try to close modal jika ada
            try:
                self.close_job_modal()
            except:
                pass
            return None
    
    def close_job_modal(self):
        """Tutup modal job detail"""
        try:
            # Coba berbagai cara untuk tutup modal
            close_selectors = [
                "//button[contains(@class, 'btn-close')]",
                "//button[@aria-label='Close']",
                "//div[contains(@class, 'modal')]//button[contains(text(), 'Close')]",
                "//button[contains(@data-dismiss, 'modal')]"
            ]
            
            for selector in close_selectors:
                try:
                    close_btn = self.driver.find_element(By.XPATH, selector)
                    if close_btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", close_btn)
                        print("Closed job modal")
                        time.sleep(1)
                        return True
                except:
                    continue
            
            # Fallback: click outside modal atau ESC key
            try:
                self.driver.execute_script("document.activeElement.blur();")
                self.driver.find_element(By.TAG_NAME, 'body').send_keys('\uE00C')  # ESC key
                print("Pressed ESC to close modal")
                time.sleep(1)
            except:
                pass
                
        except Exception as e:
            print(f"Error closing modal: {e}")
    
    def extract_school_profile_data(self):
        """Extract data sekolah dari halaman profile"""
        school_info = {
            'school_name': '',
            'address': '',
            'phone': '',
            'email': '',
            'source_url': self.driver.current_url
        }
        
        print("Extracting school profile data...")
        
        # Step 1: Ambil nama sekolah dari <h4> dengan timeout
        try:
            school_name_element = self.wait_for_element(By.XPATH, "//div[@class='card-body']//h4", 5)
            if school_name_element:
                school_info['school_name'] = school_name_element.text.strip()
                print(f"School name: {school_info['school_name']}")
            else:
                # Fallback: ambil dari title
                school_info['school_name'] = self.driver.title.replace(' | TheWorknPlay', '').strip()
                print(f"School name from title: {school_info['school_name']}")
        except:
            print("Could not get school name")
            # Continue anyway, jangan berhenti
        
        # Step 2: Ambil alamat yang tepat
        try:
            # Cari alamat dari element yang tepat (sebelum "View in Google Maps")
            address_element = self.wait_for_element(By.XPATH, "//h5[contains(text(), 'Location')]/following-sibling::div//p[@class='mb-2']", 3)
            
            if address_element:
                address_text = address_element.text.strip()
                # Filter hanya alamat yang meaningful (bukan link atau teks panjang)
                if (address_text and 
                    len(address_text) < 200 and 
                    not address_text.startswith('http') and
                    any(keyword in address_text for keyword in ['Seoul', 'Korea', '-gu', '-dong', '-ro', 'Street', 'St', 'Ave', 'Building', 'Bldg', '#'])):
                    school_info['address'] = address_text
                    print(f"Address found: {school_info['address']}")
                else:
                    print("Address text not meaningful, skipping...")
            else:
                print("Address element not found")
                
        except Exception as e:
            print(f"Error extracting address: {e}")
        
        # Jika tidak ada alamat yang ditemukan, coba method fallback
        if not school_info['address']:
            try:
                # Fallback: cari di sekitar Google Maps link
                maps_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'maps.google.com') or contains(@href, 'google.co.kr/maps')]")
                for maps_link in maps_links:
                    try:
                        # Cari sibling atau parent element yang mungkin mengandung alamat
                        parent_div = maps_link.find_element(By.XPATH, "./ancestor::div[1]")
                        paragraphs = parent_div.find_elements(By.TAG_NAME, "p")
                        for p in paragraphs:
                            text = p.text.strip()
                            if (text and len(text) < 150 and 
                                any(keyword in text for keyword in ['Seoul', 'Korea', '-gu', '-dong', '-ro']) and
                                'View in Google Maps' not in text):
                                school_info['address'] = text
                                print(f"Address found near maps link: {school_info['address']}")
                                break
                        if school_info['address']:
                            break
                    except:
                        continue
            except:
                print("Fallback address extraction failed")
        
        # Phone dan email kosong
        
        # Cek jika ada data yang berhasil di-extract
        if school_info['school_name'] or school_info['address']:
            print(f"✓ Extracted: {school_info['school_name']}")
            return school_info
        else:
            print("✗ No data extracted")
            return None
    
    def scrape_all_schools(self):
        """Main function untuk scraping SEMUA sekolah"""
        try:
            self.setup_driver()
            
            print("=== WORKNPLAY SCHOOL SCRAPER ===")
            print("🎯 TARGET: SCRAPING ALL 1787 SCHOOLS")
            print("Step 1: Loading main page...")
            
            # Step 1: Buka halaman utama
            self.driver.get(f"{self.base_url}/Work/Search/Job")
            time.sleep(6)
            
            # Step 2: AGGRESSIVE scroll sampai SEMUA sekolah ter-load
            print("Step 2: AGGRESSIVE scrolling to load ALL schools...")
            all_job_ids = self.aggressive_scroll_to_load_all_schools()
            
            if not all_job_ids:
                print("No school job IDs found!")
                return
            
            print(f"🚀 Step 3: Starting to scrape {len(all_job_ids)} schools...")
            
            # Step 3: Process ALL schools by job ID
            successful = 0
            total_to_process = len(all_job_ids)
            
            for i, job_id in enumerate(all_job_ids):
                print(f"\n[{i+1}/{total_to_process}] ", end="")
                
                # Extract school data dengan timeout
                start_time = time.time()
                school_info = self.process_school_by_job_id(job_id)
                processing_time = time.time() - start_time
                
                if school_info:
                    self.school_data.append(school_info)
                    successful += 1
                    print(f"✅ Success ({processing_time:.1f}s)")
                    
                    # Save progress every 20 schools
                    if successful % 20 == 0:
                        self.save_backup()
                else:
                    print(f"❌ Failed ({processing_time:.1f}s)")
                
                # Progress tracking
                if (i + 1) % 10 == 0:
                    print(f"\n📊 Progress: {i+1}/{total_to_process} - Successful: {successful}")
                    estimated_remaining = (total_to_process - (i + 1)) * (processing_time + 3) / 60
                    print(f"⏱️  Estimated time remaining: {estimated_remaining:.1f} minutes")
                
                # Random delay
                time.sleep(random.uniform(2, 3))
            
            # Step 4: Save final results
            if self.school_data:
                self.save_final_results()
            
            print(f"\n🎉 SCRAPING COMPLETED!")
            print(f"Total processed: {total_to_process}")
            print(f"Successfully scraped: {successful}")
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            # Save backup even if error
            if self.school_data:
                self.save_backup()
        finally:
            if self.driver:
                self.driver.quit()
                print("Browser closed.")
    
    def save_backup(self):
        """Save backup data"""
        if self.school_data:
            df = pd.DataFrame(self.school_data)
            backup_file = f"backup_schools_{len(df)}_records.csv"
            df.to_csv(backup_file, index=False, encoding='utf-8-sig')
            print(f"💾 Backup saved: {backup_file}")
    
    def save_final_results(self):
        """Save final data ke CSV"""
        df = pd.DataFrame(self.school_data)
        
        # Remove duplicates based on school name and URL
        df = df.drop_duplicates(subset=['school_name', 'source_url'], keep='first')
        
        filename = f"ALL_worknplay_schools_{len(df)}_records.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n💾 FINAL RESULTS: Saved {len(df)} schools to {filename}")
        
        # Show summary
        print(f"\n📈 FINAL SUMMARY:")
        print(f"Total unique schools: {len(df)}")
        print(f"With name: {df['school_name'].notna().sum()}")
        print(f"With address: {df['address'].notna().sum()}")
        
        # Show sample
        print(f"\n🎯 SAMPLE DATA (first 10):")
        for i, row in df.head(10).iterrows():
            print(f"{i+1}. {row['school_name']}")
            print(f"   📍 {row['address']}" if row['address'] else "   📍 No address")
            print()

# Run the scraper
if __name__ == "__main__":
    scraper = WorkNPlaySchoolScraper()
    
    # Scrape ALL schools
    scraper.scrape_all_schools()