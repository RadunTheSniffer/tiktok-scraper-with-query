import asyncio
import platform
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scrape")
async def scrape_tiktok_posts(request: Request, query: str = Form(...), count: int = Form(...)):
    try:
        print(f"Received query: {query}, count: {count}")
        # Validate input
        if not query or count <= 0:
            raise ValueError("Invalid input: query cannot be empty and count must be positive.")
        
        # Perform scraping
        scraped_data = scrape_tiktok(query, count)
        
        # Ensure data was retrieved
        if not scraped_data:
            raise ValueError("No data retrieved.")
        
        # Render results page with scraped data
        return templates.TemplateResponse("results.html", {"request": request, "posts": scraped_data})
    
    except ValueError as e:
        print(f"ValueError: {e}")
        # Handle known exceptions and provide user-friendly messages
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>", status_code=400)
    
    except Exception as e:
        print(f"Exception: {e}")
        # Handle unexpected errors
        return HTMLResponse(content=f"<h1>An unexpected error occurred: {str(e)}</h1>", status_code=500)

def scrape_tiktok(query: str, count: int):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Hide the fact that we are using Selenium
    
    
    # Format the query to match the URL structure
    formatted_query = query.replace(" ", "%20")
    url = f"https://www.tiktok.com/search?q={formatted_query}"
    
    print(f"Opening URL: {url}")
    # Open TikTok and search for the query
    driver.get(url)
    
    # Example: Scrape the first few video titles (adjust the selector as needed)
    videos = driver.find_elements(By.CSS_SELECTOR, "div[data-e2e='search-item']")[:count]
    posts = []
    for video in videos:
        try:
            username = video.find_element(By.CSS_SELECTOR, "a[data-e2e='user-card-username']").text
            content = video.find_element(By.CSS_SELECTOR, "a[data-e2e='video-title']").text
            posts.append({
                'username': username,
                'content': content
            })
        except Exception as e:
            print(f"Error scraping video: {e}")
    
    driver.quit()
    
    if not posts:
        raise ValueError("No posts found.")
    
    return posts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


