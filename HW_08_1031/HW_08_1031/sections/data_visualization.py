# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# from utils.fetch_data import fetch_thingspeak_data
#
# def calculate_vpd(temp, humid):
#     es = 0.6108 * (17.27 * temp) / (temp + 237.3)
#     vpd = (1 - humid / 100) * es
#     return max(vpd, 0)
#
# def calculate_dli(radn, light_hours=12):
#     return radn * 3600 * light_hours / 1_000_000
#
# def calculate_gdd(temp_max, temp_min, base_temp):
#     return max(((temp_max + temp_min) / 2) - base_temp, 0)
#
# def show():
#     st.header("📊 데이터 시각화")
#
#     # 기간 선택
#     st.sidebar.subheader("기간 선택")
#     start_date = st.sidebar.date_input("시작 날짜", datetime.now() - timedelta(days=7))
#     end_date = st.sidebar.date_input("종료 날짜", datetime.now())
#
#     # 집계 단위 선택
#     st.sidebar.subheader("집계 단위 선택")
#     avg_option = st.sidebar.selectbox("데이터 집계 단위", ["원본 데이터", "10분 평균", "1시간 평균", "하루 평균"])
#
#     # GDD 기준 온도 입력 (집계 단위가 하루 평균일 때만 표시)
#     base_temp = 10  # 기본값 설정
#     if avg_option == "하루 평균":
#         base_temp = st.sidebar.number_input("GDD 계산 기준 온도 (°C)", value=10)
#
#     # 데이터 불러오기
#     data = fetch_thingspeak_data(start_date, end_date)
#     if data.empty:
#         st.warning("선택한 기간 동안 데이터가 없습니다.")
#         return
#
#     # 데이터 집계 처리
#     if avg_option == "10분 평균":
#         data = data.resample('10T').mean()
#     elif avg_option == "1시간 평균":
#         data = data.resample('1H').mean()
#     elif avg_option == "하루 평균":
#         data = data.resample('D').mean()
#
#     # 계산 컬럼 추가
#     if avg_option == "원본 데이터":
#         if 'temp' in data.columns and 'humid' in data.columns:
#             data['VPD'] = data.apply(lambda row: calculate_vpd(row['temp'], row['humid']), axis=1)
#     elif avg_option == "하루 평균":
#         if 'radn' in data.columns:
#             data['DLI'] = data['radn'].apply(lambda radn: calculate_dli(radn))
#         if 'temp' in data.columns:
#             data['GDD'] = data['temp'].apply(lambda temp: calculate_gdd(temp, temp, base_temp)).cumsum()
#
#     # 시각화할 데이터 선택
#     st.sidebar.subheader("시각화할 데이터를 선택하세요:")
#     temp_checked = st.sidebar.checkbox("온도(℃)", value=True)
#     humid_checked = st.sidebar.checkbox("습도(%)")
#     radn_checked = st.sidebar.checkbox("일사량(W/㎡)")
#     wind_checked = st.sidebar.checkbox("풍속(m/s)")
#     rainfall_checked = st.sidebar.checkbox("강우량(mm)")
#     battery_checked = st.sidebar.checkbox("배터리 전압(V)")
#     vpd_checked = st.sidebar.checkbox("VPD (kPa)") if avg_option == "원본 데이터" else False
#     gdd_checked = st.sidebar.checkbox("GDD (°C)") if avg_option == "하루 평균" else False
#     dli_checked = st.sidebar.checkbox("DLI (mol/m²/day)") if avg_option == "하루 평균" else False
#
#     # 그래프 구성
#     fig = go.Figure()
#     y_axis_label = []  # y축 레이블에 표시할 선택된 데이터
#
#     # 각 데이터에 대해 선택된 항목을 기준으로 그래프에 추가
#     if temp_checked and 'temp' in data.columns:
#         fig.add_trace(go.Scatter(x=data.index, y=data['temp'], mode='lines+markers', name="Temperature (℃)"))
#         y_axis_label.append("Temperature (℃)")
#     if humid_checked and 'humid' in data.columns:
#         fig.add_trace(go.Scatter(x=data.index, y=data['humid'], mode='lines+markers', name="Humidity (%)"))
#         y_axis_label.append("Humidity (%)")
#     if radn_checked and 'radn' in data.columns:
#         fig.add_trace(go.Scatter(x=data.index, y=data['radn'], mode='lines+markers', name="Radiation (W/㎡)"))
#         y_axis_label.append("Radiation (W/㎡)")
#     if wind_checked and 'wind' in data.columns:
#         fig.add_trace(go.Scatter(x=data.index, y=data['wind'], mode='lines+markers', name="Wind Speed (m/s)"))
#         y_axis_label.append("Wind Speed (m/s)")
#     if rainfall_checked and 'rainfall' in data.columns:
#         fig.add_trace(go.Scatter(x=data.index, y=data['rainfall'], mode='lines+markers', name="Rainfall (mm)"))
#         y_axis_label.append("Rainfall (mm)")
#     if battery_checked and 'battery' in data.columns:
#         fig.add_trace(go.Scatter(x=data.index, y=data['battery'], mode='lines+markers', name="Battery Voltage (V)"))
#         y_axis_label.append("Battery Voltage (V)")
#     if vpd_checked and 'VPD' in data.columns:
#         fig.add_trace(go.Scatter(x=data.index, y=data['VPD'], mode='lines+markers', name="VPD (kPa)"))
#         y_axis_label.append("VPD (kPa)")
#     if gdd_checked and 'GDD' in data.columns:
#         fig.add_trace(go.Scatter(x=data.index, y=data['GDD'], mode='lines+markers', name="GDD (°C)"))
#         y_axis_label.append("GDD (°C)")
#     if dli_checked and 'DLI' in data.columns:
#         fig.add_trace(go.Scatter(x=data.index, y=data['DLI'], mode='lines+markers', name="DLI (mol/m²/day)"))
#         y_axis_label.append("DLI (mol/m²/day)")
#
#     # y축 레이블 설정
#     # fig.update_yaxes(title_text=", ".join(y_axis_label) if y_axis_label else "Values")
#     fig.update_yaxes(title_text="")
#
#     # x축 형식 설정 (날짜와 시간 함께 표시)
#     fig.update_xaxes(
#         title_text="Date (yy/mm/dd)",
#         tickformat="%y/%m/%d<br>%H:%M"
#     )
#
#     # 그래프 레이아웃 설정
#     fig.update_layout(
#         title="환경 데이터 시각화",
#         legend_title="데이터 종류",
#         hovermode="x unified",
#         showlegend=True
#     )
#
#     # 그래프 출력
#     st.plotly_chart(fig)
#
#
#
#
#
#


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.fetch_data import fetch_thingspeak_data
import requests



# 텔레그램 알림 함수
def send_telegram_message(message):
    # Streamlit secrets에서 봇 토큰과 챗 ID를 가져옴
    bot_token = st.secrets["telegram"]["bot_token"]
    chat_id = st.secrets["telegram"]["chat_id"]

    if bot_token and chat_id:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {"chat_id": chat_id, "text": message}
        response = requests.post(url, params=params)
        if response.status_code == 200:
            print("텔레그램 메시지가 성공적으로 전송되었습니다.")
        else:
            print(f"텔레그램 메시지 전송 실패: {response.status_code}")
    else:
        print("텔레그램 봇 토큰 또는 챗 ID가 설정되지 않았습니다.")


def calculate_vpd(temp, humid):
    humid = max(0, min(humid, 100))  # 습도는 0-100%로 제한
    es = 0.6108 * (17.27 * temp) / (temp + 237.3)  # 증기압 계산
    vpd = (1 - humid / 100) * es
    return max(vpd, 0)  # VPD는 음수가 될 수 없으므로 0 이하 값을 방지

def calculate_dli(radn, light_hours=12):
    return radn * 3600 * light_hours / 1_000_000 # 기본 단위: mol/m²/day

def calculate_gdd(temp_max, temp_min, base_temp):
    return max(((temp_max + temp_min) / 2) - base_temp, 0)

def check_rainfall_alert(data, threshold_minutes=30):
    """강우량 체크하기"""
    consecutive_rain = (data['rainfall'] != 0).astype(int)
    consecutive_rain_periods = consecutive_rain.groupby((consecutive_rain != consecutive_rain.shift()).cumsum()).cumsum()

    if (consecutive_rain_periods >= threshold_minutes / 10).any():  # Adjusted for 10-minute intervals
        alert_message = f"⚠️ 30분 이상 연속 강우가 감지되었습니다. 시설을 점검하세요."
        send_telegram_message(alert_message)
        st.warning(alert_message)


def show():
    st.header("📊 데이터 시각화")

    # 기간 선택
    st.sidebar.subheader("기간 선택")
    start_date = st.sidebar.date_input("시작 날짜", datetime.now() - timedelta(days=7))
    end_date = st.sidebar.date_input("종료 날짜", datetime.now())

    # 집계 단위 선택
    st.sidebar.subheader("집계 단위 선택")
    avg_option = st.sidebar.selectbox("데이터 집계 단위", ["원본 데이터", "10분 평균", "1시간 평균", "하루 평균"])

    # 작물 선택 메뉴 추가
    crop = st.sidebar.selectbox("작물을 선택하세요:", ["청경채", "고랭지배추"])

    # 작물에 따른 GDD 기준 온도 및 알림 기준 설정
    if crop == "청경채":
        base_temp = 4.4
    elif crop == "고랭지배추":
        base_temp = 5.0

    # 사용자가 GDD 임계값을 지정할 수 있도록 추가
    gdd_threshold = st.sidebar.number_input(f"{crop}의 GDD 경고 임계값을 설정하세요 (청경채: 400℃, 고랭지배추: 900℃)", min_value=0,
                                            max_value=10000,
                                            step=100)

    # GDD 미리 경고 임계값을 설정 (전체 임계값의 90%)
    pre_warning_threshold = gdd_threshold * 0.9

    # GDD 기준 온도 입력 (집계 단위가 하루 평균일 때만 표시)
    # base_temp = 10  # 기본값 설정
    # if avg_option == "하루 평균":
    #     base_temp = st.sidebar.number_input("GDD 계산 기준 온도 (°C)", value=10)

    # 데이터 불러오기
    data = fetch_thingspeak_data(start_date, end_date)
    if data.empty:
        st.warning("선택한 기간 동안 데이터가 없습니다.")
        return

    # 데이터 집계 처리
    if avg_option == "10분 평균":
        data = data.resample('10T').mean()
    elif avg_option == "1시간 평균":
        data = data.resample('1H').mean()
    elif avg_option == "하루 평균":
        data = data.resample('D').mean()

    # 계산 컬럼 추가
    if avg_option == "원본 데이터":
        if 'temp' in data.columns and 'humid' in data.columns:
            data['VPD'] = data.apply(lambda row: calculate_vpd(row['temp'], row['humid']), axis=1)
    elif avg_option == "하루 평균":
        if 'radn' in data.columns:
            data['DLI'] = data['radn'].apply(lambda radn: calculate_dli(radn))
        if 'temp' in data.columns:
            data['GDD'] = data['temp'].apply(lambda temp: calculate_gdd(temp, temp, base_temp)).cumsum()

            # GDD 90% 도달 시 미리 경고 알림 및 텔레그램 메시지 전송
            if data['GDD'].iloc[-1] >= pre_warning_threshold and data['GDD'].iloc[-2] < pre_warning_threshold:
                pre_warning_message = f"⚠️ {crop}의 누적 GDD가 {gdd_threshold}℃의 90%에 도달했습니다. 수확 준비를 시작하세요!"
                st.warning(pre_warning_message)
                send_telegram_message(pre_warning_message)

            # GDD 기준 도달 시 수확 알림 및 텔레그램 메시지 전송
            if data['GDD'].iloc[-1] >= gdd_threshold and data['GDD'].iloc[-2] < gdd_threshold:
                harvest_message = f"✅ {crop}의 누적 GDD가 {gdd_threshold}℃에 도달했습니다. 수확을 시작하세요!"
                st.success(harvest_message)
                send_telegram_message(harvest_message)

    # 시각화할 데이터 선택
    st.sidebar.subheader("시각화할 데이터를 선택하세요:")
    temp_checked = st.sidebar.checkbox("온도(℃)", value=True)
    humid_checked = st.sidebar.checkbox("습도(%)")
    radn_checked = st.sidebar.checkbox("일사량(W/㎡)")
    wind_checked = st.sidebar.checkbox("풍속(m/s)")
    rainfall_checked = st.sidebar.checkbox("강우량(mm)")
    battery_checked = st.sidebar.checkbox("배터리 전압(V)")
    vpd_checked = st.sidebar.checkbox("VPD (kPa)") if avg_option == "원본 데이터" else False
    gdd_checked = st.sidebar.checkbox("GDD (°C)") if avg_option == "하루 평균" else False
    dli_checked = st.sidebar.checkbox("DLI (mol/m²/day)") if avg_option == "하루 평균" else False

    # Rainfall alert check
    if rainfall_checked and 'rainfall' in data.columns:
        check_rainfall_alert(data)

    # 그래프 구성
    fig = go.Figure()
    y_axis_label = []  # y축 레이블에 표시할 선택된 데이터

    # 각 데이터에 대해 선택된 항목을 기준으로 그래프에 추가
    if temp_checked and 'temp' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['temp'], mode='lines+markers', name="Temperature (℃)"))
        # 작물에 따른 생육 적온 구간을 강조 (색칠)
        if crop == "청경채":
            # 청경채: 20-25도 구간을 색칠
            fig.add_shape(
                type="rect",
                xref="paper", yref="y",
                x0=0, x1=1,  # x 축을 전체 범위로 설정
                y0=20, y1=25,  # 청경채 생육 적온
                fillcolor="LightGreen",  # 구간 색상
                opacity=0.3,  # 투명도 설정
                layer="below",  # 라인 아래에 색칠
                line_width=0  # 선 없애기
            )
        elif crop == "고랭지배추":
            # 고랭지배추: 15-20도 구간을 색칠
            fig.add_shape(
                type="rect",
                xref="paper", yref="y",
                x0=0, x1=1,  # x 축을 전체 범위로 설정
                y0=15, y1=20,  # 고랭지배추 생육 적온
                fillcolor="LightBlue",  # 구간 색상
                opacity=0.3,  # 투명도 설정
                layer="below",  # 라인 아래에 색칠
                line_width=0  # 선 없애기
            )
        y_axis_label.append("Temperature (℃)")
    if humid_checked and 'humid' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['humid'], mode='lines+markers', name="Humidity (%)"))
        y_axis_label.append("Humidity (%)")
    if radn_checked and 'radn' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['radn'], mode='lines+markers', name="Radiation (W/㎡)"))
        y_axis_label.append("Radiation (W/㎡)")
    if wind_checked and 'wind' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['wind'], mode='lines+markers', name="Wind Speed (m/s)"))
        y_axis_label.append("Wind Speed (m/s)")
    if rainfall_checked and 'rainfall' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['rainfall'], mode='lines+markers', name="Rainfall (mm)"))
        y_axis_label.append("Rainfall (mm)")
    if battery_checked and 'battery' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['battery'], mode='lines+markers', name="Battery Voltage (V)"))
        y_axis_label.append("Battery Voltage (V)")
    if vpd_checked and 'VPD' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['VPD'], mode='lines+markers', name="VPD (kPa)"))
        y_axis_label.append("VPD (kPa)")
    if gdd_checked and 'GDD' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['GDD'], mode='lines+markers', name="GDD (°C)"))
        y_axis_label.append("GDD (°C)")
    if dli_checked and 'DLI' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['DLI'], mode='lines+markers', name="DLI (mol/m²/day)"))
        y_axis_label.append("DLI (mol/m²/day)")

    # y축 레이블 설정
    # fig.update_yaxes(title_text=", ".join(y_axis_label) if y_axis_label else "Values")
    fig.update_yaxes(title_text="")

    # x축 형식 설정 (날짜와 시간 함께 표시)
    fig.update_xaxes(
        title_text="Date (yy/mm/dd)",
        tickformat="%y/%m/%d<br>%H:%M"
    )

    # 그래프 레이아웃 설정
    fig.update_layout(
        title="환경 데이터 시각화",
        legend_title="데이터 종류",
        hovermode="x unified",
        showlegend=True
    )

    # 그래프 출력
    st.plotly_chart(fig)





