# coding:utf-8


f = open ("/Users/sun-mba/develop/bot/3j.txt","r")
members = f.readlines()
for i in range(len(members)):
    members[i] = members[i].replace('\n','')
    members[i] = members[i].replace('\r','')

n = 5
while n < len(members):
    print ("[%d]%s,[%d]%s" % (n, members[n-1], n+1, members[n] ))
    n += 2
f.close()
