# -*- coding: utf-8 -*-
#coding=utf-8
import myself_email
#from scrapy.utils.project import get_project_settings


if __name__ == '__main__':

    
    # settings['WRONG_FILE'] = '/home/chenyoubing/data/wrongLog/spider_wrong_file_2017-03-10'
    
    # settings['SUBJECT'] = '爬虫报错'

    # settings['MAIL_SEND_LIST'] = ["840704140@qq.com"]

    # mail_object = myself_email.TextEmail() #没带附件的邮件发送测试

    # mail_object.send_email('test','test')
    filename = '/home/developMent/data/update_log/update_log_2017-03-01'
    mail_object = myself_email.Email("数据更新通知",filename)


    mail_object.send_attachemail()

