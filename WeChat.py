#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 11:00:54 2017

@author: no1
"""

import requests
import itchat
from itchat.content import *
import time
import random
KEYs = ['71f28bf79c820df10d39b4074345ef8c', '8edce3ce905a4c1dbb965e6b35c3834d']

def get_response(msg):
  apiUrl = 'http://www.tuling123.com/openapi/api'
  data = {
  'key' : random.choice(KEYs),
  'info' : msg,
  'userid' : 'wechat-robot',
  }
  try:
    r = requests.post(apiUrl, data=data).json()
    return r.get('text')
  except:
    return

@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def tuling_reply(msg):
  global t1,t2
  global robot
  defaultReply1 = '[主人不在，进入机器人模式]'
  defaultReply2 = '[机器人已将消息转告给主人]'
  reply = get_response(msg['Text'])


  if not msg['FromUserName'] == myUserName:
    itchat.send(u"[%s]收到好友@%s 的信息：%s\n" %
                          (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                           msg['User']['RemarkName'],
                           msg['Text']), 'filehelper')
  if msg['FromUserName'] == myUserName:
    if '退出' in msg['Text'] or msg['Text'] == '退出机器人模式':
      itchat.send('已退出机器人模式', 'filehelper')
      robot = False
    if msg['Text'] == '进入机器人模式' or '进入' in msg['Text']:
      itchat.send('已进入机器人模式', 'filehelper')
      robot = True

  try:
    if robot == False:

      pass
    elif robot == True:

      if '已用完' in reply:
        itchat.send(defaultReply2, msg['FromUserName'])
      else:
        itchat.send(defaultReply1+reply, msg['FromUserName'])
      return
  except:
      if '已用完' in reply:
        itchat.send(defaultReply2, msg['FromUserName'])
      else:
        itchat.send(defaultReply1+reply, msg['FromUserName'])

@itchat.msg_register([PICTURE,ATTACHMENT,VIDEO])
def download_files(msg):
  msg['Text'](msg['FileName'])
  if not msg['FromUserName'] == myUserName:
    itchat.send( '@%s@%s'%({'Picture':'img','Video':'vid'}.get(msg['Type'],'fil'),msg['FileName']),'filehelper')


itchat.auto_login(hotReload=True)
myUserName = itchat.get_friends(update=True)[0]["UserName"]

itchat.run()
