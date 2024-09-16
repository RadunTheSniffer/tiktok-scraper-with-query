from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def scrape_tiktok(query: str, count: int):
    driver = None  # Initialize driver variable
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Path to your ChromeDriver
        service = Service('/path/to/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get('https://www.tiktok.com')
        time.sleep(5)  # Wait for the page to load
        
        # Search for posts
        search_box = driver.find_element(By.XPATH, '//input[@placeholder="Search"]')
        search_box.send_keys(query)
        search_box.submit()
        time.sleep(5)  # Wait for search results to load
        
        # Collect data
        posts = []
        elements = driver.find_elements(By.XPATH, '//div[@class="tiktok-post"]')  # Adjust as needed
        
        for element in elements[:count]:
            try:
                username = element.find_element(By.XPATH, './/a[@class="username"]').text
                date = element.find_element(By.XPATH, './/time').text
                content = element.find_element(By.XPATH, './/p[@class="content"]').text
                posts.append({
                    'username': username,
                    'date': date,
                    'content': content
                })
            except NoSuchElementException as e:
                print(f"Element not found: {e}")
        
        if not posts:
            raise ValueError("No posts found.")
        
        return posts
    
    except TimeoutException as e:
        raise RuntimeError("The page took too long to load.")
    
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while scraping: {str(e)}")
    
    finally:
        driver.quit()

