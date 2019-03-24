# -*- coding: utf-8 -*-
import os
import sys

import networkhost
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir))
from news_spider.mysetting.json_parse import JsonLoad
from ps.ps_stop import ProcessDeal
from news_spider.spiders.Mail_2.myself_email import morePeopleSend
from news_spider.time_translation.time_operation import TimeOperate
def check_time(configure):

    time_object = TimeOperate()
    firsttime = ''
    secondtime = time_object.getnow()
    try:

        firsttime = time_object.str2datetime(configure['last_info_time'])
       
    except:
       
        pass
    if firsttime == '' or time_object.difftimeminitue(firsttime,secondtime) > 60:
        configure['last_info_time'] = str(secondtime)
        return True
    return False

def send_Email(title,content):

    email_object = morePeopleSend()

    email_object.send_email(title,content)




if __name__ =='__main__':

    #读入配置文件
    
    config_obj = JsonLoad("./settings/monitor.json")

    configure = config_obj.getdata()


    # 开始
    monitor_host = networkhost.MonitorHost("host",configure)

    if monitor_host.run_ping():
        
        if configure['redundancy'] == 1:
            if check_time(configure):
                send_email("有一台机器死机通知",configure["redundancy_info"])
                config_obj.changejson("./settings/monitor.json")
        print("it is running")

    else:

        print("it not running")

        process_object = ProcessDeal(configure)

        process_object.run_process()
        if check_time(configure):
            send_email("断电关机通知",process_object.get_email_info())
            config_obj.changejson("./settings/monitor.json")
        process_object.shutdown()
        # time_object = TimeOperate()
        # firsttime = ''
        # secondtime = time_object.getnow()
        # try:
  
        #     firsttime = time_object.str2datetime(configure['last_info_time'])
           
        # except:
           
        #     pass
        # if firsttime == '' or time_object.difftimeminitue(firsttime,secondtime) > 60:

        #     email_object = morePeopleSend()
        
        #     email_object.send_email()
        
        #     configure['last_info_time'] = str(secondtime)
            
        



