import pandas as pd

# 별미 메뉴 및 국 종류 정의
SPECIAL_MENUS = {
    "제육볶음", "간장불고기", "닭도리탕", "고추장불고기",
    "돈까스", "치킨까스", "떡갈비", "잔치국수", "망향비빔국수",
    "토마토파스타", "오일파스타", "봉골레", "햄버거"
}

SPECIAL_SOUPS = {
    "육개장", "뼈해장국", "소고기무국", "한우국밥", "내장탕", "순대국"
}

def load_csv(file_path):
    return pd.read_csv(file_path, encoding="utf-8-sig")

def merge_future_data(menu_df, weather_df):
    df = pd.merge(menu_df, weather_df, on=["날짜", "요일"], how="left")
    return df

def calculate_weight(row):
    weight = 0

    # 날씨 영향
    if row["눈 또는 비 여부"] == "있음":
        weight += 1
    if 15 <= row["온도"] <= 27:
        weight -= 1

    # 메뉴 영향
    if row["메인메뉴"] in SPECIAL_MENUS:
        weight += 1
    if row["국의 이름"] in SPECIAL_SOUPS:
        weight += 1

    # 요일 영향
    if row["요일"] == "금요일":
        weight -= 1

    return weight * 10  # 가중치 계수

def apply_weights(df):
    df["가중치"] = df.apply(calculate_weight, axis=1)
    return df

def prepare_forecast_input(past_df):
    df = past_df.copy()
    df = df.dropna()
    df["ds"] = pd.to_datetime(df["날짜"])
    df["y"] = df["실제 식사했던 인원"]
    return df[["ds", "y"]]