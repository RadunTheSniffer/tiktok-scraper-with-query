from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

def scrape_tiktok(query: str, count: int):
    formatted_query = query.replace(" ", "%20")
    url = f"https://www.tiktok.com/search?q={formatted_query}"
    
    # Set up Selenium with Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service('C:\chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Update with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print(f"Opening URL: {url}")
    driver.get(url)
    
    # Wait for the content to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='search-item']"))
        )
    except Exception as e:
        driver.quit()
        raise ValueError(f"Failed to load the page: {e}")
    
    # Click on the first video to load more content
    try:
        first_video = driver.find_element(By.CSS_SELECTOR, "div[data-e2e='search-item']")
        ActionChains(driver).move_to_element(first_video).click().perform()
        time.sleep(2)  # Wait for the video to load
    except Exception as e:
        print(f"Error clicking on the first video: {e}")
    
    # Scroll until the count limit is reached
    posts = []
    while len(posts) < count:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        
        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Example: Scrape the first few video titles (adjust the selector as needed)
        videos = soup.select("div[data-e2e='search-item']")
        for video in videos:
            if len(posts) >= count:
                break
            try:
                username = video.select_one("a[data-e2e='user-card-username']").text
                date = video.select_one("span[data-e2e='video-date']").text
                caption = video.select_one("a[data-e2e='video-title']").text
                comments = [comment.text for comment in video.select("p[data-e2e='comment-level-1']")]
                posts.append({
                    'username': username,
                    'date': date,
                    'caption': caption,
                    'comments': comments
                })
            except Exception as e:
                print(f"Error scraping video: {e}")
    
    driver.quit()
    
    if not posts:
        raise ValueError("No posts found.")
    
    return posts







