from flask import Flask, request,jsonify
from flask_pymongo import PyMongo
from linebot.exceptions import LineBotApiError
from linebot.models import *
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)
from datetime import datetime
#from flask_cors import CORS,cross_origin
#from wsgiref.simple_server import make_server, demo_app
from flask import Flask, request, abort
import requests
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['MONGO_URI'] = ()
mongo = PyMongo(app)

myCollection_track = mongo.db.track
myCollection_user = mongo.db.user



#don't forget to delete token
line_bot_api = LineBotApi(<line_token>)




def create_rich_menu(image):
    rich_menu = RichMenu()
    rich_menu.size = {'width':1920,'height':1080}
    rich_menu.selected = False
    rich_menu.chatBarText = "Test_Chat_bar"
    rich_menu.name = "Test_Menu_Name"
    arealist = []

    #create area rich menu1
    ar = RichMenuArea()
    ACTION = Action()
    #ACTION.type = 'uri'
    #ACTION.uri = "https://www.youtube.com/watch?v=kvEHNOr4EFs"
    ACTION.type= 'message'
    #setuptext = open("setupguide.txt","r").read()
    ACTION.text="!lock_my_box"
    ar.action= ACTION
    #ar.bounds = RichMenuArea(1980,1080)
    ar.bounds = {"x":0,"y":0,"width":1920/2,"height":1080}
    arealist.append(ar)

    #create  are another rich menu2
    ar2 = RichMenuArea()
    ACTION2 = Action()
    #ACTION2.type = 'uri'
    #ACTION2.uri = 'https://www.youtube.com/watch?v=gVZyDJDbXMQ'
    ACTION2.type= 'message'
    #setuptext = open("setupguide.txt","r").read()
    ACTION2.text="!unlock_my_box"
    ar2.action = ACTION2
    ar2.bounds = {"x":1920/2,"y":0,"width":1920/2,"height":1080}
    arealist.append(ar2)
    
    #create rich menu 
    rich_menu.areas = arealist
    menuId=line_bot_api.create_rich_menu(rich_menu)
    contentType = 'image/jpeg' #insert image
    img = open(image,'rb').read()
    line_bot_api.set_rich_menu_image(menuId,contentType,img)
    return menuId


"""def create_rich_menu(image):
    rich_menu = RichMenu()
    rich_menu.size = {'width':1920,'height':1080}
    rich_menu.selected = False
    rich_menu.chatBarText = "Test_Chat_bar"
    rich_menu.name = "Test_Menu_Name"
    arealist = []
    ar = RichMenuArea()
    ACTION = Action()
    #ACTION.type = 'uri'
    #ACTION.uri = "https://www.youtube.com/watch?v=kvEHNOr4EFs"
    ACTION.type= 'message'
    #setuptext = open("setupguide.txt","r").read()
    ACTION.text= "!setupguide"
    ar.action= ACTION
    #ar.bounds = RichMenuArea(1980,1080)
    ar.bounds = {"x":0,"y":0,"width":1920,"height":1080}
    arealist.append(ar) 
    rich_menu.areas = arealist
    menuId=line_bot_api.create_rich_menu(rich_menu)
    contentType = 'image/jpeg' #insert image
    img = open(image,'rb').read()
    line_bot_api.set_rich_menu_image(menuId,contentType,img)
    return menuId"""


@app.route('/webhook',methods =['POST'])
def reply_message():
    hook = request.json
    if((hook['events'][0]['type'] == "follow")):
      line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='สวัสดีท่านสมาชิกชมรมคนชอบ-'))
      line_bot_api.link_rich_menu_to_user(hook['events'][0]['source']["userId"],"richmenu-c3c2fdf3db15434d3ed21d7e8ee7f882")
    elif(hook['events'][0]['type'] == "message"):
      word = (hook['events'][0]['message']['text'])
      check = word[0:6]
      if check == "!setup" and word.count(':') == 2:
       word2 = word.split(':')
       user = word2[1]
       pas = word2[2] 
       #check user and passwd is wheter matching in database  or not
       que = myCollection_user.find({"username": user })
       que2 = myCollection_user.find({"ID_line": hook['events'][0]['source']["userId"] })
       lis = []
       lis2 = []
       for ele in que:
        lis.append(ele)

       for ele in que2:
        lis2.append(ele)

       c = len(lis)
       c2 = len(lis2)
       if c == 1:
        real_pas = lis[0]['password']
       if (c == 0):
        line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='ไม่พบผู้ใช้งาน'))
       #elif c == 1 and real_pas == pas and c2 != 0:
       elif c2 != 0:
        line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='ท่านได้เคยทำการลงทะเบียนเพื่อใช้งานpostboxnewgenด้วยLineนี้แล้ว'))
        line_bot_api.push_message(hook['events'][0]['source']["userId"], TextSendMessage(text="หากต้องการที่จะเปลี่ยนมาใช้username นี้ กรุณา พิมพ์"+'\n'+"!cancel_user:<usernameเก่า>:<passwordของusernameเก่า>"+'\n'+"เพื่อยกเลิกบัญชีเก่า แล้วจึง ทำการ setup อีกครั้ง"))
       elif c == 1  and lis[0]["ID_line"] != 0:
        line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text="username นี้ได้เคยทำการลงเบียนด้วยline accountแล้ว "))
        line_bot_api.push_message(hook['events'][0]['source']["userId"], TextSendMessage(text="หากต้องการที่จะเปลี่ยนมาใช้line account นี้ กรุณา พิมพ์"+'\n'+"!cancel_user:<username>:<password>"+'\n'+"เพื่อยกเลิกบัญชีเก่า แล้วจึง ทำการ setup อีกครั้ง"))
       elif c == 1 and lis[0]["ID_line"]== 0 and check_password_hash(real_pas,pas) and c2 == 0:
        update = {"$set":{
        "ID_line": hook['events'][0]['source']["userId"]
        }}
        myCollection_user.update_one({"username":user},update)
        #menu=create_rich_menu("blackwhite.jpg")
        line_bot_api.link_rich_menu_to_user(hook['events'][0]['source']["userId"],"richmenu-a7884105185a3657f40829948dfe8c8f")
        line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='ขอบคุณที่ใช้บริการ=]'))
       elif c == 1 and  not(check_password_hash(real_pas,pas))  :
        line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='รหัสผ่านไม่ถูกต้อง'))
       else :
        line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='พบผู้ใช้งานมากกว่า1คน'))
      elif hook['events'][0]['message']['text'][0:7] == "!cancel" and word.count(':') == 2:
        word2 = (hook['events'][0]['message']['text']).split(':')
        que = myCollection_user.find({"username": word2[1] })
        lis = []
        for ele in que:
         lis.append(ele)
        if(len(lis)==0):
         line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='ไม่พบผู้ใช้งาน'))
        elif check_password_hash(lis[0]["password"],word2[2]):
         update = {"$set":{
         "ID_line": 0
         }}
         myCollection_user.update_one({"username":word2[1]},update)
         line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='username:'+word2[1]+'ได้ทำการยกเลิกการเชื่อมต่อกับบัญชีline'))
         line_bot_api.link_rich_menu_to_user(hook['events'][0]['source']["userId"],"richmenu-c3c2fdf3db15434d3ed21d7e8ee7f882")
        else:
         line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='username หรือ password ไม่ถูกต้อง'))
      elif hook['events'][0]['message']['text'] == "!setupguide":
       guide = open("setupguide.txt","r").read()
       line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text=guide))
      elif hook['events'][0]['message']['text'] == "!unlock_my_box":
       url = "http://158.108.182.23:3001/user/unlock?ID_line="+hook['events'][0]['source']["userId"]
       req = requests.patch(url)
       line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='your locker is open =]'))
      elif hook['events'][0]['message']['text'] == "!lock_my_box":
       url = "http://158.108.182.23:3001/user/lock?ID_line="+hook['events'][0]['source']["userId"]
       req = requests.patch(url)
       print(req)
       line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='your locker is safe =]'))
      elif hook['events'][0]['message']['text'] == "ชายเหมี่ยง":
       line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='เชียงใหม่'))
      elif hook['events'][0]['message']['text'] == "ชายเรียง":
       line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='เชียงราย'))
      elif hook['events'][0]['message']['text'] == "ชายสี่":
       line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='หมี่เกี๊ยว ผ่าม!'))
      elif hook['events'][0]['message']['text'] == "โส่เอีย":
       line_bot_api.reply_message(hook['events'][0]['replyToken'], TextSendMessage(text='เสี่ยโ'))
    return "=]"


@app.route('/message', methods = ['GET'])
def message():
        arg = request.args.get('user')
        que = myCollection_user.find({'username':arg})
        lis = []
        for ele in que:
         lis.append(ele)
        line = lis[0]["ID_line"]
        line_bot_api.push_message(line, TextSendMessage(text="พัสดุมาส่ง"))
        return 'hello'


if __name__ == "__main__":
      #menu=create_rich_menu("blackwhite.jpg")
      app.run(host='0.0.0.0', port='3000', debug=True)


                                                                                                                                                    
