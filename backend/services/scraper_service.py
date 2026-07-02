import sys
import os

# Add the scraper folder to Python's path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../scraper"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../scraper"))

from scrape_reviews import (
    create_driver,
    search_product,
    get_product_links,
    open_reviews_page,
    scrape_reviews
)


def run_scraper(product_name, max_products=5, max_reviews=10):
    """
    Runs the Selenium scraper for a given product name.
    Returns a list of raw review dictionaries.
    """
    driver = create_driver()
    all_reviews = []

    try:
        search_product(driver, product_name)
        links = get_product_links(driver)

        if not links:
            print("No product links found.")
            return []

        for i, link in enumerate(links[:max_products]):
            print(f"Scraping product {i+1} of {max_products}...")
            open_reviews_page(driver, link)
            reviews = scrape_reviews(driver, max_scrolls=5, max_reviews=max_reviews)
            all_reviews.extend(reviews)

    except Exception as e:
        print(f"Scraper error: {e}")

    finally:
        driver.quit()

    print(f"Scraper finished. Total reviews: {len(all_reviews)}")
    return all_reviews