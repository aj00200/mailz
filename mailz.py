#! /usr/bin/python2.6
import re
import time
import getpass
import poplib
import colorz
import subprocess
class quit(Exception):
    pass
def read(cmd):
    try:
        num=int(cmd[cmd.find(' '):])
        for line in messages[num-1].split('\n'):
            print line
            time.sleep(0.2)
            count+=1
    except:
        print('Error')
def scroll(cmd):
    num=int(cmd[cmd.find(' '):])
    try:
        for line in messages[num-1].split('\n'):
            subprocess.call(['clear'])
            print line
            i=raw_input('Press <enter> to scroll, or <q><enter> to exit')
            if i=='q':
                break
    except:
        print('Error')
        
def help(cmd):
    print '''
==Commands==
read <id>      -Read message with id, <id>
info <id>      -Get info about message with id, <id>
'''
def info(cmd):
    try:
        num=int(cmd[cmd.find(' '):])
        print '''
Info about message: %s
Sender: %s
Subject: %s
'''%(num,sender[num-1],subject[num-1])
    except:
        print('Error')
def quit(cmd):
    m.quit()
    raise quit()
def delete(cmd):
    num=int(cmd[cmd.find(' '):])
    m.dele(num)
uname=raw_input('Username: ')
passwd=getpass.getpass()
server=raw_input('POP Server: ')
port=raw_input('Port: ')
m=poplib.POP3_SSL(server,port)
m.user(uname)
m.pass_(passwd)
print '''
Downloading Messages From:
%s:%s
'''%(server,port)
print 'You have %s messages that take up %s Octets'%m.stat()
#total=len(m.list()[1])
list=m.list()[1]
total=len(list)
messages={}
subject={}
sender={}
for i in range(total):
    need_sender=True
    need_subject=True
    for line in m.retr(i+1)[1]: #This messages start at 1, not 0
        if line.find('From: ')!=-1 and need_sender:
            sender[i]=line[line.find(' '):]
            need_sender=False
        if line.find('Subject: ')!=-1 and need_subject:
            subject[i]=line[line.find(' '):]
            need_subject=False
        text=line.replace('<a ','LINK: ')
        text=re.sub('<*[^<>]*>','',text)
        try:
            messages[i]+=text+'\n'
        except:
            messages[i]=text+'\n'
while 1:
    cmd=raw_input('Enter a command: ')
    if cmd.find('help')!=-1:
        help(cmd)
    elif cmd.find('info')!=-1:
        info(cmd)
    elif cmd.find('read')!=-1:
        read(cmd)
    elif cmd.find('scroll')!=-1:
        scroll(cmd)
    elif cmd.find('delete')!=-1:
        delete(cmd)
    elif cmd.find('quit')!=-1:
        quit(cmd)
#for i in range(total):
#    for each in m.retr(i+1)[1]:
#        print each
    
