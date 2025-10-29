from prophet import Prophet
import pandas as pd
from data_utils import prepare_forecast_input, apply_weights, merge_future_data

def forecast_meal_count(past_df, future_menu_df, future_weather_df):
    # 1. Prophet 학습용 데이터 준비
    train_df = prepare_forecast_input(past_df)

    # 2. Prophet 모델 학습
    model = Prophet()
    model.fit(train_df)

    # 3. 미래 날짜 생성
    future_dates = pd.date_range(start=future_menu_df["날짜"].min(), end=future_menu_df["날짜"].max())
    future_df = pd.DataFrame({"ds": future_dates})

    # 4. 기본 예측값 생성
    forecast = model.predict(future_df)
    forecast = forecast[["ds", "yhat"]]

    # 5. 미래 메뉴 + 날씨 병합
    merged_df = merge_future_data(future_menu_df, future_weather_df)

    # 6. 가중치 계산
    weighted_df = apply_weights(merged_df)

    # 7. 날짜 형식 맞추기
    weighted_df["ds"] = pd.to_datetime(weighted_df["날짜"])

    # 8. 예측값 병합
    result_df = pd.merge(forecast, weighted_df, on="ds", how="left")

    # 9. 최종 식수 예측값 계산
    result_df["예측 식수 인원"] = result_df["yhat"] + result_df["가중치"]

    # 10. 결과 정리
    result_df["날짜"] = result_df["ds"].dt.strftime("%Y-%m-%d")
    result_df = result_df[["날짜", "요일", "메인메뉴", "국의 이름", "눈 또는 비 여부", "온도", "예측 식수 인원"]]

    return result_df