import json
from dodam import practice_dodam
import requests


def lambda_handler(event, context):

    date = event["queryStringParameters"]["date"]
    try:
        menu_dict = practice_dodam(date)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

    form_json = {
        "todayMenuList": []
    }
    for restrant_name, value in menu_dict.items():
        if not value:
            continue

        form_json["todayMenuList"] = value
        if "중식" in restrant_name:
            res = requests.post(url=f"https://eatssu.shop/menu/", json=form_json,
                                params={"date": date, "restaurant": "DODAM", "time": "LUNCH"}, timeout=10)
        elif "석식" in restrant_name:
            res = requests.post(url=f"https://eatssu.shop/menu/", json=form_json,
                                params={"date": date, "restaurant": "DODAM", "time": "DINNER"}, timeout=10)
        else:
            raise Exception

    return {
        'statusCode': 200,
        'body': json.dumps(menu_dict, ensure_ascii=False).encode('utf-8')
    }
