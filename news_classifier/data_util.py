# coding=utf-8
from db_connection import MongoDBConnection
from bson import ObjectId
import re
import random
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='news_classifier.log',
    filemode='a')

class DataUtil(object):
    def __init__(self, label):
        self.mongoDB = MongoDBConnection(label)


    def filter_data(self, data_list, label):
        new_datalist = []
        for data in data_list:
                newdata = {}
                newdata["processed_content"] =  self.del_unknowIndex(data['processed_content'])
                newdata["processed_title"] =  self.del_unknowIndex(data['processed_title'])
                newdata["label"] = label
                new_datalist.append(newdata)
        return new_datalist      
    
    def del_unknowIndex(self, enum):
        #过滤unknow的值
        news_list = []
        for x in enum:
            if x != 511001:
                news_list.append(x)
        return news_list
 
    def get_data(self):
        #获取所有的正例和负例
        try:
            logging.info("get_data()")
            coll = self.mongoDB.dbConnection()
            positive_data = coll.find({'article_label':1,'article_label_state':{'$gte':1}})
            pos_data = self.filter_data(positive_data, 1) 
            pos_length =  len(pos_data)
            logging.info("pos_length=[" + str(pos_length)+']')
            print "positive data num:", pos_length
            if pos_length == 0:
            	return []
           
            negative_data = coll.find({'article_label':0,'article_label_state':{'$gte':1}}).limit(pos_length) 
            neg_data = self.filter_data(negative_data, 0)
            self.mongoDB.dbClose()
            data = {}
            data['pos'] = pos_data
            data['neg'] = neg_data
            return data
        except BaseException, e:
            logging.error(e)
            return {}

    def transfer_form(self, data):
        # 将原来的数据格式转换为模型需要的数据类型
        processed_content = []
        processed_title = []
        label = [] 
        for enum in data:
            processed_content.append(enum["processed_content"])
            processed_title.append(enum["processed_title"])
            label.append(enum["label"])
        data = {}
        data["processed_content"] = processed_content
        data["processed_title"] = processed_title
        data["label"] = label
        return data
       
    def flod_cross_data(self, data):
        pos_data = data['pos']
        neg_data = data['neg']
        length = len(pos_data)
        indexs = range(length)
        random.shuffle(indexs)
        pos_data = [pos_data[i] for i in indexs]
        neg_data = [neg_data[i] for i in indexs]
     
        data_list = []
        for i in range(length):
            data_list.append(pos_data[i]) 
            data_list.append(neg_data[i]) 
        
 
        test_num = length / 5
        test_data = data_list[0:test_num]
        dev_data = data_list[test_num: 2*test_num]
        train_data = data_list[2*test_num:]
        logging.info("test_data num=" + str(len(test_data)))
        logging.info("dev_data num=" + str(len(dev_data)))
        logging.info("train_data num=" + str(len(train_data)))

        print "test:", len(test_data)
        print "dev_data:",len(dev_data)
        print "train_data:",len(train_data)
                                        
        test_data = self.transfer_form(test_data)
        dev_data = self.transfer_form(dev_data)
        train_data = self.transfer_form(train_data)

        new_data = {}
        new_data["test_data"] = test_data
        new_data["dev_data"] = dev_data
        new_data["train_data"] = train_data          
        return new_data


    def predict_preprecess(self, data):
        data = self.filter_data(data, -1)
        data = self.transfer_form(data)



#dataUtil = DataUtil("articles_testN")
#data = dataUtil.get_data()
#dataUtil.flod_cross_data(data)


