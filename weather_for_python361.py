#WARNING: This program may ONLY SUIT FOR Python 3.6.1
#Version 1.2.20210618

#导入运行库
import requests
from bs4 import BeautifulSoup
import datetime
import time
import sys

#函数定义
num_a = ['0','1','2','3','4','5','6','7','8','9','0']
#数据文件丢失、找不到时
def file_not_found():
    print('错误：找不到数据文件！')
    print('请检查你的编辑器启动路径。如果该路径下没有citydata.txt数据文件，')
    print('请将这文件拷贝至编辑器启动路径。例如：已知Microsoft Visual Studio Code')
    print("存在这个问题，因为其使用的Powershell默认以C:\\Users\\*用户名*为启动路径")
    sys.exit()

#在数据文件中检查到错误
def file_read_error():
    print('错误：数据文件被损坏')
    sys.exit()

#检查城市是否为行政区
def district_check(ct_name):
    district = False
    for letter in ct_name:
        if letter == '#':
            district = True
            break
        else:
            pass
    
    if district == True:
        return True
    else:
        return False

#检查一个城市下是否有已记录的行政区
def province_check(ct_name):
    province = False
    for letter in ct_name:
        if letter == '>':
            province = True
            break
        else:
            pass
    
    if province == True:
        return True
    else:
        return False

#删除城市前的#号行政区标识符
def delete_num_sign(ct_name):
    out_word = ''
    for letter in ct_name:
        if letter == '#':
            pass
        else:
            out_word += letter

    return out_word

#删除城市前的>号存在已记录行政区标识符
def delete_bracket(ct_name):
    out_word = ''
    for letter in ct_name:
        if letter == '>':
            pass
        else:
            out_word += letter

    return out_word

#获得温度的数字表示并去除符号
def tempe_int_get(tempe):
    cold_temte = False
    tempe_out = 0
    for letter in tempe:
        if letter == '℃':
            break
        elif letter == '-':
            cold_temte = True
        else:
            tempe_out = tempe_out*10+int(letter)
    if cold_temte:
        tempe_out = -tempe_out
    
    return tempe_out

#删除除数字外的字符
def delete_except_num(ct_code):
    ot_code = ''
    for letter in ct_code:
        if letter in num_a:
            ot_code += letter
        else:
            pass
    return ot_code

#准备支持的城市ID对应字典
#准备主要城市名、城市编号
#对应城市行政区划分
print('>>读取数据...')
district_city = []
city_key = []
city_value = []
cities = {}
city_name = True
try:
    with open('citydata.txt', 'r', encoding='utf-8') as key_object:
        for line in key_object:
            line = line.rstrip()
            if line == '':
                continue
            if city_name == True:
                if district_check(line):
                    #不记录行政区
                    pass
                else:
                    if province_check(line):
                        #去除含>的城市前的符号并加入含行政区城市列表
                        district_city.append(delete_bracket(line))
                        city_key.append(delete_bracket(line))
                        city_name = False
                    else:
                        city_key.append(line)
                        city_name = False
            else:
                if district_check(line):
                    #不记录行政区
                    pass
                else:
                    city_value.append(str(line))
                    city_name = True
except FileNotFoundError:
    file_not_found()

#将所有可查询的城市写入文件
all_city = []
all_code = []
record_city = []
with open('citydata.txt', 'r', encoding='utf-8') as key_object:
    city_name = True
    for line in key_object:
        line = line.rstrip()
        if city_name == True:
            all_city.append(line)
            city_name = False
        else:
            #去除数字前的#号并写入列表
            putin_letter = delete_num_sign(line)
            all_code.append(putin_letter)
            city_name = True

#纠错程序
if len(city_key) != len(city_value):
    file_read_error()
if len(all_city) != len(all_code):
    file_read_error()
if len(all_city) == 0:
    file_read_error()

#将主要城市写入字典
write_number = 0
while write_number < len(city_key):
    write_key = city_key[write_number]
    write_value = city_value[write_number]
    cities[write_key] = write_value
    write_number += 1

#输出信息
print('这个程序由张义文-Matt Zhang设计')
time.sleep(0.5)
print('--------------------')
print('如果你对于输入什么城市名称(内容)有疑惑，请键入[city]')

#准备资源
district_print = False
check_box = True
supported_cities = []
for city_name in cities.keys():
    supported_cities.append(city_name)

search_district = []
#询问城市
while check_box:
    city = input('输入城市名称(例如：贵阳市)：')

    if city == 'city':
        #帮助文件
        print_sen = ''
        write_number = 0
        print_sen += '所有支持查询的城市(不包含区，含*号表示该城市有下属行政区可查询)：'
        for p_city in supported_cities:
            print_sen += p_city
            if p_city in district_city:
                print_sen += '*'
            write_number += 1
            if write_number < len(supported_cities):
                print_sen += '、'
            else:
                print_sen += '.'

        print(print_sen)
    #检查城市是否在数据文件中
    if city in supported_cities:
        if city in district_city:
            #含有下属行政区的城市
            print('提示：目前'+city+'有一个或多个下属行政区可供查询。')
            print('但您也可以继续查询'+city+'的天气')
            user_answer = input('继续查询'+city+'的天气请输入[y]，否则输入其他字符：')
            if user_answer == 'y':
                city_code = cities[city]
                break
            #查找该城市
            check_number = 0
            search_number = 0
            search_district = []
            record_city = []
            all_items = len(all_city) - 1
            while check_number <= all_items:
                if city == delete_bracket(all_city[check_number]):
                    #记录其在所有城市列表中的位置
                    search_number = check_number
                    break
                else:
                    check_number += 1
            district_check_box = True
            search_number += 1
            while district_check_box and search_number<len(all_city):
                #从匹配城市向后顺序查找含#的城市
                if district_check(all_city[search_number]):
                    search_district.append(delete_num_sign(all_city[search_number]))
                    record_city.append(search_number)
                    search_number += 1
                    district_check_box = True
                else:
                    #当查找到没有#的城市时停止
                    district_check_box = False
            write_number = 0
            #输出查找到的行政区信息
            print('--------------------')
            print_sen = '所有'+city+'可供查询的区：'
            for dis_city in search_district:
                write_number += 1
                print_sen += dis_city
                if write_number < len(search_district):
                    print_sen += '、'
                else:
                    print_sen += '.'
            print(print_sen)
            print('请在下方输入上方展示的'+city+'的某个区以查询天气')
            print('--------------------')
            city_district = city
        else:
            check_box = False
            city_code = cities[city]
    elif city == 'city':
        pass
    elif city in search_district:
        #搜索含行政区的城市后储存的上一次查询城市
        write_number = 0
        while True:
            if city == search_district[write_number]:
                check_box = False
                district_print = True
                city_code = all_code[record_city[write_number]]
                break
            else:
                write_number += 1
    else:
        check_box = True
        print('请输入一个受支持的城市名称（注意必须全字匹配）')
        print('如果你对于输入什么城市名称有疑惑，请键入‘city’')

#自检模块
try:
    city_code = int(city_code)
except ValueError:
    print('检测到可能的文件损坏，正在尝试修复')
    city_code = delete_except_num(city_code)
else:
    city_code = str(city_code)
print('>>连接中...')

#定义网页
url_1day = 'http://www.weather.com.cn/weather1d/'+city_code+'.shtml'
url_7day = 'http://www.weather.com.cn/weather/'+city_code+'.shtml'

#获取及解析网页，并在连接失败时发出警告
check_box = True
try_times = 0
retry_sta = False
while check_box:
    try:
        check_box = False
        response_web_1day = requests.get(url_1day)
    except requests.exceptions.ConnectionError:
        print('错误：无法连接中国天气网：请检查你的网络连接！')
        if retry_sta == False:
            print('将在7秒后重试')
            retry_sta = True
            check_box = True
            time.sleep(7)

    
try:
    response_web_1day.encoding = 'utf-8'
except NameError:
    print('错误：无法解析网页')
    sys.exit()

check_box = True
try_times = 0
retry_sta = False

while check_box:
    try:
        check_box = False
        response_web_7day = requests.get(url_7day)
    except requests.exceptions.ConnectionError:
        print('错误：无法连接中国天气网：请检查你的网络连接！')
        if retry_sta == False:
            print('将在7秒后重试')
            retry_sta = True
            check_box = True
            time.sleep(7)

    
try:
    response_web_7day.encoding = 'utf-8'
except NameError:
    print('错误：无法解析网页')
    sys.exit()

bt_soup_1day = BeautifulSoup(response_web_1day.text, 'lxml')
bt_soup_7day = BeautifulSoup(response_web_7day.text, 'lxml')

#自检模块
try:
    check_web = str(bt_soup_1day.find(id='hidden_title')['value'])
except TypeError:
    print('找不到该城市天气信息')
    file_read_error()

#获取今天的数据
all_today_data = str(bt_soup_1day.find(id='hidden_title')['value'])
hour_data_3 = str(bt_soup_1day.find(id='today').script.string)
update_time = str(bt_soup_1day.find(id="update_time")['value'])
sun_up = str(bt_soup_1day.find(class_='sun sunUp').span.string)
sun_down = str(bt_soup_1day.find(class_='sun sunDown').span.string)
weather_day = str(bt_soup_1day.find_all(class_='wea')[0]['title'])
weather_night = str(bt_soup_1day.find_all(class_='wea')[1]['title'])
wind_day = str(bt_soup_1day.find_all(class_='win')[0].span['title'])
wind_night = str(bt_soup_1day.find_all(class_='win')[0].span['title'])
max_tempe_today = str(bt_soup_1day.find_all(class_='tem')[1].span.string)
min_tempe_today = str(bt_soup_1day.find_all(class_='tem')[0].span.string)
wind_level_today = str(bt_soup_1day.find_all(class_='win')[0].span.string)
ray_today = str(bt_soup_1day.find_all(class_='li1 hot')[0].span.string)
#获取明天的数据
all_tomorrow = bt_soup_7day.find_all(class_='c7d')[0]
weather_tomorrow = str(all_tomorrow.find_all(class_='wea')[1]['title'])
tempe_tomorrow = all_tomorrow.find_all(class_='tem')[1]
tempe_high_tomorrow = str(tempe_tomorrow.span.string)
tempe_low_tomorrow = str(tempe_tomorrow.i.string)
wind_tomorrow = all_tomorrow.find_all(class_='win')[1].find_all('span')
wind_tomorrow_day = str(wind_tomorrow[0]['title'])
wind_tomorrow_night = str(wind_tomorrow[1]['title'])
wind_level_tomorrow = str(all_tomorrow.find_all(class_='win')[1].i.string)

#输出天气
if district_print == True:
    print('\n当前查询的城市(区)：'+city_district+'-'+city)
else:
    print('\n当前查询的城市(区)：'+city)

print_sentence = '现在是'+str(datetime.date.today().year)+'年'
print_sentence += str(datetime.date.today().month)+'月'+str(datetime.date.today().day)+'日'
print(print_sentence,datetime.datetime.now().strftime('%a. %H:%M:%S'))

#日出日落
#转换为有格式的时间
time = []
for letter in sun_up:
    time.append(letter)
hour = int(time[3]+time[4])
minute = int(time[6]+time[7])
sun_rise = datetime.time(hour,minute,0,0)

time = []
for letter in sun_down:
    time.append(letter)
hour = int(time[3]+time[4])
minute = int(time[6]+time[7])
sun_fall = datetime.time(hour,minute,0,0)
time_now = datetime.datetime.now().time()

#输出日出日落信息
if sun_rise.__lt__(time_now):
    if sun_fall.__lt__(time_now):
        print('现在是夜间')
    else:
        fall_minute = sun_fall.minute - time_now.minute
        fall_hour = sun_fall.hour - time_now.hour
        if fall_minute < 0:
            fall_hour -= 1
            fall_minute += 60
        
        if fall_hour != 0:
            print('还有'+str(fall_hour)+'小时'+str(fall_minute)+'分钟太阳落山')
        else:
            print('还有'+str(fall_minute)+'分钟太阳落山')
else:
    rise_minute = sun_rise.minute - time_now.minute
    rise_hour = sun_rise.hour - time_now.hour
    if rise_minute < 0:
        rise_hour -= 1
        rise_minute += 60

    if rise_hour != 0:
        print('还有'+str(rise_hour)+'小时'+str(rise_minute)+'分钟太阳升起')
    else:
        print('还有'+str(rise_minute)+'分钟太阳升起')

print('上一次天气更新时间', update_time)

#输出天气更新时间(精确到小时)的数字形式
num_upt = 0
for letter in update_time:
    if letter == ':':
        break
    else:
        num_upt = num_upt*10 + int(letter)

#检查天气更新时间是否在当天18时后
if num_upt >= 18:
    tempe_night_mode = True
else:
    tempe_night_mode = False

if weather_day == weather_night:
    print('\n'+city+'今天的天气是'+weather_day)
else:
    print('\n'+city+'今天的天气是'+weather_day+'转'+weather_night)

#紫外线指数检测提示
print('今天的紫外线指数等级'+ray_today)
if ray_today == '最弱':
    print('可涂擦SPF8-12防晒护肤品保护皮肤')
elif ray_today == '很弱':
    print('可涂擦SPF8-12防晒护肤品保护皮肤')
elif ray_today == '弱':
    print('可涂擦SPF12-15、PA+护肤品保护皮肤')
elif ray_today == '中等':
    print('提示：当地紫外线辐射相对较强，请做好个人防护，')
    print('同时涂擦SPF大于15、PA+防晒护肤品。')
elif ray_today == '较强':
    print('提示：当地紫外线辐射相对较强，请做好个人防护，')
    print('同时涂擦SPF大于15、PA+防晒护肤品。')
elif ray_today == '强':
    print('提示：当地紫外线辐射较强，请做好个人防护，减少不必要出门，')
    print('同时涂擦SPF大于15、PA+防晒护肤品。尽量避免强光直射')
elif ray_today == '很强':
    print('提示：当地紫外线辐射强，请做好个人防护，减少不必要出门，')
    print('同时涂擦SPF20以上、PA++护肤品，避免强光直射。')
elif ray_today == '最强':
    print('提示：当地紫外线辐射强，请做好个人防护，减少不必要出门，')
    print('同时涂擦SPF20以上、PA++护肤品，避免强光直射。')
else:
    print('请注意防护紫外线伤害！')

#注意：已知问题，傍晚18时之后显示的是当天晚上及明天早晨的温度！（待验证）
#将温度转换为整数
min_tempe_today_int = tempe_int_get(min_tempe_today)
max_tempe_today_int = tempe_int_get(max_tempe_today) 

if min_tempe_today_int > max_tempe_today_int:
    switch_tem = min_tempe_today_int
    min_tempe_today_int = max_tempe_today_int
    max_tempe_today_int = switch_tem

if tempe_night_mode == False:
    print('气温是'+str(min_tempe_today_int)+'℃ ~'+str(max_tempe_today_int)+'℃')
    #检查温差、温度
    if max_tempe_today_int >= 20:
        print('提示：今天气温较高')
    elif min_tempe_today_int <= 5:
        print('今天气温较低，注意增加衣物保暖')

    if max_tempe_today_int-min_tempe_today_int >= 8:
        if max_tempe_today_int>17 and min_tempe_today_int<12:
            print('今天早晚温差较大，注意增减衣物')
elif tempe_night_mode == True:
    print('今天夜间气温是'+str(min_tempe_today_int)+'℃')


#风向
if time_now.hour <= 15:
    if wind_day == '无持续风向':
        print('今天白天无风')
    else:
        print('今天白天有'+wind_day+'，风力'+wind_level_today)
else:
    if wind_night == '无持续风向':
        print('今天夜间无风')
    else:
        print('今天夜间有'+wind_night+'，风力'+wind_level_today)

#明天天气状况
print('\n--------------------')
print(city+'明天的天气是'+weather_tomorrow)
check_box = False
for letter in tempe_high_tomorrow:
    if letter == '℃':
        check_box = True
if check_box:
    print('气温是'+tempe_low_tomorrow+' ~'+tempe_high_tomorrow)
else:
    print('气温是'+tempe_low_tomorrow+' ~'+tempe_high_tomorrow+'℃')

#检查温差、温度
tempe_low_tomorrow_int = tempe_int_get(tempe_low_tomorrow)
tempe_high_tomorrow_int = tempe_int_get(tempe_high_tomorrow)

if tempe_low_tomorrow_int >= 20:
    print('提示：明天气温较高')
elif tempe_high_tomorrow_int <= -5:
    print('明天气温寒冷，注意增加衣物保暖')
elif tempe_high_tomorrow_int <= 5:
    print('明天气温较低，注意增加衣物保暖')

if tempe_high_tomorrow_int-tempe_low_tomorrow_int >= 8:
    if tempe_high_tomorrow_int>17 and tempe_low_tomorrow_int<12:
        print('明天早晚温差较大，注意增减衣物')

#明天风向
if wind_tomorrow_day == wind_tomorrow_night:
    if wind_tomorrow_day == '无持续风向':
        print('明天全天无风')
    else:
        print('明天全天有'+wind_tomorrow_day+'，风力'+wind_level_tomorrow)
elif wind_tomorrow_day == '无持续风向':
    print('明天白天有无风，而夜间有'+wind_tomorrow_night+'，风力'+wind_level_tomorrow)
elif wind_tomorrow_night == '无持续风向':
    print('明天白天有'+wind_tomorrow_day+'，而夜间有无风')
else:
    print('明天白天有'+wind_tomorrow_day+'，而夜间有'+wind_tomorrow_night+'，风力'+wind_level_tomorrow)