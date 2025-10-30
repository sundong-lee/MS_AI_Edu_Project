from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from io import StringIO

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def process_chat(user_input, df):
    table_text = df.to_csv(index=False)

    prompt = f"""
너는 구내식당 식수 예측 조정 전문가야.
다음은 예측된 식수 데이터야:

{table_text}

운영자가 아래와 같은 메시지를 입력했어:
"{user_input}"

이 메시지를 반영해서 예측 식수 인원이 영향을 받을 날짜를 찾아서 해당 날짜의 식수 인원을 조정해줘.
조정된 결과를 동일한 CSV 형식으로 반환해줘.
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    csv_text = response.choices[0].message.content
    print("GPT chat adjustment 응답:\n", response.choices[0].message.content)

    adjusted_df = pd.read_csv(StringIO(csv_text))
    return adjusted_df