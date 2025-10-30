from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime

def get_today_range(days=14):
    """
    오늘부터 지정된 일수(days)만큼의 날짜 리스트를 반환
    """
    today = datetime.today()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]

def add_weekday_column(df, date_column="날짜"):
    """
    날짜 컬럼을 기준으로 요일 컬럼을 추가
    """
    df["요일"] = pd.to_datetime(df[date_column]).dt.day_name()
    return df

def format_datetime_for_filename():
    """
    현재 시간을 YYYYMMDDHH 형식으로 반환 (파일명용)
    """
    return datetime.now().strftime("%Y%m%d%H")

def is_weekend_or_holiday(date_str):
    """
    주말 또는 공휴일 여부 판단 (기본적으로 주말만 처리)
    """
    date = pd.to_datetime(date_str)
    return date.weekday() >= 5  # 토요일(5), 일요일(6)


def format_datetime_for_filename():
    """
    현재 시간을 기반으로 파일명에 사용할 문자열 생성
    예: 20251030_1644
    """
    return datetime.now().strftime("%Y%m%d_%H%M")