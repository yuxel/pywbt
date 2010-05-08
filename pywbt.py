#!/usr/bin/python

""" 
Python Web Benchark Tool

Example usage:

    debian:~/$ python pywbt.py -n 100 -c 30 http://google.com
     > Requests between  0 and 30  sent
     > Requests between  30 and 60  sent
     > Requests between  60 and 90  sent
     > Requests between  90 and 100  sent
     ------------------------------------------------- 
    Process took  0.990706205368 seconds ( 0.00990706205368  per/request)
    Number of succeeded requests  100
    Number of failed requests  0

Osman Yuksel <yuxel |ET| sonsuzdongu (DOT).com

"""

__appName__ = "Python Web Benchark Tool"
__version__ = '0.0.1'

from threading import Thread
from optparse import OptionParser
from urlparse import urlparse
import httplib, time, sys, math


class PyWBT:
    """ parse options and run threads """
    """ TODO: split into some methods """
    def __init__(self):
        options, args, urlData = self.parseOptions()

        numOfRequestBlocks = int(options.numberOfRequests / options.concurentRequestCount)
        numOfRequestsForLastBlock = (options.numberOfRequests % options.concurentRequestCount)

        startTime = time.time()
        requestSucceed = 0
        requestFailed = 0

        threadList = {}

        for requestBlock in range(0, numOfRequestBlocks + 1):
            
            threadList[requestBlock] = []

            concurentRequestCount = options.concurentRequestCount
                
            if requestBlock == numOfRequestBlocks :
                concurentRequestCount = numOfRequestsForLastBlock

            for count in range(0,concurentRequestCount):
                currentThread = PyWBThread(count, urlData)
                threadList[requestBlock].append(currentThread)
                currentThread.start()

            # join threads
            for thread in threadList[requestBlock]:
                try:
                    thread.join()
                    if thread.completed :
                        requestSucceed = requestSucceed + 1
                    else:
                        requestFailed = requestFailed + 1
                except Exception, error:
                    print error;

            startFrom = requestBlock * options.concurentRequestCount
            endTo = startFrom + concurentRequestCount
            print " > Requests between ", startFrom, "and", endTo ," sent"
       
        # end time tracker
        endTime = time.time()


        """ print results """
        totalRequstTime = endTime - startTime
        perRequst = totalRequstTime / options.numberOfRequests
        print " ------------------------------------------------- "
        
        print "Process took ", totalRequstTime , "seconds (", perRequst, " per/request)"
        print "Number of succeeded requests " , requestSucceed
        print "Number of failed requests " , requestFailed


    """ print usage and help """
    def parseOptions(self):
        usage = "usage: %prog -n numberOfRequests -c concurentRequestCount http://URL"
        parser = OptionParser(usage=usage, version=__appName__+" "+__version__)
        parser.add_option("-n", "--numberOfRequests", action="store", type="int", 
                          default=1, dest="numberOfRequests", help="input number of requests to URL")
        parser.add_option("-c", "--concurentRequestCount", action="store", type="int", 
                          default=1, dest="concurentRequestCount", help="input number of concurent requests")
        (options, args) = parser.parse_args()

        """ only one url """
        if len(args) != 1:
            parser.error('You have to specify a URL')
        else:
            """  check if url is valid 
                 TODO: bad """
            url = urlparse(args[0])
            if  url.scheme != "http":
                parser.error('You have to specify valid URL starts with http://')
            elif len(url.netloc) < 1:
                parser.error('You have to specify valid URL starts with http://')


        """ get url and query string """
        queryString = None
        if  url.path or url.params:
            queryString = url.path + "?" + url.params

        urlData = {"host": url.netloc,
                   "queryString" : queryString}
                   
        return options, args, urlData


""" Threads to send requests """
class PyWBThread(Thread):
    def __init__ (self,count, urlData):
        Thread.__init__(self)
        self.host = urlData['host']
        self.queryString = urlData['queryString']
        self.count = count
    def run(self):
        try:
            connection = httplib.HTTPConnection(self.host)
            connection.request("GET", self.queryString)
            response = connection.getresponse()
            connection.close()
            self.completed = True
        except Exception, error:
            self.completed = False


if __name__ == '__main__':
    PyWBT()

