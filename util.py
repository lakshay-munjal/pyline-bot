from msilib import _directories


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
                    "text": "姿勢画像の送信 lawddde~",
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



def simpleTextMessage(msg):
    dictResp = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": msg
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

    return dictResp 