const puppeteer = require('puppeteer');

async function scrapeTikTok(query, count) {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    const formattedQuery = query.replace(" ", "%20");
    const url = `https://www.tiktok.com/search/video?q=${formattedQuery}`;

    await page.goto(url, { waitUntil: 'networkidle2' });

    // Inject the provided script into the page
    await page.evaluate((count) => {
        window.allVideos = [];
        getInitialVideoIDs();

        const origOpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function(method, url) {
            this.addEventListener('load', function() {
                if (this.readyState === 4 && isVideoFetch(url)) {
                    const responseData = JSON.parse(this.responseText);
                    pushVideoIDs(responseData);
                    checkAutoScroller(responseData);
                }
            });
            origOpen.apply(this, arguments);
        };

        const autoScroller = setInterval(function() {
            window.scrollTo(0, document.body.scrollHeight);
        }, 1000);

        function isVideoFetch(url) {
            const videoFetchRegEx = /\/api\/post\/item_list\//;
            return videoFetchRegEx.test(url);
        }

        function pushVideoIDs(responseData) {
            responseData.itemList.forEach(item => {
                if (allVideos.indexOf(item.id) === -1) {
                    allVideos.push(item.id);
                }
            });
        } 

        function checkAutoScroller(responseData) {
            if (!responseData.hasMore || allVideos.length >= count) {
                clearInterval(autoScroller);
            }
        }

        function getInitialVideoIDs() {
            const videos = document.querySelectorAll('.tt-feed .video-feed-item-wrapper');
            videos.forEach(video => {
                const urlObj = new URL(video.href);
                const path = urlObj.pathname;
                const id = (path.match(/\/video\/(\d+)/) || [])[1];
                allVideos.push(id);
            });
        }
    }, count);

    // Wait for the auto-scroller to finish
    await new Promise(resolve => setTimeout(resolve, 30000)); // Adjust the timeout as needed

    // Retrieve the video IDs
    const videoIDs = await page.evaluate(() => window.allVideos);

    await browser.close();
    return videoIDs.slice(0, count);
}

const query = process.argv[2];
const count = parseInt(process.argv[3], 10);

scrapeTikTok(query, count).then(data => {
    console.log(JSON.stringify(data, null, 2));
}).catch(error => {
    console.error(error);
    process.exit(1);
});





