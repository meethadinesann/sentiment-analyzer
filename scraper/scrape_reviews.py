from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def create_driver():
    """
    Sets up and returns a Selenium Chrome driver.
    Automatically detects whether running locally or in Docker/Render.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Check if running in Docker/Render (Chrome installed at fixed path)
    chrome_bin = os.environ.get("CHROME_BIN")
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")

    if chrome_bin and chromedriver_path:
        # Running in Docker/Render
        print("Using system Chrome (Docker/Render environment)")
        options.binary_location = chrome_bin
        service = Service(chromedriver_path)
    else:
        # Running locally on Mac
        print("Using ChromeDriver Manager (local environment)")
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver

def search_product(driver, product_name):
    """
    Opens Flipkart and searches for the given product.
    """
    print(f"Opening Flipkart and searching for: {product_name}")
    driver.get("https://www.flipkart.com")
    time.sleep(2)

    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"✕")]'))
        )
        close_button.click()
        print("Login popup closed.")
    except:
        print("No login popup appeared.")

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    print("Search completed. Results page loaded.")


def get_product_links(driver):
    """
    Collects all product links from the search results page.
    Tries multiple class names to handle different Flipkart layouts.
    """
    print("Collecting product links from search results...")
    time.sleep(2)

    # Flipkart uses different class names for different product categories
    # We try each one until we find links
    possible_classes = ["pIpigb", "CGtC98", "s1Q9rs", "IRpwTa", "WKTcLC"]

    product_elements = []
    for class_name in possible_classes:
        elements = driver.find_elements(By.CLASS_NAME, class_name)
        if elements:
            print(f"Found products using class: {class_name}")
            product_elements = elements
            break

    # Fallback: find all <a> tags pointing to /p/ (product pages)
    if not product_elements:
        print("Class name approach failed. Trying link fallback...")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        links = []
        for a in all_links:
            try:
                href = a.get_attribute("href")
                if href and "/p/" in href and "flipkart.com" in href:
                    links.append(href)
            except:
                continue
        # Remove duplicates
        links = list(dict.fromkeys(links))
        print(f"Found {len(links)} products via fallback.")
        return links

    links = []
    for element in product_elements:
        try:
            url = element.get_attribute("href")
            if url:
                links.append(url)
        except:
            continue

    print(f"Found {len(links)} products.")
    return links


def open_reviews_page(driver, product_url):
    """
    Opens the reviews page directly using the correct Flipkart URL format.
    """
    print("Constructing reviews page URL...")

    try:
        # Split URL at /p/ to get slug and the rest
        parts = product_url.split("/p/")
        slug = parts[0]

        # From the second part, get item_id and pid
        second_part = parts[1]
        item_id = second_part.split("?")[0]
        pid = second_part.split("pid=")[1].split("&")[0]

        # Construct the correct reviews URL
        reviews_url = f"{slug}/product-reviews/{item_id}?pid={pid}"
        print(f"Reviews URL: {reviews_url}")

        driver.get(reviews_url)
        time.sleep(3)
        print("Opened reviews page successfully.")

    except Exception as e:
        print(f"Error constructing reviews URL: {e}")


def scrape_reviews(driver, max_scrolls=5, max_reviews=10):
    """
    Scrapes reviews using infinite scroll.
    Stops when max_reviews is reached or no new reviews load.
    """
    all_reviews = []
    last_count = 0
    no_change_count = 0

    for scroll in range(max_scrolls):
        print(f"Scroll {scroll + 1} of {max_scrolls}...")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        review_cards = driver.find_elements(By.CLASS_NAME, "asbjxx")
        current_count = len(review_cards)
        print(f"Review cards visible: {current_count}")

        # Stop scrolling if we already have enough cards
        if current_count >= max_reviews:
            print(f"Reached {max_reviews} reviews limit. Stopping scroll.")
            break

        if current_count == last_count:
            no_change_count += 1
            if no_change_count >= 3:
                print("No new reviews loading. Stopping scroll.")
                break
        else:
            no_change_count = 0

        last_count = current_count

    # Scrape only up to max_reviews cards
    review_cards = driver.find_elements(By.CLASS_NAME, "asbjxx")[:max_reviews]
    print(f"\nScraping {len(review_cards)} review cards...")

    for card in review_cards:
        try:
            # --- Rating ---
            try:
                rating_element = card.find_element(
                    By.XPATH,
                    './/div[contains(@style,"color: rgb(14, 119, 45)") or contains(@style,"color: rgb(255") or contains(@style,"color: rgb(0")]'
                )
                rating = rating_element.text.strip().split('\n')[0].strip()
            except:
                rating = "N/A"

            # --- Review Title ---
            try:
                title_element = card.find_element(
                    By.XPATH,
                    './/div[contains(@style,"margin-left: 8px")]'
                )
                title = title_element.text.strip()
            except:
                title = "N/A"

            # --- Review Body ---
            try:
                body_element = card.find_element(
                    By.CLASS_NAME, "css-1jxf684"
                )
                body = body_element.text.strip()
            except:
                body = "N/A"

            if body != "N/A" and body != "":
                all_reviews.append({
                    "rating": rating,
                    "title": title,
                    "body": body
                })

        except Exception as e:
            continue

    print(f"Successfully scraped {len(all_reviews)} reviews.")
    return all_reviews


def save_to_csv(reviews, filename="data/raw_reviews.csv"):
    """
    Saves the list of review dictionaries to a CSV file.
    """
    df = pd.DataFrame(reviews)
    df.to_csv(filename, index=False)
    print(f"Reviews saved to {filename}")


# --- Main execution ---
if __name__ == "__main__":
    driver = create_driver()
    all_reviews = []

    try:
        # Ask the user to type a product name in the terminal
        product_name = input("Enter product name to search: ").strip()

        if not product_name:
            print("No product name entered. Exiting.")
            driver.quit()
            exit()

        search_product(driver, product_name)
        links = get_product_links(driver)

        # Scrape first 10 products, 10 reviews each = ~100 total
        for i, link in enumerate(links[:10]):
            print(f"\n--- Scraping product {i+1} of 10 ---")
            open_reviews_page(driver, link)
            reviews = scrape_reviews(driver, max_scrolls=5, max_reviews=10)
            all_reviews.extend(reviews)
            print(f"Total reviews so far: {len(all_reviews)}")
            time.sleep(2)

        if all_reviews:
            save_to_csv(all_reviews)
        else:
            print("No reviews were scraped.")

        input("Press Enter to close the browser...")
    finally:
        driver.quit()