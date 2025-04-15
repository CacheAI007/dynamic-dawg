import time
import random
import sys
import itertools
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

from threading import Thread

# ====== CONFIGURATION ======
USE_PROXY = False  # Set to True if using proxies
PROXY = "your_proxy:port"  # Replace with your proxy if needed

# Initialize Chrome Options
options = Options()
options.add_argument("--headless")  # Uncomment to run in headless mode (stealthier)
options.add_argument("--disable-blink-features=AutomationControlled")  # Hide Selenium detection
options.add_argument("--incognito")  # Use Incognito Mode
options.add_argument("--disable-gpu")  # Improve stability
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Prevent crashes

# Set a random User-Agent
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")

# Enable Proxy (if needed)
if USE_PROXY:
    options.add_argument(f"--proxy-server={PROXY}")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def random_delay(min_delay=1, max_delay=3):
    """Helper function to add a random delay between actions"""
    time.sleep(random.uniform(min_delay, max_delay))

def animated_banner(stop_event):
    """Displays a rotating banner to indicate scraping is in progress"""
    for char in itertools.cycle(["|", "/", "-", "\\"]):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\rScraping in progress... {char} ")
        sys.stdout.flush()
        time.sleep(0.2)

def scroll_and_load(driver, max_scrolls=10):
    """Scrolls down and clicks 'Load More' if present to reveal all listings"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0

    while scrolls < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_delay(2, 4)  # Human-like delay

        # Check if "Load More" button appears
        try:
            load_more_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Load More')]")
            if load_more_button.is_displayed():
                print("\nClicking 'Load More' button...")
                driver.execute_script("arguments[0].click();", load_more_button)
                random_delay(2, 5)  # Wait for new content
        except:
            pass  # No "Load More" button found

        # Wait for new content
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            print("\nNo more results found.")
            break  # Stop scrolling when no new content loads

        last_height = new_height
        scrolls += 1

def save_data_to_csv(data, filename="storage_units.csv"):
    """Helper function to save scraped data as a CSV file"""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Address", "Size", "Price"])  # Header row
        writer.writerows(data)
    print(f"\n✅ Data saved to {filename}")

try:
    # Start animated banner in a separate thread
    import threading
    stop_event = threading.Event()
    banner_thread = threading.Thread(target=animated_banner, args=(stop_event,))
    banner_thread.start()

    # Open website
    driver.get("https://www.selfstorage.com/")
    random_delay(2, 4)

    # Handle Cookie Banner (if exists)
    try:
        cookie_banner = driver.find_element(By.ID, "ensCloseBanner")
        cookie_banner.click()
        print("\n✅ Cookie banner closed.")
        random_delay(1, 3)
    except:
        print("\n⚠️ No cookie banner found or already closed.")

    # Locate search box and enter query
    search_box = driver.find_element(By.ID, "hero-search")
    search_box.clear()
    search_box.send_keys("Redwood City, CA")
    random_delay(1, 3)
    search_box.send_keys(Keys.RETURN)
    random_delay(5, 8)  # Allow results to load

    # Scroll and load all results
    scroll_and_load(driver)

    # Scrape storage unit details
    units = driver.find_elements(By.CLASS_NAME, "unit-container")
    print(f"\n🔍 Found {len(units)} storage units.")

    data = [["Name", "Address", "Size", "Price"]]  # Initialize 2D list with header row

    for idx, unit in enumerate(units, start=1):
        try:
            name_element = driver.find_elements(By.XPATH, "//div[@class='unit-container']//div[@class='facility-name']")
            size_element = unit.find_element(By.XPATH, ".//p[contains(@class, 'ss-type-weight-standard')]")
            price_element = unit.find_element(By.XPATH, ".//p[contains(@class, 'ss-type-blue')]")

            # Extract text or assign "N/A" if element not found
            name = name_element.text if name_element else "N/A"
            size = size_element.text if size_element else "N/A"
            price = price_element.text if price_element else "N/A"

            # Extract only price following the "$" sign using regex
            price_match = re.search(r"\$\d+(?:,\d+)?(?:\.\d{1,2})?", price)  # Match prices like $50, $1,200, or $99.99
            price = price_match.group(0) if price_match else "N/A"

            data.append([name, "N/A", size, price])  # Store as a row in the 2D list

            # Display progress update
            sys.stdout.write(f"\r📦 Extracting unit {idx}/{len(units)}: {name[:30]}...  ")
            sys.stdout.flush()

            # Random delay between actions to avoid bot detection
            random_delay(2, 5)
        except Exception as e:
            print(f"\n⚠️ Error extracting data: {e}")
            continue

    # Stop animated banner
    stop_event.set()
    banner_thread.join()

    # Print results to console
    #print("\n\n📊 Scraped Data:")
   # for row in data[1:]:  # Skip header for display
       # print(f"📦 Name: {row[0]}")
       # print(f"📍 Address: {row[1]}")
       # print(f"📏 Size: {row[2]}")
        # print(f"💲 Price: {row[3]}")
       # print("-" * 50)

    # Save raw results to a CSV file
    save_data_to_csv(data[1:])  # Exclude header from CSV writing

except Exception as e:
    print(f"\n❌ Error occurred: {e}")

finally:
    driver.quit()
    print("\n🛑 Browser closed.")
