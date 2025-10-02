# KiddoWorksheets Scraper

A Python web scraper for downloading educational worksheets from KiddoWorksheets.com.

## Features

- Scrapes worksheets from KiddoWorksheets.com
- Downloads PDF worksheets and direct image files (PNG, JPG, etc.)
- Organizes files by educational categories
- Generates JSON metadata file with all worksheet information
- Dockerized for easy deployment and consistent environment

## Quick Start

### Using Docker (Recommended)

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually:**
   ```bash
   # Build the image
   docker build -t kiddoworksheets-scraper .
   
   # Run the container
   docker run -v $(pwd)/worksheets:/app/worksheets -v $(pwd)/worksheets.json:/app/worksheets.json kiddoworksheets-scraper
   ```

### Using Python directly

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the scraper:**
   ```bash
   python scraper.py
   ```

## Configuration

### Download Mode
Edit `scraper.py` and change the `DOWNLOAD_PDFS` flag:
- `DOWNLOAD_PDFS = True` - Downloads actual files
- `DOWNLOAD_PDFS = False` - Only collects metadata

### Docker Environment Variables
You can set environment variables in `docker-compose.yml` or create a `.env` file:
```
DOWNLOAD_PDFS=true
```

## Output

- **`worksheets/`** - Directory containing downloaded worksheet files
- **`worksheets.json`** - JSON file with metadata organized by categories

## Docker Files Explained

- **`Dockerfile`** - Multi-stage build with Python 3.12 slim image
- **`docker-compose.yml`** - Easy orchestration with volume mounts
- **`.dockerignore`** - Excludes unnecessary files from Docker context
- **`requirements.txt`** - Python dependencies

## Dependencies

- `requests` - HTTP requests
- `beautifulsoup4` - HTML/XML parsing
- `lxml` - XML parser backend
