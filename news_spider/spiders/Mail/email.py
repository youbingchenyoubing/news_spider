# -*- coding: utf-8 -*-
#coding=utf-8

from scrapy.mail import MailSender
import datetime

def singleton(cls):

    instance = {}

    def wrapper(*args,**kwargs):

        if cls not in instance:

            instance[cls] = cls(*args,**kwargs)

        return instance[cls]
    return wrapper
@singleton
class Email(object):

    def __init__(self,settings = None,times = 1):


        

        self.settings = settings
        #self.sendtoMail = sendtoMail

        self.inform = False

        self.times = 0

        self.max_time = times

        




    def send_information(self,sendInformation,subject = '',boolAttach = False):

        try:
            self.boolAttach = boolAttach
            if subject == '':
                self.subject = self.settings['SUBJECT']
            else:
                self.subject = subject
                self.inform = False
            if self.inform == False:
                self.__real_send(sendInformation)
                self.inform = True
                self.times += 1

        except BaseException,error:

            date =  datetime.datetime.now()

            filename = self.settings['WRONG_FILE']

            with open(filename,'a') as f:
                f.write("邮件发送错误:"+ str(error))

    def __real_send(self,sendInformation):
        attach = []
        if self.boolAttach:
            f = open(self.settings['WRONG_FILE'],'rb')
            #f.read()
            attach = [
             ("wrong_file","text/plain",f)
            ]

            #print "添加附件"
        self.mailer = MailSender.from_settings(self.settings)
        self.mailer.send(to = self.settings['MAIL_SEND_LIST'],subject = self.subject, body = sendInformation, attachs = attach)
        #print "通知成功"
        
        if self.boolAttach:
            f.close()
