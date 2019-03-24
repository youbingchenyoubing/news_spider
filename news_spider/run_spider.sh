# -*- coding: utf-8 -*-
#!/bin/bash
run_spider()
{

    # 爬虫
    cd /home/developMent/news_spider/news_spider

    python run_sina.py

    #python test_run_fenghuang.py

    # python run_spider.py

   
}
run_update()
{
    # 转换词向量、分类、计算重复率等
    cd /home/developMent/news_spider/news_update

    python run_update.py
}
run_backup()
{
   cd /home/developMent/news_spider/backup

   bash mount.sh #备份数据库
}
#检查硬盘的大小 
diskrate_home=$(df -h | grep '/dev/mapper/centos-home' | awk '{print $5}' | cut -d '%' -f 1)
diskrate_usr=$(df -h | grep '/dev/mapper/centos-usr' | awk '{print $5}' | cut -d '%' -f 1) 
backup_home=$(df -h | grep '/dev/sdb1' | awk '{print $5}' | cut -d '%' -f 1)
backup_usr=$(df -h | grep '/dev/sdc1' | awk '{print $5}' | cut -d '%' -f 1) 
#diskrate_home=$(df -h | grep '/home' | awk '{print $5}' | cut -d '%' -f 1)
#diskrate_usr=$(df -h | grep '/usr' | awk '{print $5}' | cut -d '%' -f 1) 
#echo $diskrate_home
if [[ $diskrate_home -gt 90 ||  $diskrate_usr -gt 90 || $backup_home -gt 90 || $backup_usr -gt 90 ]]
  then
   #echo "hello"
   cd /home/developMent/news_spider/news_spider/spiders/Mail_2
   information=$(df -h) 
   python inform_admin.py "恐怖新闻系统友情提请你" "你好,遗憾地告诉你硬盘快满了\n${information}"
fi

run_spider
#run_update
#run_backup
