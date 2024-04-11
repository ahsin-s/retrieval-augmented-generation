import weaviate
import weaviate.classes as wvc

client = weaviate.connect_to_local()

schema_definition = {
    "classes": [
        {
            "class": "Question",
            "description": "Information from a Jeopardy! question",
            "invertedIndexConfig": {
                "bm25": {
                    "b": 0.75,
                    "k1": 1.2
                },
                "cleanupIntervalSeconds": 60,
                "stopwords": {
                    "additions": None,
                    "preset": "en",
                    "removals": None
                }
            },
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                    "vectorizeClassName": True
                }
            },
            "properties": [
                {
                    "dataType": [
                        "text"
                    ],
                    "description": "The question",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": False,
                            "vectorizePropertyName": False
                        }
                    },
                    "name": "question",
                    "tokenization": "word"
                },
                {
                    "dataType": [
                        "text"
                    ],
                    "description": "The answer",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": False,
                            "vectorizePropertyName": False
                        }
                    },
                    "name": "answer",
                    "tokenization": "word"
                },
                {
                    "dataType": [
                        "text"
                    ],
                    "description": "The category",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": False,
                            "vectorizePropertyName": False
                        }
                    },
                    "name": "category",
                    "tokenization": "word"
                }
            ],
            "replicationConfig": {
                "factor": 1
            },
            "shardingConfig": {
                "virtualPerPhysical": 128,
                "desiredCount": 1,
                "actualCount": 1,
                "desiredVirtualCount": 128,
                "actualVirtualCount": 128,
                "key": "_id",
                "strategy": "hash",
                "function": "murmur3"
            },
            "vectorIndexConfig": {
                "skip": False,
                "cleanupIntervalSeconds": 300,
                "maxConnections": 64,
                "efConstruction": 128,
                "ef": -1,
                "dynamicEfMin": 100,
                "dynamicEfMax": 500,
                "dynamicEfFactor": 8,
                "vectorCacheMaxObjects": 1000000000000,
                "flatSearchCutoff": 40000,
                "distance": "cosine"
            },
            "vectorIndexType": "hnsw",
            "vectorizer": "text2vec-openai"
        }
    ]
}

try:
    questions = client.collections.create(
        name="Question",
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),    # Set the vectorizer to "text2vec-openai" to use the OpenAI API for vector-related operations
        generative_config=wvc.config.Configure.Generative.cohere(),             # Set the generative module to "generative-cohere" to use the Cohere API for RAG
        properties=[
            wvc.config.Property(
                name="question",
                data_type=wvc.config.DataType.TEXT,
                vectorize_property_name=True,  # Include the property name ("question") when vectorizing
                tokenization=wvc.config.Tokenization.LOWERCASE  # Use "lowecase" tokenization
            ),
            wvc.config.Property(
                name="answer",
                data_type=wvc.config.DataType.TEXT,
                vectorize_property_name=False,  # Skip the property name ("answer") when vectorizing
                tokenization=wvc.config.Tokenization.WHITESPACE  # Use "whitespace" tokenization
            ),
        ]
    )

finally:
    client.close()