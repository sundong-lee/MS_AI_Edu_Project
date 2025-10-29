import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI

# 환경변수 설정 필요
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
BLOB_CONNECTION_STRING = os.environ.get("BLOB_CONNECTION_STRING")


blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
container_client = blob_service.get_container_client("cafeteria")

client = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    api_version=OPENAI_API_VERSION,
    azure_endpoint=OPENAI_ENDPOINT
)

st.title("구내식당 운영 도우미 MVP")
st.caption("업로드 → 자동 예측 → 다운로드/시각화 → 챗봇 Q&A")

# 1) 업로드
st.header("데이터 업로드 (past_attendance.csv)")
uploaded = st.file_uploader("CSV 파일 선택 (date, attendance_count)", type=["csv"])
if uploaded is not None:
    content = uploaded.read()
    container_client.upload_blob("past_attendance.csv", content, overwrite=True)
    st.success("past_attendance.csv 업로드 완료. 예측이 곧 생성됩니다(Blob Trigger).")

# 2) 다운로드
st.header("예측 결과 다운로드 (forecast_30d.csv)")
if st.button("예측 결과 새로고침"):
    try:
        data = container_client.download_blob("forecast_30d.csv").readall().decode("utf-8")
        st.download_button("forecast_30d.csv 다운로드", data, file_name="forecast_30d.csv")
        st.success("예측 결과를 불러왔습니다.")
    except Exception as e:
        st.error("아직 예측 결과가 생성되지 않았습니다.")

# 3) 시각화
st.header("시각화")
col1, col2 = st.columns(2)

with col1:
    st.subheader("과거 1년 식수 인원")
    try:
        past = container_client.download_blob("past_attendance.csv").readall().decode("utf-8")
        df_past = pd.read_csv(StringIO(past))
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(pd.to_datetime(df_past['date']), df_past['attendance_count'], color='steelblue')
        ax.set_title("과거 식수 인원")
        ax.set_xlabel("날짜")
        ax.set_ylabel("인원")
        st.pyplot(fig)
    except Exception:
        st.info("past_attendance.csv를 업로드하면 그래프가 표시됩니다.")

with col2:
    st.subheader("예측 30일 식수 인원")
    try:
        pred = container_client.download_blob("forecast_30d.csv").readall().decode("utf-8")
        df_pred = pd.read_csv(StringIO(pred))
        fig2, ax2 = plt.subplots(figsize=(8, 3))
        ax2.plot(pd.to_datetime(df_pred['date']), df_pred['yhat'], color='tomato')
        ax2.fill_between(pd.to_datetime(df_pred['date']), df_pred['yhat_lower'], df_pred['yhat_upper'], color='tomato', alpha=0.2)
        ax2.set_title("예측 30일 (신뢰구간 포함)")
        ax2.set_xlabel("날짜")
        ax2.set_ylabel("예상 인원")
        st.pyplot(fig2)

        st.table(df_pred.tail(7))  # 최근 1주 표 형태
    except Exception:
        st.info("forecast_30d.csv가 생성되면 예측 그래프가 표시됩니다.")

# 4) 챗봇 (RAG 스타일)
st.header("Azure OpenAI 챗봇 (과거/예측 데이터 기반 Q&A)")
user_q = st.text_input("질문을 입력하세요 (예: 다음 주 수요일 예상 인원은?)")

def build_context_text():
    ctx = []
    try:
        past = container_client.download_blob("past_attendance.csv").readall().decode("utf-8")
        ctx.append("과거데이터\n" + past[:50_000])  # 컨텍스트 길이 제한
    except Exception:
        pass
    try:
        pred = container_client.download_blob("forecast_30d.csv").readall().decode("utf-8")
        ctx.append("예측데이터\n" + pred[:50_000])
    except Exception:
        pass
    return "\n\n".join(ctx) if ctx else "데이터 없음"

if st.button("질문하기"):
    context = build_context_text()
    messages = [
        {"role": "system", "content": "You are a helpful cafeteria assistant. Use provided CSV context to answer."},
        {"role": "user", "content": f"컨텍스트:\n{context}"},
        {"role": "user", "content": f"질문:\n{user_q}"}
    ]
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.2
        )
        st.markdown("**답변:**")
        st.write(resp.choices[0].message["content"])
    except Exception as e:
        st.error(f"OpenAI 호출 오류: {e}")