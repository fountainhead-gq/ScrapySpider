# InstagramCrawler
### Installation

`pip install selenium`

Note:  selenium = 3.4, geckodriver = 0.15(it doesn't work on windows if you use higher version)



### Usage:

```
usage: instagramcrawler.py [-h] [-q QUERY] [-n NUMBER] [-c] [-d DIR]
```

- [-d DIR]: the directory to save crawling results, default is './data/[query]'
- [-q QUERY] : username, add '#' to search for hashtags, e.g. '#hashtag'
- [-t CRAWL_TYPE]: crawl_type, Options: 'photos | followers | following'
- [-c]: add this flag to download captions(what user wrote to describe their photos)
- [-n NUMBER]: number of posts, followers, or following to crawl
  ​

### Example:
Download the first 100 photos from username "liekevandervorst"

```
 python instagramcrawler.py -q liekevandervorst -c -n 100
```
Search for the hashtag "#nbafinals" and download first 50 photos
```
 python instagramcrawler.py -q #nbafinals -n 50
```

Record the first 30 followers of the username "liekevandervorst", requires log in
```
 python instagramcrawler.py -q liekevandervorst -t followers -n 30
```



