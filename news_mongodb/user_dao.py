import pymongo
from bson import ObjectId
from models.user import User
from db_connection import MongoDBConnection

class UserDAO(object):
    def __init__(self):
        self.mongoDB = MongoDBConnection('user')
   
    def addUser(self, user):
        try:
            information = {"username":user.username, "password": user.password, "role":user.role}
            coll = self.mongoDB.dbConnection()
            coll.insert(information)
            self.mongoDB.dbClose()
            return True
        except:
            return False
         

    def isexist(self, user):
        coll = self.mongoDB.dbConnection()
        query_result = coll.find_one({"username":user.username})
        self.mongoDB.dbClose()
        if query_result:
            return True
        else:
            return False

    def login(self, user): 
        coll = self.mongoDB.dbConnection()
        query_result = coll.find_one({"username":user.username, 'password':user.password}) 
        print query_result
        self.mongoDB.dbClose()

        if query_result:
            query_result['_id'] = str(query_result['_id'])
            return query_result
        else:
            return None

    def userlist(self):
        coll = self.mongoDB.dbConnection()
        query_result = coll.find()
        self.mongoDB.dbClose()
        userList = []
        for item in query_result:
            item['_id'] = str(item['_id'])
            item['id'] = item['_id']
            #print item
            userList.append(item)
        return userList       

    def deluser(self, userId):
        coll = self.mongoDB.dbConnection()
        query_result = coll.remove({"_id":ObjectId(userId)}) 
        self.mongoDB.dbClose()
        return True
     


def test(): 
    userDAO = UserDAO()
    user = User()
    user.username = 'zjl'
    user.password = 'zjl'
    user.role = '0'
    #userDAO.addUser(user)
    #print userDAO.isexist(user)
    print userDAO.userlist()


#test()
