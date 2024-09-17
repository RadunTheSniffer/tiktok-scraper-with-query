
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from scraper import scrape_tiktok
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scrape")
async def scrape_tiktok_posts(request: Request, query: str = Form(...), count: int = Form(...)):
    try:
        print(f"Received query: {query}, count: {count}")
        if not query or count <= 0:
            raise ValueError("Invalid input: query cannot be empty and count must be positive.")
        
        scraped_data = scrape_tiktok(query, count)
        
        if not scraped_data:
            raise ValueError("No data retrieved.")
        
        return JSONResponse(content=scraped_data)
    
    except ValueError as e:
        print(f"ValueError: {e}")
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>", status_code=400)
    
    except Exception as e:
        print(f"Exception: {e}")
        return HTMLResponse(content=f"<h1>An unexpected error occurred: {str(e)}</h1>", status_code=500)

@app.post("/dump")
async def dump_tiktok_posts(request: Request, query: str = Form(...), count: int = Form(...)):
    try:
        print(f"Received query: {query}, count: {count}")
        if not query or count <= 0:
            raise ValueError("Invalid input: query cannot be empty and count must be positive.")
        
        scraped_data = scrape_tiktok(query, count)
        
        if not scraped_data:
            raise ValueError("No data retrieved.")
        
        # Serialize the data to JSON
        json_data = json.dumps(scraped_data, ensure_ascii=False, indent=4)
        return JSONResponse(content=json.loads(json_data))
    
    except ValueError as e:
        print(f"ValueError: {e}")
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>", status_code=400)
    
    except Exception as e:
        print(f"Exception: {e}")
        return HTMLResponse(content=f"<h1>An unexpected error occurred: {str(e)}</h1>", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, 
                host="0.0.0.0", 
                reload=False,
                port=8000)












