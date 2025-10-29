import pandas as pd
import numpy as np

# 날짜 생성
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")

attendance = []
np.random.seed(42)

for d in dates:
    # 기본값: 평일 500명, 주말 220명
    if d.weekday() < 5:  # 월~금
        base = 500
    else:  # 토/일
        base = 220
    
    # 계절성 반영
    if d.month in [7, 8]:  # 여름휴가철
        base *= 0.8
    if d.month == 12:  # 연말 변동성
        base *= np.random.uniform(0.8, 1.2)
    
    # 노이즈 추가
    count = int(base + np.random.normal(0, 50))
    
    # 최소/최대 보정
    count = max(50, min(1000, count))
    
    attendance.append(count)

df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "attendance_count": attendance})

# CSV 저장
df.to_csv("past_attendance.csv", index=False)
print("past_attendance.csv 생성 완료")