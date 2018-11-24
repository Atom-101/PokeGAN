import urllib.request

with open('PokeImageFile.txt','r') as f:
  for i,url in enumerate(f):
    try:
        if(i<554):
            continue
        filename = url.split('/')[-1]
        urllib.request.urlretrieve(url, 'Pokemon_Dataset/'+filename)
        print(i)
    except:
        continue
