# Timgiuptui services

Event-driven microservices for [timgiuptui.com](https://timgiuptui.com).

## Tech stack

- Frameworks: FastAPI, Flask
- Database: Firestore
- Event handling: Cloud Pub/Sub

## Installation

Each service has its own `README.md` file. Please refer to each service's `README.md` file for installation instructions.

Generally, you need to install the following:

- Python 3.8+
- Docker
- Docker Compose

For better development, you can install `shared` packages:

```bash
pip install -e 'git+https://github.com/timgiuptui/timgiuptui-services.git@main#egg=common&subdirectory=share'
```

## Services

### gateway

- API gateway
- FastAPI

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

### analytics

- analyze metrics from crawled news
- Flask

## Diagrams

// TBA
