from prophet import Prophet
import pandas as pd
from storage.blob_manager import download_from_blob, upload_to_blob
from core.adjuster import apply_adjustments
from core.utils import get_today_range
from core.utils import format_datetime_for_filename

def run_prediction():
    # 1. 데이터 불러오기
    past_df = download_from_blob("past_data.csv")
    future_menu_df = download_from_blob("future_data.csv")
    future_weather_df = download_from_blob("future_weather.csv")

    # 2. 병합 전 요일 컬럼 제거
    for df in [past_df, future_menu_df, future_weather_df]:
        df.drop(columns=[col for col in df.columns if "요일" in col], inplace=True)

    # 3. Prophet 학습용 데이터 준비
    train_df = past_df[["날짜", "실제 식사 인원"]].rename(columns={"날짜": "ds", "실제 식사 인원": "y"})
    train_df["ds"] = pd.to_datetime(train_df["ds"])

    # 4. 모델 학습 및 예측
    model = Prophet()
    model.fit(train_df)

    future_dates = future_menu_df["날짜"]
    future_df = pd.DataFrame({"ds": pd.to_datetime(future_dates)})
    forecast = model.predict(future_df)

    # 5. 예측값 추출
    forecast_df = forecast[["ds", "yhat"]].rename(columns={"ds": "날짜", "yhat": "예측 식수 인원"})
    forecast_df["날짜"] = forecast_df["날짜"].dt.strftime("%Y-%m-%d")

    # 여기서 정수 변환 추가
    forecast_df["예측 식수 인원"] = forecast_df["예측 식수 인원"].round().astype(int)

    # 5. future 메뉴/날씨/요일 병합
    result_df = forecast_df.merge(future_menu_df, on="날짜")
    result_df = result_df.merge(future_weather_df, on="날짜")

     # 6. 요일 컬럼 추가
    result_df["요일"] = pd.to_datetime(result_df["날짜"]).dt.day_name()

    # 주말이면 식수 인원 제거
    result_df.loc[result_df["요일"].isin(["Saturday", "Sunday"]), "예측 식수 인원"] = None

    # 6. 가중치 조정
    adjusted_df = apply_adjustments(result_df)

# 9. 결과 저장
    filename = f"meal_cover_{format_datetime_for_filename()}.csv"
    upload_to_blob(filename, result_df)

    return result_df
