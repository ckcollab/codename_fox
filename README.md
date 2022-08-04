# codename_fox

This project is for scraping articles from popular news organizations for further analysis.


Usage:

```bash
$ git clone https://github.com/ckcollab/codename_fox.git
$ cd codename_fox
$ pip install -r requirements.txt
$ ./scraper.py

# articles written to output/
```

Edit `scraper.py` to configure the project

## TODO:

 - Get dump of article urls for
   - cnn
     - ~~may need custom parser for articles? only grabs up to "READ MORE"~~ fixed with more recent pip install
     - removed espanol, arabic
   - fox
     - remove these strings:
       - ~~"NEW You can now listen to Fox News articles!\n\n"~~ removed
   - newsmax
     - this seems OK
   - breitbart
     - this seems OK
   - msnbc
     - this seems OK

 - For each page dump text to output/<org name>/<date> - <title>.txt

 - Use pool to fetch articles?

 - For each set of article urls, comb through them and find problems
   - espanol?
   - arabic?
   - videos?
   - need to remove non-english stuff
