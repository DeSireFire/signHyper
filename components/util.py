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