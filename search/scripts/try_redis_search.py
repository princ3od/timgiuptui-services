import datetime
import json

from init_redis_index import redis_client
from redis.commands.json.path import Path
from redis.commands.search.field import NumericField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

books = []
titles = [
    "Chuyện Tình Yêu",
    "Cuộc Đời Nhỏ",
    "Ngày Hạnh Phúc",
    "Sứ Mệnh Đại Chiến Covid-19",
    "Tình Yêu Không Thể Nói Covid-12",
    "Hành Trình Đến Thành Công",
    "Tình Bạn Trẻ Tuổi",
    "Chiến Trận Tự Do",
    "Cuộc Đời Lớn",
    "Người Tình Của Tôi",
]
for i in range(10):
    title = titles[i]
    timestamp = datetime.datetime.now().timestamp()
    books.append({"title": title, "date": timestamp})

for index, book in enumerate(books):
    redis_client.json().set(f"books:{book['title']}", Path.rootPath(), book)

try:
    schema = (
        TextField("$.title", as_name="title"),
        NumericField("$.date", as_name="date"),
    )

    redis_client.ft("books").create_index(
        schema, definition=IndexDefinition(prefix=["books:"], index_type=IndexType.JSON)
    )
except Exception as e:
    print(e)

term = "covid 19"
fuzzy_term = "".join([f"%%{w}%%" for w in term.split(" ")])
print(fuzzy_term)
query = bytes(fuzzy_term, "utf-8")
result = redis_client.ft("books").search(Query(query).with_scores())

books = sorted(result.docs, key=lambda x: x.score)

for book in books:
    _book = json.loads(book.json)
    score = book.score
    print(f"{_book['title']} - {score}")
