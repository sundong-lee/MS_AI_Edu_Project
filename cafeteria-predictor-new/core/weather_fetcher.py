from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from io import StringIO
from core.utils import get_today_range

load_dotenv()

#print("API_VERSION:", os.getenv("AZURE_OPENAI_API_VERSION"))

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def fetch_weather_data():
    dates = get_today_range(14)
    prompt = f"""
너는 서울 서초구 방배동의 날씨 예측 전문가야. 아래 날짜들에 대해 각각의 날씨 정보를 알려줘.

각 날짜에 대해 다음 정보를 제공해줘:
- 날짜
- 요일
- 눈 또는 비 여부 (눈, 비, 없음 중 하나)
- 낮 12시 기준 온도 (섭씨)

반드시 CSV 형식으로만 출력해줘. 설명이나 코드 블록 없이 아래 형식 그대로:

날짜,요일,눈 또는 비 여부,온도
2025-10-30,목요일,없음,18
...

날짜 목록:
{', '.join(dates)}

"""

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    csv_text = response.choices[0].message.content
    print("GPT weather 응답:\n", response.choices[0].message.content)

    df = pd.read_csv(StringIO(csv_text))
    return df