import os
from redis import Redis
from dotenv import load_dotenv


load_dotenv()

redis_client = Redis(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    password=os.environ.get("REDIS_PASSWORD"),
)

# schema = (
#     TextField("$.title", as_name="title"),
#     NumericField("$.date", as_name="date"),
# )

# redis_client.ft("articles").create_index(
#     schema, definition=IndexDefinition(prefix=["articles:"], index_type=IndexType.JSON)
# )
