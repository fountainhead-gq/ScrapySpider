# LagouSpider
使用`scrapy`实现对拉勾网招聘信息的爬虫。



## 功能说明
通过`proxy`更新代理池并检测代理的可用性，将获取并保存到proxy.txt文件。


### 避免爬虫被ban的策略
- 调整设置`settings.py`的`DOWNLOAD_DELAY`
- 添加代理中间件`ProxyMiddleWare`
- 设置`Header`  
     ```
     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
     ```

### 数据存储
- 通过`pipelines.py`里的`LagouPipeline`插入到`MongoDB`数据库
