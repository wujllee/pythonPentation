# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:12:20 2019

@author: wujianling
"""

import requests
from threading import Thread
import sys
import getopt

def banner():
    print('\n**********************************')
    print('* ForzaBruta 1.0*')
    print('**********************************')

def usage():
    print("Usage:")
    print("\t-w: url (http://somesite.com/fuzz)")
    print("\t-t: threads")
    print("\t-f: dictionary file\n")
    print("example:forzabruta.py -w http://targetsite.com/fuzz -t 5 -f con.file")
    
class request_Performer(Thread):
    def __init__(self,word,url):
        Thread.__init__(self)
        try:
            self.word=word.split("\n")[0]
            self.urly=url.replace("FUZZ",self.word)
            self.url=self.urly
        except Exception, e :
            print(e)
    
    def run(self):
        try:
            r=requests.get(self.url)
            print(self.url+' - '+str(r.status_code))
            i[0]=i[0]-1 #here we remove one thread from the counter
        except Exception, e:
            print (e)
def start(argv):
    banner()
    if len(sys.argv)<5 :
        usage()
        sys.exit()
        
    try:
        opts,args=getopt.getopt(argv,"w:t:f:")
    except getopt.GetoptError:
        print("error in arguments.")
        sys.exit()
        
    for opt,arg in opts:
        if opt=='-w':
            url=arg
        elif opt=='-t':
            threads=arg
        elif opt=='-f':
            dic=arg
    try:
        f=open(dic,'r')
        words=f.readlines()
    except:
        print("Fail openning file :"+dic+'\n')
        sys.exit()
        
    launcher_thread(words,threads,url)
        
def launcher_thread(names,th,url):
    global i
    i=[]
    resultlist=[]
    i.append[0]
    while(len(names)):
        try:
            if i[0]<th:
                n=names.pop(0)
                i[0]=i[0]+1
                thread=request_Performer(n,url)
                thread.start()
        except KeyboardInterrupt:
            print("ForzaBruta interrupted by user,finishing attack...")
            sys.exit()
        thread.join()
    return
if __name__=="__main__":
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("ForzaBruta interrupted by user.killing all threads....")