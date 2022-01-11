import os
import json
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
state_dict["state"] = "start"
state_dict["cq"] = 1
questionaire = {}
questionflex = {}
options = "\n選択肢一つを選択してください。\n 1. まったくその通りだ \n 2. どちらかというとそうだ  \n 3. ときどき思い当たることがある \n 4. そんなことはない"

f =  open('./resources/quesaire.json', encoding='utf8')
questionaire = json.load(f)
f.close()

f =  open('./resources/question.json', encoding='utf8')
questionflex = json.load(f)
f.close()
 
 
app = Flask(__name__)

line_bot_api = LineBotApi('lnoN3pNo/DUuie5L3OT9exNM+/WZzquIkqGIZdVFcOTHOAhdkNe8IXDilhrKQNrFLQViNJv0MVcZtIzaU7sFKoOkc9s657sq5xb64EtiVqbCoDPEwqt0xwZgkuFriqVOVKVQrP7sXhjR4dNQm5Gk1QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fb93092bbba827e36296a2cfdbdde14d')

# def richmenswitch(text, alias):
#     RichMenuSwitchAction(rich_menu_alias_id="back_menu_alias", data="menswi1")
#     MessageAction(text = text)

# rich_menu_to_create = RichMenu(
#     size=RichMenuSize(width=2500, height=1686),
#     selected=True,
#     name="Nice richmenu",
#     chat_bar_text="RMenu",
#     areas=[RichMenuArea(
#         bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
#         action=RichMenuSwitchAction(rich_menu_alias_id="back_menu_alias", data="menswi1")),
#         RichMenuArea(
#         bounds=RichMenuBounds(x=1250, y=0, width=1250, height=843),
#         action=RichMenuSwitchAction(rich_menu_alias_id="back_menu_alias", data="menswi2")),
#         RichMenuArea(
#         bounds=RichMenuBounds(x=0, y=843, width=1250, height=843),
#         action=RichMenuSwitchAction(rich_menu_alias_id="back_menu_alias", data="menswi3")),
#         RichMenuArea(
#         bounds=RichMenuBounds(x=1250, y=843, width=1250, height=843),
#         action=RichMenuSwitchAction(rich_menu_alias_id="back_menu_alias", data="menswi4"))]
# )
# rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
# back_menu_to_create = RichMenu(
#     size=RichMenuSize(width=2500, height=843),
#     selected=True,
#     name="Nice backmenu",
#     chat_bar_text="RMenu",
#     areas=[RichMenuArea(
#         bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
#         action=RichMenuSwitchAction(rich_menu_alias_id="rich_menu_alias", data="menswiBack"))]
# )
# back_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
# with open("./resources/richmenu.jpg", 'rb') as f:
#     line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)
# with open("./resources/backmenu.jpg", 'rb') as g:
#     line_bot_api.set_rich_menu_image(back_menu_id, "image/jpeg", g)
# line_bot_api.create_rich_menu_alias(RichMenuAlias(rich_menu_alias_id= "rich_menu_alias", rich_menu_id= rich_menu_id))
# line_bot_api.create_rich_menu_alias(RichMenuAlias(rich_menu_alias_id= "back_menu_alias", rich_menu_id= back_menu_id))
# line_bot_api.set_default_rich_menu(rich_menu_id)

# print("check "+str(len(line_bot_api.get_rich_menu_list(timeout = 2))))

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
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text=resp))

        # debug

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(contents=questionflex,alt_text="yo"))

def statehandle(event):

    response = ''

    ###########debugging################
    if event.message.text.lower() == 'back' :
        state_dict['state'] = "start"
        state_dict['cq'] = 1
        # print(line_bot_api.get_rich_menu_list())
        response = "rebooted"
    ###########debugging################

    if state_dict['state'] == "start":
        print("nycbruh")
        # "Please select one option. \ n 1. Motion \ n 2. Meal \ n 3. Attitude \ n 4. Record"
        response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        state_dict['state'] = "menu_select"

    elif state_dict['state'] == "menu_select":
        if event.message.text == '1':
            # Please select one option. \ n 1. Stretch \ n 2. Self-weight exercise \ n 3. Item 1 \ n 4. Item 2 \ n 5. Item 3 \ n 6. Customize
            response = "選択肢一つを選択してください。\n 1. ストレッチ \n 2. 自重運動  \n 3. アイテム１ \n 4. アイテム２ \n 5. アイテム３\n 6. カスタマイズ"
            state_dict['state'] = 'selected_motion'
            # line_bot_api.set_default_rich_menu(back_menu_id)

        elif event.message.text == '2':

            # f =  open('./resources/quesaire.json', encoding='utf8')
            # questionaire = json.load(f)
            print("qqq")
            print(questionaire)
            
            response = "アンケートを始めましょう: \n Q1) " + questionaire['questions'][0]['question'] + options
            state_dict['state']= 'questionaire'
            # line_bot_api.set_default_rich_menu(back_menu_id)

        elif event.message.text == '3':
            response = "still to be updated"
            state_dict['state'] = 'selected_attitude'
            # line_bot_api.set_default_rich_menu(back_menu_id)
        elif event.message.text == '4':
            response = "still to be updated"
            state_dict['state'] = 'selected_record'
            # line_bot_api.set_default_rich_menu(back_menu_id)
        else:
            # "Please select a valid option."
            response = "有効なオプションを選択してください。"

    elif state_dict['state'] == 'selected_motion':
        if event.message.text == '1':
            # Please select one option. \ n 1. Whole body \ n 2. Head / neck \ n 3. Shoulders / chest \ n 4. Waist / back \ n 5. Knees / feet \ n 6. Customize
            response = "選択肢一つを選択してください。\n 1. 全身 \n 2. 頭・首  \n 3. 肩･胸 \n 4. 腰・背 \n 5. 膝・足\n 6. カスタマイズ"
            state_dict['state'] = 'selected_motion_strech'


        elif event.message.text == '2':
            response = "still to be updated"
            state_dict['state'] = 'selected_motion_self_weight'


        elif event.message.text == '3':
            response = "still to be updated"
            state_dict['state'] = 'selected_motion_item1'

        elif event.message.text == '4':
            response = "still to be updated"
            state_dict['state'] = 'selected_motion_item2'

        elif event.message.text == '5':
            response = "still to be updated"
            state_dict['state'] = 'selected_motion_item3'
        
        elif event.message.text == '6':
            response = "still to be updated"
            state_dict['state'] = 'selected_motion_customize'

        else:
            # "Please select a valid option."
            response = "有効なオプションを選択してください。"

    elif state_dict['state'] == 'questionaire':
        if state_dict['cq'] >= len(questionaire['questions']):
            print(state_dict['cq'])
            
            state_dict['cq']=1
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text="Thank You for your responses."))            
            response= "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
            state_dict['state']='menu_select'
        else:
            response = "Q" + str(state_dict['cq']+1)+ ") "+ questionaire['questions'][state_dict['cq']]['question'] + options
            state_dict['cq']+=1
    elif state_dict['state'] == 'selected_motion_strech':
        if event.message.text == '1':
            # Please select one option. \ n 1. Dull \ n 2. Easy to get tired \ n 3. Swelling \ n 4. Shortness of breath \ n 5. Hot flashes \ n 6. Can't sleep
            response = "選択肢一つを選択してください。\n 1. だるい \n 2. 疲れやすい  \n 3. むくみ \n 4. 息切れがする \n 5. のぼせ\n 6. 眠れない"
            state_dict['state'] = 'selected_motion_strech_wholebody'

        elif event.message.text == '2':
            response = "still to be updated"
            state_dict['state'] = 'selected_motion_strech_headneck'

        elif event.message.text == '3':
            response = "still to be updated"
            state_dict['state'] = 'selected_motion_strech_shoulderchest'


        elif event.message.text == '4':
            response = "still to be updated"
            state_dict['state'] = 'selected_motion_strech_waistback'

        elif event.message.text == '5':
            response = "still to be updated"
            state_dict['state'] = 'selected_motion_strech_kneesfeet'

        elif event.message.text == '6':
            response = "still to be updated"
            state_dict['state'] = 'selected_motion_strech_customize'

        else:
            # "Please select a valid option."
            response = "有効なオプションを選択してください。"
        

    else:
        response = "errrrr"
    return response  

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



