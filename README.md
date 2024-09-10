# twitter-scraper
A twitter data scraper through chrome browser extension. The usage of browser extension is for easy execution without wasting time and resources to create a specified
environment forthe program. This app can be edited to scrape other social media platform through snscrape alone though certain extra modules may be needed to bypass CAPTCHA like Selenium

# Main Idea
Main program will be a flask app that will handle multiple clients through browser extension with gunicorn and nginx

# Modules
Modules used is tweepy and snscrape

# Server
Set Up a DigitalOcean Droplet

1. **Create a DigitalOcean Account**: Sign up at [DigitalOcean](https://www.digitalocean.com/).

2. **Create a New Droplet**:
   - Go to the DigitalOcean dashboard and click "Create" -> "Droplets".
   - Choose an Ubuntu image.
   - Select a plan (the basic plan is usually sufficient).
   - Choose a data center region.
   - Add your SSH key (generate one if you don't have it using `ssh-keygen`).

3. **Connect to Your Droplet**:
   - Get the IP address of your Droplet from the DigitalOcean dashboard.
   - Open a terminal on your local machine and connect using SSH:
     ```bash
     ssh root@your_droplet_ip

# Environment 
Set Up the Server Environment

1. **Update Packages**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Python and Pip**:
   ```bash
   sudo apt install python3-pip python3-venv -y
   ```

3. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Flask, Tweepy, and Snscrape**:
   ```bash
   pip install Flask tweepy snscrape




