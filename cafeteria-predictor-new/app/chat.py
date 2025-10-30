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

**- 먼저 자연어로 조정 이유를 간단히 설명해줘.
**- 그 다음에 순수 CSV 데이터를 코드블록 안에 넣어줘.
**- CSV에는 헤더를 포함하고, 기존 테이블 구조를 유지해줘.

예측식수를 조정한 이유에 대한 자연어 예시:
11월 3일에 외부 인사 방문으로 20명 증가했습니다.

CSV 데이터 예시:
날짜,예측 식수 인원,메인메뉴,국의 이름,눈 또는 비 여부,온도,요일 2025-11-03,538.54,볶음밥,내장탕,비,15,Monday ...
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    full_text = response.choices[0].message.content.strip()

    if not full_text:
        raise ValueError("GPT 응답이 비어 있습니다. 입력을 다시 확인해주세요.")
    else:
        print("GPT 응답 수신 성공.",full_text)

    # 코드블록 분리
    if "```" in full_text:
        parts = full_text.split("```")
        # parts 예시: [설명, 'csv\n날짜,...', '']
        explanation = parts[0].strip()
        # 두 번째 파트에서 'csv' 접두어 제거
        csv_text = parts[1].strip()
        if csv_text.lower().startswith("csv"):
            csv_text = csv_text[3:].strip()
    else:
        # fallback: '날짜,' 헤더 찾기
        lines = full_text.splitlines()
        header_idx = None
        for i, line in enumerate(lines):
            if line.strip().startswith("날짜,"):
                header_idx = i
                break
        if header_idx is not None:
            explanation = "\n".join(lines[:header_idx]).strip()
            csv_text = "\n".join(lines[header_idx:]).strip()
        else:
            explanation = full_text
            csv_text = ""


    if not csv_text:
        raise ValueError("GPT 응답에 CSV 데이터가 포함되어 있지 않습니다.")

    print("GPT 전체 응답:\n", full_text)
    print("GPT 설명:\n", explanation)
    print("GPT CSV:\n", csv_text)

    # CSV 파싱
    try:
        adjusted_df = pd.read_csv(StringIO(csv_text))
    except Exception as e:
        raise ValueError(f"CSV 파싱 실패: {e}")

    return explanation, adjusted_df
