import logging
import azure.functions as func
import pandas as pd
from io import StringIO
from forecast import forecast_meal_count
from data_utils import load_csv
from blob_utils import upload_blob

app = func.FunctionApp()

# @app.function_name(name="forecastTrigger")
@app.blob_trigger(arg_name="myblob",
                  path="cafeteria/{name}",
                  connection="AzureWebJobsStorage")
def run_forecast(myblob: func.InputStream):
    logging.info(f"📦 Blob trigger: {myblob.name}, Size: {myblob.length} bytes")

    try:
        # 모든 파일 로딩
        past_df = load_csv("past_data.csv")
        future_menu_df = load_csv("future_data.csv")
        future_weather_df = load_csv("future_weather.csv")

        # 예측 수행
        result_df = forecast_meal_count(past_df, future_menu_df, future_weather_df)

        # 결과를 CSV로 변환
        output = StringIO()
        result_df.to_csv(output, index=False, encoding="utf-8-sig")
        output_bytes = output.getvalue().encode("utf-8-sig")

        # 결과 업로드
        upload_blob(output_bytes, "forecast_result.csv")
        logging.info("✅ 예측 결과 업로드 완료: forecast_result.csv")

    except Exception as e:
        logging.error(f"❌ 예측 트리거 실패: {str(e)}")