import openai
import pandas as pd
from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_MODEL,
    AZURE_OPENAI_API_VERSION
)

# Azure OpenAI 설정
openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_KEY
openai.api_version = AZURE_OPENAI_API_VERSION

def adjust_forecast_with_gpt(user_input: str, forecast_df: pd.DataFrame) -> pd.DataFrame:
    """
    운영자의 입력을 기반으로 GPT가 예측값을 조정
    """
    # 예측 데이터 요약 텍스트 생성
    forecast_text = ""
    for _, row in forecast_df.iterrows():
        forecast_text += f"{row['날짜']} ({row['요일']}): {row['메인메뉴']}, {row['국의 이름']}, 예측 식수 인원: {int(row['예측 식수 인원'])}\n"

    # GPT 프롬프트 구성
    prompt = f"""
너는 단체급식 식수 예측 전문가야. 아래는 미래 2주간의 식수 예측 데이터야.
운영자가 다음과 같은 요청을 했어: "{user_input}"
요청을 반영해서 각 날짜별 식수 예측값을 조정해줘. 날짜별로 숫자만 다시 알려줘.

예측 데이터:
{forecast_text}

반환 형식은 다음과 같아:
날짜, 조정된 식수 인원
"""

    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )

    # GPT 응답 파싱
    adjusted_lines = response["choices"][0]["message"]["content"].strip().split("\n")
    adjusted_dict = {}
    for line in adjusted_lines:
        try:
            date, count = line.split(",")
            adjusted_dict[date.strip()] = int(count.strip())
        except:
            continue

    # 기존 예측값에 반영
    forecast_df["조정된 식수 인원"] = forecast_df["날짜"].apply(
        lambda d: adjusted_dict.get(d, forecast_df.loc[forecast_df["날짜"] == d, "예측 식수 인원"].values[0])
    )

    return forecast_df