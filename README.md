# Web Scraping Template

A reusable Python web scraping template using Selenium and BeautifulSoup.
It outputs the information structurized in CSV format.


## Features

- Firefox browser automation with Selenium
- Cookie consent handling
- Optional login functionality
- Pagination support
- Structured data extraction (titles, images, countries, descriptions)
- CSV export with customizable column order
- Test mode with limit
- Text normalization

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the scraper in `src/constants/config.py`:
- Set the target URLs
- Configure test mode and limits
- Add login credentials if needed
- Customize cookie consent selectors

3. Customize the scraper in `src/scraper/scraper.py`:
- Implement login logic if needed
- Customize data extraction selectors for:
  - Company titles (`div.exhibitors-catalog__body-row-name-text`)
  - Images (`img.exhibitors-catalog__body-row-image--size`)
  - Countries (filtered from `span[data-v-ba95349e]`)
  - Descriptions (`span.exhibitors-catalog__body-row-sector-text`)

## Usage

Run the scraper:
```bash
python main.py
```

The output will be saved in `src/outputs/output.csv`.

## Project Structure

```
template_scrapper/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── src/
    ├── constants/
    │   └── config.py
    ├── utils/
    │   └── browser.py
    ├── scraper/
    │   └── scraper.py
    └── outputs/
        └── output.csv
```