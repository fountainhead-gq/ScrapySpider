import random
import os
import time
import logging


logger = logging.getLogger()


class ProxyMiddleWare(object):
    # request对象加上proxy
    def process_request(self,request, spider):
        proxy = self.get_random_proxy()
        request.meta['proxy'] = 'http://%s' % proxy
        logger.debug('-'*10)
        logger.debug(request.body)
        logger.debug(proxy)
        logger.debug('-' * 10)

    def process_response(self, request, response, spider):
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            logger.error('-' * 10)
            logger.error(response.url)
            logger.error(request.body)
            logger.error(request.meta['proxy'])
            logger.error('proxy block!')
            logger.error('-' * 10)
            proxy = self.get_random_proxy()
            request.meta['proxy'] = 'http://%s' % proxy  # 对当前request加上代理
            return request
        return response

    def get_random_proxy(self):   # 随机从文件中读取proxy
        while 1:
            proxy_dir=os.getcwd()
            proxy_dir= os.path.join(proxy_dir, r'Lagou/proxy.txt')
            with open(proxy_dir, 'r') as f:
                proxies = f.readlines()

            if proxies:
                break
            else:
                time.sleep(3)
        proxy = random.choice(proxies).strip()
        return proxy