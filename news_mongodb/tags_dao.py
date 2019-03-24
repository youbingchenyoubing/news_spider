# coding=utf-8
from db_connection import MongoDBConnection
import logging
from bson import ObjectId

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='news_web.log',
    filemode='a')


class TagsDAO(object):
    def __init__(self):
	self.mongoDB = MongoDBConnection('articles_tags')
	pass

    def addTag(self, tag):
	try:
	    if self.find(tag):
		return True
	    information = {"tag":tag}
	    coll = self.mongoDB.dbConnection()
	    coll.insert(information)
	    self.mongoDB.dbClose()
	    return True
	except BaseException, e:
	    logging.error(e)
	    return False

    def delTag(self, tagId):
	try:
	    coll = self.mongoDB.dbConnection()
	    coll.remove({"_id":ObjectId(tagId)}) 
	    self.mongoDB.dbClose()
	    return True
	except BaseException, e:
	    logging.error(e)
	    return False    

    def find(sef, tag):
	try:
	    information = {"tag":tag}
	    coll = self.mongoDB.dbConnection()
            result = coll.find_one(information)
            self.mongoDB.dbClose()
            if result:
                return True
            else:
	        return False
	except BaseException, e:
	    logging.error(e)
	    return False   

    def tagList(self):
	try:
	    coll = self.mongoDB.dbConnection()
            query_result = coll.find()
	    self.mongoDB.dbClose()
	    tagList = []
	    for item in query_result:
	    	item['_id'] = str(item['_id'])
	    	item['id'] = item['_id']
	        tagList.append(item)
            return tagList       
	except BaseException, e:
	    logging.error("[tagList]"+e)
	    return None


		
