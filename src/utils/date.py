from datetime import datetime

def parse_time_string(time_str):
    # 使用datetime.strptime解析输入的时间字符串
    dt = datetime.strptime(time_str, "%a, %d %b %Y %H:%M:%S %z")
    # 将datetime对象格式化为所需的格式
    return dt.strftime("%Y-%m-%d %H:%M:%S")