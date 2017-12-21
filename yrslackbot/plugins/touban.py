# coding:utf-8
import os
#定期投稿用
def main():
    members = openmember()
    a = ""
    b = ""
    count = opennumber()
    for i in range(5):
        a += "[%d]%s " % (count[0],members[count[0]-1])
        count[0] += 1
        if count[0]==(len(members)+1):
            count[0] = 1
    for i in range(2):
        b += "[%d]%s " % (count[1],members[count[1]-1])
        count[1] += 1
        if count[1]==(len(members)+1):
            count[1] = 1
    #print -> slack.message
    Path = os.getcwd()
    os.remove(Path+"/plugins/num.txt")
    f = open(Path+"/plugins/num.txt","w")
    f.write(str(count[0]))
    f.write('\n')
    f.write(str(count[1]))
    f.close()

def openmember():
    Path = os.getcwd()
    f = open(Path+"/plugins/3j.txt","r")
    members = f.readlines()
    f.close()
    for i in range(len(members)):
        members[i] = members[i].replace('\n','')
        members[i] = members[i].replace('\r','')
    return members

def opennumber():
    Path = os.getcwd()
    f = open(Path+"/plugins/num.txt","r")
    num = f.readlines()
    f.close()
    for i in range(len(num)):
        num[i] = num[i].replace('\n','')
        num[i] = num[i].replace('\r','')
        num[i] = int(num[i])
    return num

#slackbot用
def m_print():
    members = openmember()
    a = ""
    b = ""
    count = opennumber()
    for i in range(5):
        a += "[%d]%s " % (count[0],members[count[0]-1])
        count[0] += 1
        if count[0]==(len(members)+1):
            count[0] = 1
    for i in range(2):
        b += "[%d]%s " % (count[1],members[count[1]-1])
        count[1] += 1
        if count[1]==(len(members)+1):
            count[1] = 1
    msg = [a,b]
    return msg
