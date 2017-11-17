# coding: utf-8
import sys,os
sys.path.append(os.pardir)
import touban as t

def touban():
    msg = t.m_print()
    #print -> slack.message
    print msg[0]
    print msg[1]
