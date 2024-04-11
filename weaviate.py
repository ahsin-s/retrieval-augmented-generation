import weaviate

client = weaviate.connect_to_local()


article_class = client.schema.create_class(
    class_name="Article",
    description="Represents an article",
    properties=[
        {"name": "title", "dataType": ["string"]},
        {"name": "content", "dataType": ["text"]}
    ]
)
article_object = client.data.create_object(
    class_name="Article",
    properties={
        "title": "Introduction to Weaviate",
        "content": "Weaviate is a powerful vector database for semantic search."
    }
)
client.data.add_object(article_object)
client.close()
