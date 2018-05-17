import re

#####clas,関数の定義###################################################################################

class Working_data:
    def __init__(self,data,week_set):
        self.day = int(data[0].split("/")[2])
        self.week = (self.day + week_set) % 7
        self.week_number = int(self.week/7)
        self.work_times = len(data)-1
        self.start = []
        self.end = []
        for i in range(self.work_times):
            time = re.split("[:-]",data[i+1])
            start_time = int(time[0])*60+int(time[1])
            end_time = int(time[2])*60+int(time[3])
            self.start.append(start_time)
            self.end.append(end_time)
    


#先月の部分か今月の部分かを判定
def Check_month(data,month):
    check_month=data[0].rsplit("/",1)[0]
    if check_month == month:
        return "This month"

#データの読み込み,今月の月,データのインスタンスを作成,曜日ごとのにデータを格納
#week_setで曜日と日付を固定する
def Input():
    month = "month"
    input_other = []
    input_fri = []
    input_sat = []
    input_sun = []
    line_count = 0
    first_day_check = 0
    week_set = 0
    f = open("test.txt")
    for line in f:
        data = line.split()
        if line_count == 0:
            month = data[0]
        elif Check_month(data,month) == "This month":
            first_day_check += 1
            working_data = Working_data(data,week_set)
            if first_day_check == 1:
                week_set = line_count - int(data[0].split("/")[2])
        
            if working_data.week == 5:
                input_fri.append(working_data)
            elif working_data.week == 6:
                input_sat.append(working_data)
            elif working_data.week == 0:
                input_sun.append(working_data)
            else:
                input_other.append(working_data)
    
        line_count += 1
    
    f.close    
    return  month, input_other, input_fri, input_sat, input_sun

#分を時間に変換
def Sum_hour_calculation(time_sum_minute):
    time_sum = []
    for i in time_sum_minute:
        hour = int(i/60)
        if i%60 >= 30:
            hour +=1
        time_sum.append(hour)
    return time_sum

#法定内と外残業時間
def Legal_out_time(input_weekday):
    work_time = 0
    legal_in_time = 0
    legal_out_time = 0
    after_16_time = 0
    for i in input_weekday:
        for j in range(i.work_times):
            #work_timeは1日の労働時間
            work_time += i.end[j] - i.start[j]
            if i.start[j] < 960 and i.end[j] > 960:
                after_16_time += i.end[j] - 960
            elif i.start[j] >= 960:
                after_16_time += i.end[j] - i.start[j]
        if work_time > 420:
            if work_time - after_16_time > 420:
                if work_time > 480:
                    legal_in_time += 60
                else:
                    legal_in_time += work_time - 420





#深夜残業時間を計算
def Night_time_calculation(input):
    night_time = 0
    for i in input:
        end = i.end
        for j in end:
            t = j - 1320
            if t > 0:
                night_time += t
    return night_time

#所定休日労働時間の計算
def Pre_holiday_time_fri(input_fri):
    pre_holiday_time = 0
    for i in input_fri:
        for j in range(i.work_times):
            t = i.end[j] - 1440
            if t > 0:
                pre_holiday_time += t
    return pre_holiday_time


def Pre_holiday_time_sat(input_sat):
    pre_holiday_time = 0
    for i in input_sat:
        for j in range(i.work_times):
            pre_holiday_time += i.end[j] - i.start[j]
    return pre_holiday_time


#法定休日労働時間の計算
def Legal_holiday_time_sat(input_sat):
    legal_holiday_time = 0
    for i in input_sat:
        for j in range(i.work_times):
            t = i.end[j] - 1440
            if t > 0:
                legal_holiday_time += t
    return legal_holiday_time

def Legal_holiday_time_sun(input_sun):
    legal_holiday_time = 0
    for i in input_sun:
        for j in range(i.work_times):
            legal_holiday_time += i.end[j] - i.start[j]
    return legal_holiday_time

#結果の出力
def Print_result(time_sum):
    for i in time_sum:
        print(i)


####メイン部分,関数を利用###############################################################################

#初期設定
time_sum_minute = [0,0,0,0,0]
input_other = []
input_fri= []
input_sat = []
input_sun = []
month, input_other, input_fri, input_sat, input_sun = Input()

#法定内業時間


#法定外残業時間

#深夜残業時間を計算
time_sum_minute[2] = Night_time_calculation(input_other) + Night_time_calculation(input_fri) +Night_time_calculation(input_sat) + Night_time_calculation(input_sun)

#所定休日労働時間を計算
time_sum_minute[3] = Pre_holiday_time_fri(input_fri) + Pre_holiday_time_sat(input_sat)

#法定休日労働時間を計算
time_sum_minute[4] =  Legal_holiday_time_sat(input_sat) + Legal_holiday_time_sun(input_sun)

#分を時間に変換
time_sum = Sum_hour_calculation(time_sum_minute)

#結果の出力
Print_result(time_sum)








