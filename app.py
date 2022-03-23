from asyncio.windows_events import NULL
from http import client
import os
import json
import requests
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)
from linebot.models.flex_message import BubbleContainer, FlexContainer


from linebot.models import rich_menu
from linebot.models.rich_menu import *
from linebot.models.actions import (MessageAction, RichMenuSwitchAction)

state_dict = {}
# state_dict["state"] = "start"
# state_dict["cq"] = 1
questionaire = {}
questionflex = {}
motionopt = {}
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

bot_id = "lkMI2xb0HpBdCpeOZpvM"
apiurl = 'http://localhost:3000/bot' 
client = requests.session()
app = Flask(__name__)

line_bot_api = LineBotApi('lnoN3pNo/DUuie5L3OT9exNM+/WZzquIkqGIZdVFcOTHOAhdkNe8IXDilhrKQNrFLQViNJv0MVcZtIzaU7sFKoOkc9s657sq5xb64EtiVqbCoDPEwqt0xwZgkuFriqVOVKVQrP7sXhjR4dNQm5Gk1QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fb93092bbba827e36296a2cfdbdde14d')


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
    if event.type == "message": 
        resp = statehandle(event)
        print(event)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=resp))
    if event.type == "follow": 
        resp = followhandle(event)
        print(event)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=resp))

def authheaders():
    return {
          "Accept": "application/json",
          "Content-Type": "application/json",
        }

def followhandle(event):
    if(event.source.type == "user"):
        r = client.post(apiurl+'/followevent', data= {"userId": event.source.userId}, headers=authheaders())
        print(r)
        if(r.status_code == 200):
            state_dict[event.source.userId]= {"state": "start", "cq":1}
            return 'added'
        else:
            return 'error'
    
def apicall(event, url, postdata):
    if(event.source.type == "user"):
        r = client.post(apiurl+url, data= postdata, headers=authheaders())
        print(r)
        if(r.status_code == 200):
            return r.json()
        else:
            return NULL

def statehandle(event):

    response = ''

    ###########debugging################
    if event.message.text.lower() == 'back' :
        state_dict[event.source.userId]['state'] = "start"
        state_dict[event.source.userId]['cq'] = 1
        # print(line_bot_api.get_rich_menu_list())
        response = "rebooted"
    ###########debugging################

    if state_dict[event.source.userId]['state'] == "start":
        print("nycbruh")
        # "Please select one option. \ n 1. Motion \ n 2. Meal \ n 3. Attitude \ n 4. Record"
        response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        state_dict[event.source.userId]['state'] = "menu_select"

    elif state_dict[event.source.userId]['state'] == "menu_select":
        if event.message.text == '1':
            response = "選択肢一つを選択してください。"
            for item in motionopt:
                response+= "\n"+item["label"]
            state_dict[event.source.userId]['state'] = 'selected_motion'
            # line_bot_api.set_default_rich_menu(back_menu_id)

        elif event.message.text == '2':

            resp = apicall(event, '/questionaire', {"bot_id": bot_id})
            # f =  open('./resources/quesaire.json', encoding='utf8')
            # questionaire = json.load(f)
            global questionaire
            if(resp): questionaire = resp
            else: response = "有効なオプションを選択してください。"
            print("qqq")
            print(questionaire)
            
            response = "アンケートを始めましょう: \n Q1) " + questionaire['questionItems'][0]['questionText'] + options
            state_dict[event.source.userId]['state']= 'questionaire'
            # line_bot_api.set_default_rich_menu(back_menu_id)

        elif event.message.text == '3':
            response = "still to be updated"
            state_dict[event.source.userId]['state'] = 'selected_attitude'
            # line_bot_api.set_default_rich_menu(back_menu_id)
        elif event.message.text == '4':
            response = "still to be updated"
            state_dict[event.source.userId]['state'] = 'selected_record'
            # line_bot_api.set_default_rich_menu(back_menu_id)
        else:
            # "Please select a valid option."
            response = "有効なオプションを選択してください。"

    elif state_dict[event.source.userId]['state'] == 'selected_motion':
        itemselected = int(event.message.text)-1
        if itemselected >= len(motionopt) or itemselected < 0:
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text="Please select a valid response."))            
            response = "選択肢一つを選択してください。"
            for item in motionopt:
                response+= "\n"+item["label"]
            state_dict[event.source.userId]['state'] = 'selected_motion'
        else:
            responsehist["selected_motion"]=itemselected
            response = "選択肢一つを選択してください。"
            for option in motionopt[itemselected]["subopt"]:
                response+="\n"+option["label"]
            state_dict[event.source.userId]['state'] = 'selected_motion_item'
    elif state_dict[event.source.userId]['state'] == 'selected_motion_item':
        optionselected = int(event.message.text)-1
        if optionselected >= len(motionopt[responsehist["selected_motion"]]["subopt"]) or optionselected < 0:
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text="Please select a valid response."))            
            response = "選択肢一つを選択してください。"
            for option in motionopt[responsehist["selected_motion"]]["subopt"]:
                response+="\n"+option["label"]
            state_dict[event.source.userId]['state'] = 'selected_motion_item'
        else:
            responsehist["selected_motion_item"]=optionselected
            response = "選択肢一つを選択してください。"
            for elmnt in motionopt[responsehist["selected_motion"]]["subopt"][optionselected]["subtext"]:
                response+="\n"+elmnt
            state_dict[event.source.userId]['state'] = 'selected_motion_item_option'
    elif state_dict[event.source.userId]['state'] == 'selected_motion_item_option':
        elmntselected = int(event.message.text)-1
        if elmntselected >= len(motionopt[responsehist["selected_motion"]]["subopt"][responsehist["selected_motion_item"]]["subtext"]) or elmntselected < 0:
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text="Please select a valid response."))            
            response = "選択肢一つを選択してください。"
            for elmnt in motionopt[responsehist["selected_motion"]]["subopt"][responsehist["selected_motion_item"]]["subtext"]:
                response+="\n"+elmnt
            state_dict[event.source.userId]['state'] = 'selected_motion_item_option'
        else:
            responsehist["selected_motion_item_option"]=elmntselected
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text="Thank You for your response."))            
            response= "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
            responsehist.clear()
            state_dict[event.source.userId]['state']='menu_select'
    elif state_dict[event.source.userId]['state'] == 'questionaire':
        if state_dict[event.source.userId]['cq'] >= len(questionaire['questionItems']):
            print(state_dict[event.source.userId]['cq'])
            
            state_dict[event.source.userId]['cq']=1
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text="Thank You for your responses."))            
            response= "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
            state_dict[event.source.userId]['state']='menu_select'
        else:
            response = "Q" + str(state_dict[event.source.userId]['cq']+1)+ ") "+ questionaire['questionItems'][state_dict[event.source.userId]['cq']]['questionText'] + options
            state_dict[event.source.userId]['cq']+=1    
    else:
        response = "errrrr"
    return response  

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



