import pandas as pd
import random
from datetime import datetime, timedelta

# 오늘 날짜 기준
start_date = datetime(2025, 10, 29)
days = 14

weekday_map = {
    0: "월요일", 1: "화요일", 2: "수요일",
    3: "목요일", 4: "금요일", 5: "토요일", 6: "일요일"
}

main_menu_all = [
    "제육볶음", "간장불고기", "닭도리탕", "고추장불고기",
    "돈까스", "치킨까스", "떡갈비", "잔치국수", "망향비빔국수",
    "토마토파스타", "오일파스타", "봉골레", "햄버거",
    "볶음밥", "비빔밥", "카레라이스", "생선구이", "두부조림"
]

soup_all = [
    "육개장", "뼈해장국", "소고기무국", "한우국밥", "내장탕", "순대국",
    "된장국", "미역국", "채소국", "계란국", "김치찌개"
]

rows = []

for i in range(days):
    date = start_date + timedelta(days=i)
    date_str = date.strftime("%Y-%m-%d")
    weekday_kor = weekday_map[date.weekday()]
    menu = random.choice(main_menu_all)
    soup = random.choice(soup_all)
    rows.append([date_str, weekday_kor, menu, soup])

df = pd.DataFrame(rows, columns=["날짜", "요일", "메인메뉴", "국의 이름"])
df.to_csv("future_data.csv", index=False, encoding="utf-8-sig")