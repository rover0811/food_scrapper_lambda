# import boto3
import requests
import datetime
import logging
# from concurrent.futures import ThreadPoolExecutor
import json
import asyncio
import aiohttp



# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS Lambda에서 실행되는 함수
def lambda_handler(event, context):
    
    body = asyncio.run(main())

    return {
        'statusCode': 200,
        'body': json.dumps(body, ensure_ascii=False).encode("utf-8")
    }

async def main():
    # 다음 주 월요일부터 금요일까지의 날짜를 가져옴
    weekdays = get_next_weekdays()
    # # weekdays = ["20231002", "20231010", "20231011", "20231012", "20231013"]
    # weekdays = ["20231009", "20231010", "20231011", "20231012", "20231013"]

    base_url = "https://drvrj3q50b.execute-api.ap-northeast-2.amazonaws.com/get_dodam"

    # 결과를 저장할 리스트
    results = {}

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, base_url, date) for date in weekdays]
        responses = await asyncio.gather(*tasks)

        for date, response_data in zip(weekdays, responses):
            results[date] = response_data
    
    return results

    

async def send_request(session, base_url, date):
    try:
        async with session.get(url=base_url, params={"date": date}) as response:
            response_text = await response.text()
            response_data = json.loads(response_text)
            return response_data
    except Exception as e:
        print(f"Error sending request: {e}")
        return None




def get_next_weekdays():
    current_date = datetime.date.today()

    # 다음 주 월요일까지의 날짜 계산
    days_until_monday = (7 - current_date.weekday()) % 7
    next_monday = current_date + datetime.timedelta(days=days_until_monday)

    # 다음 주 금요일까지의 날짜 계산
    days_until_friday = 4  # 다음 주 금요일까지는 4일 필요
    next_friday = next_monday + datetime.timedelta(days=days_until_friday)

    # 날짜 범위 내의 날짜를 생성하여 리스트에 추가
    date_list = []

    for i in range(5):  # 월요일부터 금요일까지 5일
        date_list.append(next_monday.strftime("%Y%m%d"))
        next_monday += datetime.timedelta(days=1)
    return date_list

# def send_request(base_url, date):
#     try:
#         response = requests.get(url=base_url, params={"date": date})
#         response_data = response.json()
#         logger.info(f"Response: {response_data}")
#         return response_data
#     except Exception as e:
#         logger.error(f"Error sending request: {e}")
#         return None


