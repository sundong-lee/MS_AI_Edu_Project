import streamlit as st

def render_upload_section():
    col1, col2, col3 = st.columns(3)

    with col1:
        past_file = st.file_uploader("📂 과거 1년치 식수 데이터 업로드", type="csv")

    with col2:
        future_file = st.file_uploader("📂 2주일치 메뉴 데이터 업로드", type="csv")

    with col3:
        weather_clicked = st.button("☁️ 날씨 정보 가져오기")

    return past_file, future_file, weather_clicked

def render_chat_input():
    return st.text_input("💬 식수 관련 문의를 입력하세요")

def render_result_table(df):
    st.subheader("📊 예측 결과")
    st.dataframe(df)

def render_success_message(text):
    st.success(f"✅ {text}")