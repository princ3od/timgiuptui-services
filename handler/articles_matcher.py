from constants import SIMILARITY_THRESHOLD
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from logs import logger
from models import Article, ArticlesFromCrawler
from stopwords import stopwords
from underthesea import word_tokenize


def match_articles(data: ArticlesFromCrawler):
    """
    Match articles with their similars using Doc2Vec model.
    """
    logger.info("Start matching articles...")

    for topic_id, articles in data.articles.items():
        matching_model = _create_matching_model(topic_id, articles)
        data.articles[topic_id] = _match_articles(matching_model, articles)

    logger.info("Finished matching articles.")


def _create_matching_model(topic_id: str, articles: list[Article]):
    """
    Create matching model.
    """
    logger.info(f"Creating matching model for topic {topic_id}...")
    tokenized_articles = {}
    for article in articles:
        tokenized_articles[article.id] = _tokenize_article(article)
    tagged_data = [
        TaggedDocument(words=tokenized_article, tags=[index])
        for index, tokenized_article in enumerate(tokenized_articles.values())
    ]
    model = Doc2Vec(tagged_data, vector_size=20, window=2, min_count=1, workers=4)
    logger.info(f"Created matching model for topic {topic_id}.")
    return model


def _tokenize_article(article: Article):
    """
    Tokenize article.
    """
    tokens = word_tokenize(article.get_full_text().lower())
    return [token for token in tokens if token not in stopwords]


def _match_articles(model: Doc2Vec, articles: list[Article]):
    """
    Match articles.
    """
    logger.info("Matching articles...")
    for article in articles:
        targeted_article_vector = model.infer_vector(_tokenize_article(article))
        similarities = model.docvecs.most_similar([targeted_article_vector], topn=5)
        is_print_targeted_article = False
        targeted_article_source = article.source
        for similarity in similarities[1:]:
            similar_article = articles[similarity[0]]
            similar_percentage = round(similarity[1], 4)
            if not is_print_targeted_article:
                logger.info(f"> Targeted article: {article.id}")
                is_print_targeted_article = True
            if similar_percentage < SIMILARITY_THRESHOLD:
                break
            if similar_article.source == targeted_article_source:
                continue
            logger.info(
                f">> Similar article: {similar_article.id} - {similar_percentage}"
            )
            article.similar_articles[similar_article.id] = {
                "title": similar_article.title,
                "url": similar_article.url,
                "source": similar_article.source,
                "thumbnail": similar_article.thumbnail,
                "similarity": similar_percentage,
            }
    logger.info("Matched articles.")
    return articles
