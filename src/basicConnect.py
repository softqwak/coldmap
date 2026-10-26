from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import numpy as np

# Подключение к Qdrant
client = QdrantClient(host="localhost", port=6333)

collection_name = "my_collection"

# Безопасная проверка и удаление коллекции для v1.7.4
existing_collections = [col.name for col in client.get_collections().collections]
if collection_name in existing_collections:
    client.delete_collection(collection_name=collection_name)

# Создание коллекции
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=128, distance=Distance.COSINE),
)

# Добавление векторов
points = [
    PointStruct(
        id=1,
        vector=np.random.rand(128).tolist(),
        payload={"text": "Пример документа 1"},
    ),
    PointStruct(
        id=2,
        vector=np.random.rand(128).tolist(),
        payload={"text": "Пример документа 2"},
    ),
]

client.upsert(collection_name=collection_name, points=points)

# Поиск похожих векторов
search_result = client.search(
    collection_name=collection_name,
    query_vector=np.random.rand(128).tolist(),
    limit=5,
)

print("Найденные результаты:")
for result in search_result:
    print(f"ID: {result.id}, Score: {result.score}")
    print(f"Payload: {result.payload}")