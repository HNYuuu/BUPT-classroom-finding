# -*- coding: utf-8 -*-

import tkinter as tk
import requests
from bs4 import BeautifulSoup
import re
# import sys

# reload(sys) 
# sys.setdefaultencoding('utf-8') 

cache = {}
result_cache = {}
temp = {}
flag = 0
time_map = {'8-10':0, '10-12':1, '13-15':2, '15-17':3, '17-18':4, '18-20':5}
building_map = {u'教一':1, u'教二':2, u'教三':3, u'教四':4}

p = re.compile(r'-(\d+),')

r = requests.get("http://jwxt.bupt.edu.cn/zxqDtKxJas.jsp")
# print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')
main_table = soup.find_all('table')[-1]
# print(type(main_table))

for i in range(6):
	cache[i] = main_table.find_all('tr')[i]
# print(cache)

for i in range(6):
	current_class_state = cache[i].find_all('td')[-1]
	# print(current_class_state)
	for string in current_class_state.stripped_strings:
		# print(string)
		if '教一楼' in string:
			flag = 1
			continue
		elif '教二楼' in string:
			flag = 2
			continue
		elif '教三楼' in string:
			flag = 3
			continue
		elif '教四楼' in string:
			flag = 4
			continue
		elif '图书馆' in string:
			continue
		else:
			temp[flag] = p.findall(string)
			# print(temp)
	# print(temp)
	cache[i] = temp.copy()
	temp.clear()
# print(cache)
# Spider end

root = tk.Tk()
root.title("今天哪有空")

root.geometry('500x250')

space = tk.Label(root, height=1)
space.pack()

var_start = tk.StringVar()
var_start.set('8-10')
start_option = tk.OptionMenu(root, var_start, '8-10', '10-12', '13-15', '15-17', '17-18', '18-20')
start_option.config(width=8)
start_option.pack()

var_end = tk.StringVar()
var_end.set('8-10')
end_option = tk.OptionMenu(root, var_end, '8-10', '10-12', '13-15', '15-17', '17-18', '18-20')
end_option.config(width=8)
end_option.pack()

var_building = tk.StringVar()
var_building.set('教一')
building_option = tk.OptionMenu(root, var_building, '教一', '教二', '教三', '教四')
building_option.config(width=8)
building_option.pack()

def give_me_data():
	start_text = time_map[var_start.get()]
	end_text = time_map[var_end.get()]
	building_text = building_map[var_building.get()]
	temp = []

	if start_text > end_text:
		var.set('您输入的有误，请重新输入')
		# TODO: handle some special case
		pass
	else:
		for i in range(start_text, end_text+1):
			if building_text not in cache[i].keys():
				continue
			else:
				temp.append(cache[i][building_text])
		# print(temp)
		if len(temp) != end_text-start_text+1:
			var.set('不好意思，没有符合要求的教室，别学习了')
			return
		result = list(set.intersection(*map(set, temp)))
		# print(result)
		result = list(result)
		print(result)
		if len(result) == 0:
			var.set('不好意思，没有符合要求的教室，别学习了')
		elif len(result) == 1:
			var.set('符合要求的空教室有： ' + result[0])
		else:
			result.sort()
			var.set('符合要求的空教室有：' + ' '.join(result))
		return

space2 = tk.Label(root, height=1)
space2.pack()

search = tk.Button(root, text='search', command=give_me_data).pack()

var = tk.StringVar()
show = tk.Label(root, textvariable=var, height=30, wraplength=450)
show.pack()

tk.mainloop()