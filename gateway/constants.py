import os

SEARCH_SERVICE_URL = os.getenv(
    "SEARCH_SERVICE_URL", "https://search-rtfemypala-as.a.run.app"
)

PLATFORM_SERVICE_URL = os.getenv(
    "PLATFORM_SERVICE_URL", "https://platform-rtfemypala-as.a.run.app"
)

ARTICLES_SERVICE_URL = os.getenv(
    "ARTICLES_SERVICE_URL", "https://articles-rtfemypala-as.a.run.app"
)