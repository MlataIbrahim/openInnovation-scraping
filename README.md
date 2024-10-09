# Steam Market Scraper

This project scrapes product data from the Steam marketplace and stores it in a MongoDB database. It using the Steam Community Market API and provides a FastAPI application to serve the scraped data via an API. 

## Features

- Scrape product data from Steam marketplace.
- Handle pagination, network retries, and rate limits.
- Store scraped data in MongoDB.
- FastAPI application to serve the data with pagination.
- Tests using `unittest`.

## Prerequisites

Ensure you have the following installed:

- Docker
- Docker Compose

## Setup

1. **Clone the repository**:

    ```bash
    git clone git@github.com:MlataIbrahim/openInnovation-scraping.git
    cd openInnovation-scraping
    ```

2. **Docker Compose**:

    The project is orchestrated using Docker Compose. This will set up the MongoDB instance, the FastAPI service, and the scraper service.

    To start the services, run:

    ```bash
    docker-compose up --build
    ```

    This will build the Docker images and start the application.

3. **Scraping with Docker**:

    The scraper service is included in the Docker setup. It runs continuously, scraping data and storing it in MongoDB.

4. **Accessing the API**:

    Once the FastAPI service is up, the API will be available at:

    ```
    http://localhost:8000/products/
    ```

    You can use query parameters for pagination:

    ```
    http://localhost:8000/products/?offset=0&limit=10
    ```

## Project Structure

```
.
├── app/
│   ├── app.py                # FastAPI application
│   ├── Dockerfile            # Dockerfile for FastAPI service
│   └── requirements.txt      # Dependencies for FastAPI service
├── scraping/
│   ├── Games/
│   │   ├── spiders/
│   │   │   ├── steam.py      # Scrapy spider for Steam Market data
│   │   ├── items.py          # Scrapy items definition
│   │   ├── pipelines.py      # Pipeline for MongoDB insertion
│   │   ├── middlewares.py    # Middleware (if needed)
│   │   ├── settings.py       # Project settings
│   ├── Dockerfile            # Dockerfile for Scrapy service
│   ├── requirements.txt      # Dependencies for Scrapy
│   ├── scrapy.cfg            # Scrapy project configuration
├── tests/
│   ├── test_api.py           # Tests for FastAPI application
│   ├── test_pipeline.py      # Tests for Scrapy MongoDB pipeline
│   ├── test_spider.py        # Tests for Scrapy spider
├── docker-compose.yml        # Docker Compose setup
├── tox.ini                   # Configuration for tox testing
└── README.md                 # Project documentation
```

## Endpoints

- **`GET /products/`** - Retrieves a paginated list of products from MongoDB.
  - Query Parameters:
    - `offset`: Number of products to skip (default: 0)
    - `limit`: Number of products to return (default: 10)

## Testing

Tests are available for:

- **MongoDB Pipeline**: Tests the insertion of items into MongoDB.
- **API Endpoints**: Tests for product retrieval.
- **Scraper Spider**: Ensures correct data extraction from the Steam marketplace.

## Running Tests

The project uses `unittest` for testing.

To run the tests inside the Docker container:

```bash
docker-compose exec fastapi_server python -m unittest discover -s tests

```
## Troubleshooting

If you encounter issues with MongoDB or the FastAPI application, ensure the containers are running correctly:

```bash
docker-compose ps
```

If a container is not running, check the logs for more details:

```bash
docker-compose logs <container_name>
```