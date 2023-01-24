# Timgiuptui services

Backend microservices for timgiuptui.com

## Tech stack

Each service is a separate project, and each project is a separate git repository. They may use one or more of the following frameworks:

- Flask
- FastAPI

## Installation

Each service has its own `README.md` file. Please refer to each service's `README.md` file for installation instructions.

Generally, you need to install the following:

- Python 3.8+
- Docker
- Docker Compose

To run any service, you need to:

```bash

# move to the service directory
cd <service_name>

docker-compose up -d

```

## Services

### gateway

- API gateway
- FastAPI

### analytics

- analyze metrics from crawled news
- Flask

### crawler

- crawl news from different sources
- Flask

### articles

- CRUD articles
- FastAPI

### handler

- handle crawled news
- Flask

### platform

- manage analytic, configuration
- FastAPI

### search

- search articles
- FastAPI
