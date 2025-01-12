from http import client
import os
import json

from re import ASCII
import re
import requests
from flask import Flask, request, abort
import pyrebase
import base64

import util
import hmac
import hashlib


firebaseConfig = {
  "apiKey": "AIzaSyCulzTY93K3424lDUEAQwHV6vj35z-gSYE",
  "authDomain": "linewebbot.firebaseapp.com",
  "projectId": "linewebbot",
  "storageBucket": "linewebbot.appspot.com",
  "messagingSenderId": "432628358278",
  "appId": "1:432628358278:web:8329e7c5e6ccdfccf60507",
  "databaseURL": "https://lineweb-d1174.firebaseio.com/"
}
# firebaseConfig = {
#   "apiKey": "AIzaSyBbpL1cGJHXiQsqaFc7C-F41VgcG8LN3pk",
#   "authDomain": "lineweb-d1174.firebaseapp.com",
#   "projectId": "lineweb-d1174",
#   "storageBucket": "lineweb-d1174.appspot.com",
#   "messagingSenderId": "854065790129",
#   "appId": "1:854065790129:web:0f9c4747e925b9fc1db690",
#   "databaseURL": "https://lineweb-d1174.firebaseio.com/"
# };

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

def login(email,password):
    # print("Log in...")
    # email=input("Enter email: ")
    # password=input("Enter password: ")
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        if(login["idToken"]): 
            return login["idToken"]
        else:
            return None
        # print(auth.get_account_info(login['idToken']))
       # email = auth.get_account_info(login['idToken'])['users'][0]['email']
       # print(email)
    except:
        print("Invalid email or password")
    return None

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
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
botdict = {}
options = "\n選択肢一つを選択してください。\n 1. まったくその通りだ \n 2. どちらかというとそうだ  \n 3. ときどき思い当たることがある \n 4. そんなことはない"

indtxt = [
    ['ストレスがたまることでついつい食べてしまうタイプ', \
    'このタイプのリスクポイントは、つい食べてしまうことが続くことで、満腹感が鈍感に なりがち。 このタイプは、空腹感を満たすために油や砂糖の多いおやつや砂糖の多く入った飲料水選びがち。ドーナツ、ポテトチップス、クリームサンドクッキーを好むことが多い。',
    'ストレスがたまりやすいこのタイプは、一息整えてから温かい汁物やお茶を飲んでから食事を始めてみましょう。脳をリラックスさせるためにも楽しい食事過ごしましょう。うま味成分のグルタミン酸をプラスしたり、脳の疲れ解消にビタミンDを含む食品を摂ることがおすすめです。'],
    ['何かを食べていないと落ちつけないタイプ。',
    'このタイプのリスクポイントは、ついつい食べてしまうことが続き、少ししか食べていないのにブクブク太ってしまうと思い込んでいる。また、菓子パンが食事になっていることもある。食べすぎ飲みすぎることで、肌荒れや口内炎などになりやすい体質になりがち。食事が偏ることで、隠れ栄養不足になってしまい代謝が悪くなりやすい。'
    '買い物に行くとついつい買ってしまう習慣があるため、買い物の前の大豆サポニンがおすすめ。この習慣をストップするためには、BMAL１の分泌を意識した食べ方やある習慣をすると減らすことができます。'],
    ['食事は手軽に済ませ、早食べタイプ。','このタイプのリスクポイントは、早く食べることが習慣になっていること。早く食べすぎることで、食後の眠気にもつながることも。このような習慣は、睡眠不足や食事の不摂生により、燃焼しにくいカラダになりがち。',
    'よく噛む事とある意識をするだけで、胃腸がスッキリする。まずは、ナッツや根菜類を上手に取り入れること。おすすめの食べ合わせは、ある調味料＋フコダイン。',
    ],
    ['高カロリーの食べ物が大好きなタイプ。','このタイプのリスクポイントは、糖質＋脂質の食べ物を選びがち。食べる前に、ソースやマヨネーズをかけていませんか。その習慣はメタボリックシンドロームだけではなく、塩分の摂りすぎで血圧の上昇や、むくみやのどの渇きにつながることも。',
    '食事前の汁物や、朝一番の○○をすることで味覚が生まれ変わります。味覚の改善を助けてくれる亜鉛やグルタミン酸を含む食材を取り入れること。'],
    ['人一倍健康に気を付けて、ついつい頑張りすぎて疲れてしまうタイプ。','食事の時間を楽しむことより、体調がすぐれないのにも関わらず体に良いと思ったものを食べ続けてしまう。良いものを取り入れすぎて、健康を害してしまうことも。',
    '時には大好きなものを食べて気分転換。買い物の仕方やいつもと違う食材を使ってみるとさらに食が豊かになります。']
]

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
apiurl = 'https://lineweb.e-posture.jp/api/bot' 
client = requests.session()
app = Flask(__name__)

# botdict[event.mode]['line_bot_api'] = LineBotApi('lnoN3pNo/DUuie5L3OT9exNM+/WZzquIkqGIZdVFcOTHOAhdkNe8IXDilhrKQNrFLQViNJv0MVcZtIzaU7sFKoOkc9s657sq5xb64EtiVqbCoDPEwqt0xwZgkuFriqVOVKVQrP7sXhjR4dNQm5Gk1QdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('fb93092bbba827e36296a2cfdbdde14d')

rich_menu_to_create = RichMenu(
size=RichMenuSize(width=2500, height=1686),
selected=False,
name="Bot Menu",
chat_bar_text="Tap here",
areas=[RichMenuArea(
    bounds=RichMenuBounds(x=0, y=0, width=1250, height=693),
    action=MessageAction(label='text1', text='運動')),
    RichMenuArea(
    bounds=RichMenuBounds(x=1250, y=0, width=1250, height=693),
    action=MessageAction(label='text1', text='食事')),
    RichMenuArea(
    bounds=RichMenuBounds(x=0, y=693, width=1250, height=693),
    action=MessageAction(label='text1', text='姿勢')),
    RichMenuArea(
    bounds=RichMenuBounds(x=1250, y=693, width=1250, height=693),
    action=MessageAction(label='text1', text='記録')),
    RichMenuArea(
    bounds=RichMenuBounds(x=0, y=1386, width=2500, height=300),
    action=MessageAction(label='text1', text='リセット'))]
)

def addAllHandlers():
    global botdict

    allHandlersData = apicall(None,"/allhandlers",None)

    print("all handlers") 
    print(allHandlersData)
    print("all handlers Data end")
    if allHandlersData == None:
        allHandlersData = []
    # botdict["HhgIEQXfBgn8f1M3V2uU"] = {
    #         'handler': WebhookHandler('fb93092bbba827e36296a2cfdbdde14d'),
    #         'line_bot_api':  LineBotApi('lnoN3pNo/DUuie5L3OT9exNM+/WZzquIkqGIZdVFcOTHOAhdkNe8IXDilhrKQNrFLQViNJv0MVcZtIzaU7sFKoOkc9s657sq5xb64EtiVqbCoDPEwqt0xwZgkuFriqVOVKVQrP7sXhjR4dNQm5Gk1QdB04t89/1O/w1cDnyilFU=')
    #     }

    
    for handlerBot in allHandlersData:
        try:
            handlerbotid = handlerBot["botID"]
            channelSecret = handlerBot["channelSecret"]
            channelAccessToken =handlerBot["channelAccessToken"] 
            print("all handler values .. ")
            print(handlerbotid)
            print(channelSecret)
            print(channelAccessToken)


            newHandler = WebhookHandler(channelSecret)
            newHandler.add(MessageEvent,message=TextMessage)(handle_message)
            newHandler.add(FollowEvent)(handle_follow)
            newHandler.add(MessageEvent, message=ImageMessage)(handle_imagemessage)
            print(os.getcwd())
            new_bot_api = LineBotApi(channelAccessToken)
            rich_menu_id = new_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
            with open('./resources/PUI9T2n.jpg', 'rb') as f:
                new_bot_api.set_rich_menu_image(rich_menu_id, 'image/jpeg', f)
            new_bot_api.set_default_rich_menu(rich_menu_id)

            botdict[handlerbotid] = {
                'handler': newHandler,
                'line_bot_api': new_bot_api,
                'channelSecret': channelSecret
            }
        except:
            print("oh no, anyways")
    
    print("all handlers 2") 
    print(allHandlersData)

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

@app.route("/helloworld")
def helloworld():
    return "<h1>Hello World</h1>"
# what to do here
@app.route("/callback/<botid>", methods=['POST'])
def callback(botid):
    global botdict

    if botid not in botdict.keys():
            addAllHandlers()
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # botid = request.args.get("botid")

    # Get request body as text
    body = request.get_data(as_text=True)
    print("Request body init: " + body)

    jsonBody = json.loads(body)

    for event in jsonBody['events']:
        event['mode'] = botid

    

    body = json.dumps(jsonBody,ensure_ascii=False,separators=(',', ':'))


    hackerlak = hmac.new(
        botdict[botid]["channelSecret"].encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).digest()

    hackerlak = base64.b64encode(hackerlak).decode('utf-8')

    print("Request body: " + body)
    print(botdict)

    # Handle webhook body
    try:
        botdict[botid]["handler"].handle(body, hackerlak)
        print("Works here too")
    except InvalidSignatureError:
        print("callback::InvalidSignatureError")
        abort(422)

    return 'OK'


@app.route("/newbot")
def addNewHandler():
    body = request.get_json()
    #list of secret keys

    handlerbotid = body["botID"]
    channelSecret = body["channelSecret"]
    channelAccessToken = body["channelAccessToken"]
    

    newHandler = WebhookHandler(channelSecret)

    newHandler.add(MessageEvent,message=TextMessage)(handle_message)
    newHandler.add(FollowEvent)(handle_follow)
    newHandler.add(MessageEvent, message=ImageMessage)(handle_imagemessage)

    new_bot_api = LineBotApi(channelAccessToken)


    rich_menu_id = new_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    with open('./resources/PUI9T2n.jpg', 'rb') as f:
        new_bot_api.set_rich_menu_image(rich_menu_id, 'image/jpeg', f)
    new_bot_api.set_default_rich_menu(rich_menu_id)

    botdict[handlerbotid] = {
        'handler': newHandler,
        'line_bot_api': new_bot_api
    }

            




def handle_message(event):
    """ Here's all the messages will be handled and processed by the program """
    print("handleevent")
    print(event)
    resp,flag = statehandle(event)

    print("$$$$$$$$$$$$$$$")
    print(resp)
    print(flag)
    # # #print(event)
    # botdict[event.mode]['line_bot_api'].reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=resp))

    # botdict[event.mode]['botdict[event.mode]['line_bot_api']']

    if not flag:
        print("jugaad working")
        botdict[event.mode]['line_bot_api'].reply_message(
            event.reply_token,
            TextSendMessage(text=resp))

    else:
        botdict[event.mode]['line_bot_api'].reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="yo",contents=resp))


def handle_imagemessage(event):
    """ Here's all the messages will be handled and processed by the program """
    print("handleevent")
    print(event)
    resp,flag = imstatehandle(event)
    # #print(event)
    
    if not flag:
        print("jugaad working")
        botdict[event.mode]['line_bot_api'].reply_message(
            event.reply_token,
            TextSendMessage(text=resp))

    else:
        botdict[event.mode]['line_bot_api'].reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="yo",contents=resp))

def handle_follow(event):
    """ Here's all the messages will be handled and processed by the program """
    print("handleevent")
    print(event)
    print(state_dict)
    resp = followhandle(event)
    print(state_dict)
    #print(event)
    
    # print("jugaad working")
    botdict[event.mode]['line_bot_api'].reply_message(
        event.reply_token,
        TextSendMessage(text=resp))

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     """ Here's all the messages will be handled and processed by the program """
#     print("handleevent")
#     print(event)
#     resp,flag = statehandle(event)

#     print("$$$$$$$$$$$$$$$")
#     print(resp)
#     print(flag)
#     # # #print(event)
#     # botdict[event.mode]['line_bot_api'].reply_message(
#     #     event.reply_token,
#     #     TextSendMessage(text=resp))

#     if not flag:
#         print("jugaad working")
#         botdict[event.mode]['line_bot_api'].reply_message(
#             event.reply_token,
#             TextSendMessage(text=resp))

#     else:
#         botdict[event.mode]['line_bot_api'].reply_message(
#             event.reply_token,
#             FlexSendMessage(alt_text="yo",contents=resp))

# # @handler.add(MessageEvent,message=FlexM/essage)

# @handler.add(MessageEvent, message=ImageMessage)
# def handle_imagemessage(event):
#     """ Here's all the messages will be handled and processed by the program """
#     print("handleevent")
#     print(event)
#     resp,flag = imstatehandle(event)
#     # #print(event)
    
#     if not flag:
#         print("jugaad working")
#         botdict[event.mode]['line_bot_api'].reply_message(
#             event.reply_token,
#             TextSendMessage(text=resp))

#     else:
#         botdict[event.mode]['line_bot_api'].reply_message(
#             event.reply_token,
#             FlexSendMessage(alt_text="yo",contents=resp))

# @handler.add(FollowEvent)
# def handle_follow(event):
#     """ Here's all the messages will be handled and processed by the program """
#     print("handleevent")
#     print(event)
#     print(state_dict)
#     resp = followhandle(event)
#     print(state_dict)
#     #print(event)
    
#     # print("jugaad working")
#     botdict[event.mode]['line_bot_api'].reply_message(
#         event.reply_token,
#         TextSendMessage(text=resp))


    
        
    

def followhandle(event):
    print("followhandle")

    if(event.source.type == "user"):
        
        try:
            print("follow handle event")
            print(event)
            profile = botdict[event.mode]['line_bot_api'].get_profile(event.source.user_id)
        
        
            r = client.post(apiurl+'/followevent', data= json.dumps({"user_id": event.source.user_id,"bot_id": event.mode,"user_username": profile.display_name}), headers=authheaders())
            print(r)
            if(r != None and r.status_code == 200):
                print("ff")
                #print(event)
                print("gaygan")
        
                re = client.post(apiurl+'/greeting', data= json.dumps({"user_id": event.source.user_id,"bot_id": event.mode}), headers=authheaders())
                
                # if(re != None and re.status_code == 200):
                #     botdict[event.mode]['line_bot_api'].push_message(
                #         event.source.user_id,
                #         TextSendMessage(text=re["greet"])) 
                if(re != None and re.status_code == 200):
                    re = re.json()
                    botdict[event.mode]['line_bot_api'].push_message(
                        event.source.user_id,
                        FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage(re["greet"]))) 

                        
                else:
                    botdict[event.mode]['line_bot_api'].push_message(
                        event.source.user_id,
                        TextSendMessage(text="Hey there!!")) 
                # response = "正常にログインしました。 \n\n 選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
                responseOptions = ["運動","食事","姿勢","記録"]
                response = util.listTextMessageWithText(responseOptions)
                flag = True
                if event.source.user_id not in state_dict:
                    state_dict[event.source.user_id] = {"state": "start", "cq":1}                
                state_dict[event.source.user_id]['state'] = "menu_select"

                return "Follow Successful"
            else:

                print("Follow Failed")
                # state_dict[event.source.user_id]= {"state": "start", "cq":1}
                return 'Follow Failed'
        except LineBotApiError as e:
            print("Error in line bot api")
            return 'error in fetching profile'

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
        return "Not a valid input", False
    if event.mode not in botdict.keys():
        addAllHandlers()
    message_content = botdict[event.mode]['line_bot_api'].get_message_content(event.message.id)
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
        angnames= resp["angnames"]
    else: return "api failed", False

    print("gaygaygyaygaygyagyaygaygay")

    botdict[event.mode]['line_bot_api'].push_message(
        event.source.user_id,
        ImageSendMessage(original_content_url=orurl, preview_image_url=orurl))
        
    angtext=[]
    for angnam, ang  in zip(angnames, angles):
        angtext.append(angnam + ': '+ang)
    botdict[event.mode]['line_bot_api'].push_message(
        event.source.user_id,
        FlexSendMessage(alt_text="yo",contents=util.responseList( "角度", angtext)))

    resp = apicall(event, '/conditionprocess', {"user_id": event.source.user_id,"pose": pos, "direction": dir, "angles":angles,"bot_id": event.mode})
    if(resp): 
        print(resp)
        eva = resp["eval"]
        typ = resp["type"]
        responsetexts = resp["resp"]
    else: return "api failed", False     
    botdict[event.mode]['line_bot_api'].push_message(
        event.source.user_id,
        FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("Evaluation: "+eva+", Type: "+typ , weight=True)))
    
    if responsetexts is None:
        responsetexts = []
    
    for responsetext in responsetexts:
        botdict[event.mode]['line_bot_api'].push_message(
            event.source.user_id,
            FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage(responsetext)))
    
   
    state_dict[event.source.user_id]['state'] = "menu_select"
    # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
    responseOptions = ["運動","食事","姿勢","記録"]
    response = util.listTextMessageWithText(responseOptions)
    flag = True


    return response, flag
def statehandle(event):
    global questionaire
    global motionopt
    global responsehist
    response = 'ff'
    flag = False
    # false -> text, true -> flex 

    if event.source.user_id not in state_dict.keys(): 
        respNew = followhandle(event)
        return respNew,True
        
    ###########debugging################
    if event.message.text == 'リセット' :
        state_dict[event.source.user_id]['state'] = "start"
        state_dict[event.source.user_id]['cq'] = 1
        print("reset")
        response = "Reset"
    elif event.message.text in ["運動","食事","姿勢","記録"]:
        state_dict[event.source.user_id]['state'] = "menu_select"
        state_dict[event.source.user_id]['cq'] = 1
    ###########debugging################
    print("state")
    # #print(event)
    # print(event.source)
    # print(type(event))
    # print(type(event.source))
    # # print(len(event.source))
    # print(event.source.user_id)
    # print(event.source.user_id)
    print(state_dict[event.source.user_id]['state'] )
    print(state_dict)
    if state_dict[event.source.user_id]['state'] == "init":
        re = client.post(apiurl+'/greeting', data= json.dumps({"user_id": event.source.user_id,"bot_id": event.mode}), headers=authheaders())
        
        # if(re != None and re.status_code == 200):
        #     botdict[event.mode]['line_bot_api'].push_message(
        #         event.source.user_id,
        #         TextSendMessage(text=re["greet"])) 
        if(re != None and re.status_code == 200):
            re = re.json()
            botdict[event.mode]['line_bot_api'].push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage(re["greet"]))) 

                
        else:
            botdict[event.mode]['line_bot_api'].push_message(
                event.source.user_id,
                TextSendMessage(text="Hey there!!")) 
        # response = "正常にログインしました。 \n\n 選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessageWithText(responseOptions)
        flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"


    elif state_dict[event.source.user_id]['state'] == "start":
        print("nycbruh")
        # "Please select one option. \ n 1. Motion \ n 2. Meal \ n 3. Attitude \ n 4. Record"
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        # response = util.simpleTextMessage("選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録")
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessageWithText(responseOptions)
        flag = True
        print("ttttttttttttttttttt")
        print(response)
        # botdict[event.mode]['line_bot_api'].reply_message(
        #     event.reply_token,
        #     FlexSendMessage(alt_text="yo",contents=resp))
        # flag = True
        state_dict[event.source.user_id]['state'] = "menu_select"

    elif state_dict[event.source.user_id]['state'] == "menu_select":

        print("ffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        if event.message.text == '運動':

            resp = apicall(event, '/motionopt', {"user_id": event.source.user_id,"bot_id": event.mode})
            # f =  open('./resources/quesaire.json', encoding='utf8')
            # questionaire = json.load(f)
            if(resp): 
                print(resp)
                motionopt = resp["motionopt"]["items"]
                responsehist = resp["responsehist"]
            else: 
                return "api failed", False
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
            # botdict[event.mode]['line_bot_api'].set_default_rich_menu(back_menu_id)

        elif event.message.text == '食事':

            resp = apicall(event, '/questionaire', {"user_id": event.source.user_id,"bot_id": event.mode})
            # f =  open('./resources/quesaire.json', encoding='utf8')
            # questionaire = json.load(f)
            if(resp): questionaire = resp["questionaire"]
            else: return "api failed", False
            print("qqq")
            print(questionaire)
            
            # response = "アンケートを始めましょう: \n Q1) " + questionaire['questionItems'][0]['questionText'] + options
            if len(questionaire['questionItems']) == 0:
                botdict[event.mode]['line_bot_api'].push_message(
                    event.source.user_id,
                    FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("アンケートなし",False)))
                # print("options")
                # print(optionsAll)
                responseOptions = ["運動","食事","姿勢","記録"]
                response = util.listTextMessageWithText(responseOptions)
                flag = True
                state_dict[event.source.user_id]['state']= 'menu_select'

            else:
                optionsAll = makeoptions(questionaire['questionItems'][0]['choiceItems'])
                botdict[event.mode]['line_bot_api'].push_message(
                    event.source.user_id,
                    FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("Q1) " + questionaire['questionItems'][0]['questionText'],True)))
                print("options")
                print(optionsAll)
                response = util.listTextMessage(optionsAll,"アンケートを始めましょう")
                flag = True

                state_dict[event.source.user_id]['state']= 'questionaire'
            # botdict[event.mode]['line_bot_api'].set_default_rich_menu(back_menu_id)

        elif event.message.text == '姿勢':
            # response = "Enter Pose: \n1. Standing\n2. Sitting"
            response = util.listTextMessage(["スタンディング","座位"],"ポーズを入力する")
            flag = True
            state_dict[event.source.user_id]['state'] = 'selected_attitude'
            # botdict[event.mode]['line_bot_api'].set_default_rich_menu(back_menu_id)
        elif event.message.text == '記録':

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
            recs = ["身長","体重","脂肪率","筋量","血圧","筋力","柔軟性","血液検査"]
            resp = apicall(event, '/getrecords', {"bot_id": event.mode})
            if(resp): 
                recs = resp
            else: return "api failed", False
            # response = "何を録音したいですか？ \n 1) 身長 \n 2) 体重 \n 3) 脂肪率 \n 4) 筋量 \n 5) 血圧 \n 6) 筋力 \n 7) 柔軟性 \n 8) 血液検査" #update this line
            response = util.listTextMessage(recs,"何を録音したいですか？")
            flag = True
            state_dict[event.source.user_id]['state'] = 'selected_record'
            # botdict[event.mode]['line_bot_api'].set_default_rich_menu(back_menu_id)
        else:
            # "Please select a valid option."
            # response = "有効なオプションを選択してください。"
            response = util.simpleTextMessage("有効なオプションを選択してください。")
            flag = True

    elif state_dict[event.source.user_id]['state'] == 'selected_motion':

        resp = apicall(event, '/motionopt', {"user_id": event.source.user_id,"bot_id": event.mode})
        # f =  open('./resources/quesaire.json', encoding='utf8')
        # questionaire = json.load(f)
        if(resp): 
            motionopt = resp["motionopt"]["items"]
            responsehist = resp["responsehist"]
        else: return "api failed", False
        # print(questionaire)


        itemselected = int(event.message.text)-1
        if itemselected >= len(motionopt) or itemselected < 0:
            botdict[event.mode]['line_bot_api'].push_message(
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

        resp = apicall(event, '/motionopt', {"user_id": event.source.user_id,"bot_id": event.mode})
        # f =  open('./resources/quesaire.json', encoding='utf8')
        # questionaire = json.load(f)
        if(resp): 
            motionopt = resp["motionopt"]["items"]
            responsehist = resp["responsehist"]
        else: return "api failed", False
        print("qqq5")
        # print(questionaire)

            
        if optionselected >= len(motionopt[responsehist["selected_motion"]]["subItems"]) or optionselected < 0:
            botdict[event.mode]['line_bot_api'].push_message(
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

        resp = apicall(event, '/motionopt', {"user_id": event.source.user_id,"bot_id": event.mode})
        # f =  open('./resources/quesaire.json', encoding='utf8')
        # questionaire = json.load(f)
        if(resp): 
            motionopt = resp["motionopt"]["items"]
            responsehist = resp["responsehist"]
        else: return "api failed", False
        print("qqq6")
        # print(questionaire)

            
        if elmntselected >= len(motionopt[responsehist["selected_motion"]]["subItems"][responsehist["selected_motion_item"]]["subSubItems"]) or elmntselected < 0:
            # botdict[event.mode]['line_bot_api'].push_message(
            #     event.source.user_id,
            #     TextSendMessage(text="Please select a valid response."))  

            botdict[event.mode]['line_bot_api'].push_message(
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


            # botdict[event.mode]['line_bot_api'].push_message(
            #     event.source.user_id,
            #     TextSendMessage(text="Thank You for your response."))  

            botdict[event.mode]['line_bot_api'].push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))


            respmsg=apicall(event, '/clearhistmotionopt', {"user_id": event.source.user_id,"data": responsehist,"bot_id": event.mode})

            # for msg in respmsg["text"]:
            #     botdict[event.mode]['line_bot_api'].push_message(
            #         event.source.user_id,
            #         TextSendMessage(text=msg))  

            for msg in respmsg["text"]:
                botdict[event.mode]['line_bot_api'].push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage(msg)))  


            print(respmsg["image"])

            botdict[event.mode]['line_bot_api'].push_message(
                event.source.user_id,
                TextSendMessage(text=respmsg["image"]))
                
            if respmsg["image"] is not None:
                botdict[event.mode]['line_bot_api'].push_message(
                    event.source.user_id,
                    ImageSendMessage(original_content_url=respmsg["image"],preview_image_url=respmsg["image"]))  

            # response= "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
            responseOptions = ["運動","食事","姿勢","記録"]
            response = util.listTextMessageWithText(responseOptions)
            flag = True
             
            responsehist.clear()
            state_dict[event.source.user_id]['state']='menu_select'
    elif state_dict[event.source.user_id]['state'] == 'questionaire':

        resp = apicall(event, '/questionaire', {"user_id": event.source.user_id,"bot_id": event.mode})
        # f =  open('./resources/quesaire.json', encoding='utf8')
        # questionaire = json.load(f)
        if(resp): 
            questionaire = resp["questionaire"]
            responsehist = resp["responsehist"]
        else: return "api failed", False
        print("qqq2")
        # print(questionaire)
        choiceselected = int(event.message.text)-1
        if choiceselected < 0 or choiceselected >= len(questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['choiceItems']):
            options = makeoptions(questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['choiceItems'])

            # response = "Q" + str(state_dict[event.source.user_id]['cq'])+ ") "+ questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['questionText'] + options

            botdict[event.mode]['line_bot_api'].push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("Q" + str(state_dict[event.source.user_id]['cq'])+ ") "+ questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['questionText'],True)))

            response = util.listTextMessage(options,"アンケートを始めましょう")
            flag = True
        else:
            responsehist["questionaire"][str(state_dict[event.source.user_id]['cq'])] = {"choicenum": choiceselected, "choiceWeight": questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['choiceItems'][choiceselected-1]["choiceWeight"], "questionType": questionaire['questionItems'][state_dict[event.source.user_id]['cq']-1]['questionType']}
            if state_dict[event.source.user_id]['cq'] >= len(questionaire['questionItems']):
                print(state_dict[event.source.user_id]['cq'])
                
                state_dict[event.source.user_id]['cq']=1
                # botdict[event.mode]['line_bot_api'].push_message(
                #     event.source.user_id,
                #     TextSendMessage(text="Thank You for your responses."))     
                botdict[event.mode]['line_bot_api'].push_message(
                    event.source.user_id,
                    FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))  

                # response= "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
                responseOptions = ["運動","食事","姿勢","記録"]
                response = util.listTextMessageWithText(responseOptions)
                flag = True

                state_dict[event.source.user_id]['state'] = "menu_select"
                res = apicall(event, '/clearhistques',{"user_id": event.source.user_id, "data": responsehist, "questionName": questionaire['questionName'],"bot_id": event.mode}, nores=True)
                if res:
                    ind = res['ques']
                else:
                    ind = 0
                for txt in indtxt[ind]:
                    botdict[event.mode]['line_bot_api'].push_message(
                        event.source.user_id,
                        FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage(txt)))
                responsehist.clear()

                state_dict[event.source.user_id]['state']='menu_select'
            else:
                options = makeoptions(questionaire['questionItems'][state_dict[event.source.user_id]['cq']]['choiceItems'])
                # response = "Q" + str(state_dict[event.source.user_id]['cq']+1)+ ") "+ questionaire['questionItems'][state_dict[event.source.user_id]['cq']]['questionText'] + options
                botdict[event.mode]['line_bot_api'].push_message(
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
        elif event.message.text == '3':
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
        elif event.message.text == '3':
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

        recs = ["身長","体重","脂肪率","筋量","血圧","筋力","柔軟性","血液検査"]
        resp = apicall(event, '/getrecords', {"bot_id": event.mode})
        if(resp): 
            recs = resp
        else: return "api failed", False
        ## record the value here
        if int(event.message.text) >= 1 and int(event.message.text)<= len(recs):
            state_dict[event.source.user_id]['recordselect'] = recs[int(event.message.text)-1]
            state_dict[event.source.user_id]['state'] ='record_value'
        else:
            botdict[event.mode]['line_bot_api'].push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("有効なオプションを選択してください。")))  
            response = util.listTextMessage(recs,"何を録音したいですか？")
            state_dict[event.source.user_id]['state'] = 'selected_record'        
            # response = "選択肢一つを選択してください。"
            # response = util.simpleTextMessage("選択肢一つを選択してください。")
            # for option in motionopt[responsehist["selected_motion"]]["subItems"]:
            #     response+="\n"+option["subItemName"]
    
    elif state_dict[event.source.user_id]['state'] == 'record_value':
        apicall(event,"/user_record",{"user_id": event.source.user_id,"data": {"value": float(event.message.text),"type": state_dict[event.source.user_id]['recordselect'],"user_id": event.source.user_id},"bot_id": event.mode}, nores=True)
        # response = "ご返信ありがとうございます。"
        # botdict[event.mode]['line_bot_api'].push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="Thank You for your response."))  
        botdict[event.mode]['line_bot_api'].push_message(
                event.source.user_id,
                FlexSendMessage(alt_text="yo",contents=util.simpleTextMessage("ご回答ありがとうございました。")))
        # response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        responseOptions = ["運動","食事","姿勢","記録"]
        response = util.listTextMessageWithText(responseOptions)
        flag = True
        state_dict[event.source.user_id]['recordselect'] = ""
        state_dict[event.source.user_id]['state'] = "menu_select"


            

    else:
        response = "errrrr"
    return response,flag






if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    addAllHandlers()



