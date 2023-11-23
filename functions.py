import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

def maindef(month, day, time, subwayStop, direction):
    # 몇호선인지 판별하기 위한 변수 (etc.군자역의 경우 5호선, 7호선 동시 존재)
    global status
    line = 0
    week_day = ""

    direc_dict = {
        "up": "상선",
        "down": "하선",
        "in": "내선",
        "out": "외선"
    }

    if day == "HOL":
        week_day = "공휴일"
    elif day == "MON" or day == "TUE" or day == "WED" or day == "THU" or day == "FRI":
        week_day = "평일"
    elif day == "SAT":
        week_day = "토요일"

    direction = direc_dict.get(direction)

    if subwayStop == "어린이대공원역 7호선":
        line = 7.0
        if direction == "상선":
            subwayStop = "군자"
        if direction == "하선":
            subwayStop = "건대입구"
    elif subwayStop == "건대입구역 7호선":
        line = 7.0
        if direction == "상선":
            subwayStop = "어린이대공원"
        if direction == "하선":
            subwayStop = "뚝섬유원지"
    elif subwayStop == "건대입구역 2호선":
        line = 2.0
        if direction == "내선":
            subwayStop = "구의"
        if direction == "외선":
            subwayStop = "뚝섬"

    # print(day, direction, subwayStop, line)

    # 처리할 데이터 판별

    # CSV 파일 읽기
    # print(f"File path: {file_path}")
    data = pd.read_csv("dataset/Congestion.csv")

    # # 한글 폰트 설정
    # rc('font', family='AppleGothic')

    # '역번호'가 1과 2이고 '상하구분'이 '외선'인 데이터 필터링
    filtered_data = data[(data['출발역'] == subwayStop) & (data['상하구분'] == direction) & (data['호선'] == line)].copy()
    # print(filtered_data)

    # 05시 30분, 00시 30분의 데이터와 인덱스 삭제
    filtered_data = filtered_data.drop(['5시30분', '00시30분', '00시00분'], axis=1)

    # 시간열 선택
    time_columns = filtered_data.columns[6:]

    # 날짜별로 데이터 분류하기 (평일, 토요일, 공휴일)
    weekday_data = filtered_data[filtered_data['요일구분'] == '평일']
    saturday_data = filtered_data[filtered_data['요일구분'] == '토요일']
    holiday_data = filtered_data[filtered_data['요일구분'] == '공휴일']

    # 시간열을 30분 간격으로 묶어 평균 계산
    average_weekday = []
    average_saturday = []
    average_holiday = []
    average_time_list = [time.split('시')[0] + '시' for time in time_columns if time.endswith('00분')]

    for i in range(0, len(time_columns), 2):
        start_index = filtered_data.columns.get_loc(time_columns[i])
        end_index = filtered_data.columns.get_loc(time_columns[i + 1]) + 1
        average_weekday.append(weekday_data.iloc[:, start_index:end_index].mean(axis=1).values[0])
        average_saturday.append(saturday_data.iloc[:, start_index:end_index].mean(axis=1).values[0])
        average_holiday.append(holiday_data.iloc[:, start_index:end_index].mean(axis=1).values[0])

    if week_day == "공휴일":
        # # 시간대별 데이터 시각화
        # plt.figure(figsize=(12, 6))
        # plt.plot(range(0, len(time_columns), 2), average_holiday, label='공휴일')
        # plt.title(f'{subwayStop}역 {direction} 특정 시간대별 평균 승객 수')
        # plt.xlabel('시간')
        # plt.ylabel('평균 승객 수')
        # plt.legend()
        # plt.xticks(range(0, len(time_columns), 2), [time_columns[i] for i in range(0, len(time_columns), 2)],
        #            rotation=45)
        # plt.grid(True)
        # # 값 표시
        # for i in range(len(average_holiday)):
        #     plt.text(i * 2, average_holiday[i], f'{average_holiday[i]:.2f}', ha='right', va='bottom', fontsize=8,
        #              color='blue')
        # plt.show()
        status = get_status_time(average_holiday, average_time_list, time, month, day)
    elif week_day == "평일":
        # # 시간대별 데이터 시각화
        # plt.figure(figsize=(12, 6))
        # plt.plot(range(0, len(time_columns), 2), average_weekday, label='평일')
        # plt.title(f'{subwayStop}역 {direction} 특정 시간대별 평균 승객 수')
        # plt.xlabel('시간')
        # plt.ylabel('평균 승객 수')
        # plt.legend()
        # plt.xticks(range(0, len(time_columns), 2), [time_columns[i] for i in range(0, len(time_columns), 2)],
        #            rotation=45)
        # plt.grid(True)
        # # 값 표시
        # for i in range(len(average_weekday)):
        #     plt.text(i * 2, average_weekday[i], f'{average_weekday[i]:.2f}', ha='right', va='bottom', fontsize=8,
        #              color='blue')
        # plt.show()
        status = get_status_time(average_weekday, average_time_list, time, month, day)
    elif week_day == "토요일":
        # # 시간대별 데이터 시각화
        # plt.figure(figsize=(12, 6))
        # plt.plot(range(0, len(time_columns), 2), average_saturday, label='토요일')
        # plt.title(f'{subwayStop}역 {direction} 특정 시간대별 평균 승객 수')
        # plt.xlabel('시간')
        # plt.ylabel('평균 승객 수')
        # plt.legend()
        # plt.xticks(range(0, len(time_columns), 2), [time_columns[i] for i in range(0, len(time_columns), 2)],
        #            rotation=45)
        # plt.grid(True)
        # # 값 표시
        # for i in range(len(average_saturday)):
        #     plt.text(i * 2, average_saturday[i], f'{average_saturday[i]:.2f}', ha='right', va='bottom', fontsize=8,
        #              color='blue')
        # plt.show()
        status = get_status_time(average_saturday, average_time_list, time, month, day)

    return status


# 시간으로 분류
def get_status_time(data, time_list, time, month, day):
    status_dict = {
        "6시": [],
        "7시": [],
        "8시": [],
        "9시": [],
        "10시": [],
        "11시": [],
        "12시": [],
        "13시": [],
        "14시": [],
        "15시": [],
        "16시": [],
        "17시": [],
        "18시": [],
        "19시": [],
        "20시": [],
        "21시": [],
        "22시": [],
        "23시": []
    }
    # print(len(time_columns))
    for i in range(len(data)):
        data_value = float(data[i])
        time_key = time_list[i]
        # print(data_value)
        if data_value <= 45.0:
            status_dict[time_key].append(("good", 8))
            if data_value < 30.0:
                status_dict[time_key].pop()
                status_dict[time_key].append(("good", 9))
                if data_value < 15.0:
                    status_dict[time_key].pop()
                    status_dict[time_key].append(("good", 10))
        elif data_value <= 90.0:
            status_dict[time_key].append(("soso", 5))
            if data_value < 75.0:
                status_dict[time_key].pop()
                status_dict[time_key].append(("soso", 6))
                if data_value < 60.0:
                    status_dict[time_key].pop()
                    status_dict[time_key].append(("soso", 7))
        elif data_value <= 150.0:
            status_dict[time_key].append(("bad", 1))
            if data_value < 135.0:
                status_dict[time_key].pop()
                status_dict[time_key].append(("bad", 2))
                if data_value < 120.0:
                    status_dict[time_key].pop()
                    status_dict[time_key].append(("bad", 3))
                    if data_value < 105.0:
                        status_dict[time_key].pop()
                        status_dict[time_key].append(("bad", 4))

    time = time.split(":")[0] + "시"
    time_index = str(int(str(time.split('시')[0]))) + "시"
    MON_index = ["9시", "22시", "23시"]
    FRI_index = ["16시", "17시", "18시", "19시", "20시", "21시", "22시", "23시"]
    # 월, 요일, 시간대별 가중치 적용
    if day=="MON":
        for i in MON_index:
            temp = list(status_dict[i][0])
            if (temp[1] < 10):
                temp[1] += 1
            temp = tuple(temp)
            status_dict[i].pop()
            status_dict[i].append(temp)
            if status_dict[i][0][1] >= 8:
                temp2 = list(status_dict[i][0])
                temp2[0] = "good"
                temp2 = tuple(temp2)
                status_dict[i].pop()
                status_dict[i].append(temp2)
            elif status_dict[i][0][1] >= 4:
                temp3 = list(status_dict[i][0])
                temp3[0] = "soso"
                temp3 = tuple(temp3)
                status_dict[i].pop()
                status_dict[i].append(temp3)
            elif status_dict[i][0][1] >= 4:
                temp4 = list(status_dict[i][0])
                temp4[0] = "bad"
                temp4 = tuple(temp4)
                status_dict[i].pop()
                status_dict[i].append(temp4)
    elif day == "FRI":
        for i in FRI_index:
            temp = list(status_dict[i][0])
            if (temp[1] < 10):
                temp[1] -= 1
            temp = tuple(temp)
            status_dict[i].pop()
            status_dict[i].append(temp)
            if status_dict[i][0][1] >= 8:
                temp2 = list(status_dict[i][0])
                temp2[0] = "good"
                temp2 = tuple(temp2)
                status_dict[i].pop()
                status_dict[i].append(temp2)
            elif status_dict[i][0][1] >= 4:
                temp3 = list(status_dict[i][0])
                temp3[0] = "soso"
                temp3 = tuple(temp3)
                status_dict[i].pop()
                status_dict[i].append(temp3)
            elif status_dict[i][0][1] >= 4:
                temp4 = list(status_dict[i][0])
                temp4[0] = "bad"
                temp4 = tuple(temp4)
                status_dict[i].pop()
                status_dict[i].append(temp4)

    status = status_dict[time_index][0][0]
    data = []
    now = int(str(time.split('시')[0]))
    #print(now)
    if now == 6 or now == 7:
        for i in range(6, 11):
            data.append((str(i), status_dict.get(str(i) + "시")[0][1]))
    elif now == 22 or now == 23:
        for i in range(19, 24):
            data.append((str(i), status_dict.get(str(i) + "시")[0][1]))
    else:
        for i in range(now - 2, now + 3):
            data.append((str(i), status_dict.get(str(i) + "시")[0][1]))

    # print(time)
    # print(status)
    return status, data