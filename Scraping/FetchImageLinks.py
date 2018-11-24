#This script will search for images for each pokemon in PokeList.txt 
#and write the URLs of found images in PokeImageFile.txt

from DuckDuckImageScrape import search

with open('PokeList.txt', 'r') as f:
    for pokemon in f:
        search(pokemon, max_fetch=8, out='PokeImageFile.txt', png = False)
