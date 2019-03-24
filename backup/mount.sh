# -*- coding: utf-8 -*-
#!/bin/bash
targetPath='/mnt/mongodb'
targetlog="/mnt/mongodb/log"
diskrate_home=$(df -h | grep '/dev/mapper/centos-home' | awk '{print $5}' | cut -d '%' -f 1)
diskrate_usr=$(df -h | grep '/dev/mapper/centos-usr' | awk '{print $5}' | cut -d '%' -f 1) 
backup_home=$(df -h | grep '/dev/sdb1' | awk '{print $5}' | cut -d '%' -f 1)
backup_usr=$(df -h | grep '/dev/sdc1' | awk '{print $5}' | cut -d '%' -f 1) 

#:echo $backup_mongo
#判断本机磁盘是否快满了
if [[ $diskrate_home -gt 90 ||  $diskrate_usr -gt 90 || $backup_home -gt 90 || $backup_usr -gt 90 ]]
  then
   #echo "hello"
   cd /home/developMent/news_spider/news_spider/spiders/Mail_2
   information=$(df -h) 
   python inform_admin.py "恐怖新闻系统友情提请你" "你好,遗憾地告诉你硬盘快满了\n${information}"
fi
if ps -ef | grep rpcbind | egrep -v grep > /dev/null
then
    echo "rpc already running"
else
    systemctl start rpcbind.service
    if [ "$?" -ne 0 ]
    then 
        echo "rpc service strart error"
        cd /home/developMent/news_spider/news_spider/spiders/Mail_2
        python inform_admin.py "恐怖新闻系统友情提示你" "你好,服务器开启rpc服务失败"
        exit 1
    fi
fi

if [ -d ${targetPath} ]
then 
    echo "directory ${targetPath} already exits"
else
    mkdir -p ${targetPath}

    if [ "$?" -ne 0 ]
    then
       echo "create mount directory error"
       cd /home/developMent/news_spider/news_spider/spiders/Mail_2
       python inform_admin.py "恐怖新闻系统友情提请你" "你好,创建挂载文件目录错误"
       exit 1
    fi
fi

if df -h | grep ${targetPath} |  egrep -v grep > /dev/null
then 
     echo "remote disk already mounted"
else
     
    mount -t nfs 210.34.216.233:/volume1/mongodb ${targetPath} -o nolock,nfsvers=3,vers=3
     
    if [ "$?" -ne 0 ]
    then 
       echo "mount 210.34.216.233:/volume1/mongodb error"
       cd /home/developMent/news_spider/news_spider/spiders/Mail_2
       python inform_admin.py "恐怖新闻系统友情提示你" "你好,挂载远程硬盘出现错误"
       exit 1
    fi
fi

# 挂载完毕，开始增量备份,使用的工具是mongobackup
backup_mongo=$(df -h | grep ${targetPath} | awk '{print $5}' | cut -d '%' -f 1)
backtime=$(date +%Y%m%d%H%M)
startback_db3()
{
  dbPath="/disk/home/data/db"
  cp -r ${dbPath} ${targetPath}/${backtime} # 直接拷贝
}
startback_db2() 
{
  #实现全量备份
 /usr/local/mongodb/bin/mongodump -h 127.0.0.1 --port 27017 -d news_spider_db -o ${targetPath}/${backtime}
}
startback_db()
{
#实现增量备份
/usr/local/mongodb/bin/mongobackup --port 27017 -h 127.0.0.1 -d news_spider_db -o ${targetPath}/${backtime} --backup
}
startback_log()
{
   # 日志备份函数
  dblog=$1
  targetlogPath=$2
  if [ ! -d "${targetlogPath}/${backtime}/" ]
  then

    mkdir -p  ${targetlogPath}/${backtime}
    if [ "$?" -ne 0 ]
    then
       echo "create directory ${targetlogPath}/${backtime} failed!!!"
       cd /home/developMent/news_spider/news_spider/spiders/Mail_2
       python inform_admin.py "恐怖新闻系统友情提示你" "你好,创建目录失败:${targetlogPath}/${backtime}"
       exit 1
    fi
  fi
  cp -r ${dblog} ${targetlogPath}/${backtime}
  if [ "$?" -ne 0 ]
  then
        cd /home/developMent/news_spider/news_spider/spiders/Mail_2
     python inform_admin.py "恐怖新闻系统友情提示你" "数据库日志拷贝失败:${backtime}"
  else
  if ps -ef | grep news_spider.sh | egrep -v grep > /dev/null
    then
     echo "don't delete"
  else
  rm -f ${dblog}/*
  fi
fi
}
delete_backup_days()
{
  days=2
  #nowtime=$( date -d $)
  lastday=$( date -d ${backtime} --date="-${days} day" +%Y%m%d%H%M) #几天之前
  for i in `ls ${targetPath}`
  do
  #echo ${i}
  #temp_date=$( date -d ${i} +%Y%m%d%H%M)
  if [ ${i} -lt ${lastday} ]
    then
    #echo temp_date
    rm -rf ${targetPath}/${i}
    rm -rf ${targetlog}/${i}
  fi
  done
  #earlyday=${earlyday:0:16}
  
}
delete_backup_months()
{
  months=$1

  lastday=$(date -d ${backtime} --date="-${months} month" +%Y%m%d%H%M )
  for i in `ls ${targetPath}`
  do
  #echo ${i}
  #temp_date=$( date -d ${i} +%Y%m%d%H%M)
  if [ ${i} -le ${lastday} ]
    then
    echo "delete the backup ${1}"
    rm -rf ${targetPath}/${i}
    rm -rf ${targetlog}/${i}
  fi
  done
}
execute()
{
   if [  $backup_mongo -gt 90 ]
   then
   delete_backup_months 1 #删除一个月前的备份
   fi
   startTime=$(date +%s%N)
   start_ms=${startTime:0:16} 

   startback_db3
   if [ "$?" -ne 0 ]
   then
     echo "backup filed,time:${backtime}!!!"
     cd /home/developMent/news_spider/news_spider/spiders/Mail_2
     python inform_admin.py "恐怖新闻系统友情提示你" "你好，备份失败,时间:${backtime}"

   else
    delete_backup_months 6  #删除六个月前的备份
    endTime=$(date +%s%N)
    end_ms=${endTime:0:16}
    cost_time= ${end_ms}-${start_ms}
    cost_time= ${start_ms}/1000000
     echo "backup sucessfully, time:${backtime},costTime:${cost_time}"  
   fi
}

executelog()
{
startback_log "/home/developMent/data/dbLog" ${targetlog}
startback_log "/home/developMent/data/spiderLog"  ${targetlog}
startback_log "/home/developMent/data/update_log" ${targetlog}
startback_log "/home/developMent/data/wrongLog"  ${targetlog}
}
if [ ! -d "${targetPath}/${backtime}/" ]
then

    mkdir ${targetPath}/${backtime}
    if [ "$?" -ne 0 ]
    then
       echo "create directory ${targetPath}/${backtime} failed!!!"
       cd /home/developMent/news_spider/news_spider/spiders/Mail_2
       python inform_admin.py "恐怖新闻系统友情提示你" "你好,创建目录失败:${targetPath}/${backtime}"

    
    fi
fi

execute
executelog
#delete_backup_months 1 
