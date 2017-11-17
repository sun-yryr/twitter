# coding: utf-8
import sys,os
sys.path.append(os.pardir)
import touban as t

def touban(a):
    msg = t.m_print()
    #print -> slack.message
    if a==0:
        return msg[0]
    else:
        return msg[1]
