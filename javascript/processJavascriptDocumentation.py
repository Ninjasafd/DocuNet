from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import spacy

# Initialize the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the JavaScript-heavy page to scrape
url = "https://262.ecma-international.org/14.0/?_gl=1*1dg5ih4*_ga*MTU0OTI3OTc4MC4xNzAwMDE5MjIx*_ga_TDCK4DWEPP*MTcwMDAxOTIyMC4xLjAuMTcwMDAxOTIyNS4wLjAuMA..&_ga=2.216617808.717254865.1700019221-1549279780.1700019221#sec-jobs"
# Go to the webpage
driver.get(url)

# Wait for the dynamic content to load
driver.implicitly_wait(10)  # Adjust the time as necessary

# Now that the page is fully loaded, get the page source
html_content = driver.page_source

# Close the driver
driver.quit()

# Use Beautiful Soup to parse the fetched HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Process the content with Beautiful Soup or other tools as needed...
