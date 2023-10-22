import json
import requests
import datetime

def lambda_handler(event, context):
    # TODO implement

    if event.get("date") is not None:
        date = event["date"]
    date = datetime.date.today().strftime("%Y%m%d")
    # date = datetime.datetime(2023,10,1).strftime("%Y%m%d")

    res = requests.get("https://drvrj3q50b.execute-api.ap-northeast-2.amazonaws.com/get_dormitory",params={"date":date})
    print(res.text)

    return {
        'statusCode': 200,
        'body': json.dumps(res.json(),ensure_ascii=False).encode("utf-8")
    }