# -*- coding: utf-8 -*-

import os

class ProcessDeal(object):



    def __init__(self,configure):

   
        self.configure = configure
        
        self.email_info = self.configure['email_info']
    

    def run_process(self):
        try:
            for one_process in self.configure['program']:
                self.__process_exit(one_process)
        except:
            RuntimeError("the fileds missing")
    def __process_exit(self,process_name):

        p_checkresp = os.popen('ps aux | grep "' + process_name + '" | grep -v grep').readlines()

        if len(p_checkresp) > 0 :

            try:
                if 'command' in self.configure['program'][process_name]:
                    self.__exit_command(process_name)
                if 'email' in self.configure['program'][process_name]:
                    
                    self.email_info = self.email_info + '\n' +  self.configure['program'][process_name]['email']
            except:

               pass
            
    def __exit_command(self,process_name):
        
        os.popen(self.configure['program'][process_name]["command"])

    def get_email_info(self):

        return self.email_info

    def shutdown(self):
        try:
            minutes = self.configure['time']
        except:
            minutes = 0
        finally:
            os.system("shutdown -h +"+ str(minutes))


        




        











