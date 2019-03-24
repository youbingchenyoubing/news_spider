

# -*- coding: utf-8 -*-
#coding=utf-8     
import datetime
import sys  
#import time
reload(sys)  
sys.setdefaultencoding('utf8')
def singleton(cls):

    instance = {}

    def wrapper(*args,**kwargs):

        if cls not in instance:

            instance[cls] = cls(*args,**kwargs)

        return instance[cls]
    return wrapper

@singleton
class TimeOperate(object):

    def __init__(self):

        self.today = datetime.date.today()

    def getyesterdaydate(self):

        #today = datetime.date.today()

        oneday = datetime.timedelta(days = 1)

        yesterday = self.today - oneday

        return yesterday

    def gettoday(self):
        

        return  self.today


    def str2date(self,timestr):
        return datetime.datetime.strptime(timestr,'%Y-%m-%d').date()

    def getthepreviousday(self,the_date,day_num = 1): 

        #year,month,day = self.getyearmonthday(the_date)

        # datetime include date and time
        the_date = datetime.date(the_date.year,the_date.month,the_date.day)

        one_day = datetime.timedelta(days = day_num)

        return  (the_date-one_day)
    def getthefutureday(self,the_date,day_num = 1):

        the_date = datetime.date(the_date.year,the_date.month,the_date.day)

        one_day = datetime.timedelta( days = day_num)

        return (the_date + one_day)

    def getyear(self,the_date):

        return  str(the_date.year)


    def getmonth(self,the_date):

        month = the_date.month
        if month < 10:

            return '0' + str(month)
        else:
            return str(month)

    def getday(self,the_date):

        day = the_date.day

        if day < 10:

            return '0' + str(day)

        else:
            return str(day)
    def difftime(self,firstday,seconday):

        firsta = datetime.date(firstday.year,firstday.month,firstday.day)

        secondb = datetime.date(seconday.year,seconday.month,seconday.day)

        return (firsta - secondb).days
    def getnow(self):

        return datetime.datetime.now()

    def __formattime(self,onetime):

        return datetime.datetime(onetime.year,onetime.month,onetime.day,onetime.hour,onetime.minute,onetime.second)
    def difftimeminitue(self,firsttime,secondtime):
        #firsttime = self.__formattime(firsttime)
        #secondtime = self.__formattime(secondtime)
        #print "firsttime=",firsttime
        #print "secondtime=",secondtime
        #print "result=",(secondtime-firsttime).seconds/60
        return (secondtime-firsttime).seconds/60
    def str2datetime(self,onetime):
        
        return datetime.datetime.strptime(onetime,"%Y-%m-%d %H:%M:%S.%f")

    def difftidays(self,firsttime,secondtime):

        return (secondtime-firsttime).seconds/60/24







