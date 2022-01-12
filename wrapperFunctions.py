import os
import json

import copy

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



f =  open('./resources/question.json', encoding='utf8')
questionflex = json.load(f)
f.close()


optionsQuestionnaire = ['まったくその通りだ','どちらかというとそうだ','ときどき思い当たることがある','そんなことはない']

def questionnaireWrapper(ques):
    # ques is a string
    question = copy.deepcopy(questionflex)
    question["body"]["contents"][1]["text"] = ques
    
    with open("sample.json", "w") as outfile:
        json.dump(question, outfile)

    return question


questionnaireWrapper("arigato")


    