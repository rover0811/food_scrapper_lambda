import json
from dodam import practice_dodam
import requests
def lambda_handler(event, context):

    date = event["queryStringParameters"]["date"]
    
    menu_dict = practice_dodam(date)
    
    form_json = {
        "todayMenuList": []
    }

    for restrant_name, value in menu_dict.items():
        form_json["todayMenuList"] = value
        if "중식" in restrant_name:
            requests.post(url=f"https://eatssu.shop/menu/", json=form_json,
                        params={"date": date, "restaurant": "DODAM", "time": "LUNCH"},timeout=10)
        elif "석식" in restrant_name:
            requests.post(url=f"https://eatssu.shop/menu/", json=form_json,
                        params={"date": date, "restaurant": "DODAM", "time": "DINNER"},timeout=10)

    
    return {
        'statusCode': 200,
        'body': json.dumps(menu_dict, ensure_ascii=False).encode('utf-8')
    }



if __name__ == "__main__":

    for i in range(16,20):
        print(lambda_handler({"queryStringParameters":{"date":f"202310{i}"}},None))