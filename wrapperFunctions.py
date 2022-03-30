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


bot_id = "lkMI2xb0HpBdCpeOZpvM"
apiurl = 'https://linewebbackend.herokuapp.com/api/bot' 
client = requests.session()
app = Flask(__name__)

def authheaders():
    return {
          "Accept": "application/json",
          "Content-Type": "application/json",
        }


def apicall(event, url, postdata):
    if(not event):
        r = client.get(apiurl+url, headers=authheaders())
        print(r)
        if(r != None and r.status_code == 200):
            return r.json()
        else:
            return None
    if(event.source.type == "user"):
        r = client.post(apiurl+url, data= postdata, headers=authheaders())
        print(r)
        if(r != None and r.status_code == 200):
            return r.json()
        else:
            return None

print(apicall(None, '/userlist', {"bot_id": bot_id}))

# import os
# import json

# import copy

# from flask import Flask, request, abort

# from linebot import (
#     LineBotApi, WebhookHandler
# )
# from linebot.exceptions import (
#     InvalidSignatureError
# )
# from linebot.models import (
#     MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
# )
# from linebot.models.flex_message import BubbleContainer, FlexContainer


# from linebot.models import rich_menu
# from linebot.models.rich_menu import *
# from linebot.models.actions import (MessageAction, RichMenuSwitchAction)



# f =  open('./resources/question.json', encoding='utf8')
# questionflex = json.load(f)
# f.close()


# optionsQuestionnaire = ['まったくその通りだ','どちらかというとそうだ','ときどき思い当たることがある','そんなことはない']

# def questionnaireWrapper(ques):
#     # ques is a string
#     question = copy.deepcopy(questionflex)
#     question["body"]["contents"][1]["text"] = ques
    
#     with open("sample.json", "w") as outfile:
#         json.dump(question, outfile)

#     return question


# questionnaireWrapper("arigato")


    