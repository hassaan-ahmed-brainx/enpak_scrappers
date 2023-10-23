from pymongo import MongoClient
from datetime import datetime, timedelta
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
client = MongoClient(settings.get('MONGODB_URI'))
db = client[settings.get('MONGODB_DATABASE')]
collection = db[settings.get('MONGODB_COLLECTION')]

past_date = int((datetime.utcnow() - timedelta(days=30)).timestamp())

result = collection.delete_many({'isScrapped': True, 'createdAt': {'$lt': past_date}})
print("Deleted documents:", result.deleted_count)

client.close()
