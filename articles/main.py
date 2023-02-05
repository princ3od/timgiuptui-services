from fastapi import FastAPI, HTTPException, status
from models import Article, SimilarArticle
from provider import Provider

app = FastAPI(version="0.1.0", title="FastAPI", description="FastAPI example")

provider = Provider()


@app.get("/", status_code=status.HTTP_200_OK)
def health():
    return "OK"


@app.get("/articles/{id}", status_code=status.HTTP_200_OK, response_model=Article)
def get_article(id: str):
    article = provider.get(id)
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    return article


@app.get(
    "/articles/{id}/similar",
    status_code=status.HTTP_200_OK,
    response_model=list[SimilarArticle],
)
def get_article(id: str):
    similar_articles = provider.get_similar_articles_of(id)
    if similar_articles is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    return similar_articles
