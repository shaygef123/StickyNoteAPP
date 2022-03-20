import pymongo
import os
MONGO_SERVER = os.getenv("MONGO_SERVER")
class MongoDB:
    def __init__(self,DB_username,DB_password,DB_name,DB_collection):
        client = pymongo.MongoClient(f"mongodb://{DB_username}:{DB_password}@{MONGO_SERVER}:27017/")
        self.db = client[DB_name]
        self.collection = self.db[DB_collection]

    def account_exists(self,ID):
        try:
            check = self.collection.find_one({"_id": ID})
            return check
        except:
            return "There was problem with the search"

    def login_check(self,username,ID,password):
        check = self.account_exists(ID)
        if check == None:
            return False
        else:
            try:
                if check["password"] == password and check["username"] == username:
                    return True
                else:
                    return False
            except:
                return False

    def create_new_user(self,username,ID,password):
        check = self.account_exists(ID)
        if check != None:
            return "The account is already exists"
        else:
            create_post = {"_id":ID,
                   "username":username,
                    "password":password,
                    "body":f"Welcome {username}"}
            try:
                self.collection.insert_one(create_post)
                ans = self.account_exists(ID)
                if ans["_id"] == ID:
                    return "True"
            except:
                return "There is problem to add new id"

    def edit_data(self,ID,data):
        check = self.account_exists(ID)
        if check == None:
            return False
        else:
            try:
                self.collection.update_one({"_id":ID},{"$set":{"body":data}})
                if self.get_data(ID)==data:
                    return True
                else:
                    return False
            except:
                return "There was problem with edit data"

    def get_data(self,ID):
        check = self.account_exists(ID)
        if check == None:
            return "There is no user exists"
        else:
            return check["body"]

