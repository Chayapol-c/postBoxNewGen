#create 1 area for no money user 

def create_rich_menu(image):
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
    setuptext = open("setupguide.txt","r").read()
    ACTION.text=setuptext
    ar.action= ACTION
    #ar.bounds = RichMenuArea(1980,1080)
    ar.bounds = {"x":0,"y":0,"width":1920,"height":1080}
    arealist.append(ar) 
    rich_menu.areas = arealist
    menuId=line_bot_api.create_rich_menu(rich_menu)
    contentType = 'image/jpeg' #insert image
    img = open(image,'rb').read()
    line_bot_api.set_rich_menu_image(menuId,contentType,img)
    return menuId


#create 2 area for rich user 

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
    ACTION.type = 'uri'
    ACTION.uri = "https://www.youtube.com/watch?v=kvEHNOr4EFs"
    #ACTION.type= 'message'
    #setuptext = open("setupguide.txt","r").read()
    #ACTION.text=setuptext
    ar.action= ACTION
    #ar.bounds = RichMenuArea(1980,1080)
    ar.bounds = {"x":0,"y":0,"width":1920/2,"height":1080}
    arealist.append(ar) 
   
    #create  are another rich menu2
    ar2 = RichMenuArea()
    ACTION2 = Action()
    ACTION2.type = 'uri'
    ACTION2.uri = 'https://www.youtube.com/watch?v=gVZyDJDbXMQ'
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


