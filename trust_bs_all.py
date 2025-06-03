# Ilias DUYCK - Github p-ilipili - 2025
# # MIT License
# Copyright (c) 2025 Ilias Duyck
# 
# This file is licensed under the MIT License.
import requests
import os
import shutil
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup as bs
from langdetect import detect
from googletrans import Translator
import time
import random

# Initialize google_trans_lzx translator
#translator = Translator()

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)...'
]

headers = {'User-Agent': random.choice(user_agents)}

# File and folder setup
file_name = "trust_score_all.csv"
backup_folder = "./old"
os.makedirs(backup_folder, exist_ok=True)

# Check if the file exists
if os.path.exists(file_name):
    # Use current date for renaming
    creation_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Rename the file
    backup_file = f"trust_score_{creation_date}.csv"
    backup_path = os.path.join(backup_folder, backup_file)
    shutil.move(file_name, backup_path)
    #print(f"Moved {file_name} to {backup_path}")


base_url = 'https://www.trustpilot.com/review/'
rank_site = 'www.backmarket.fr?languages=all&page='
# x sets the number of pages which will be scraped.
x = 3586
#x=1
pages = list(range(1, x + 1))
print(pages)

r_name_all = []
r_country_all = []
r_stars_all = []
r_title_all = []
r_text_all = []
r_date_all = []

# Function to translate text if it's not in English
def translate_text_lzx(text, target_lang='en'):
    if text:
        text = str(text)
        try:
            return translator.translate(text, dest=target_lang).text
        except Exception as e:
            raise ValueError(f"Translation error: {e}")  # Raise an error to skip this job

    raise ValueError("No text provided for translation")  # Raise an error if text is None or empty

# Function to check if text is in English
def is_english(text):
    try:
        return detect(text) == 'en'
    except Exception as e:
        print(f"Error detecting language: {e}")
        return False  # Treat as non-English if detection fails


batch_size = 80
for i in range(0, len(pages), batch_size):
    session = requests.Session()  # New session per batch
    batch = pages[i:i + batch_size]
    print(f"\n🔍 Scraping batch {i + 1} to {i + len(batch)}...")

    for page in batch:
        URL=f"{base_url}{rank_site}{page}"
        res = session.get(URL, headers=headers)
        # Check if request was successful
        if res.status_code == 200:
            bs_trust = bs(res.content,'lxml')
            #print(bs_trust.prettify().splitlines())
            with open('page_dump.txt', 'w', encoding='utf-8') as f:
                f.write(bs_trust.prettify())
            reviews = bs_trust.find_all('div', class_ = "styles_cardWrapper__g8amG styles_show__Z8n7u")
            #print(reviews)

            for review in reviews:
                uname = review.article.div.a.span.text
                #uname = review.article.div.div.aside.div.a.span.text    -> it's the same
                #print(uname)
                r_name_all.append(uname)

                country = review.article.div.a.div.span.text
                #print(country)
                r_country_all.append(country)

                star = review.article.div.section.div.get('data-service-review-rating')
                #print(star)
                r_stars_all.append(star)

                title = review.article.find('h2', class_ = "typography_heading-xs__osRhC typography_appearance-default__t8iAq").text
                #print(title)
                r_title_all.append(title)

                r_text = review.article.div.section.div.find_next_sibling('div').p.text
                '''if not is_english(r_text_ori):
                    r_text = translate_text_lzx(r_text_ori)
                else:
                    r_text = r_text_ori '''
                #r_text = r_text_ori
                r_text_all.append(r_text)

                r_date = review.article.time.get('datetime')
                #print(r_date)
                r_date_all.append(r_date)
        else:
            print(f"Failed to retrieve data for page {page}")

    timewait = random.uniform(160, 320)
    print(f"✅ Finished batch {i + 1} to {i + len(batch)}. Sleeping for {timewait} seconds...\n")
    time.sleep(timewait)

df_trust_score = pd.DataFrame({
    'username' : r_name_all,
    'country' : r_country_all,
    'rating' : r_stars_all,
    'date' : r_date_all,
    'title' : r_title_all,
    'review' : r_text_all
})

df_trust_score.to_csv(file_name, sep=';', index=False, encoding='utf-8')