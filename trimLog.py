import re
import os
import csv
import sys
from tkinter import messagebox
from tkinter import Tk
from tkinter import simpledialog

# 定义正则表达式模式
date_pattern = re.compile(r'\[(.*?)\]')
url_pattern = re.compile(r'url=(.*?),')
# 修改timecost_pattern以分别匹配数字和"ms"
timecost_pattern = re.compile(r'timecost=(.*?)\((ms)\)')
output = []

# 检查log目录是否存在
if not os.path.exists('log'):
    root = Tk()
    root.withdraw()  # 隐藏Tk窗口
    messagebox.showerror('错误', 'log目录不存在，请在当前目录创建log文件夹，并将日志放进文件夹中！')
    sys.exit(1)  # 停止程序

root = Tk()
root.withdraw()  # 隐藏Tk窗口
encoding_choice = simpledialog.askstring("输入编码", "请输入文件编码: utf-8 或 ISO-8859-1", initialvalue="ISO-8859-1")
if encoding_choice not in ['utf-8', 'ISO-8859-1']:
    messagebox.showerror('错误', '选择了无效的编码。请重新运行程序并选择utf-8或ISO-8859-1。')
    sys.exit(1)

# 遍历文件夹
# 遍历文件夹
for filename in os.listdir('log'):
    try:
        with open(os.path.join('log', filename), 'r', encoding=encoding_choice) as file:
            line_number = 0  # 初始化行号
            for line in file:
                line_number += 1  # 行号递增
                date_match = date_pattern.search(line)
                url_match = url_pattern.search(line)
                timecost_match = timecost_pattern.search(line)
                if date_match and url_match and timecost_match:
                    # 分别获取数字和"ms"
                    timecost_number, timecost_unit = timecost_match.groups()
                    # 添加文件名和行号
                    output.append((filename, str(line_number), f"'{date_match.group(1)}", url_match.group(1), timecost_number, timecost_unit))
    except UnicodeDecodeError as e:
        root = Tk()
        root.withdraw()  # 隐藏Tk窗口
        messagebox.showerror('编码错误', f'文件 {filename} 无法使用 {encoding_choice} 编码解析。错误详情：{e}')
        sys.exit(1)

# 将结果写入到一个新的CSV文件中
with open('各个接口耗时.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    # 写入标题，添加“文件名”和“行号”
    writer.writerow(['文件名', '行号', '时间', '接口', '耗时', '单位'])
    # 写入数据
    for row in output:
        writer.writerow(row)

# 程序完成后显示提示框
root = Tk()
root.withdraw()  # 隐藏Tk窗口
messagebox.showinfo('完成', '处理完毕，结果已写入到各个接口耗时.csv文件中。')
root.destroy()  # 关闭Tk窗口