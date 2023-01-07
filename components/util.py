
def convert_cookies_to_dict(cookies):
    """
    cookies转字典
    :param cookies: str
    :return:
    """
    if isinstance(cookies, str):
        cookies = cookies.strip()
        return cookies

    try:
        ck = dict([l.strip().split("=", 1) for l in list(filter(None, cookies.split(";")))])
    except Exception as E:
        ck = {}
        print(f'cookie解析错误:{E}！ cookies明细:{cookies}')
    return ck