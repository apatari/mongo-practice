from config import client



db = client.PRACTICE_DB

cursor = db.inventory.find({
    "status":"D"
})
for item in cursor:
    print(item['item'])