from DuckDuckImageScrape import search

with open('Safe/PokeList (copy).txt', 'r') as f:
    for pokemon in f:
        search(pokemon, max_fetch=8, out='PokeImageFile.txt', png = False)
