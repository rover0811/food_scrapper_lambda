import json
from dormitory import Dormitory
import requests
import datetime


def lambda_handler(event, context):
    # TODO implement

    weekly_dorm = Dormitory(event["queryStringParameters"]["date"])

    weekly_menu = weekly_dorm.get_menu()

    for today in weekly_menu:
        for meal_time, menus in today["menu"].items():

            date_obj = datetime.datetime.strptime(today["date"], "%Y%m%d")

            if (date_obj.weekday() == 5 and meal_time == "조식") or (date_obj.weekday() == 5 and meal_time == "조식") == 6:  # 주말 조식은 운영을 안함
                continue

            for menu in menus:
                if "운영" in menu:
                    break
            else:
                json_data = {
                    'todayMenuList': [
                        '돈까스',
                        '샐러드',
                        '김치',
                    ],
                }
                if menus is None:
                    continue
                else:
                    json_data["todayMenuList"] = menus

                params = {
                    "date": today["date"],
                    "restaurant": "DOMITORY",  # dormitory 오타
                    "time": get_time_of_day(meal_time)
                }

                res = requests.post(url="https://eatssu.shop/menu/", json=json_data,
                                    params=params, timeout=10)


    return {
        'statusCode': 200,
        'body': json.dumps(weekly_menu, ensure_ascii=False).encode("utf-8")
    }


def get_time_of_day(meal_time):
    if meal_time == "조식":
        return "MORNING"
    elif meal_time == "중식":
        return "LUNCH"
    elif meal_time == "석식":
        return "DINNER"
    else:
        return None


if __name__ == "__main__":

    dorm = Dormitory("20231016")

    weekly_menu: list = dorm.get_menu()


    for today in weekly_menu:
        for meal_time, menus in today["menu"].items():

            date_obj = datetime.datetime.strptime(today["date"], "%Y%m%d")

            if (date_obj.weekday() == 5 and meal_time == "조식") or (date_obj.weekday() == 5 and meal_time == "조식") == 6:  # 주말 조식은 운영을 안함
                continue

            for menu in menus:
                if "운영" in menu:
                    break
            else:
                json_data = {
                    'todayMenuList': [
                        '돈까스',
                        '샐러드',
                        '김치',
                    ],
                }
                if menus is None:
                    continue
                else:
                    json_data["todayMenuList"] = menus

                params = {
                    "date": today["date"],
                    "restaurant": "DOMITORY",  # dormitory 오타
                    "time": get_time_of_day(meal_time)
                }

                res = requests.post(url="https://eatssu.shop/menu/", json=json_data,
                                    params=params, timeout=10)
