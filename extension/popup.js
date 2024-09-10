document.getElementById('scrapeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const count = document.getElementById('count').value;
    const response = await fetch('http://your_server_ip:5000/scrape_tweepy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${username}&count=${count}`
    });
    const data = await response.json();
    document.getElementById('results').innerText = JSON.stringify(data, null, 2);
});
