from config import client
from bson.objectid import ObjectId



db = client.PRACTICE_DB

# cursor = db.inventory.find({
#     "_id": ObjectId("66216367815b33209271c615")
# })
# # print(len(list(cursor)))
# for item in cursor:
    
#     print(str(item['_id']))




# result = db.inventory.find_one({
#     "_id": ObjectId("66216367815b33209271c611")
# })

# print(result)


count = db.inventory.count_documents({})
print(count)