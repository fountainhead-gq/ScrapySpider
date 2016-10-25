# -*- coding: utf-8 -*-

import re
import zlib
import json
import operator
import functools
import html.parser
import urllib.parse
import chardet.universaldetector
import time
import random
import urllib.parse
import urllib.request
import http.cookiejar
from SinaWeiboSpider.WeiboLogin import WeiboConfig


def make_cookie(name, value, domain, port=None, path=None, expires=None):
    """
    make cookie based on "name", "value" and "domain", etc. domain like ".baidu.com" or "baidu.com"
    :key: cookiejar.set_cookie(cookie)
    """
    # check parameters
    assert (not domain.startswith("http")) and (not domain.startswith("www.")), "make_cookie: domain is invalid"

    # change parameters
    path = "/" if not path else path
    expires = (time.time() + 3600 * 24 * 30) if not expires else expires

    # make cookie
    cookie = http.cookiejar.Cookie(
        version=0, name=name, value=value, port=port, port_specified=False,
        domain=domain, domain_specified=False, domain_initial_dot=False, path=path, path_specified=True,
        secure=False, expires=expires, discard=True, comment=None, comment_url=None, rest=None
    )
    return cookie


def make_cookies_maps(cookies_maps):
    """
    make cookies list from a map_list, cookies_maps: [{"name": xxx, "value": xxx, "domain": xxx, ...}, ...]
    :key: for cookie in cookies_list: cookiejar.set_cookie(cookie)
    """
    cookies_list = [
        make_cookie(item["name"], item["value"], item["domain"], port=item.get("port"), path=item.get("path"), expires=item.get("expires"))
        for item in cookies_maps if ("name" in item) and ("value" in item) and ("domain" in item)
    ]
    return cookies_list


def make_cookies_string(cookies_string, domain):
    """
    make cookies list from a string, cookies_string: "name1=value1; name2=value2", this string also can be one part of headers
    :key: for cookie in cookies_list: cookiejar.set_cookie(cookie)
    """
    frags = [item.strip() for item in cookies_string.strip("; ").split(";") if item.strip()]
    cookies_list = [make_cookie(k.strip(), v.strip(), domain) for k, v in [item.split("=") for item in frags] if k.strip()]
    return cookies_list


def make_cookiejar_opener(is_cookie=True, proxies=None):
    """
    make cookiejar and opener for requesting, proxies: None or {"http": "http://proxy.example.com:8080/"}
    :key: opener.addheaders = make_headers(...).items()
    """
    assert is_cookie or proxies, "make_cookiejar_opener: one of parameters(is_cookie, proxies) must be True"
    cookie_jar, opener = None, None
    if is_cookie:
        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar=cookie_jar))
    if proxies:
        if opener:
            opener.add_handler(urllib.request.ProxyHandler(proxies=proxies))
        else:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies=proxies))
    return cookie_jar, opener


def make_headers(user_agent="pc", **kwargs):
    """
    make dictionary headers for requesting, user_agent: "pc", "phone", "all" or a ua_string
    :key: headers["Cookie"] = cookies_string
    """
    kwargs["user_agent"] = random.choice(WeiboConfig.CONFIG_USERAGENT_ALL) if user_agent == "all" else (
        random.choice(WeiboConfig.CONFIG_USERAGENT_PC) if user_agent == "pc" else (
            random.choice(WeiboConfig.CONFIG_USERAGENT_PHONE) if user_agent == "phone" else user_agent
        )
    )
    return {WeiboConfig.CONFIG_HEADERS_MAP[key]: kwargs[key] for key in kwargs if key in WeiboConfig.CONFIG_HEADERS_MAP}


def make_post_data(post_dict, boundary=None):
    """
    make post_data based on post_dict, post_dict: {name: value, ...}
    :key: "Content-Type" in headers is "multipart/form-data; boundary=----WebKitFormBoundaryzUJDUghs3ChlA3U1"
    :param post_dict: if include file, name must start with "_file_", and value=[file_bytes, file_name, con_name, con_type]
    """
    # make post_data without boundary and file
    if not boundary:
        return urllib.parse.urlencode(post_dict).encode()

    # make post_data with boundary and file
    post_data = []
    for name, value in post_dict.items():
        if name.startswith("_file_"):
            file_bytes, file_name, con_name, con_type = value
            post_data.append(("--%s" % boundary).encode())
            post_data.append(('Content-Disposition: form-data; name="%s"; filename="%s"' % (con_name, file_name)).encode())
            post_data.append(("Content-Type: %s\r\n" % con_type).encode())
            post_data.append(file_bytes)
        else:
            post_data.append(("--%s" % boundary).encode())
            post_data.append(('Content-Disposition: form-data; name="%s"\r\n' % name).encode())
            post_data.append(str(value).encode())
    post_data.append(("--%s--\r\n" % boundary).encode())
    return b'\r\n'.join(post_data)


def make_referer_url(url, path=False):
    """
    make referer url for requesting, params="", query="" and fragment=""
    :param path: whether referer_url include path
    """
    url_frags = urllib.parse.urlparse(url, allow_fragments=True)
    url_path = url_frags.path if path else "/"
    return urllib.parse.urlunparse((url_frags.scheme, url_frags.netloc, url_path, "", "", ""))

def get_html_content(response, charset=None):
    """
    get html content from a response, charset can be None, "utf-8", "gb2312" and "gbk", etc
    """
    # get info and content
    info = response.info()
    content = response.read()

    # decompress the content by info
    content_encoding = info.get("Content-Encoding", failobj="").lower()
    content = zlib.decompress(content, zlib.MAX_WBITS | 16) if (content_encoding.find("gzip") >= 0) else (
        zlib.decompress(content, zlib.MAX_WBITS) if (content_encoding.find("zlib") >= 0) else (
            zlib.decompress(content, -zlib.MAX_WBITS) if (content_encoding.find("deflate") >= 0) else content
        )
    )

    # find the charset by info
    content_charset = info.get_content_charset(failobj="").lower()
    if content_charset:
        charset = content_charset

    # find the charset by chardet
    if not charset:
        detector = chardet.universaldetector.UniversalDetector()
        for line in content.split(b"\n"):
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        charset = detector.result["encoding"]

    # decode the content
    return content.decode(charset, errors="ignore")


def get_json_data(string, pattern=None, annotation_pattern=None, begin_pattern=None):
    """
    get json data from a string, using pattern to extract
    :param annotation_pattern: define annotation regex pattern to remove annotation
    :param begin_pattern: define begin regex pattern string to add " to the key of json
    """
    # get string_re
    string_re = re.search(pattern if pattern else r"(?P<item>\{[\w\W]*?\})", string, flags=re.IGNORECASE)
    if not string_re:
        return None

    # get string_json
    string_json = string_re.group(1).strip()

    # remove annotation: r"(/\*[\w\W]*?\*/)|(//[\w\W]*?)\n"
    if annotation_pattern:
        string_json = re.sub(annotation_pattern, "\n", string_json, flags=re.IGNORECASE)
    string_json = html.parser.unescape(string_json.replace("'", '"'))

    # try and except the exception
    try:
        result = json.loads(string_json)
    except json.JSONDecodeError:
        # change key to "key"
        regex = r"%s(?P<key>\w+?)(?P<temp>\s*:)" % (begin_pattern if begin_pattern else r"[(^{),\s]")
        for key, temp in re.findall(regex, string_json, flags=re.IGNORECASE):
            string_json = string_json.replace(key+temp, '"%s":' % key.strip())
        result = json.loads(string_json)

    # return json object
    return result


def get_string_num(string, base=None):
    """
    get float number from a string, if base is not None, K means (base * B), M means (base * K), ...
    """
    temp = re.search(r"(?P<num>\d+(\.\d+)?)(?P<param>[\w\W]*?)$", string.upper().strip(), flags=re.IGNORECASE)
    if not temp:
        return 0.0
    num, param = float(temp.group("num")), temp.group("param")
    if param.find("亿") >= 0:
        num *= 100000000
    if param.find("万") >= 0:
        num *= 10000
    if param.find("千") >= 0:
        num *= 1000
    if param.find("百") >= 0:
        num *= 100
    if param.find("十") >= 0:
        num *= 10
    if (param.find("K") >= 0) and base:
        num *= base
    if (param.find("M") >= 0) and base:
        num *= (base * base)
    if (param.find("G") >= 0) and base:
        num *= (base * base * base)
    if (param.find("T") >= 0) and base:
        num *= (base * base * base * base)
    if param.find("%") >= 0:
        num /= 100
    return num


def get_string_split(string, split_chars=(" ", "\t", ","), is_remove_empty=False):
    """
    get string list by splitting string based on split_chars, len(split_chars) must >= 2
    """
    assert len(split_chars) >= 2, "get_string_split: len(split_chars) must >= 2"
    string_list = string.split(split_chars[0])
    for char in split_chars[1:]:
        string_list = functools.reduce(operator.add, [item.split(char) for item in string_list], [])
    return string_list if not is_remove_empty else [item.strip() for item in string_list if item.strip()]


def get_string_strip(string):
    """
    get string striped \t, \r, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", " ", string, flags=re.IGNORECASE).strip() if string else ""


def get_url_legal(url, base_url, encoding=None):
    """
    get legal url from a url, based on base_url, and url_frags.fragment=""
    """
    url_join = urllib.parse.urljoin(base_url, url, allow_fragments=True)
    url_legal = urllib.parse.quote(url_join, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding)
    url_frags = urllib.parse.urlparse(url_legal, allow_fragments=True)
    return urllib.parse.urlunparse((url_frags.scheme, url_frags.netloc, url_frags.path, url_frags.params, url_frags.query, ""))


def get_url_params(url, is_unique_value=True, keep_blank_value=False, encoding="utf-8"):
    """
    get main_part(a string) and query_part(a dictionary) from a url
    """
    url_frags = urllib.parse.urlparse(url, allow_fragments=True)
    querys = urllib.parse.parse_qs(url_frags.query, keep_blank_values=keep_blank_value, encoding=encoding)
    main_part = urllib.parse.urlunparse((url_frags.scheme, url_frags.netloc, url_frags.path, url_frags.params, "", ""))
    query_part = {key: querys[key][0] for key in querys} if is_unique_value else querys
    return main_part, query_part