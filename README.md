# TrustPilot Score Scraper and Translator

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

## Overview

This script, `trust_bs_all.py`, automates the process of:

- Scraping Trustpilot review pages
- Extracting structured information such as star ratings, dates, user names, and review content
- Detecting the language of reviews
- Translating non-English reviews into English using Google Translate
- Saving the results to a CSV file
- Backing up previous runs

It is intended for research, data analysis, or quality monitoring purposes.

## Features (translation deactivated by default, needs tweaked google-trans-lzx depending on your OS)

- Web scraping with `requests` and `BeautifulSoup`
- Language detection via `langdetect`
- Translation using `googletrans` (or a patched `google-trans-lzx`)
- Automatic CSV backup in an `old/` folder
- User-agent randomization to reduce bot detection

## Requirements

- Python 3.8+
- Required packages:
  - `requests`
  - `beautifulsoup4`
  - `langdetect`
  - `googletrans==4.0.0-rc1` or compatible fork (e.g. `google-trans-lzx`)
  - `pandas`
