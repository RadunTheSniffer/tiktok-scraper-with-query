from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from scraper import scrape_tiktok

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scrape")
async def scrape_tiktok_posts(request: Request, query: str = Form(...), count: int = Form(...)):
    try:
        # Validate input
        if not query or count <= 0:
            raise ValueError("Invalid input: query cannot be empty and count must be positive.")
        
        # Perform scraping
        scraped_data = scrape_tiktok(query, count)
        
        # Ensure data was retrieved
        if not scraped_data:
            raise ValueError("No data retrieved.")
        
        # Render results page with scraped data
        return templates.TemplateResponse("results.html", {"request": request, "tweets": scraped_data})
    
    except ValueError as e:
        # Handle known exceptions and provide user-friendly messages
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>", status_code=400)
    
    except Exception as e:
        # Handle unexpected errors
        return HTMLResponse(content=f"<h1>An unexpected error occurred: {str(e)}</h1>", status_code=500)

