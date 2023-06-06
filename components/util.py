import http.cookies

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
