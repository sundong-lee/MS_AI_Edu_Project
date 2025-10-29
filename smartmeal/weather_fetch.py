import openai
import pandas as pd
from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_MODEL,
    AZURE_OPENAI_API_VERSION
)

openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_KEY
openai.api_version = AZURE_OPENAI_API_VERSION

def fetch_weather_from_gpt():
    prompt = """
서울시 서초구 방배동의 오늘부터 2주간(14일간) 낮 12시 기준 날씨 예보를 알려줘.
각 날짜별로 다음 형식으로 정리해줘:
날짜, 요일, 눈 또는 비 여부, 온도(℃)
"""

    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )

    content = response["choices"][0]["message"]["content"]
    lines = content.strip().split("\n")

    rows = []
    for line in lines:
        try:
            date, weekday, rain_or_snow, temp = line.split(",")
            rows.append([date.strip(), weekday.strip(), rain_or_snow.strip(), float(temp.strip())])
        except:
            continue

    df = pd.DataFrame(rows, columns=["날짜", "요일", "눈 또는 비 여부", "온도"])
    df.to_csv("future_weather.csv", index=False, encoding="utf-8-sig")
    print("✅ GPT 기반 날씨 정보 저장 완료")

if __name__ == "__main__":
    fetch_weather_from_gpt()