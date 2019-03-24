# -*- coding: utf-8 -*-
#coding=utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os



def singleton(cls):

    instance = {}

    def wrapper(*args,**kwargs):

        if cls not in instance:

            instance[cls] = cls(*args,**kwargs)

        return instance[cls]
    return wrapper
@singleton
class Email(object):  # 带邮件发送

    def __init__(self,subject = '',attachs = ''):

        try:
            self.filename = attachs
            if attachs =='' or (not os.path.exists(self.filename)):
                self.send_txtemail(subject + "无日志附件")
                return
                  
            
            self.msg = MIMEMultipart('information') #创建一个带附件的实例

            self.msg['To'] = '840704140@qq.com'

            self.msg['From'] = 'news_spider@sina.com'

            self.msg['Subject'] =  subject

        except BaseException,error:

            self.send_txtemail(str(error))

   


    def send_attachemail(self):

        try:
            if self.filename == '' or (not os.path.exists(self.filename)):
                self.send_txtemail(self.msg['Subject']+"无日志附件")
                return

            #构建附件
            data = open(self.filename,'rb')
            attach = MIMEText(data.read(),'base64','utf-8')
            data.close()
            attach['Content-Type'] = 'application/octet-stream'

            attach['Content-Disposition'] = 'attachment; filename="update_log.txt"'


            self.msg.attach(attach)

            server = smtplib.SMTP()
        
            server.connect('smtp.sina.com',25)

            server.login(self.msg['From'],'zhengjianglong')

            #print "send"
            server.sendmail(self.msg['From'],self.msg['To'],self.msg.as_string())
            #print "send over"
            server.quit()

        except BaseException,error:

            self.send_txtemail(str(error))









    def send_txtemail(self,information):

        textemail_object = TextEmail()

        textemail_object.send_email("带附件邮件发送失败",information)



@singleton
class TextEmail(object): # 文本邮件发送

    def __init__(self):

        self.mailto_list = "840704140@qq.com"

        self.mail_host = "smtp.sina.com"

        self.mail_user = "news_spider@sina.com"

        self.mail_password = "zhengjianglong"

        self.mail_postfix = "sina.com" #发信箱后缀
    def send_email(self,subject,content):

        try:
            #me = "恐怖新闻系统通知" + "<" + self.mail_user + "@" + self.mail_postfix + ">"

            msg = MIMEText(content,_subtype = 'plain',_charset = 'utf-8')

            msg['Subject'] = subject

            msg['From'] = self.mail_user

            msg['To'] = self.mailto_list

            server = smtplib.SMTP()
            server.connect(self.mail_host,25)
            server.login(self.mail_user,self.mail_password)
            server.sendmail(self.mail_user,self.mailto_list,msg.as_string())
            server.close()

        except BaseException,error:

            print str(error)

@singleton
class morePeopleSend(object):

    def __init__(self):

        self.mailto_list = ["840704140@qq.com"]

        self.mail_host = "smtp.sina.com"

        self.mail_user = "news_spider@sina.com"

        self.mail_password = "zhengjianglong"
        #self.mail_password = "zjl123"

        self.mail_postfix = "sina.com" #发信箱后缀

    def send_email(self,subject,content,receive=[]):

        for one_person in self.mailto_list:

            self.__send_email(subject,content,one_person)
        for one_person in receive:

            self.__send_email(subject,content,one_person)

    def __send_email(self,subject,content,one_person):

        try:
            #me = "恐怖新闻系统通知" + "<" + self.mail_user + "@" + self.mail_postfix + ">"

            msg = MIMEText(content,_subtype = 'plain',_charset = 'utf-8')

            msg['Subject'] = subject

            msg['From'] = self.mail_user

            msg['To'] = one_person

            server = smtplib.SMTP()
            server.connect(self.mail_host,25)
            server.login(self.mail_user,self.mail_password)
            server.sendmail(self.mail_user,one_person,msg.as_string())
            server.close()

        except BaseException,error:

            print str(error)



    
     



