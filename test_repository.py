from database.memory_repository import MemoryRepository

repo = MemoryRepository()

repo.save(
    "preferences",
    "favorite_language",
    "Python"
)

print(repo.get("favorite_language"))

print(repo.all())