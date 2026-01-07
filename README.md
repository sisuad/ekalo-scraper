# KiddoWorksheets Scraper

[中文文档](README_zh.md) | [English](README.md)

A Python web scraper for downloading educational worksheets from KiddoWorksheets.com.

## Features

- Scrapes worksheets from KiddoWorksheets.com
- Downloads PDF worksheets and direct image files (PNG, JPG, etc.)
- **Configurable download formats (PDF/PNG)**
- Organizes files by educational categories
- Generates JSON metadata file with all worksheet information
- Dockerized for easy deployment and consistent environment

## Quick Start

### Using Docker (Recommended)

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```
   *Note: The service is configured to restart if the image is already present.*

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
   # Optional: set environment variables
   export DOWNLOAD_PDFS=false
   export DOWNLOAD_PNGS=true
   
   python scraper.py
   ```

## Configuration

You can control which file types to download using environment variables.

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `DOWNLOAD_PDFS` | `false` | Set to `true` to enable PDF downloads |
| `DOWNLOAD_PNGS` | `true` | Set to `true` to enable PNG downloads |

### Docker Configuration
You can set these variables in `docker-compose.yml` or create a `.env` file:
```yaml
environment:
  - DOWNLOAD_PDFS=false
  - DOWNLOAD_PNGS=true
```

## Output

- **`worksheets/`** - Directory containing downloaded worksheet files
- **`worksheets.json`** - JSON file with metadata organized by categories

## Docker Files Explained

- **`Dockerfile`** - Multi-stage build with Python 3.12 slim image
- **`docker-compose.yml`** - Easy orchestration with volume mounts. Optimized to reuse existing images.
- **`.dockerignore`** - Excludes unnecessary files from Docker context
- **`requirements.txt`** - Python dependencies

## Dependencies

- `requests` - HTTP requests
- `beautifulsoup4` - HTML/XML parsing
- `lxml` - XML parser backend
