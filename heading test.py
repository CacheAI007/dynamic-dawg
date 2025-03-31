from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize Chrome Options
options = Options()
options.add_argument("--headless")  # Run in headless mode (optional)
options.add_argument("--disable-blink-features=AutomationControlled")  # Hide Selenium detection

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Open the target website
    driver.get("https://www.selfstorage.com/self-storage/california/redwood-city/")  # Replace with actual URL
    time.sleep(5)  # Allow time for the page to load

    # Handle Cookie Popup (if it exists)
    try:
        cookie_button = driver.find_element(By.ID, "ensCloseBanner")  # Update the ID if different
        cookie_button.click()
        print("✅ Cookie popup closed.")
        time.sleep(2)  # Wait a bit for actions to apply
    except:
        print("⚠️ No cookie popup found or already closed.")

    # Extract facility names
    facility_elements = driver.find_elements(By.XPATH, "//h3[contains(@class, 'facility-name')]")

    facility_names = [element.text.strip() for element in facility_elements if element.text.strip()]

    # Print extracted facility names
    print("\n📍 Extracted Facility Names:")
    for idx, name in enumerate(facility_names, start=1):
        print(f"{idx}. {name}")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    driver.quit()
    print("\n🛑 Browser closed.")
