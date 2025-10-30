import pandas as pd

# 메뉴 및 국 종류에 따른 영향도 (+)
SPECIAL_MAIN = ["제육볶음", "간장불고기", "닭도리탕", "고추장불고기", "돈까스", "치킨까스", "떡갈비", "잔치국수", "망향비빔국수", "토마토파스타", "오일파스타", "봉골레", "햄버거"]
SPECIAL_SOUP = ["육개장", "뼈해장국", "소고기무국", "한우국밥", "내장탕", "순대국"]

def apply_adjustments(df):
    adjusted = df.copy()

    for i, row in adjusted.iterrows():
        factor = 1.0

        # 날씨 영향
        if row["눈 또는 비 여부"] in ["눈", "비"]:
            factor += 0.1  # 이용율 증가
        # 온도 영향
        temp = row["온도"]
        if 15 <= temp <= 27:
            factor -= 0.1  # 쾌적하면 이용율 감소

        # 메뉴 영향
        if row["메인메뉴"] in SPECIAL_MAIN:
            factor += 0.1
        if row["국의 이름"] in SPECIAL_SOUP:
            factor += 0.1

        # 요일 영향
        if row["요일"] == "금요일":
            factor -= 0.1

        # 예측값이 NaN이면 조정하지 않음
        base = row.get("예측 식수 인원")
        if pd.isna(base):
            continue

        # 최종 식수 인원 조정
        adjusted.at[i, "예측 식수 인원"] = max(0, round(base * factor))

    return adjusted