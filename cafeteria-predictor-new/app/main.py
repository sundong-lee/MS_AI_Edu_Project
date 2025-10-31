import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from storage.blob_manager import upload_to_blob, download_from_blob
from core.weather_fetcher import fetch_weather_data
from core.predictor import run_prediction
from app.chat import process_chat
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="급식 식수 예측 서비스", layout="wide")
#st.title("🍱 대규모 급식 식수 예측 AI 서비스")
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <h1 style="margin: 0;">대규모 급식 식수 예측 AI 서비스</h1>
        <div style="margin-left: auto;">
            <h5 style="margin: 0; color: gray;">AM BD팀 이선동</h5>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 파일 업로드 영역 ---
col1, col2, col3 = st.columns(3)

with col1:
    past_file = st.file_uploader("📂 과거 1년치 식수 데이터 업로드", type="csv")

with col2:
    future_file = st.file_uploader("📂 2주일치 메뉴 데이터 업로드", type="csv")

with col3:
    if st.button("☁️ 2주일치 날씨 정보 가져오기"):
        with st.spinner("⏳ 날씨 정보를 불러오는 중입니다..."):
            weather_df = fetch_weather_data()
            upload_to_blob("future_weather.csv", weather_df)
            st.success("✅ 날씨 정보 저장 완료")

# --- 챗 입력 영역 ---
user_input = st.text_input("💬 챗GPT에게 식수 관련 추가 조정 요인을 이야기 하세요")

# --- 예측 실행 버튼 ---
if st.button("📊 식수 예측 실행"):
    if past_file and future_file:
        # 1. 업로드된 파일을 Blob에 저장
        upload_to_blob("past_data.csv", past_file)
        upload_to_blob("future_data.csv", future_file)

        # 2. 예측 실행
        result_df = run_prediction()

        # 3. 운영자 챗 입력 반영
        if user_input:
            with st.spinner("💡 GPT가 식수 예측을 조정 중입니다... 잠시만 기다려주세요."):
                explanation, adjusted_df = process_chat(user_input, result_df)
            st.success("✅ 운영자 입력 반영 완료")

            # GPT 설명 출력
            st.markdown(f"**💬 GPT 응답:**\n\n{explanation}")

            # 조정된 결과 테이블 출력
            st.dataframe(adjusted_df)

            # 필요 시 result_df 업데이트
            result_df = adjusted_df

        # 4. 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d%H")
        filename = f"meal_cover_{timestamp}.csv"
        upload_to_blob(filename, result_df)

        # 5. 결과 표시
        st.success("✅ 예측 완료! 아래에 결과를 표시합니다.")
        st.dataframe(result_df)
    else:
        st.warning("⚠️ 두 개의 CSV 파일을 모두 업로드해주세요.")