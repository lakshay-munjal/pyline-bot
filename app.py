import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

state_dict = {}
state_dict["state"] = "start"
 
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

    response = ''

    ###########debugging################
    if event.message.text == 'reboot':
        state_dict['state'] = "start"
        response = "rebooted"
    ###########debugging################

    elif state_dict['state'] == "start":
        # "Please select one option. \ n 1. Motion \ n 2. Meal \ n 3. Attitude \ n 4. Record"
        response = "選択肢一つを選択してください。\n 1. 運動 \n 2. 食事  \n 3. 姿勢 \n 4. 記録"
        state_dict['state'] = "menu_select"

    elif state_dict['state'] == "menu_select":
        if event.message.text == '1':
            # Please select one option. \ n 1. Stretch \ n 2. Self-weight exercise \ n 3. Item 1 \ n 4. Item 2 \ n 5. Item 3 \ n 6. Customize
            response = "選択肢一つを選択してください。\n 1. ストレッチ \n 2. 自重運動  \n 3. アイテム１ \n 4. アイテム２ \n 5. アイテム３\n 6. カスタマイズ"
            state_dict['state'] = 'selected_motion'

        elif event.message.text == '2':
            response = "still to be updated"
            state_dict['state'] = 'selected_meal'


        elif event.message.text == '3':
            response = "still to be updated"
            state_dict['state'] = 'selected_attitude'

        elif event.message.text == '4':
            response = "still to be updated"
            state_dict['state'] = 'selected_record'

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
        



    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
