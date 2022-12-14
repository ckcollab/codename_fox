#!/usr/bin/env python3
import os

import dateutil.parser
import newspaper
import re

from datetime import datetime
from newspaper import Article, Config, ArticleException

# ----------------------------------------------------------------------------
# Configuration section
# ----------------------------------------------------------------------------
ORGANIZATIONS = [
    # liberal
    # ("Lcnn", "https://cnn.com"),
    # ("Lmsnbc", "https://msnbc.com/"),
    # ("LVOX","https://www.vox.com/"),
    # ("LDaily Beast","https://www.thedailybeast.com/"),
    # ("LBuzzfeed News","https://www.buzzfeednews.com/"),
    # ("LVICE","https://www.vice.com/en"),
    # ("LPalmer Report","https://www.palmerreport.com/"),
    # ("LDemocracy Now","https://www.democracynow.org/"),
    # ("LHuff Post","https://www.huffpost.com/"),
    # ("LNY Times","https://www.nytimes.com/"),

    # neutral
    # ("NReuter","https://www.reuters.com/"),
    # ("NAP","https://www.ap.org/en/"),
    # ("NBBC","https://www.bbc.com/news"),
    # ("NC-Span","https://www.c-span.org/"),
    # ("NBloomberg","https://www.bloomberg.com/"),
    # ("NStat","https://www.statnews.com/"),
    # ("NNYJournalMEd","https://www.nejm.org/"),
    # ("NUSA Today","https://www.usatoday.com/"),
    # ("NNature","https://www.nature.com/"),
    # ("NScience","https://www.sciencenews.org/"),

    # Conservative
    # ("Cfoxnews", "https://www.foxnews.com/"),
    # ("Cbreitbart", "https://www.breitbart.com/"),
    # ("Cnewsmax", "https://newsmax.com/"),
    ("COAN", "https://www.oann.com/"),
    ("CDailywire","https://www.dailywire.com/read"),
    ("CEagle Fourm","https://eagleforum.org/"),
    ("CRed State","https://redstate.com/"),
    ("CDailycaller","https://dailycaller.com/"),
    ("CNew York Post","https://nypost.com/"),
    ("CDailyMail","https://www.dailymail.co.uk/ushome/"),
]

URL_PATTERNS_TO_IGNORE = [
    # CNN
    r"cnnespanol.cnn.com",
    r"arabic.cnn.com",

    # Fox
    r"video.foxnews.com",
]

TEXT_CHUNKS_TO_REMOVE = [
    "NEW You can now listen to Fox News articles!\n\n",
]

OUTPUT_DIRECTORY = "./output/"

# ----------------------------------------------------------------------------
# Don't edit below here!
# ----------------------------------------------------------------------------
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

for news_organization, base_url in ORGANIZATIONS:
    # Get articles from front pages
    source = newspaper.build(base_url, config=config, memoize_articles=False)
    # source.download_articles()

    # Read 'em
    for article in source.articles:
        if any([re.search(p, article.url) for p in URL_PATTERNS_TO_IGNORE]):
            # Skip this one!
            continue

        print(f"Downloading {article.url}")

        try:
            article.download()
            article.parse()
        except ArticleException:
            # Article not found?! go onto next one..
            continue

        extracted_text = article.text
        for chunk in TEXT_CHUNKS_TO_REMOVE:
            extracted_text = extracted_text.replace(chunk, "")

        # Get date...
        published_date = article.publish_date
        if not published_date:
            # CNN helpers
            if "og" in article.meta_data:
                if article.meta_data["og"].get("pubdate"):
                    pubdate = article.meta_data["og"].get("pubdate")
                    published_date = dateutil.parser.parse(pubdate)

            # Try to snag the article date from Fox in various ways
            if article.meta_data.get("dc.date"):
                dc_date = article.meta_data.get("dc.date")
                try:
                    published_date = datetime.strptime(dc_date, "%Y-%m-%d %I:%M:%S %p")
                except ValueError:
                    published_date = datetime.strptime(dc_date, "%Y-%m-%d")

        # No date found? set today
        if not published_date:
            published_date = datetime.today()

        # Write 'em
        document_title = f"{published_date:%Y-%m-%d} - {article.title}.txt"
        document_output_path = os.path.join(OUTPUT_DIRECTORY, news_organization, document_title)
        os.makedirs(os.path.dirname(document_output_path), exist_ok=True)
        with open(document_output_path, "w") as f:
            f.write(extracted_text)
