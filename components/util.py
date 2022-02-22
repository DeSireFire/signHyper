
def convert_cookies_to_dict(cookies):
    """
    cookies转字典
    :param cookies: str
    :return:
    """
    ck = {}
    for k_v in cookies.split(':'):
        k, v = k_v.split('=', 1)
        ck[k.strip()] = v.replace('"', '')
    return ck