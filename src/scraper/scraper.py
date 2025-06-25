from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import re
from src.utils.browser import init_browser, handle_cookie_consent
from src.constants.config import (
    MAIN_URL, LOGIN_URL, OUTPUT_CSV, OUTPUT_DIR,
    TEST_MODE, TEST_LIMIT, USERNAME, PASSWORD
)

class WebScraper:
    def __init__(self):
        self.browser = init_browser()
        self.profile_count = 0
        self.data = []



    def login(self):
        """Handle login if credentials are provided."""
        if not LOGIN_URL or not USERNAME or not PASSWORD:
            return
        
        self.browser.get(LOGIN_URL)
        # Add login logic here based on the specific website
        # This is a placeholder that needs to be customized
        pass

    def normalize_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text.strip())

    def extract_company_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract company data including titles, images, country, and description from the page."""
        # Extract titles
        titles = soup.select('div.exhibitors-catalog__body-row-name-text')
        
        # Extract images
        images = soup.select('img.exhibitors-catalog__body-row-image--size')
        
        # Extract descriptions (sector information)
        descriptions = soup.select('span.exhibitors-catalog__body-row-sector-text')
        
        # For countries, we need a more specific selector
        # Looking for spans that contain only country names (typically shorter text)
        all_spans = soup.select('span[data-v-ba95349e]')
        countries = []
        for span in all_spans:
            text = self.normalize_text(span.text)
            # Country names are typically short and don't contain commas or "..."
            if text and len(text) < 30 and "..." not in text and "," not in text:
                # Check if it's a known country name
                if any(country_name in text.lower() for country_name in ["españa", "spain", "italia", "italy", "france", "francia", "germany", "alemania", "portugal"]):
                    countries.append(span)
        
        # Create a list to store company data
        company_data = []
        
        # Determine the maximum number of companies we can extract data for
        max_companies = max(len(titles), len(images), len(descriptions))
        
        for i in range(min(max_companies, TEST_LIMIT if TEST_MODE else max_companies)):
            title_text = self.normalize_text(titles[i].text) if i < len(titles) else ""
            image_src = images[i]['src'] if i < len(images) else ""
            description_text = self.normalize_text(descriptions[i].text) if i < len(descriptions) else ""
            country_text = self.normalize_text(countries[i].text) if i < len(countries) else ""
            
            # Add the data to our list with ID as the first column
            company_data.append({
                'ID': i + 1,  # Start IDs from 1
                'Title': title_text,
                'Description': description_text,
                'Image': image_src,
                'Country': country_text
                
            })
        
        return company_data

    def handle_pagination(self) -> List[Dict]:
        """Navigate through paginated results and collect company data."""
        all_company_data = []
        current_page = 1
        
        while True:
            self.browser.get(f"{MAIN_URL}?page={current_page}")
            handle_cookie_consent(self.browser)
            
            soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            page_company_data = self.extract_company_data(soup)
            all_company_data.extend(page_company_data)
            
            # Break if no more data or reached test limit
            if not page_company_data or (TEST_MODE and len(all_company_data) >= TEST_LIMIT):
                break
                
            current_page += 1
            
        return all_company_data

    def run(self):
        """Main execution method."""
        try:
            self.login()
            company_data = self.handle_pagination()
            
            for entry in company_data:
                if TEST_MODE and self.profile_count >= TEST_LIMIT:
                    break
                
                self.data.append(entry)
                self.profile_count += 1
            
            self.save_to_csv()
            
        except Exception as e:
            print(f"An error occurred during scraping: {str(e)}")
        finally:
            self.browser.quit()

    def save_to_csv(self):
        """Save scraped data to CSV file."""
        df = pd.DataFrame(self.data)
        df.to_csv(f"{OUTPUT_DIR}/{OUTPUT_CSV}", index=False) 