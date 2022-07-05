from http import client
import os
import json

from re import ASCII
import requests
from flask import Flask, request, abort
import pyrebase
import base64

import util


firebaseConfig = {
  "apiKey": "AIzaSyBbpL1cGJHXiQsqaFc7C-F41VgcG8LN3pk",
  "authDomain": "lineweb-d1174.firebaseapp.com",
  "projectId": "lineweb-d1174",
  "storageBucket": "lineweb-d1174.appspot.com",
  "messagingSenderId": "854065790129",
  "appId": "1:854065790129:web:0f9c4747e925b9fc1db690",
  "databaseURL": "https://lineweb-d1174.firebaseio.com/"
};

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

def login(email,password):
    # print("Log in...")
    # email=input("Enter email: ")
    # password=input("Enter password: ")
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        return login["idToken"]
        print("Successfully logged in!")
        # print(auth.get_account_info(login['idToken']))
       # email = auth.get_account_info(login['idToken'])['users'][0]['email']
       # print(email)
    except:
        print("Invalid email or password")
    return

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, FollowEvent, FlexSendMessage, BubbleContainer
)
from linebot.models.flex_message import BubbleContainer, FlexContainer


from linebot.models import rich_menu
from linebot.models.rich_menu import *
from linebot.models.actions import (MessageAction, RichMenuSwitchAction)
import copy

state_dict = {}
# state_dict["state"] = "start"
# state_dict["cq"] = 1
questionaire = {}
questionflex = {}
motionopt = {}
records = {}
responsehist = {}
options = "\n選択肢一つを選択してください。\n 1. まったくその通りだ \n 2. どちらかというとそうだ  \n 3. ときどき思い当たることがある \n 4. そんなことはない"

# f =  open('./resources/quesaire.json', encoding='utf8')
# questionaire = json.load(f)
# f.close()

# f =  open('./resources/question.json', encoding='utf8')
# questionflex = json.load(f)
# f.close()
# f =  open('./resources/motionopt.json', encoding='utf8')
# motionopt = json.load(f)
# f.close()


#points for records
#1) api name is records
#2) records has multiple fileds like height that is a map from timestamp to value registered


# 333333333 = "lkMI2xb0HpBdCpeOZpvM"
apiurl = 'https://linewebbackend.herokuapp.com/api/bot' 
client = requests.session()
app = Flask(__name__)

line_bot_api = LineBotApi('lnoN3pNo/DUuie5L3OT9exNM+/WZzquIkqGIZdVFcOTHOAhdkNe8IXDilhrKQNrFLQViNJv0MVcZtIzaU7sFKoOkc9s657sq5xb64EtiVqbCoDPEwqt0xwZgkuFriqVOVKVQrP7sXhjR4dNQm5Gk1QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fb93092bbba827e36296a2cfdbdde14d')

######################init for every user init dict - lakshay
def authheaders():
    return {
          "Accept": "application/json",
          "Content-Type": "application/json",
        }

def makeoptions(choices):
    optionslst = []
    if len(choices)==0:
        # options = "\n選択肢一つを選択してください。\n 1. まったくその通りだ \n 2. どちらかというとそうだ  \n 3. ときどき思い当たることがある \n 4. そんなことはない"
        # return util.listTextMessage(["まったくその通りだ","どちらかというとそうだ","ときどき思い当たることがある","そんなことはない"],"n選択肢一つを選択してください。")
        return ["まったくその通りだ","どちらかというとそうだ","ときどき思い当たることがある","そんなことはない"]
    else:
        # options = "\n選択肢一つを選択してください。"
        count = 0
        for choice in choices:
            count+=1
            # options+= "\n "+count+". "+choice["choiceText"]
            optionslst.append(choice["choiceText"])
        return optionslst
        # options = util.listTextMessage(optionslst,"n選択肢一つを選択してください。")
    return options
def apicall(event, url, postdata, nores = False):
    postdata = json.dumps(postdata)
    if(not event):
        r = client.get(apiurl+url, headers=authheaders())
        print(r)
        if(r != None and r.status_code == 200):
            return r.json()
        else:
            return None
    else:
        r = client.post(apiurl+url, data= postdata, headers=authheaders())
        print(r)
        if(r != None and not nores and r.status_code == 200):
            return r.json()
        else:
            return None

usrlist = apicall(None, '/userlist', {"bot_id":""})
if(usrlist): print("userlist returned")
else: print("userlist wasn't returned")

for usr in usrlist:
    state_dict[usr]= {"state": "start", "cq":1}


def questionnaireWrapper(ques):
    # ques is a string
    question = copy.deepcopy(questionflex)
    question["body"]["contents"][1]["text"] = ques

    with open("sample.json", "w") as outfile:
        json.dump(question, outfile)
    
    return question

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ Here's all the messages will be handled and processed by the program """
    print("handleevent")
    print(event)
    resp,flag = statehandle(event)

    print("$$$$$$$$$$$$$$$")
    print(resp)
    print(flag)
    # # #print(event)
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=resp))

    if not flag:
        print("jugaad working")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=resp))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="yo",contents=resp))

# @handler.add(MessageEvent,message=FlexM/essage)

@handler.add(MessageEvent, message=ImageMessage)
def handle_imagemessage(event):
    """ Here's all the messages will be handled and processed by the program """
    print("handleevent")
    print(event)
    resp,flag = imstatehandle(event)
    # #print(event)
    
    if not flag:
        print("jugaad working")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=resp))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="yo",contents=resp))

@handler.add(FollowEvent)
def handle_follow(event):
    """ Here's all the messages will be handled and processed by the program """
    print("handleevent")
    print(event)
    print(state_dict)
    resp = followhandle(event)
    print(state_dict)
    #print(event)
    
    # print("jugaad working")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=resp))


    
        
    

def followhandle(event):
    print("followhandle")
    if(event.source.type == "user"):
        r = client.post(apiurl+'/followevent', data= json.dumps({"user_id": event.source.user_id}), headers=authheaders())
        print(r)
        if(r != None and r.status_code == 200):
            print("ff")
            #print(event)
            print("gaygan")

            state_dict[event.source.user_id]= {"state": "init", "cq":1,"creds": {"username": "","password": ""}}
            return "ユーザー名を入力してください："
        else:

            print("error")
            # state_dict[event.source.user_id]= {"state": "start", "cq":1}
            return 'error'

def imstatehandle(event):
    pos="standing"
    dir="front"
    if state_dict[event.source.user_id]['state'] == "att_stand_front":
        pos="standing"
        dir="front"
    elif state_dict[event.source.user_id]['state'] == "att_stand_left":
        pos="standing"
        dir="left"
    elif state_dict[event.source.user_id]['state'] == "att_stand_right":
        pos="standing"
        dir="right"
    elif state_dict[event.source.user_id]['state'] == "att_sit_front":
        pos="sitting"
        dir="front"
    elif state_dict[event.source.user_id]['state'] == "att_sit_left":
        pos="sitting"
        dir="left"
    elif state_dict[event.source.user_id]['state'] == "att_sit_right":
        pos="sitting"
        dir="right"
    else:
        return "Not a valid input"
    message_content = line_bot_api.get_message_content(event.message.id)
    # file_path = "./iter_cont.txt"
    # with open(file_path, 'wb') as fd:
    #     for chunk in message_content.iter_content():
    #         fd.write(chunk)
    encoded = base64.b64encode(message_content.content).decode("ascii")
    # file_path2 = "./encoded.txt"
    # with open(file_path2,"wb") as fd:
    #     fd.write(encoded)
    resp = apicall(event, '/posturedata', {"user_id": event.source.user_id,"pose": pos, "direction": dir, "image":"data:image/jpeg;base64," + encoded})
    if(resp): 
        print(resp)
        orurl = resp["orurl"]
        angles = resp["angles"]
    else: return "api failed"

    line_bot_api.push_message(
        event.source.user_id,
        TextSendMessage(text=orurl))

    line_bot_api.push_message(
        event.source.user_id,
        ImageSendMessage(original_content_url=orurl, preview_image_url=orurl))
    resp = apicall(event, '/conditionprocess', {"user_id": event.source.user_id,"pose": pos, "direction": dir, "image":angles})
    if(resp): 
        print(resp)
        eva = resp["eval"]
        typ = resp["type"]
        responsetexts = resp["resp"]
    else: return "api failed"     
    line_bot_api.push_message(
        event.source.user_id,
        FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("Evaluation: "+eva+", Type: "+typ , weight=True)))

    for responsetext in responsetexts:
        line_bot_api.push_message(
            event.source.user_id,
            FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage(responsetext)))
    
   
    state_dict[event.source.user_id]['state'] = "menu_select"
    # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
    responseOptions = ["運動","食事","姿勢","記録"]
    response = util.listTextMessage(responseOptions)
    flag = True


    return response, flag
def statehandle(event):
    global questionaire
    global motionopt
    global responsehist
    response = 'ff'
    flag = False
    # false -> text, true -> flex 

    ###########debugging################
    if event.message.text.lower() == 'back' :
        state_dict[event.source.user_id]['state'] = "start"
        state_dict[event.source.user_id]['cq'] = 1
        # print(line_bot_api.get_rih_menu_list)
        response = "rebooted"

        dict1 = util.func()
        line_bot_api.push_message(
            event.source.user_id,
            FlexSendMessage(alt_text="yo",contents=dict1))

    ###########debugging################
    print("state")
    #print(event)
    print(event.source)
    print(type(event))
    print(type(event.source))
    # print(len(event.source))
    print(event.source.user_id)
    # print(event.source.user_id)
    print(state_dict)
    if state_dict[event.source.user_id]['state'] == "init":
        # Please enter your password:
        # response = "パスワードを入力してください："
        response = util.simpleTextMessage("パスワードを入力してください：")
        flag = True
        state_dict[event.source.user_id]['creds']['username'] = event.message.text
        state_dict[event.source.user_id]['state'] = "init_password"

    elif state_dict[event.source.user_id]['state'] == "init_password":
        state_dict[event.source.user_id]['creds']['password'] = event.message.text
        # resp = apicall(event, '/register', {"user_id": event.source.user_id, "email": state_dict[event.source.user_id]['creds']['username'],"password": state_dict[event.source.user_id]['creds']['password']})
        resp = login(state_dict[event.source.user_id]['creds']['username'],state_dict[event.source.user_id]['creds']['password'])
        if(resp == None):
            # response = "正しいクレデンシャルを入力してください。\n\n ユーザー名を入力してください："
            response = util.simpleListTextMessage(["正しいクレデンシャルを入力してください。","ユーザー名を入力してください："])
            flag = True
            state_dict[event.source.user_id]['state'] = "init"
        else:
            resp2 = apicall(event, '/register', {"user_id": event.source.user_id,"idToken": resp})
            if(resp2 == None):
                # response = "正しいクレデンシャルを入力してください。\n\n ユーザー名を入力してください："
                response = util.simpleListTextMessage(["正しいクレデンシャルを入力してください。","ユーザー名を入力してください："])
                flag = True
                state_dict[event.source.user_id]['state'] = "init"
            else:
                re = client.post(apiurl+'/greeting', data= json.dumps({"user_id": event.source.user_id}), headers=authheaders())
                # if(re != None and re.status_code == 200):
                #     line_bot_api.push_message(
                #         event.source.user_id,
                #         TextSendMessage(text=re["greet"])) 
                if(re != None and re.status_code == 200):
                    line_bot_api.push_message(
                        event.source.user_id,
                        FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage(re["greet"]))) 

                        
                else:
                    line_bot_api.push_message(
                        event.source.user_id,
                        TextSendMessage(text="Hey there!!")) 
                # response = "正常にログインしました。 \n\n 選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
                responseOptions = ["運動","食事","姿勢","記録"]
                response = util.listTextMessage(responseOptions)
                flag = True
                state_dict[event.source.user_id]['state'] = "menu_select"
    

    elif state_dict[event.source.user_id]['state'] == "start":
        print("nycbruh")
        # "Please select one option. \ n 1. Motion \ n 2. Meal \ n 3. Attitude \ n 4. Record"
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        # response = util.simpleTextMessage("選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録")
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessage(responseOptions)
        flag = True
        print("ttttttttttttttttttt")
        print(response)
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     FlexSendMessage(alt_text="yo",contents=resp))
        # flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"

    elif state_dict[event.source.user_id]['state'] == "menu_select":

        print("ffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        if event.message.text == '1':

            resp = apicall(event, '/motionopt', {"user_id": event.source.user_id})
            # f =  open('./resources/quesaire.json', encoding='utf8')
            # questionaire = json.load(f)
            if(resp): 
                print(resp)
                motionopt = resp["motionopt"]["items"]
                responsehist = resp["responsehist"]
            else: 
                return "api failed"
            print("qqq3")
            # print(questionaire)


            # response = "選択肢一つを選択してください。"
            # for item in motionopt:
            #     response+= "\n"+item["itemName"]

            respItems = []
            for item in motionopt:
                respItems.append(item["itemName"])
            response = util.listTextMessage(respItems)
            print("respppp")
            print(response)
            flag = True

            state_dict[event.source.user_id]['state'] = 'selected_motion'
            # line_bot_api.set_default_rich_menu(back_menu_id)

        elif event.message.text == '2':

            resp = apicall(event, '/questionaire', {"user_id": event.source.user_id})
            # f =  open('./resources/quesaire.json', encoding='utf8')
            # questionaire = json.load(f)
            if(resp): questionaire = resp["questionaire"]
            else: return "api failed"
            print("qqq")
            print(questionaire)
            optionsAll = makeoptions(questionaire['questionItems'][0]['choiceItems'])
            # response = "アンケートを始めましょう: \n Q1) " + questionaire['questionItems'][0]['questionText'] + options
            line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("Q1) " + questionaire['questionItems'][0]['questionText'],True)))
            print("options")
            print(optionsAll)
            response = util.listTextMessage(optionsAll,"アンケートを始めましょう")
            flag = True

            state_dict[event.source.user_id]['state']= 'questionaire'
            # line_bot_api.set_default_rich_menu(back_menu_id)

        elif event.message.text == '3':
            # response = "Enter Pose: \n1. Standing\n2. Sitting"
            response = util.listTextMessage(["スタンディング","座位"],"ポーズを入力する")
            flag = True
            state_dict[event.source.user_id]['state'] = 'selected_attitude'
            # line_bot_api.set_default_rich_menu(back_menu_id)
        elif event.message.text == '4':

            # resp = apicall(event, '/records', {"bot_id": bot_id})
            # f =  open('./resources/quesaire.json', encoding='utf8')
            # questionaire = json.load(f)
            # global questionaire
            # if(resp): questionaire = resp
            # else: response = "有効なオプションを選択してください。"
            # print("qqq")
            # print(questionaire)

        #     const recordTypes = {
        #     height: {label: "身長", id: "height", unit: "cm", format: "number"},
        #     weight: {label: "体重", id: "weight", unit: "kg", format: "number"},
        #     fatrate: {label: "脂肪率", id: "fatrate", unit: "%", format: "number"},
        #     muscleamt: {label: "筋量", id: "muscleamt", unit: "kg", format: "number"},
        #     bloodpressure: {label: "血圧", id: "bloodpressure", unit: "mmHg", format: "number"},
        #     musclepow: {label: "筋力", id: "musclepow", unit: "kg", format: "number"},
        #     flexibility: {label: "柔軟性", id: "flexibility", unit: "cm", format: "number"},
        #     bloodtest: {label: "血液検査", id: "bloodtest", unit: " ", format: "text"}
        # };


            # response = "何を録音したいですか？ \n 1) 身長 \n 2) 体重 \n 3) 脂肪率 \n 4) 筋量 \n 5) 血圧 \n 6) 筋力 \n 7) 柔軟性 \n 8) 血液検査" #update this line
            response = util.listTextMessage(["身長","体重","脂肪率","筋量","血圧","筋力","柔軟性","血液検査"],"何を録音したいですか？")
            flag = True
            state_dict[event.source.user_id]['state'] = 'selected_record'
            # line_bot_api.set_default_rich_menu(back_menu_id)
        else:
            # "Please select a valid option."
            # response = "有効なオプションを選択してください。"
            response = util.simpleListTextMessage("有効なオプションを選択してください。")
            flag = True

    elif state_dict[event.source.user_id]['state'] == 'selected_motion':

        resp = apicall(event, '/motionopt', {"user_id": event.source.user_id})
        # f =  open('./resources/quesaire.json', encoding='utf8')
        # questionaire = json.load(f)
        if(resp): 
            motionopt = resp["motionopt"]["items"]
            responsehist = resp["responsehist"]
        else: return "api failed"
        # print(questionaire)


        itemselected = int(event.message.text)-1
        if itemselected >= len(motionopt) or itemselected < 0:
            line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("有効なオプションを選択してください。"))) 

            # response = "選択肢一つを選択してください。"
            # for item in motionopt:
            #     response+= "\n"+item["itemName"]

            respOptions = []
            for item in motionopt:
                respOptions.append(item["itemName"])
            response = util.simpleListTextMessage(respOptions,"選択肢一つを選択してください。")
            flag = True

            state_dict[event.source.user_id]['state'] = 'selected_motion'
        else:
            responsehist["selected_motion"]=itemselected
            # response = "選択肢一つを選択してください。"
            # for option in motionopt[itemselected]["subItems"]:
            #     response+="\n"+option["subItemName"]

            respOpt = []
            for opt in motionopt[itemselected]["subItems"]:
                respOpt.append(opt["subItemName"])
            response = util.listTextMessage(respOpt,"選択肢一つを選択してください。")
            flag = True

            apicall(event, '/updatehistmotionopt', {"user_id": event.source.user_id, "data": responsehist}, nores=True)
            state_dict[event.source.user_id]['state'] = 'selected_motion_item'
    elif state_dict[event.source.user_id]['state'] == 'selected_motion_item':
        optionselected = int(event.message.text)-1

        resp = apicall(event, '/motionopt', {"user_id": event.source.user_id})
        # f =  open('./resources/quesaire.json', encoding='utf8')
        # questionaire = json.load(f)
        if(resp): 
            motionopt = resp["motionopt"]["items"]
            responsehist = resp["responsehist"]
        else: return "api failed"
        print("qqq5")
        # print(questionaire)

            
        if optionselected >= len(motionopt[responsehist["selected_motion"]]["subItems"]) or optionselected < 0:
            line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("有効なオプションを選択してください。")))          
            # response = "選択肢一つを選択してください。"
            # response = util.simpleTextMessage("選択肢一つを選択してください。")
            # for option in motionopt[responsehist["selected_motion"]]["subItems"]:
            #     response+="\n"+option["subItemName"]

            respOpt = []
            flag = True

            for option in motionopt[responsehist["selected_motion"]]["subItems"]:
                respOpt.append(option["subItemName"])

            response = util.listTextMessage(respOpt,"選択肢一つを選択してください。")

            
            state_dict[event.source.user_id]['state'] = 'selected_motion_item'
        else:
            responsehist["selected_motion_item"]=optionselected

            # response = "選択肢一つを選択してください。"
            # for elmnt in motionopt[responsehist["selected_motion"]]["subItems"][optionselected]["subSubItems"]:
            #     response+="\n"+elmnt["menuText"]

            respOpt = []
            flag = True

            for option in motionopt[responsehist["selected_motion"]]["subItems"][optionselected]["subSubItems"]:
                respOpt.append(option["menuText"])

            response = util.listTextMessage(respOpt,"選択肢一つを選択してください。")


            apicall(event, '/updatehistmotionopt', {"user_id": event.source.user_id, "data": responsehist}, nores=True)
            state_dict[event.source.user_id]['state'] = 'selected_motion_item_option'
    elif state_dict[event.source.user_id]['state'] == 'selected_motion_item_option':
        elmntselected = int(event.message.text)-1

        resp = apicall(event, '/motionopt', {"user_id": event.source.user_id})
        # f =  open('./resources/quesaire.json', encoding='utf8')
        # questionaire = json.load(f)
        if(resp): 
            motionopt = resp["motionopt"]["items"]
            responsehist = resp["responsehist"]
        else: return "api failed"
        print("qqq6")
        # print(questionaire)

            
        if elmntselected >= len(motionopt[responsehist["selected_motion"]]["subItems"][responsehist["selected_motion_item"]]["subSubItems"]) or elmntselected < 0:
            # line_bot_api.push_message(
            #     event.source.user_id,
            #     TextSendMessage(text="Please select a valid response."))  

            line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("有効なオプションを選択してください。")))

                      
            # response = "選択肢一つを選択してください。"
            # for elmnt in motionopt[responsehist["selected_motion"]]["subItems"][responsehist["selected_motion_item"]]["subSubItems"]:
            #     response+="\n"+elmnt["menuText"]

            respOpt = []
            flag = True

            for option in motionopt[responsehist["selected_motion"]]["subItems"][responsehist["selected_motion_item"]]["subSubItems"]:
                respOpt.append(option["menuText"])

            response = util.listTextMessage(respOpt,"選択肢一つを選択してください。")


            state_dict[event.source.user_id]['state'] = 'selected_motion_item_option'
        else:
            responsehist["selected_motion_item_option"]=elmntselected

            #noob lakshay


            # line_bot_api.push_message(
            #     event.source.user_id,
            #     TextSendMessage(text="Thank You for your response."))  

            line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))


            respmsg=apicall(event, '/clearhistmotionopt', {"user_id": event.source.user_id,"data": responsehist})

            # for msg in respmsg["text"]:
            #     line_bot_api.push_message(
            #         event.source.user_id,
            #         TextSendMessage(text=msg))  

            for msg in respmsg["text"]:
                line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage(msg)))  


            print(respmsg["image"])
            if respmsg["image"] is not None:
                line_bot_api.push_message(
                    event.source.user_id,
                    ImageSendMessage(original_content_url=respmsg["image"],preview_image_url=respmsg["image"]))  

            # response= "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
            responseOptions = ["運動","食事","姿勢","記録"]
            response = util.listTextMessage(responseOptions)
            flag = True
             
            responsehist.clear()
            state_dict[event.source.user_id]['state']='menu_select'
    elif state_dict[event.source.user_id]['state'] == 'questionaire':

        resp = apicall(event, '/questionaire', {"user_id": event.source.user_id})
        # f =  open('./resources/quesaire.json', encoding='utf8')
        # questionaire = json.load(f)
        if(resp): 
            questionaire = resp["questionaire"]
            responsehist = resp["responsehist"]
        else: return "api failed"
        print("qqq2")
        # print(questionaire)
        choiceselected = int(event.message.text)-1
        if choiceselected < 0 or choiceselected >= len(questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['choiceItems']):
            options = makeoptions(questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['choiceItems'])

            # response = "Q" + str(state_dict[event.source.user_id]['cq'])+ ") "+ questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['questionText'] + options

            line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("Q" + str(state_dict[event.source.user_id]['cq'])+ ") "+ questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['questionText'],True)))

            response = util.listTextMessage(options,"アンケートを始めましょう")
            flag = True
        else:
            responsehist["questionaire"][str(state_dict[event.source.user_id]['cq'])] = {"choicenum": choiceselected, "choiceWeight": questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['choiceItems'][choiceselected-1]["choiceWeight"], "questionType": questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['questionType']}
            if state_dict[event.source.user_id]['cq'] >= len(questionaire['questionItems']):
                print(state_dict[event.source.user_id]['cq'])
                
                state_dict[event.source.user_id]['cq']=1
                # line_bot_api.push_message(
                #     event.source.user_id,
                #     TextSendMessage(text="Thank You for your responses."))     
                line_bot_api.push_message(
                    event.source.user_id,
                    FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))  

                # response= "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
                responseOptions = ["運動","食事","姿勢","記録"]
                response = util.listTextMessage(responseOptions)
                flag = True

                state_dict[event.source.user_id]['state'] = "menu_select"
                apicall(event, '/clearhistques',{"user_id": event.source.user_id, "data": responsehist, "questionName": questionaire['questionName']}, nores=True)
                responsehist.clear()

                state_dict[event.source.user_id]['state']='menu_select'
            else:
                options = makeoptions(questionaire['questionItems'][state_dict[event.source.user_id]['cq']]['choiceItems'])
                # response = "Q" + str(state_dict[event.source.user_id]['cq']+1)+ ") "+ questionaire['questionItems'][state_dict[event.source.user_id]['cq']]['questionText'] + options
                line_bot_api.push_message(
                    event.source.user_id,
                    FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("Q" + str(state_dict[event.source.user_id]['cq']+1)+ ") "+ questionaire['questionItems'][state_dict[event.source.user_id]['cq']]['questionText'],True)))

                response = util.listTextMessage(options,"アンケートを始めましょう")
                flag = True
                state_dict[event.source.user_id]['cq']+=1 
                apicall(event, '/updatehistques', {"user_id": event.source.user_id, "data": responsehist}, nores=True)
 
    elif state_dict[event.source.user_id]['state'] == 'selected_attitude':
        if event.message.text == '1':
            state_dict[event.source.user_id]['state'] = 'att_stand'
            # response = "Enter direction: \n1. front\n2. left\n3. right"
            response = util.listTextMessage(["フロント","左","右"],"方向を入力してください。")
            flag = True
        elif event.message.text == '2':
            state_dict[event.source.user_id]['state'] = 'att_sit'
            # response = "Enter direction: \n1. front\n2. left\n3. right"
            response = util.listTextMessage(["フロント","左","右"],"方向を入力してください。")
            flag = True
        else:
            # response = "Please enter a valid value"
            response = util.simpleTextMessage("有効な値を入力してください。")
            flag = True
    elif state_dict[event.source.user_id]['state'] == 'att_stand':
        if event.message.text == '1':
            state_dict[event.source.user_id]['state'] = 'att_stand_front'
            # response = "Upload the image"
            response = util.func()
            flag = True
        elif event.message.text == '2':
            state_dict[event.source.user_id]['state'] = 'att_stand_left'
            # response = "Upload the image"
            response = util.func()
            flag = True
        elif event.message.text == '2':
            state_dict[event.source.user_id]['state'] = 'att_stand_right'
            # response = "Upload the image"
            response = util.func()
            flag = True
        else:
            response = "Please enter a valid value"
    elif state_dict[event.source.user_id]['state'] == 'att_sit':
        if event.message.text == '1':
            state_dict[event.source.user_id]['state'] = 'att_sit_front'
            # response = "Upload the image"
            response = util.func()
            flag = True
        elif event.message.text == '2':
            state_dict[event.source.user_id]['state'] = 'att_sit_left'
            # response = "Upload the image"
            response = util.func()
            flag = True
        elif event.message.text == '2':
            state_dict[event.source.user_id]['state'] = 'att_sit_right'
            # response = "Upload the image"
            response = util.func()
            flag = True
        else:
            # response = "Please enter a valid value"
            response = util.simpleTextMessage("有効な値を入力してください。")
            flag = True
    elif state_dict[event.source.user_id]['state'] == 'selected_record':
        # response = "Please enter the value"
        # response = "値を入力してください"
        response = util.simpleTextMessage("値を入力してください")
        flag = True
        ## record the value here

        if event.message.text == '1':
            state_dict[event.source.user_id]['state'] = 'height'
        elif event.message.text == '2':
            state_dict[event.source.user_id]['state'] = 'weight'
        elif event.message.text == '3':
            state_dict[event.source.user_id]['state'] = 'fatrate'
        elif event.message.text == '4':
            state_dict[event.source.user_id]['state'] = 'muscleamt'
        elif event.message.text == '5':
            state_dict[event.source.user_id]['state'] = 'bloodpressure'
        elif event.message.text == '6':
            state_dict[event.source.user_id]['state'] = 'musclepow'
        elif event.message.text == '7':
            state_dict[event.source.user_id]['state'] = 'flexibility'
        elif event.message.text == '8':
            state_dict[event.source.user_id]['state'] = 'bloodtest'
    
    
    elif state_dict[event.source.user_id]['state'] == 'height':
        apicall(event,"/user_record",{"user_id": event.source.user_id,"data": {"value": float(event.message.text),"type": "height","user_id": event.source.user_id}}, nores=True)
        # response = "ご返信ありがとうございます。"
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="Thank You for your response."))  
        line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessage(responseOptions)
        flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"

    elif state_dict[event.source.user_id]['state'] == 'weight':
        apicall(event,"/user_record",{"user_id": event.source.user_id,"data": {"value": float(event.message.text),"type": "weight","user_id": event.source.user_id}}, nores=True)
        # response = "ご返信ありがとうございます。"
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="Thank You for your response.")) 
        line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessage(responseOptions)
        flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"
    
    elif state_dict[event.source.user_id]['state'] == 'fatrate':
        apicall(event,"/user_record",{"user_id": event.source.user_id,"data": {"value": float(event.message.text),"type": "fatrate","user_id": event.source.user_id}}, nores=True)
        # response = "ご返信ありがとうございます。"
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="Thank You for your response.")) 
        line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessage(responseOptions)
        flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"

    
    elif state_dict[event.source.user_id]['state'] == 'muscleamt':
        apicall(event,"/user_record",{"user_id": event.source.user_id,"data": {"value": float(event.message.text),"type": "muscleamt","user_id": event.source.user_id}}, nores=True)
        # response = "ご返信ありがとうございます。"
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="Thank You for your response.")) 
        line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessage(responseOptions)
        flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"

    elif state_dict[event.source.user_id]['state'] == 'bloodpressure':
        apicall(event,"/user_record",{"user_id": event.source.user_id,"data": {"value": float(event.message.text),"type": "bloodpressure","user_id": event.source.user_id}}, nores=True)
        # response = "ご返信ありがとうございます。"
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="Thank You for your response.")) 
        line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessage(responseOptions)
        flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"

    elif state_dict[event.source.user_id]['state'] == 'musclepow':
        apicall(event,"/user_record",{"user_id": event.source.user_id,"data": {"value": float(event.message.text),"type": "musclepow","user_id": event.source.user_id}}, nores=True)
        # response = "ご返信ありがとうございます。"
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="Thank You for your response.")) 
        line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessage(responseOptions)
        flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"
    
    elif state_dict[event.source.user_id]['state'] == 'flexibility':
        apicall(event,"/user_record",{"user_id": event.source.user_id,"data": {"value": float(event.message.text),"type": "flexibility","user_id": event.source.user_id}}, nores=True)
        # # response = "ご返信ありがとうございます。"
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="Thank You for your response.")) 
        line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessage(responseOptions)
        flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"

    elif state_dict[event.source.user_id]['state'] == 'bloodtest':
        apicall(event,"/bloodtest",{"data": {"value": float(event.message.text),"type": "bloodtest","user_id": event.source.user_id}}, nores=True)
        # response = "ご返信ありがとうございます。"
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="Thank You for your response.")) 
        line_bot_api.push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessage(responseOptions)
        flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"


            

    else:
        response = "errrrr"
    return response,flag

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



