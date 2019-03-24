# -*- coding: utf-8 -*-
import re
import sys
import socket
import datetime
import subprocess

from monitor import Monitor



class MonitorHost(Monitor):
    """Ping a host to make sure it's up"""

    host = ""
    ping_command = ""
    ping_regexp = ""
    type = "host"
    time_regexp = ""
    tolerance = 1
    def __init__(self, name, config_options):
        """
        Note: We use -w/-t on Windows/POSIX to limit the amount of time we wait to 5 seconds.
        This is to stop ping holding things up too much. A machine that can't ping back in <5s is
        a machine in trouble anyway, so should probably count as a failure.
        """
        Monitor.__init__(self, name, config_options)
        try:
            ping_ttl = config_options["ping_ttl"]
        except:
            ping_ttl = "5"
        ping_ms = ping_ttl * 1000
        platform = sys.platform
        if platform in ['win32', 'cygwin']:
            self.ping_command = "ping -n 1 -w " + str(ping_ms) + " %s"
            self.ping_regexp = "Reply from "
            self.time_regexp = "Average = (?P<ms>\d+)ms"
        elif platform.startswith('freebsd') or platform.startswith('darwin'):
            self.ping_command = "ping -c1 -t" + str(ping_ttl) + " %s"
            self.ping_regexp = "bytes from"
            self.time_regexp = "min/avg/max/stddev = [\d.]+/(?P<ms>[\d.]+)/"
        elif platform.startswith('linux'):
            self.ping_command = "ping -c1 -W" + str(ping_ttl) + " %s"
            self.ping_regexp = "bytes from"
            self.time_regexp = "min/avg/max/stddev = [\d.]+/(?P<ms>[\d.]+)/"
        else:
            RuntimeError("Don't know how to run ping on this platform, help!")

        try:
            host = config_options["host"]
        except:
            raise RuntimeError("Required configuration fields missing")
        if host == "":
            raise RuntimeError("missing hostname")
        self.host = host

        try:
            tolerance = config_options['tolerance']
        except: 
            print("Warning the tolerance fields unset, it will be set one")
        self.tolerance = tolerance
        self.config = config_options
        self.config['redundancy'] = 0
    def run_ping(self):
    
        for i in xrange(self.tolerance):
            print("%sth times to ping hosts" %(i+1))
            if self.__run():
                return True
        return False
    def __run(self):


        for one_host in self.host:
            if not self.__run_test(one_host):
                if not self.__run_test(self.host[0]):
                    return False
                else: #路由器ping的通但是对方机器ping不同，说明不是断电，而是当机 
                    self.config['redundancy'] = 1
                    return True
        return True
    def __run_test(self,one_host):
        r = re.compile(self.ping_regexp)
        r2 = re.compile(self.time_regexp)
        success = False
        pingtime = 0.0
        try:
            cmd = (self.ping_command % one_host).split(' ')

            output = subprocess.check_output(cmd)
            #print("output=",str(output))
            for line in str(output).split("\n"):
                matches = r.search(line)
                if matches:
                    success = True
                else:
                    matches = r2.search(line)
                    if matches:
                        pingtime = matches.group("ms")
        except Exception, e:
            self.record_fail(e)
            return False
        if success:
            if pingtime > 0:
                self.record_success("%sms" % pingtime)
            else:
                self.record_success()
            return True
        self.record_fail()
        return False

    def describe(self):
        """Explains what this instance is checking"""
        return "checking host %s is pingable" % self.host

    def get_params(self):
        return (self.host, )
        