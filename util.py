# from msilib import _directories





def func():
    dict1 = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "姿勢画像の送信",
                "weight": "bold",
                "size": "lg",
                "align": "center"
            },
            {
                "type": "text",
                "text": "どちらで送信しますか？",
                "wrap": True,
                "align": "center",
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "uri",
                    "label": "カメラ",
                    "uri": "https://line.me/R/nv/camera/",
                    "altUri": {
                        "desktop": "https://line.me/R/nv/camera/"
                    }
                    },
                    "style": "secondary",
                    "height": "sm"
                },
                {
                    "type": "button",
                    "action": {
                    "type": "uri",
                    "label": "画像",
                    "uri": "https://line.me/R/nv/cameraRoll/single",
                    "altUri": {
                        "desktop": "https://line.me/R/nv/cameraRoll/single"
                    }
                    },
                    "style": "secondary",
                    "height": "sm",
                    "adjustMode": "shrink-to-fit"
                }
                ]
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": []
        },
        "styles": {
            "body": {
            "backgroundColor": "#F4F3F9"
            },
            "footer": {
            "separator": True,
            "backgroundColor": "#F4F3F9"
            }
        }
    }
    return dict1



def func2():
    dict1 = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "食事",
                "weight": "bold",
                "size": "lg",
                "align": "center"
            },
            {
                "type": "text",
                "text": "下からご希望の項目をお選びください。",
                "wrap": True,
                "align": "center",
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "lg",
                    "contents": [
                    {
                        "type": "text",
                        "text": "・食事アンケート",
                        "size": "md",
                        "align": "start",
                        "weight": "bold",
                        "flex": 5,
                        "gravity": "center",
                        "margin": "sm",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": "選択",
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "flex": 2,
                        "offsetStart": "12px",
                        "weight": "bold",
                        "decoration": "underline",
                        "action": {
                        "type": "message",
                        "label": "action",
                        "data": "shokuji="
                        }
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "lg",
                    "contents": [
                    {
                        "type": "text",
                        "text": "・カスタマイズ",
                        "size": "md",
                        "align": "start",
                        "weight": "bold",
                        "flex": 5,
                        "gravity": "center",
                        "margin": "sm",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": "選択",
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "flex": 2,
                        "offsetStart": "12px",
                        "weight": "bold",
                        "decoration": "underline",
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": "http://yahoo.co.jp/"
                        }
                    }
                    ]
                }
                ]
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": []
        },
        "styles": {
            "body": {
            "backgroundColor": "#F4F3F9"
            },
            "footer": {
            "separator": True,
            "backgroundColor": "#F4F3F9"
            }
        }
        }
    return dict1


def simpleContent(msg):
    
    return {
        "type": "text",
        "text": ". " + msg,
        "wrap": True
    }
    
    

def simpleListTextMessage(msgs):
    n = len(msgs)
    msgList = []
    for el in msgs:
        msgList.append(simpleContent(el))
    
    dictResp = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": msgList
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": []
        },
        "styles": {
            "body": {
            "backgroundColor": "#F4F3F9"
            },
            "footer": {
            "separator": False,
            "backgroundColor": "#F4F3F9"
            }
        }
    }

    return dictResp

    



def simpleTextMessage(msg,weight=False):
    if weight:
        return {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": msg,
                    "wrap": True,
                    "weight": "bold"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": []
            },
            "styles": {
                "body": {
                "backgroundColor": "#F4F3F9"
                },
                "footer": {
                "separator": False,
                "backgroundColor": "#F4F3F9"
                }
            }
        }

    else:
        return {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": msg,
                    "wrap": True
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": []
            },
            "styles": {
                "body": {
                "backgroundColor": "#F4F3F9"
                },
                "footer": {
                "separator": False,
                "backgroundColor": "#F4F3F9"
                }
            }
    }




def responseList(headingMsg,respItems):

    respList = []
    for resp in respItems:
        respList.append(simpleContent(resp))

    listDict = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": headingMsg,
                "wrap": True,
                "align": "center",
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "spacing": "sm",
                "contents": respList
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": []
        },
        "styles": {
            "body": {
            "backgroundColor": "#F4F3F9"
            },
            "footer": {
            "separator": True,
            "backgroundColor": "#F4F3F9"
            }
        }
    }

    return listDict


def singleElementofList(index,msg):
    contentdict = {
        "type": "box",
        "layout": "horizontal",
        "margin": "lg",
        "contents": [
            {
            "type": "text",
            "text": str(index+1)+") "+ msg,
            "size": "md",
            "align": "start",
            "weight": "bold",
            "flex": 5,
            "gravity": "center",
            "margin": "sm",
            "wrap": True
            },
            {
            "type": "text",
            "text": "選択",
            "size": "lg",
            "color": "#111111",
            "align": "center",
            "flex": 2,
            "offsetStart": "12px",
            "weight": "bold",
            "decoration": "underline",
            "action": {
                "type": "message",
                "label": "action",
                "text": str(index+1)
            }
            }
        ]
    }
    return contentdict

def listTextMessage(optionsList,question="下からご希望の項目をお選びください。"):
    n = len(optionsList)

    msgList = []

    for i in range(n):
        msgList.append(singleElementofList(i,optionsList[i]))

    listDict = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "メニュー",
                "weight": "bold",
                "size": "lg",
                "align": "center"
            },
            {
                "type": "text",
                "text": question,
                "wrap": True,
                "align": "center",
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "spacing": "sm",
                "contents": msgList
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": []
        },
        "styles": {
            "body": {
            "backgroundColor": "#F4F3F9"
            },
            "footer": {
            "separator": True,
            "backgroundColor": "#F4F3F9"
            }
        }
    }

    return listDict









#####################


# {
#   "type": "bubble",
#   "size": "kilo",
#   "body": {
#     "type": "box",
#     "layout": "vertical",
#     "contents": [
#       {
#         "type": "text",
#         "text": "記録",
#         "weight": "bold",
#         "size": "lg",
#         "align": "center"
#       },
#       {
#         "type": "text",
#         "text": "下からご希望の項目をお選びください。",
#         "wrap": true,
#         "align": "center",
#         "margin": "md"
#       },
#       {
#         "type": "separator",
#         "margin": "sm"
#       },
#       {
#         "type": "box",
#         "layout": "vertical",
#         "margin": "md",
#         "spacing": "sm",
#         "contents": [
#           {
#             "type": "box",
#             "layout": "horizontal",
#             "margin": "lg",
#             "contents": [
#               {
#                 "type": "text",
#                 "text": "・各種記録/会員ページ",
#                 "size": "md",
#                 "align": "start",
#                 "weight": "bold",
#                 "flex": 5,
#                 "gravity": "center",
#                 "margin": "sm",
#                 "wrap": true
#               },
#               {
#                 "type": "text",
#                 "text": "選択",
#                 "size": "lg",
#                 "color": "#111111",
#                 "align": "center",
#                 "flex": 2,
#                 "offsetStart": "12px",
#                 "weight": "bold",
#                 "decoration": "underline",
#                 "action": {
#                   "type": "uri",
#                   "label": "action",
#                   "uri": "https://liff.line.me/1655722756-xD1G698J"
#                 }
#               }
#             ]
#           },
#           {
#             "type": "box",
#             "layout": "horizontal",
#             "margin": "lg",
#             "contents": [
#               {
#                 "type": "text",
#                 "text": "・フォーム1",
#                 "size": "md",
#                 "align": "start",
#                 "weight": "bold",
#                 "flex": 5,
#                 "gravity": "center",
#                 "margin": "sm",
#                 "wrap": true
#               },
#               {
#                 "type": "text",
#                 "text": "選択",
#                 "size": "lg",
#                 "color": "#111111",
#                 "align": "center",
#                 "flex": 2,
#                 "offsetStart": "12px",
#                 "weight": "bold",
#                 "decoration": "underline",
#                 "action": {
#                   "type": "uri",
#                   "label": "action",
#                   "uri": "http://yahoo.co.jp/"
#                 }
#               }
#             ]
#           },
#           {
#             "type": "box",
#             "layout": "horizontal",
#             "margin": "lg",
#             "contents": [
#               {
#                 "type": "text",
#                 "text": "・フォーム2",
#                 "size": "md",
#                 "align": "start",
#                 "weight": "bold",
#                 "flex": 5,
#                 "gravity": "center",
#                 "margin": "sm",
#                 "wrap": true
#               },
#               {
#                 "type": "text",
#                 "text": "選択",
#                 "size": "lg",
#                 "color": "#111111",
#                 "align": "center",
#                 "flex": 2,
#                 "offsetStart": "12px",
#                 "weight": "bold",
#                 "decoration": "underline",
#                 "action": {
#                   "type": "uri",
#                   "label": "action",
#                   "uri": "http://yahoo.co.jp/"
#                 }
#               }
#             ]
#           },
#           {
#             "type": "box",
#             "layout": "horizontal",
#             "margin": "lg",
#             "contents": [
#               {
#                 "type": "text",
#                 "text": "・フォーム3",
#                 "size": "md",
#                 "align": "start",
#                 "weight": "bold",
#                 "flex": 5,
#                 "gravity": "center",
#                 "margin": "sm",
#                 "wrap": true
#               },
#               {
#                 "type": "text",
#                 "text": "選択",
#                 "size": "lg",
#                 "color": "#111111",
#                 "align": "center",
#                 "flex": 2,
#                 "offsetStart": "12px",
#                 "weight": "bold",
#                 "decoration": "underline",
#                 "action": {
#                   "type": "uri",
#                   "label": "action",
#                   "uri": "http://yahoo.co.jp/"
#                 }
#               }
#             ]
#           },
#           {
#             "type": "box",
#             "layout": "horizontal",
#             "margin": "lg",
#             "contents": [
#               {
#                 "type": "text",
#                 "text": "・フォーム4",
#                 "size": "md",
#                 "align": "start",
#                 "weight": "bold",
#                 "flex": 5,
#                 "gravity": "center",
#                 "margin": "sm",
#                 "wrap": true
#               },
#               {
#                 "type": "text",
#                 "text": "選択",
#                 "size": "lg",
#                 "color": "#111111",
#                 "align": "center",
#                 "flex": 2,
#                 "offsetStart": "12px",
#                 "weight": "bold",
#                 "decoration": "underline",
#                 "action": {
#                   "type": "uri",
#                   "label": "action",
#                   "uri": "http://yahoo.co.jp/"
#                 }
#               }
#             ]
#           },
#           {
#             "type": "box",
#             "layout": "horizontal",
#             "margin": "lg",
#             "contents": [
#               {
#                 "type": "text",
#                 "text": "・フォーム5",
#                 "size": "md",
#                 "align": "start",
#                 "weight": "bold",
#                 "flex": 5,
#                 "gravity": "center",
#                 "margin": "sm",
#                 "wrap": true
#               },
#               {
#                 "type": "text",
#                 "text": "選択",
#                 "size": "lg",
#                 "color": "#111111",
#                 "align": "center",
#                 "flex": 2,
#                 "offsetStart": "12px",
#                 "weight": "bold",
#                 "decoration": "underline",
#                 "action": {
#                   "type": "uri",
#                   "label": "action",
#                   "uri": "http://yahoo.co.jp/"
#                 }
#               }
#             ]
#           }
#         ]
#       }
#     ]
#   },
#   "footer": {
#     "type": "box",
#     "layout": "vertical",
#     "contents": []
#   },
#   "styles": {
#     "body": {
#       "backgroundColor": "#F4F3F9"
#     },
#     "footer": {
#       "separator": true,
#       "backgroundColor": "#F4F3F9"
#     }
#   }
# }


