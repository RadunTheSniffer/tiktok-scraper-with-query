from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_tiktok(query: str, count: int):
    # Set up Selenium options for Chromium
    chrome_options = Options()
    chrome_options.binary_location = '/usr/bin/chromium-browser'  # Change the path if on Windows or macOS
    chrome_options.add_argument("--start-maximized")
    
    # Disable headless mode to see the browser interactions (for debugging)
    # If you want headless mode, uncomment the following line:
    # chrome_options.add_argument("--headless")
    
    # Use WebDriver Manager to handle ChromeDriver installation
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Form the TikTok search URL
        formatted_query = query.replace(" ", "%20")
        url = f"https://www.tiktok.com/search?q={formatted_query}&type=video"
        
        # Go to the TikTok search page
        driver.get(url)
        time.sleep(5)  # Allow time for page to load
        
        # Scroll down to load more posts (if needed, depending on the number of posts you want)
        for _ in range(count // 5):  # Assuming each scroll loads 5 posts, adjust as needed
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Add a delay to let the content load
            
        # Extract post data (This is a simplified version, you will need to adjust this based on actual HTML structure)
        posts = driver.find_elements_by_css_selector("div[data-testid='search-post']")  # Adjust the selector

        scraped_data = []
        for post in posts[:count]:
            username = post.find_element_by_css_selector(".username").text
            caption = post.find_element_by_css_selector(".caption").text
            date = post.find_element_by_css_selector(".date").text
            
            # Collect data in a dictionary
            scraped_data.append({
                "username": username,
                "caption": caption,
                "date": date
            })
        
        return scraped_data
    
    except Exception as e:
        print(f"Error occurred while scraping: {e}")
        return []
    
    finally:
        # Ensure the browser is closed after scraping
        driver.quit()
        
