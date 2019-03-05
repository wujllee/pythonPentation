# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:12:20 2019

@author: wujianling
"""

import requests
from threading import Thread
import sys
import getopt
import re
from termcolor import  colored


def banner():
    print('\n**********************************')
    print('* ForzaBruta 1.0*')
    print('**********************************')

def usage():
    print("Usage:")
    print("\t-w: url (http://somesite.com/fuzz)")
    print("\t-t: threads")
    print("\t-f: dictionary file\n")
    print("\t-c: hidecode\n")
    print("example:forzabruta.py -w http://targetsite.com/fuzz -t 5 -f con.file")
    
class request_Performer(Thread):
    '''
    Thread: thread,handle one word in dictionary
    '''
    def __init__(self,word,url,hidecode):
        Thread.__init__(self)
        try:
            self.word=word.split("\n")[0]
            self.urly=url.replace("FUZZ",self.word)
            self.url=self.urly
            self.hidecode=hidecode
        except Exception as e:
            print(e)
    
    def run(self):
        '''
        be careful the usage of try-except in python 3.0 above:
        for python 2.x:
            try:
                ....
            :except Exception, e:
                ...
        for python 3.x:
            try:
                ....
            :except Exception as e:
                ...
        otherwise, you will get a syntax error that causes a crash of your program
        '''
        try:
            r=requests.get(self.url)
            lines=str(str(r.content).count('\\n'))#r.content is a bytes object, use count method may cause typeError,pls converse it to string objects first
            chars=str(len(r._content))

            words=str(len(re.findall("\S+",str(r.content))))#r.content is a bytes object, use count method may cause typeError,pls converse it to string objects first
            code=str(r.status_code)

            if self.hidecode!=code:
                if '200'<=code<'300':
                    print(colored(code,'green')+'    \t\t'+chars+'    \t\t'+lines+'    \t\t'+words+'    \t\t'+self.url)
                elif '300'<=code<'400':
                    print(colored(code, 'blue') + '    \t\t' + chars+'    \t\t'+lines+'    \t\t'+words+'    \t\t'+self.url)
                elif '400' <= code < '500':
                    print(colored(code, 'red') + '    \t\t' + chars+'    \t\t'+lines+'    \t\t'+words+'    \t\t'+self.url)
                else :
                    print(colored(code, 'yellow') + '    \t\t' + chars+'    \t\t'+lines+'    \t\t'+words+'    \t\t'+self.url)
            else:
                pass
            i[0]=i[0]-1 #here we remove one thread from the counter
        except Exception as e:
            print (e)
            sys.exit()
def start(argv):
    banner()
    if len(sys.argv)<5 :
        usage()
        sys.exit()
        
    try:
        opts,args=getopt.getopt(argv,"w:t:f:C:")
    except getopt.GetoptError:
        print("error in arguments.")
        sys.exit()
        
    hidecode='000'

    for opt,arg in opts:
        if opt=='-w':
            url=arg
        elif opt=='-t':
            threads=int(arg) #remember to do type conversion, or you'll get type error later
        elif opt=='-f':
            dic=arg
        elif opt=='-c':
            hidecode=arg
    try:
        f=open(dic,'r')
        words=f.readlines()
    except:
        print("Fail openning file :"+dic+'\n')
        sys.exit()
        
    launcher_thread(words,threads,url,hidecode)
        
def launcher_thread(names,th,url,hidecode):
    global i
    i=[]
    resultlist=[]
    i.append(0)
    while(len(names)):
        try:
            if i[0]<th:
                n=names.pop(0)
                i[0]=i[0]+1
                thread=request_Performer(n,url,hidecode)
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