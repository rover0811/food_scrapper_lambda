import json
from haksik import practice_student_restarant
import requests
def lambda_handler(event, context):

    date = event["queryStringParameters"]["date"]
    
    menu_dict = practice_student_restarant(date)
    
    form_json = {
        "todayMenuList": []
    }

    for restrant_name, value in menu_dict.items():
        form_json["todayMenuList"] = value
        requests.post(url=f"https://eatssu.shop/menu/", json=form_json,
                      params={"date": date, "restaurant": "HAKSIK", "time": "LUNCH"})

    
    return {
        'statusCode': 200,
        'body': json.dumps(menu_dict, ensure_ascii=False).encode('utf-8')
    }



if __name__ == "__main__":
    print(lambda_handler({"queryStringParameters":{"date":"20231016"}},None))