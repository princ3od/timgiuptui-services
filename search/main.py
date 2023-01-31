from fastapi import FastAPI, status, Request, HTTPException
from provider import Provider
from models import SearchQuery

app = FastAPI(
    version="0.1.0",
    title="[timgiuptui] Search Service",
    description="Search service documentation",
)
provider = Provider()


@app.get("/", status_code=status.HTTP_200_OK)
def health():
    return "OK"


@app.get("/articles/search", status_code=status.HTTP_200_OK)
def get_user(request: Request):
    params = request.query_params
    try:
        query = SearchQuery(**params)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    articles = provider.search(query)
    return articles
