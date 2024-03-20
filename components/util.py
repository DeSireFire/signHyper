import http.cookies
import re


def convert_cookies_to_dict(cookies):
    """
    cookies转字典
    :param cookies: str
    :return:
    """
    print(f"cookies type:{type(cookies)}")
    if isinstance(cookies, dict):
        return cookies
    cookies = cookies.strip()
    try:
        ck = dict([l.strip().split("=", 1) for l in list(filter(None, cookies.split(";")))])
    except Exception as E:
        ck = {}
        print(f'cookie解析错误:{E}！ cookies明细:{cookies}')
    return ck


def parse_cookies(cookies_str):
    cookies = http.cookies.SimpleCookie()
    cookies.load(cookies_str)
    return {key: morsel.value for key, morsel in cookies.items()}

def check_jd_ck(cookies_dict:dict):
    temp = {}
    for k, v in cookies_dict.items():
        if str(k).startswith("pt_"):
            temp[k] = v

    if temp.get("pt_key") and temp.get("pt_pin"):
        return True
    else:
        return False

def parse_logs(json_data):
    """
    美团脚本日志切割
    :param json_data:
    :return:
    """
    def extract_account_logs(log_part):
        return log_part.strip()

    log_text = json_data

    # 分割日志并过滤有效日志段落
    logs = [extract_account_logs(part) for part in log_text.split('---------------- 账号[')[1:]]

    # 提取执行时间
    start_time_pattern = r'开始执行...\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})'
    start_time_match = re.search(start_time_pattern, log_text)
    start_time = start_time_match.group(1) if start_time_match else None

    return logs, start_time


def desensitize_phone_numbers(text):
    """
    手机号码脱敏
    :param text:
    :return:
    """
    # 正则表达式匹配手机号码，这里以11位手机号为例
    pattern = r'1[3-9]\d{9}'
    phone_numbers = re.findall(pattern, text)

    # 对找到的手机号码进行脱敏处理，只保留前三位和后四位，中间用*代替
    for number in phone_numbers:
        text = re.sub(re.escape(number), '***' + number[3:-4] + '***', text)

    return text