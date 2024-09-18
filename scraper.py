import subprocess
import json

def scrape_tiktok(query: str, count: int):
    result = subprocess.run(['node', 'scraper.js', query, str(count)], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(result.stderr)
    
    scraped_data = json.loads(result.stdout)
    
    if not scraped_data:
        raise ValueError("No data retrieved.")
    
    return scraped_data











