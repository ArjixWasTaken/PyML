This is my API for scraping [Yify](https://www.yts.mx)

[![PyPI version](https://badge.fury.io/py/YifyAPI.png)](https://badge.fury.io/py/YifyAPI)

**#USAGE**

First you have to import it.

```python
from YifyAPI import yify as api
```

Now you are ready to use it!

Currently the only method is :

```python 
api.search_yify(query: str, proxy=None)
```

It will return a list with dictionaries for each movie result found, example below:

```json
[
    {
        "title":"Sonic the Hedgehog",
        "year":"2020",
        "director":[
            "Jeff Fowler",
            "https://www.imdb.com/name/nm1733778/"
        ],
        "cast":[
            [
                "Jim Carrey",
                "https://www.imdb.com/name/nm0000120/"
            ],
            [
                "James Marsden",
                "https://www.imdb.com/name/nm0005188/"
            ],
            [
                "Neal McDonough",
                "https://www.imdb.com/name/nm0568180/"
            ],
            [
                "Tika Sumpter",
                "https://www.imdb.com/name/nm1754366/"
            ]
        ],
        "subtitles":"https://yifysubtitles.org/movie-imdb/tt3794354/",
        "related_movies":[
            [
                "Clerks II (2006)",
                "https://yts.mx/movies/clerks-ii-2006"
            ],
            [
                "Planet of the Apes (1968)",
                "https://yts.mx/movies/planet-of-the-apes-1968"
            ],
            [
                "*batteries not included (1987)",
                "https://yts.mx/movies/batteries-not-included-1987"
            ],
            [
                "Hedgehog (2017)",
                "https://yts.mx/movies/hedgehog-2017"
            ]
        ],
        "synopsis":"Based on the global blockbuster videogame franchise from Sega, SONIC THE HEDGEHOG tells the story of the world's speediest hedgehog as he embraces his new home on Earth. In this live-action adventure comedy, Sonic and his new best friend Tom (James Marsden) team up to defend the planet from the evil genius Dr. Robotnik (Jim Carrey) and his plans for world domination. The family-friendly film also stars Tika Sumpter and Ben Schwartz as the voice of Sonic.",
        "categories":[
            "Action",
            "Adventure",
            "Comedy",
            "Family",
            "Sci-Fi"
        ],
        "link":"https://yts.mx/movies/sonic-the-hedgehog-2020",
        "imdbLink":"https://www.imdb.com/title/tt3794354/",
        "trailer":"https://www.youtube.com/watch?v=szby7ZHLnkA",
        "imdbRating":"6.5/10",
        "image":{
            "small":"https://yts.mx/assets/images/movies/sonic_the_hedgehog_2020/small-cover.jpg",
            "large":"https://img.yts.mx/assets/images/movies/sonic_the_hedgehog_2020/medium-cover.jpg"
        },
        "qualities":[
            [
                "720p.BluRay",
                "908.03 MB",
                "magnet:?xt=urn:btih:"
            ],
            [
                "1080p.BluRay",
                "1.82 GB",
                "magnet:?xt=urn:btih:"
            ],
            [
                "2160p.BluRay",
                "5.05 GB",
                "magnet:?xt=urn:btih:"
            ],
            [
                "720p.WEB",
                "911.23 MB",
                "magnet:?xt=urn:btih:"
            ],
            [
                "1080p.WEB",
                "1.65 GB",
                "magnet:?xt=urn:btih:"
            ]
        ]
    }
]
```
An example code snippet that uses YifyAPI can be found [here](https://gist.github.com/ArjixWasTaken/09a0cda12e9773b71d8ecaaf46f068ea).

If something goes bad and there was an error then it will return this:

```
{'status': "error"}
```

So make sure to check if the response is equal to the one above with an if statement.



If you encounter any bug with my code or you want to contribute in any way then [here](https://github.com/ArjixGamer/YifyAPI) is the github link
