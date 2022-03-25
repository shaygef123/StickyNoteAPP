import pymongo
import os
MONGO_SERVER = os.getenv("MONGO_SERVER")
if MONGO_SERVER == None:
    MONGO_SERVER = "localhost"
print(MONGO_SERVER)
class MongoDB:
    def __init__(self,DB_username,DB_password,DB_name,DB_collection):
        client = pymongo.MongoClient(f"mongodb://{DB_username}:{DB_password}@{MONGO_SERVER}:27017")
        db = client[DB_name]
        self.collection = db[DB_collection]
    def account_exists(self,ID):
        # try:
        print("info:\n",self.collection)
        check = self.collection.find_one({"_id":int(ID)})
        print("check is:\n",check)
        if check == None:
            return False
        else:
            return True
        # except:
        #     return None

    def get_content(self,ID):
        try:
            data = self.collection.find_one({"_id": ID})
            return data
        except:
            return None

    def login_check(self,username,ID,password):
        if self.account_exists(ID):
            check = self.get_content(ID)
            if check == None:
                return None
            else:
                if check["password"] == password and check["username"] == username:
                    return True
                else:
                    return False
        else:
            return None

    def create_new_user(self,username,ID,password):
        if not self.account_exists(ID):
            create_post = {"_id": ID,
                           "username": username,
                           "password": password,
                           "body": f"Welcome {username}"}
            try:
                self.collection.insert_one(create_post)
                return self.account_exists(ID)
            except:
                return "There is problem to add new id"

        else:
            return "The account is already exists"


    def edit_data(self,ID,data):
        if  self.account_exists(ID):
            try:
                self.collection.update_one({"_id":ID},{"$set":{"body":data}})
                if self.get_data(ID)==data:
                    return True
                else:
                    return False
            except:
                return None
        else:
            return "There is no user exists"

    def get_data(self,ID):
        if self.account_exists(ID):
            data = self.collection.find_one({"_id": ID})
            return data["body"]
        else:
            return "There is no user exists"

class MongoACTION:
    def __init__(self,DB_username,DB_password,MONGO_SERVER="localhost"):
        self.client = pymongo.MongoClient(f"mongodb://{DB_username}:{DB_password}@{MONGO_SERVER}:27017/")

    def is_DB_exists(self,DB_name):
        DB_List = self.client.list_database_names()
        for DB in DB_List:
            if DB == DB_name:
                return True
        return False

    def is_Collection_exists(self,DB_name,DB_collection):
        db = self.client[DB_name]
        collections_List = db.list_collection_names()
        for collection in collections_List:
            if collection == DB_collection:
                return True
        return False

    def create_new_DB(self,DB_name,DB_collection):
        if not self.is_DB_exists(DB_name):
            db = self.client[DB_name]
            db.create_collection(DB_collection)
            return True
        else:
            if not self.is_Collection_exists(DB_name,DB_collection):
                db = self.client[DB_name]
                db.create_collection(DB_collection)
                return True
            return False



