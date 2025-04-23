# ActivateScraper
## Overview

ActivateScraper is an asynchronous web scraper that fetches and processes event data from ActivateUTS clubs by hitting ActivateUTS hidden backend API to fetch real time data.

## Features

- Asynchronous HTTP requests using `httpx`
- Rate limiting and request throttling
- Data validation using Pydantic models
- JSON output with proper formatting
- Error handling and logging

## Requirements

- Python 3.7+
- httpx
- asyncio
- pydantic

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/activatescraper.git
cd activatescraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python main.py
```

The scraper will:
1. Load club endpoints from `files/club_paths.json`
2. Fetch event data for each club asynchronously
3. Save the results to `data/club_data.json`


## Error Handling

The scraper includes:
- Rate limit detection and retry mechanism
- Error logging for failed requests
