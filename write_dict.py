#Version 1.1.20210619
import sys
import os

try:
    with open('citydata.txt', 'r', encoding='utf-8') as file_object:
        file_object.close()
except FileNotFoundError:
    file_mode = 0
else:
    file_mode = 1

def check_num_sign(city_name):
    for letter in city_name:
        if letter == '#':
            ns_ck = True
            break
        else:
            ns_ck = False

    if ns_ck == True:
        return True
    else:
        return False

def check_bracket(city_name):
    for letter in city_name:
        if letter == '>':
            ns_ck = True
            break
        else:
            ns_ck = False

    if ns_ck == True:
        return True
    else:
        return False

def delete_bracket(ct_name):
    out_word = ''
    for letter in ct_name:
        if letter == '>':
            pass
        else:
            out_word += letter

    return out_word

city_list = []
city_code = []
if file_mode == 1:
    with open('citydata.txt', 'r+', encoding='utf-8') as file_object:
        city_check = True
        for line in file_object:
            line = line.rstrip()
            if city_check == True:
                city_list.append(line)
                city_check = False
            else:
                city_code.append(line)
                city_check = True
elif file_mode == 0:
    with open('citydata.txt', 'w', encoding='utf-8') as file_object:
        inp_city = input('城市名称：')
        inp_code = input('城市编号：')

        file_object.write(inp_city)
        file_object.write('\n')
        file_object.write(inp_code)
        sys.exit()


user_answer = input('增加(a)、修改(r)、删除(d): ')
if user_answer == 'a':
    check_box = True
    with open('citydata.txt', 'a', encoding='utf-8') as file_object:
        while check_box:
            revise_city = input('城市名: ')
            revise_code = input('城市号码: ')
            print('将增加的城市:', revise_city)
            print('此城市的号码:', revise_code)
            check_write = input('确认？(y): ')
            if check_write == 'y':
                check_box = False
                file_object.write('\n')
                file_object.write(revise_city)
                file_object.write('\n')
                file_object.write(revise_code)

if user_answer == 'r':
    print_sen = ''
    write_num = 0
    for city_name in city_list:
        print_sen += str(write_num)
        print_sen += city_name
        write_num += 1
        if write_num < len(city_list):
            print_sen += '、'
        else:
            print_sen += '.'

    print('前面有[>]符号的为有行政区的城市，[#]为行政区')
    print('所有城市：' + print_sen)
    user_ans = input('输入要操作的城市"号码"(从0开始): ')
    user_ans = int(user_ans)
    if check_num_sign(city_list[user_ans]):
        user_answer == input('修改城市代号？(y)')
        if user_answer == 'y':
            user_answer = input('修改为: ')
            city_code[user_ans] = user_answer
        else:
            print('已退出')
    else:
        user_answer = input('修改城市代号(1)、增加行政区(2): ')
        if user_answer == '1':
            user_answer = input('修改为: ')
            city_code[user_ans] = user_answer
        elif user_answer == '2':
            add_city = '#'+input('增加行政区：')
            add_code = '#'+input('行政区号码：')

            if check_bracket(city_list[user_ans]):
                city_list.insert(user_ans+1, add_city)
                city_code.insert(user_ans+1, add_code)
            else:
                city_list[user_ans] = '>'+city_list[user_ans]
                city_list.insert(user_ans+1, add_city)
                city_code.insert(user_ans+1, add_code)
        else:
            print('已退出')

    os.remove('citydata.txt')

    write_num = 0
    with open('citydata.txt', 'w', encoding='utf-8') as file_object:
        while write_num <= len(city_list)-1:
            if write_num != 0:
                file_object.write('\n')
            file_object.write(city_list[write_num])
            file_object.write('\n')
            file_object.write(city_code[write_num])
            write_num += 1

if user_answer == 'd':
    #还没写完！
    #sys.exit()
    print_sen = ''
    write_num = 0
    for city_name in city_list:
        print_sen += str(write_num)
        print_sen += city_name
        write_num += 1
        if write_num < len(city_list):
            print_sen += '、'
        else:
            print_sen += '.'

    print('前面有[>]符号的为有行政区的城市，[#]为行政区')
    print('删除含[>]符号的城市时，其行政区也将一并删除')
    print('所有城市：' + print_sen)
    user_ans = input('输入要删除的城市"号码"(从0开始): ')
    user_ans = int(user_ans)

    if check_num_sign(city_list[user_ans]):
        if user_ans+1 < len(city_list):
            if check_num_sign(city_list[user_ans+1]):
                del city_list[user_ans]
                del city_code[user_ans]
            elif check_num_sign(city_list[user_ans-1]):
                del city_list[user_ans]
                del city_code[user_ans]
            else:
                city_list[user_ans-1] = delete_bracket(city_list[user_ans-1])
                del city_list[user_ans]
                del city_code[user_ans]
        else:
            if check_num_sign(city_list[user_ans-1]):
                del city_list[user_ans]
                del city_code[user_ans]
            else:
                city_list[user_ans-1] = delete_bracket(city_list[user_ans-1])
                del city_list[user_ans]
                del city_code[user_ans]
    elif check_bracket(city_list[user_ans]):
        del_number = user_ans

        del_all_u = input('确认删除'+city_list[user_ans]+'及其所有行政区？(y)')
        if del_all_u == 'y':
            check_box = True
        else:
            check_box = False
        del_times = 0
        while check_box:
            del_times += 1
            if del_times == 1:
                del city_list[user_ans]
                del city_code[user_ans]
            else:
                if check_num_sign(city_list[user_ans]):
                    del city_list[user_ans]
                    del city_code[user_ans]
                else:
                    check_box = False
    else:
        del city_list[user_ans]
        del city_code[user_ans]

    os.remove('citydata.txt')

    write_num = 0
    with open('citydata.txt', 'w', encoding='utf-8') as file_object:
        while write_num <= len(city_list)-1:
            if write_num != 0:
                file_object.write('\n')
            file_object.write(city_list[write_num])
            file_object.write('\n')
            file_object.write(city_code[write_num])
            write_num += 1

print('完成操作')