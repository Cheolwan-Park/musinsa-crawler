# How to use
### Setup crawler.env
- CATEGORY_IDX: idx of the category (category array is in crawling/categories.py)
- START: start page number
- N: number of pages to crawl
- DELAY: time delay between page transitions

### RUN
```
docker-compose up (--abort-on-container-exit)
```
### RUN in windows
1. start 'Docker Desktop' (dl link: https://hub.docker.com/editions/community/docker-ce-desktop-windows)
2. execute 'run-crawler.bat' in project directory (click it or execute via shell)
