from pymongo import MongoClient

from datetime import datetime

con = MongoClient("localhost", 27017)

db = con['testDB']

coll = db.posts

dblist = con.list_database_names()

dbcoll = db.list_collection_names()

posts = db.posts

time = str(datetime.now())

def printColl(coll):
    for x in coll.find():
        print(x)

data = {
    "name": "jayse",
    "age": "19",
    "date" : time
}

find = {
    "age" : "15"
}

delete = {
    "age" : "15"
}

findForUpdate = {
    "name" : "Vlad"
}

update = { "$set" : { "name" : "Jayse" } }

print("databeses:\n", dblist)

print("collection:\n", dbcoll)

print("\n-- start --\n")

print("\n-- all posts --\n")
printColl(posts)

# db.posts.remove() # clear
# posts.insert_one(data) # insert

# findres = posts.find(find) # find
# for x in findres:          # find
#     print(x)               # find

# deleteres = posts.delete_one(delete) # delete
# for x in deleteres:                  # delete
#     print(x)                         # delete

posts.update_many(findForUpdate, update) # update (update_one)

print("\n-- before --\n")

printColl(posts)