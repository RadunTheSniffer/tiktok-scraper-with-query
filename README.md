Sure! Here’s an updated `README.md` file that reflects the changes and additions for using FastAPI, Selenium, and the new structure for the server setup and configuration.

### Updated `README.md`

```markdown
# TikTok Scraper

A web scraper for TikTok that uses Selenium and FastAPI. This app provides an endpoint to scrape TikTok posts based on a search query. It can be integrated with browser extensions for ease of use.

## Main Idea

The application is built using FastAPI to handle HTTP requests and Selenium to perform web scraping. The FastAPI server serves as the backend for the scraping process, and it can be contacted directly or via a browser extension.

## Modules

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python.
- **Selenium**: A tool for automating web browsers to scrape dynamic content.
- **ChromeDriver**: A WebDriver implementation for Chrome, required for Selenium.

## Server Setup

### Setting Up FastAPI Server

1. **Create a DigitalOcean Droplet**

   Follow these steps to set up a DigitalOcean Droplet:
   - Sign up at [DigitalOcean](https://www.digitalocean.com/).
   - Create a new Droplet with an Ubuntu image.
   - Choose a plan and data center region.
   - Add your SSH key for secure access.

2. **Connect to Your Droplet**

   Use SSH to connect to your Droplet:
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Set Up the Server Environment**

   Update packages and install dependencies:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3-pip python3-venv -y
   ```

   Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   Install FastAPI, Selenium, and other required packages:
   ```bash
   pip install fastapi uvicorn selenium
   ```

4. **Download and Set Up ChromeDriver**

   - Download ChromeDriver from [Chromedriver download page](https://sites.google.com/chromium.org/driver/).
   - Extract the downloaded file and place it in a directory (e.g., `/usr/local/bin`).
   - Update the path in `scraper.py` to match the location of `chromedriver`.

5. **Run the FastAPI Server**

   Create and run your FastAPI server with `uvicorn`:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 5000
   ```

6. **Handle Multiple Clients with Gunicorn and Nginx**

   - Install Gunicorn:
     ```bash
     pip install gunicorn
     ```

   - Run the FastAPI app with Gunicorn:
     ```bash
     gunicorn -w 4 -b 0.0.0.0:5000 app:app
     ```

   - Install and configure Nginx:
     ```bash
     sudo apt install nginx
     ```

     Create an Nginx configuration file:
     ```bash
     sudo nano /etc/nginx/sites-available/tiktok-scraper
     ```

     Add the following configuration:
     ```nginx
     server {
         listen 80;
         server_name your_server_ip;

         location / {
             proxy_pass http://127.0.0.1:5000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header X-Forwarded-Proto $scheme;
         }
     }
     ```

     Enable the Nginx configuration:
     ```bash
     sudo ln -s /etc/nginx/sites-available/tiktok-scraper /etc/nginx/sites-enabled
     sudo systemctl restart nginx
     ```

## Scraper Implementation

### `scraper.py`

Handles the web scraping using Selenium and ChromeDriver.

- **Function:** `scrape_tiktok(query: str, count: int) -> List[Dict[str, str]]`
- **Parameters:**
  - `query`: The search query for TikTok.
  - `count`: The number of posts to scrape.
- **Returns:** A list of dictionaries with post details (username, date, content).

### Example Usage

To test scraping directly from the command line or another script:
```python
from scraper import scrape_tiktok

results = scrape_tiktok("funny", 5)
print(results)
```

## Extension Setup

If integrating with a browser extension, update the `popup.js` script to send requests to your FastAPI server. Ensure that the `popup.html`, `popup.js`, and `manifest.json` files are correctly configured to handle user input and display results.

## Troubleshooting

- **`driver` is `None`:** Ensure that ChromeDriver is correctly installed and the path is updated in `scraper.py`.
- **Selenium Errors:** Check for updates to Selenium and ChromeDriver, and ensure compatibility with your browser version.

For additional assistance, refer to the [Selenium documentation](https://www.selenium.dev/documentation/en/) and [FastAPI documentation](https://fastapi.tiangolo.com/).

```

This updated `README.md` includes instructions for setting up FastAPI, using Selenium with ChromeDriver, and configuring Gunicorn and Nginx for handling multiple clients. It also provides a brief overview of how to test the scraper and integrate with a browser extension.
