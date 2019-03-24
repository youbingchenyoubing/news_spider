# coding=utf-8
import logging
from data_util import DataUtil
import os
import numpy as np
import util as ut
from keras.optimizers import Adagrad
from evaluate import dr_evaluate
import sys
from keras.models import Sequential
from keras.preprocessing import sequence
from keras.layers import Dense, Dropout, Embedding, Merge, MaxPooling1D, Convolution1D, Flatten
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='train_classifier.log',
    filemode='a')

wordVec_path = os.path.join(os.path.dirname(__file__),os.pardir)
sys.path.append(wordVec_path)

from news_spider.preprocess.word2Vec import Word2Vector
from news_mongodb.system_setting import SystemSetting

class Classifier():
    def __init__(self):
    	self.title_max_len =  20
        self.content_max_len = 150
        self.batch_size = 32
        self.flods =  10
        self.epochs = 15
        self.system_setting = SystemSetting()


    def train(self):
        self.system_setting.unlock_model_training()
    	if self.system_setting.islock_model_training():
    		logging.warn("model training  is locked.!!!")
    		return

    	try:

    	    self.system_setting.lock_model_training()
    	    logging.info("model training locked.....")
    	    # 训练模型
    	    logging.info("********************************")
    	    logging.info("training classifier...........")
            dataUtil = DataUtil("articles_testN")
            origin_data = dataUtil.get_data()
            if origin_data is None:
            	logging.warn("training data is NULL!!!")
            	return

            wordVec = Word2Vector()
            embeddings = np.array(wordVec.embeddings)
            adam = Adagrad(lr=0.01, epsilon=1e-06)
            bestF = 0
            bestAcc = 0
            bestPre = 0
            bestRecall = 0

	    for flod in range(self.flods):
	        # 10 折中选出一个最好的
	        model = self.model(embeddings)
	        model.compile(loss='binary_crossentropy',metrics=[ut.f_score], optimizer=adam)

	        data = dataUtil.flod_cross_data(origin_data)  
                test_data = data["test_data"]
                dev_data = data["dev_data"]
	        train_data = data["train_data"]
	        test_data["processed_content"] = sequence.pad_sequences(test_data['processed_content'],\
	               maxlen=self.content_max_len,  padding='post', truncating='post')
	        dev_data["processed_content"] = sequence.pad_sequences(dev_data["processed_content"], \
	        	    maxlen=self.content_max_len, padding='post', truncating='post')
	        train_data["processed_content"] = sequence.pad_sequences(train_data["processed_content"],\
	                 maxlen=self.content_max_len, padding='post', truncating='post')


	        test_data["processed_title"] = sequence.pad_sequences(test_data['processed_title'],\
	    	 	     maxlen=self.title_max_len,  padding='post', truncating='post')
	        dev_data["processed_title"] = sequence.pad_sequences(dev_data["processed_title"], \
	        	    maxlen=self.title_max_len, padding='post', truncating='post')
	        train_data["processed_title"] = sequence.pad_sequences(train_data["processed_title"],\
                maxlen=self.title_max_len, padding='post', truncating='post')
                model = self.do_train(model, train_data, dev_data, test_data)
	        result = model.predict_classes([test_data["processed_content"], test_data["processed_title"]], batch_size=self.batch_size, verbose=1)
	        f_measure, pre, recall, acc = dr_evaluate(test_data["label"], result)
	        logging.info("***********")
	        logging.info("[flod] "+str(flod) + '] test F-measure:' + str(f_measure) +" test acc:" + str(acc))
	        logging.info("***********")
	        if bestF < f_measure:
	            bestF = f_measure 
	            bestAcc = acc
	            bestPre = pre
	            bestRecall = recall
	            model.save_weights('cnn_model.h5')


	    model = self.model(embeddings)
	    model.compile(loss='binary_crossentropy',metrics=[ut.f_score], optimizer=adam)
            model.load_weights('cnn_model.h5')
            model.save_weights('news_classifier_model.h5')

	    logging.info("###")
	    logging.info('[** best result **] best F-measure:' + str(f_measure) +" best acc:" + str(acc))
	    logging.info("###")	
	    logging.info("********************************")
        except BaseException, e:
            logging.error(e)
        finally:
        	self.system_setting.unlock_model_training()
        	logging.info("model training unlocked.....")
            
        
    
    def do_train(self, model, train_data, dev_data, test_data):
    	# 真正执行模型训练
        devBestTestF = 0
    	for each in range(self.epochs):
            model.fit([train_data["processed_content"], train_data["processed_title"]], train_data["label"], \
        	    batch_size = self.batch_size, nb_epoch = 1, 
        	    validation_data=([dev_data["processed_content"], dev_data["processed_title"]], dev_data["label"]))
            devResult = model.predict_classes([dev_data["processed_content"], dev_data["processed_title"]], batch_size=self.batch_size, verbose=1)
            df_measure, dpre, drecall, dacc =dr_evaluate(dev_data["label"], devResult)
            logging.info("["+str(each) + '] dev F-measure:' + str(df_measure) +"  dev acc:" + str(dacc))
            if devBestTestF < df_measure:
            	devBestTestF = df_measure
            	logging.info("[** dev best **]["+str(each) + '] dev F-measure:' + str(df_measure) +"  dev acc:" + str(dacc))
                model.save_weights('cnn_model.temp.h5')

        model.load_weights('cnn_model.temp.h5')
        return model

   
    def model(self, wordVec):
        embedding_size = 511002
        wordDim = 50
        nb_filter = 50
        filter_length = 5
        pool_length = 20
        titile_pool_length = 2

        centent_part = Sequential()
        centent_part.add(Embedding(embedding_size, output_dim = wordDim, input_length = self.content_max_len,
           weights = [wordVec], mask_zero = False, name = 'embeddings1'))
        centent_part.add(Convolution1D(nb_filter = nb_filter, filter_length = filter_length, border_mode = 'full', activation = 'relu', subsample_length = 1))
        centent_part.add(MaxPooling1D(pool_length = pool_length))
        centent_part.add(Dropout(0.5))
        centent_part.add(Flatten())
 
        title_part = Sequential()
        title_part.add(Embedding(embedding_size, output_dim = wordDim, input_length = self.title_max_len,
           weights = [wordVec], mask_zero = False, name = 'embeddings2'))
        title_part.add(Convolution1D(nb_filter = nb_filter, filter_length = filter_length, border_mode = 'full', activation = 'relu', subsample_length = 1))
        title_part.add(MaxPooling1D(pool_length = titile_pool_length))
        title_part.add(Dropout(0.5))
        title_part.add(Flatten())
        
        merged = Merge([centent_part, title_part], mode = 'concat')
        cnn_model = Sequential()
        cnn_model.add(merged)
        #cnn_model.add(Flatten())
        cnn_model.add(Dropout(0.5))
        cnn_model.add(Dense(128, activation = 'relu'))
        cnn_model.add(Dropout(0.5))
        cnn_model.add(Dense(1, activation = 'sigmoid'))
        return cnn_model



    def predict(self, data):
	logging.info("predict data....")
    	# data 必须是个list 
    	if type(data) is not list:
    	    logging.error("data's type is not list.")
    	    raise Exception("data's type is not list.")

    	if len(data) == 0:
    	    logging.error("num of data is 0!")
    	    raise Exception("num of data is 0!")


    	if os.path.exists('news_classifier_model.h5') == False:
	    logging.info("news_classifier model is not exists!")
            self.train()
        
        wordVec = Word2Vector()
        embeddings = np.array(wordVec.embeddings) 
        model = self.model(embeddings)
        adam = Adagrad(lr=0.01, epsilon=1e-06)
        model.compile(loss='binary_crossentropy',metrics=[ut.f_score], optimizer=adam)
        model.load_weights('news_classifier_model.h5')
        dataUtil = DataUtil("articles_testN")
        pre_data = dataUtil.filter_data(data, 1)
        pre_data = dataUtil.transfer_form(pre_data)
        pre_data["processed_content"] = sequence.pad_sequences(pre_data['processed_content'],\
               maxlen=self.content_max_len,  padding='post', truncating='post')
        pre_data["processed_title"] = sequence.pad_sequences(pre_data['processed_title'],\
    	 	maxlen=self.title_max_len,  padding='post', truncating='post')
        result = model.predict_classes([pre_data["processed_content"], \
        	pre_data["processed_title"]], batch_size=self.batch_size, verbose=1)

        #count = 0
        for i in range(len(data)):
            data[i]["artitle_label"] = result[i][0]
        return data

            
	    

	   



classifier = Classifier()
dataUtil = DataUtil("articles_testN")
origin_data = dataUtil.get_data()
classifier.predict(origin_data['neg'])



