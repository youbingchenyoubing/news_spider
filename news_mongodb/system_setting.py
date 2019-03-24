# coding=utf-8
from db_connection import MongoDBConnection
import logging
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='system_setting.log',
    filemode='a')

class SystemSetting:

    def __init__(self):
        self.mongoDB = MongoDBConnection("system_setting")

    def lock_model_training(self):
        # 模型训练的时候锁住，防止多次触发模型训练，导致内存、cpu占用过高
	try:
	    coll = self.mongoDB.dbConnection()
            result = coll.find_one({"key":"classifier_model_training_lock" }) 
	    if result is None:
                coll.insert({"key":"classifier_model_training_lock", "value":True})
	    else:
		coll.update({"key":"classifier_model_training_lock"}, \
		    		{"$set":{"value":True}})
	    self.mongoDB.dbClose()
	    return True
        except BaseException, e:
            logging.error(e)
            return False

    def islock_model_training(self):
    	# 判断是否锁定
    	try:
	    coll = self.mongoDB.dbConnection()
            result = coll.find_one({"key":"classifier_model_training_lock" }) 
            flag = False
            if result is None:
                flag =  False
            else:
	        flag = result["value"]
            self.mongoDB.dbClose()
            return flag
        except BaseException, e:
            logging.error(e)
            return False


    def unlock_model_training(self):
        # 解锁，使得后面可以再次训练模型，提升模型效率
	try:
	    coll = self.mongoDB.dbConnection()
            result = coll.find_one({"key":"classifier_model_training_lock" })  
            if result is None:
	        coll.insert({"key":"classifier_model_training_lock", "value":False})
	    else:
		coll.update({"key":"classifier_model_training_lock"},{"$set":{"value":False}})

            self.mongoDB.dbClose()
            return True
        except BaseException, e:
            logging.error(e)
            return False

    def put(self, key, value):
        try:
            coll = self.mongoDB.dbConnection()
            result = coll.find_one({"key":key})  
            if result is None:
                coll.insert({"key":key, "value":value})
            else:
                coll.update({"key":key},{"$set":{"value":value}})
                self.mongoDB.dbClose()
                return True
        except BaseException, e:
            logging.error(e)
            return False

    def get(self, key, defaultValue):
        try:
            coll = self.mongoDB.dbConnection()
            result = coll.find_one({"key":key})  
            if result is None:
                return defaultValue
            else:
                return result["value"]
        except BaseException, e:
            logging.error(e)
            return None



