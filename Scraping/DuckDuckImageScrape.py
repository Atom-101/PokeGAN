import requests
import re
import json
import pprint
import time

OUT_FILE = 'File.txt'

def search(keywords, max_fetch=None, png = True, out=None):
    #50 entries fetched per call if png is False, unpredictable if png is True
    if(max_fetch is None):
        max_fetch = 1

    if(out is None):
        out = OUT_FILE
        
    url = 'https://duckduckgo.com/'
    params = {
    	'q': keywords
    }

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=(\d+)\&', res.text, re.M|re.I)

    headers = {
    'dnt': '1',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'x-requested-with': 'XMLHttpRequest',
    'accept-language': 'en-GB,en-USq=0.8,enq=0.6,msq=0.4',
    'user-agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'accept': 'application/json, text/javascript, */* q=0.01',
    'referer': 'https://duckduckgo.com/',
    'authority': 'duckduckgo.com',
    }

    params = (
    ('l', 'wt-wt'),
    ('o', 'json'),
    ('q', keywords),
    ('vqd', searchObj.group(1)),
    ('f', ',,,'),
    ('p', '2')
    )

    requestUrl = url + "i.js"

    for i in range(max_fetch):
        try:
            res = requests.get(requestUrl, headers=headers, params=params)
            data = json.loads(res.text)
        except:
            continue
        printJson(data["results"], png, out)
        if ("next" not in data):
            return
        requestUrl = url + data["next"]
        if(i<max_fetch-1):    
            time.sleep(4)

def printJson(objs, png, out_file):
    for obj in objs:
        print ("Width {0}, Height {1}".format(obj["width"], obj["height"]))
        print ("Thumbnail {0}".format(obj["thumbnail"]))
        print ("Url {0}".format(obj["url"]))
        print ("Title {0}".format(obj["title"].encode('utf-8')))
        print ("Image {0}".format(obj["image"]))
        print ("__________")
        if(png): #If png true, only write png
            if('.png' not in obj['image']):
                continue
        else: #never write gif
            if('.gif' in obj['image']):
                continue
        with open(out_file, 'a') as f:
            f.write(obj['image']+'\n')
