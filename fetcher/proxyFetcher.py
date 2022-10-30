# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

from json import loads
from re import findall
from time import sleep

from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        站大爷 https://www.zdaye.com/dayProxy.html
        """
        start_url = "https://www.zdaye.com/dayProxy.html"
        html_tree = WebRequest().get(start_url, verify=False).tree
        urls = html_tree.xpath("//h3[@class='thread_title']/a/@href")
        for i in range(0, 10):
            target_url = "https://www.zdaye.com/" + urls[i].strip()
            while target_url:
                _tree = WebRequest().get(target_url, verify=False).tree
                for tr in _tree.xpath("//table//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    yield "%s:%s" % (ip, port)
                next_page = _tree.xpath("//div[@class='page']/a[@title='下一页']/@href")
                target_url = "https://www.zdaye.com/" + next_page[0].strip() if next_page else False
                sleep(5)

    @staticmethod
    def freeProxy02(page_count=10):
        """
        代理66 http://www.66ip.cn/
        """

        urls = ['http://www.66ip.cn/%s.html' % n for n in range(1, page_count + 1)] + [
            'http://www.66ip.cn/areaindex_%s/%s.html' % (i, j) for i in range(1, 35) for j in range(1, 3)]
        req = WebRequest()
        for url in urls:
            resp = req.get(url, timeout=10).tree
            for i, tr in enumerate(resp.xpath("(//table)[3]//tr")):
                if i > 0:
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy03(page_count=10):
        """ 开心代理 """
        urls = ['http://www.kxdaili.com/dailiip/%s/%s.html#ip' % (i, j) for i in range(1, 3) for j in
                range(1, page_count + 1)]
        req = WebRequest()
        for url in urls:
            tree = req.get(url).tree
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                yield "%s:%s" % (ip, port)
            sleep(4)

    @staticmethod
    def freeProxy04(page_count=8):
        """ FreeProxyList https://www.freeproxylists.net/zh/ """
        urls = ['https://www.freeproxylists.net/zh/?page=%s' % i for i in range(1, page_count + 1)]
        req = WebRequest()
        for url in urls:
            tree = req.get(url, verify=False).tree
            for tr in tree.xpath("//tr[@class='Odd']") + tree.xpath("//tr[@class='Even']"):
                ip = "".join(tr.xpath('./td[1]/a/text()').strip())
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                if ip:
                    yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy05(page_count=10):
        """ 快代理 https://www.kuaidaili.com """
        urls = ['https://www.kuaidaili.com/free/inha/%s/' % i for i in range(1, page_count + 1)] + [
            'https://www.kuaidaili.com/free/intr/%s/' % i for i in range(1, page_count + 1)]
        req = WebRequest()
        for url in urls:
            tree = req.get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])
            sleep(1)  # 必须sleep 不然第二条请求不到数据

    @staticmethod
    def freeProxy06():
        """ FateZero http://proxylist.fatezero.org/ """
        url = "http://proxylist.fatezero.org/proxy.list"
        try:
            resp_text = WebRequest().get(url).text
            for each in resp_text.splitlines():
                json_info = loads(each)
                yield "%s:%s" % (json_info.get("host", ""), json_info.get("port", ""))
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy07():
        """ 云代理 """
        urls = ['http://www.ip3366.net/free/?stype=1&page=%s' % i for i in range(1, 8)] + [
            'http://www.ip3366.net/free/?stype=2&page=%s' % i for i in range(1, 4)]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy08():
        """ 小幻代理 """
        urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = findall(r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy09(page_count=1):
        """ 免费代理库 """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html_tree = WebRequest().get(url).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    @staticmethod
    def freeProxy10(page_count=23):
        """ 89免费代理 """
        urls = ['https://www.89ip.cn/index_%s.html' % i for i in range(1, page_count + 1)]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def wallProxy01():
        """
        PzzQz https://pzzqz.com/
        """
        from requests import Session
        from lxml import etree
        session = Session()
        try:
            index_resp = session.get("https://pzzqz.com/", timeout=20, verify=False).text
            x_csrf_token = findall('X-CSRFToken": "(.*?)"', index_resp)
            if x_csrf_token:
                data = {"http": "on", "ping": "3000", "country": "cn", "ports": ""}
                proxy_resp = session.post("https://pzzqz.com/", verify=False, headers={"X-CSRFToken": x_csrf_token[0]},
                                          json=data).json()
                tree = etree.HTML(proxy_resp["proxy_html"])
                for tr in tree.xpath("//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()"))
                    port = "".join(tr.xpath("./td[2]/text()"))
                    yield "%s:%s" % (ip, port)
        except Exception as e:
            print(e)

    @staticmethod
    def wallProxy02():
        """
        墙外网站 cn-proxy
        :return:
        """
        urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxy11(page_count=10):
        """
        https://proxy-list.org/english/index.php
        :return:
        """
        urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, page_count + 1)]
        request = WebRequest()
        import base64
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = findall(r"Proxy\('(.*?)'\)", r.text)
            for proxy in proxies:
                yield base64.b64decode(proxy).decode()

    @staticmethod
    def freeProxy12(page_count=6):
        urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-%s' % n for n in range(1, page_count + 1)] + [
            'https://list.proxylistplus.com/google-List-%s' % n for n in range(1, 3)]
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def wallProxy03(page_count=15):
        """ mrhinkydink.com """
        urls = ['http://www.mrhinkydink.com/proxies.htm'] + ['http://www.mrhinkydink.com/proxies%s.htm' % n for n in
                                                             range(1, page_count + 1)]
        request = WebRequest()
        for url in urls:
            tree = request.get(url, timeout=10).tree
            for td in tree.xpath("//table//tr[@class='text']"):
                ip = "".join(td.xpath('./td[1]/text()'))
                port = "".join(td.xpath('./td[2]/text()'))
                if ip:
                    yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy13(page_count=10):
        """ www.cnproxy.com """

        def find_decode_maps(rules):
            decode_map = {}
            for pin in rules:
                decode_map[pin[0]] = pin[1]
            return decode_map

        def decode_port(decode_map, input_string):
            return ''.join(decode_map[i] for i in findall(r'\w', input_string))

        urls = ['https://www.cnproxy.com/proxy%s.html' % n for n in range(1, page_count + 1)] + [
            'https://www.cnproxy.com/proxyedu%s.html' % i for i in range(1, 3)],
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            maps = find_decode_maps(findall(r'(\w)\=\"(\d)\";', r.text))
            proxies = findall(r'<tr><td>(\d+\.\d+\.\d+\.\d+)<SCRIPT type=text/javascript>document.write'
                              r'\(\"\:\"(.+)\)</SCRIPT></td><td>(HTTP|SOCKS4)\s*', r.text)
            for proxy in proxies:
                yield "%s:%s" % (proxy[0], decode_port(maps, proxy[1]))

    @staticmethod
    def freeProxy14():
        urls = ['https://proxypool.scrape.center/all', 'http://ab57.ru/downloads/proxyold.txt',
                'proxylists.net/http_highanon.txt', 'https://rmccurdy.com/.scripts/proxy/good.txt']
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            for proxy in r.text.splitlines():
                yield proxy

    @staticmethod
    def wallProxy04(page_count=10):
        """ mrhinkydink.com """

        def find_decode_maps(rules):
            decode_map = {}
            for pin in rules:
                decode_map[pin[0]] = pin[1]
            return decode_map

        def decode_port(decode_map, input_string):
            return ''.join(decode_map[i] for i in findall(r'\w', input_string))

        urls = ['http://nntime.com/proxy-list-%02d.htm' % n for n in range(1, page_count + 1)]
        request = WebRequest()
        for url in urls:
            res = request.get(url, timeout=10)
            maps = find_decode_maps(findall(r'(\w)\=(\d)', res.text))
            proxies = findall(r'<td>(\d+\.\d+\.\d+\.\d+).*\(\"\:\"(.+)\)', res.text)
            for proxy in proxies:
                yield "%s:%s" % (proxy[0], decode_port(maps, proxy[1]))

    @staticmethod
    def freeProxy15():
        urls = ['https://www.my-proxy.com/free-%s.html' % n for n in
                ['elite-proxy', 'anonymous-proxy', 'transparent-proxy', 'socks-4-proxy', 'socks-5-proxy',
                 'proxy-list'] + ['proxy-list-%s' % m for m in range(2, 11)]]
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = findall(r'(\d+\.\d+\.\d+\.\d+\:\d+)', r.text)
            for proxy in proxies:
                yield proxy

    @staticmethod
    def freeProxy16():
        urls = ['https://www.us-proxy.org', 'https://free-proxy-list.net', 'https://www.socks-proxy.net',
                'https://www.sslproxies.org']
        request = WebRequest()
        for url in urls:
            tree = request.get(url, timeout=10).tree
            for tr in tree.xpath("//section[@id='list']//tbody/tr"):
                ip = "".join(tr.xpath('./td[1]/text()'))
                port = "".join(tr.xpath('./td[2]/text()'))
                if ip:
                    yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy17():
        urls = ['https://atomintersoft.com/%s_proxy_list' % n for n in
                ['transparent', 'anonymous', 'high_anonymity_elite']]
        request = WebRequest()
        for url in urls:
            tree = request.get(url, timeout=10).tree
            for proxy in tree.xpath("//table/thead/tr//td[1]/text()[1]"):
                if proxy:
                    yield proxy

    @staticmethod
    def freeProxy18():
        urls = ['http://proxydb.net/?protocol=http']  # todo: 翻页需要offset Post 请求
        for url in urls:
            tree = WebRequest().get(url, timeout=10, verify=False).tree
            for proxy in tree.xpath('//tbody/tr/td[1]/a/text()'):
                yield proxy

    @staticmethod
    def freeProxy19():
        url = 'https://cool-proxy.net/proxies.json'
        req_text = WebRequest().get(url, timeout=10).text
        for proxy in loads(req_text):
            ip = proxy['ip']
            port = proxy['port']
            if ip:
                yield "%s:%s" % (ip, port)

    @staticmethod
    def wallProxy05(page_count=135):
        """ http://free-proxy.cz/ """
        from base64 import b64decode
        urls = ['http://free-proxy.cz/en/proxylist/main/%s' % n for n in range(1, page_count + 1)]
        request = WebRequest()
        for url in urls:
            res = request.get(url, timeout=10)
            tree = res.tree
            for tr in tree.xpath(
                    "//table[@id='proxy_list']/tbody/tr"):  # //table[@id='proxy_list']/tbody/tr/td[@class='left']
                ip = tr.xpath("./td[@class='left']//text()")
                if ip:
                    ip = b64decode(findall(r'\"(.*)\"', ip[0])[0]).decode('utf-8')
                    port = tr.xpath('./td[2]//text()')[0]
                    yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy20():
        page = 1
        while True:
            url = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page={}'.format(page)
            req_json = loads(WebRequest().get(url, timeout=10).text)
            for proxy in req_json['data']:
                ip = proxy['ip']
                port = proxy['port']
                if ip:
                    yield "%s:%s" % (ip, port)
            count = page * 500
            if count > req_json['total']:
                break
            page += 1

    @staticmethod
    def freeProxy21():
        url = 'https://proxyhub.me/'

        for i in range(1, 101):
            req_tree = WebRequest().get(url, header={'cookies': 'page=%d;' % i}).tree
            for proxy in req_tree.xpath('//table/tbody/tr'):
                ip = "".join(proxy.xpath("./td[1]/text()")).strip()
                port = "".join(proxy.xpath("./td[2]/text()")).strip()
                if ip:
                    yield "%s:%s" % (ip, port)


if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy21():
        print(_)

# https://www.cnblogs.com/bonelee/p/9250281.html
