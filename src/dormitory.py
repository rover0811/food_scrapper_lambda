import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import json

from parse_table import make2d



class Dormitory:
    def __init__(self, date) -> None:
        date = datetime.strptime(date, '%Y%m%d')
        webpage = requests.get(
            url=f'https://ssudorm.ssu.ac.kr:444/SShostel/mall_main.php',
            params={'viewform': 'B0001_foodboard_list', 'gyear': date.year, 'gmonth': date.month, 'gday': date.day})
        self.soup: BeautifulSoup = BeautifulSoup(webpage.content, 'html.parser')
        self.table = None
        self.menu_list = list()
    
    def refine_table(self):
        table_tag = self.soup.find("table", "boxstyle02")
        table = make2d(table_tag)
        df = pd.DataFrame(table)
        dt2 = df.rename(columns=df.iloc[0])
        dt3 = dt2.drop(dt2.index[0])
        dt3["조식"] = dt3["조식"].str.split("\r\n")
        dt3["중식"] = dt3["중식"].str.split("\r\n")
        dt3["석식"] = dt3["석식"].str.split("\r\n")
        del dt3["중.석식"]
        dt3 = dt3.set_index('날짜')
        self.table = dt3

    def get_table(self):
        for index, rows in self.table.iterrows():
            new_date = index.split()[0]
            new_date = new_date.replace("-", "")
            new_menu = {"date": new_date, "restaurant": "기숙사식당", "menu": {}}
            self.menu_list.append(new_menu)
            for col_name in self.table.columns:
                new_menu['menu'][col_name] = rows[col_name]

    def get_menu(self):
        self.refine_table()
        self.get_table()

        return self.menu_list


# 사용 예제
date = '20210929'
dormitory = Dormitory(date)
a = dormitory.get_menu()

# a를 json으로 변환해서 저장하는 코드

with open('dormitory.json', 'w', encoding='utf-8') as f:
    json.dump(a, f, ensure_ascii=False, indent=4)


