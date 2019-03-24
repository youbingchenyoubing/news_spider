#coding=utf-8

import sys
import datetime
sys.path.append('..')

from news_mongodb.db_operation import MongoDBTempInterface
from news_spider.preprocess.preProcessItem import BasePreProcessItem
from news_spider.preprocess.update_settings import UpdateSettings
from news_spider.time_translation.time_operation import TimeOperate
from news_spider.spiders.Mail_2.myself_email import Email
from news_spider.spiders.Mail_2.myself_email import TextEmail
import setting_for_update


class UpdateLeftDB(UpdateSettings):

    def __init__(self):
        #self.mongodb_object = None
        try:
            self.timeobj = TimeOperate()
            self.filename = setting_for_update.update_log + str(self.timeobj.gettoday())
            self.mongodb_object = MongoDBTempInterface(setting_for_update.update_rate)
            #print "开始初始化"
            self.base_object = BasePreProcessItem()
            #print "初始化完整"

        except MemoryError,error:
            self.writeerrorlog(error)
        except BaseException,error:
            print error
    def begin_update(self):
        try:
            print "开始于:",datetime.datetime.now()
            page_number = 0 
            isBegin = True
            last_date = None
            cureent_date = None
            #dict_time = dict({})
            while True:
                negative_batch = []
                #postive_batch = []
                #print "load 数据,页数:",page_number

                data = self.mongodb_object.extractPagination(0)
                #print "four"
                if data == None or data.count(True) == 0:
                    break
                if isBegin:
                    min_date = data[0]['article_publish_time']
                    #print "mindate",min_date
                    dict_time = self.mongodb_object.getdicttime2(self.timeobj.str2date(min_date)) #第一页要去数据库选择当前日期和前一天日期的数据，爬完要改
                    isBegin = False

                    #print 'dict_time',dict_time
                for onedata in data:
                    #print 'onedata',onedata
                    
                    current_date = self.timeobj.str2date(onedata['article_publish_time'])
                    #print "当前日期:",current_date
                    if not last_date:
                        print "当前日期:",current_date  
                    if last_date != None and last_date != current_date: #说明有些日期的数据过期了
                        print "当前日期:",current_date
                        days = (current_date - last_date).days
                        #print "days=",days
                        if days != 1:

                            self.email_inform_time("爬虫数据日期少了，前一天是"+str(last_date)+",现在是日期是:"+ str(current_date),"请查看后台数据库是否漏爬")
                            return 
                        begin_date = self.timeobj.getthepreviousday(current_date,day_num = 2)
                        end_date = self.timeobj.getthepreviousday(last_date,day_num = 1)
                        while begin_date >= end_date:  #删除超过两天的数据，为了内存更稳定
                            

                            if dict_time.has_key(begin_date):
                                #print "删除日期:",begin_date
                                del dict_time[begin_date]
                            begin_date = self.timeobj.getthepreviousday(begin_date,day_num = 1)
                    begin_date = current_date
                  
                    self.base_object.preProcessData(onedata)
                    onedata['is_repeate'] = 0
                    #print dict_time[begin_date]
                    
                    #print "iterdate",iterdate
                    if dict_time.has_key(begin_date):
                        for onehash in dict_time[begin_date]: #计算与当天所有新闻的重复率
                            if onedata['is_repeate'] == 1:
                                break
                            onedata['is_repeate'] = self.base_object.similarity(onedata['simhash'],long(onehash))
                    #print begin_date
                    begin_date = self.timeobj.getthepreviousday(begin_date,day_num = 1)
                    #print begin_date
                    if dict_time.has_key(begin_date):
                        for onehash in dict_time[begin_date]: # 计算与前一天所有新闻的重复率
                            if onedata['is_repeate'] == 1:
                                break
                            onedata['is_repeate'] = self.base_object.similarity(onedata['simhash'],long(onehash))
                    #print 'current_date = ',current_date
                    if not dict_time.has_key(current_date): # 如果没有请声明

                        dict_time[current_date] = []
                    #print "dict_time"
                    #print 'long=',onedata['simhash']
                    onedata['simhash'] = str(onedata['simhash']) # 如果不转换的话就会导致 MongoDB can only handle up to 8-byte ints
                    #onedata['simhash'] = long(onedata['simhash'])
                    #print 'str=',onedata['simhash']
                    if  not onedata['simhash'] in  dict_time[current_date]:

                        dict_time[current_date].append(onedata['simhash'])
                    #print onedata['is_repeate']
                    onedata['article_label_state'] = 0
                    if setting_for_update.classifier_model == '': #没有模型，直接归为
                        onedata['article_label'] = 0
                        
                    else:
                        #模型预测
                        onedata['article_label'] = 1
                        pass
                    negative_batch.append(onedata)
                    #print "heloo"
                    onedata = {} #内存释放
                    last_date = current_date
                    #for one_artcile in
                    # cureent_date
                #print '更新.......'
                data.close() #关闭游标
                if self.mongodb_object.batchinsertnegative(negative_batch): #将处理完的数据分别写到相应的数据库中
                    if not self.mongodb_object.batchdelete(negative_batch): #删除数据
                        raise Exception("数据删除错误object_id:"+self.__gernator_info(negative_batch))
                # if self.mongodb_object.batchinsertpositive(postive_batch): # 2017年5月
                #     if not self.mongodb_object.batchdelete(postive_batch): #删除数据
                #         raise Exception("正例数据除错误object_id:"+self.__gernator_info(postive_batch))
                page_number = page_number + 1 # 下一页
                print '处理页数:',page_number
                #sleep()
            self.mongodb_object.removedata() # 清空原来数据库所有的数据
            print "结束于:",datetime.datetime.now()
            self.email_inform("成功更新数据库通知")
        except BaseException,error:
            #print str(__file__) + str(__line__) + str(error)
            self.writeerrorlog(error)
    def writeerrorlog(self,error):
        self.touchfile(self.filename)
        with open(self.filename,'a') as f:
            f.write(str(datetime.datetime.now())+':' + str(error)+'\n')
        self.email_inform("错误(ERROR!!!!)更新数据库通知")
    def email_inform_time(self,title,content):
        mail_object = TextEmail()

        mail_object.send_email(title,content)
    def email_inform(self,title):
    
        mail_object = Email(title,self.filename)

        mail_object.send_attachemail()
    def __gernator_info(self,data):

        info = ""
        for one_data in data:
            info = info + str(one_data['_id'])+'\n'
        return info

    def __del__(self):
        
        print "关闭数据库"
        self.mongodb_object.db_close()
        



       
if __name__ == '__main__':

    update_obj = UpdateLeftDB()
    #update_obj.testremove()
    #print '删除成功'
    update_obj.begin_update()


    del update_obj

