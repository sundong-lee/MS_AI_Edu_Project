import pandas as pd
import random
from datetime import datetime, timedelta

# 공휴일 목록 (예시)
holidays = [
    "2024-01-01", "2024-03-01", "2024-05-05", "2024-06-06",
    "2024-08-15", "2024-09-16", "2024-09-17", "2024-10-03", "2024-12-25"
]

# 한글 요일 매핑
weekday_map = {
    0: "월요일", 1: "화요일", 2: "수요일",
    3: "목요일", 4: "금요일", 5: "토요일", 6: "일요일"
}

# 메뉴 구성
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

# 별미 메뉴 목록
main_special = {
    "제육볶음", "간장불고기", "닭도리탕", "고추장불고기",
    "돈까스", "치킨까스", "떡갈비", "잔치국수", "망향비빔국수",
    "토마토파스타", "오일파스타", "봉골레", "햄버거"
}

soup_special = {
    "육개장", "뼈해장국", "소고기무국", "한우국밥", "내장탕", "순대국"
}

rows = []
current = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

while current <= end_date:
    date_str = current.strftime("%Y-%m-%d")
    weekday_kor = weekday_map[current.weekday()]
    if weekday_kor in ["토요일", "일요일"] or date_str in holidays:
        rows.append([date_str, "", "", "", "", "", ""])
    else:
        rain_or_snow = random.choice(["있음", "없음"])
        temp = round(random.uniform(0, 30), 1)
        menu = random.choice(main_menu_all)
        soup = random.choice(soup_all)
        base_count = random.randint(480, 520)

        # 별미 메뉴 가중치
        bonus = 0
        if menu in main_special:
            bonus += random.randint(10, 20)
        if soup in soup_special:
            bonus += random.randint(10, 20)

        count = base_count + bonus
        rows.append([date_str, weekday_kor, rain_or_snow, temp, menu, soup, count])
    current += timedelta(days=1)

df = pd.DataFrame(rows, columns=["날짜", "요일", "눈 또는 비 여부", "온도", "메인메뉴", "국의 이름", "실제 식사했던 인원"])
df.to_csv("past_data.csv", index=False, encoding="utf-8-sig")