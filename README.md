# Crawler

Easily fetch the HTML from any website by using Google Chrome instead of a basic GET request.


## Quickstart

To quickly try out this service:
```
docker run -p 5002:5002 -e DEBUG_MODE='true' kristianwindsor/crawler
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://localhost:5002
```

## Run locally

To clone this project and build from source:
```
git clone https://github.com/KristianWindsor/crawler.git
cd crawler/
docker-compose up -d
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://localhost:5002
```


## Integrate with your app

You're building an app that needs to crawl websites, but some sites are witholding their HTML from your simple GET requests? And you don't want to install Google Chrome on your app's container? Well, you came to the right place.

Here's a python example:
```
import requests

crawler_url = 'http://localhost:5002'
url = 'https://example.com'
payload = { 'url': url }
response = requests.post(crawler_url, json=payload)

html = response.content
print(html)
```