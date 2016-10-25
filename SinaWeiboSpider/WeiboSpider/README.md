# 新浪微博爬虫

### 简介说明

该程序用于爬取新浪微博的数据，主要用于学术研究。具体数据包括：

-   发布微博的作者的个人信息，包括用户ID，昵称，性别，地区；
-   作者的所有关注的人；
-   作者的所有粉丝；
-   作者发布的所有微博的微博ID，发布时间；
-   每条微博的文字；
-   每条微博的所有图片；
-   每条微博的所有评论者的昵称，评论的文字，以及评论的时间；
-   每条微博的所有转发者的昵称，以及转发的时间；
-   每条微博的所有点赞者的昵称，以及点赞的时间。

另外，该爬虫还支持以下功能：

-   支持多账号爬虫。理论上，账号越多，被 ban 的几率越小；
-   支持多 user-agent 轮流使用，目的在于减小被 ban 的几率；
-   用数据库存储，爬取结束后再从数据库导出，这样方便且高效；
-   爬取结束时会自动发送邮件进行通知；


### 依赖环境

Python3.5下用到 scrapy、requests、rsa、PostgreSQL。
```python
pip install requests
pip install rsa
pip install scrapy
pip install -U psycopg2
```


###  代码运行

进入项目根目录，执行如下命令即可：
`scrapy crawl weibo`



### 相关配置

- 配置PostgreSQL并建立数据库  
打开 `PostgreSql\data\pg_hba.conf`，添加更改用户权限。  
```sql
# IPv4 local connections:
#host    all             all             127.0.0.1/32            md5
host    all             all              0.0.0.0/0            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
```

- 项目程序的配置  
在`settings.py` 中更改其相应的内容即可。

```python
# Your whole weibo username and password pairs.
WEIBO_LOGIN_INFO_LIST = [('your username_1', 'your password_1'), ('your username_2', 'your password_2'), ...]

# Each name of tables can be defined here (each value of items). These keys are not changeable.
TABLE_NAME_DICT = {
    'user_info': 'user_info_table_name',
    'follow': 'follow_table_name',
    'fan': 'fan_table_name',
    'post_info': 'post_info_table_name',
    'text': 'text_table_name',
    'image': 'image_table_name',
    'comment': 'comment_table_name',
    'forward': 'forward_table_name',
    'thumbup': 'thumbup_table_name'
}

# Your postgresql username.
POSTGRESQL_USERNAME = 'your postgresql username'
# Your postgresql password.
POSTGRESQL_PASSWORD = 'your postgresql password'
# Your postgresql databaes.
POSTGRESQL_DATABASE = 'your postgresql database name'

# The IDs of users you want to crawl.
CRAWLED_WEIBO_ID_LIST = ['123456789', '246812345', ...]
# Email notification.
MAIL_ENABLED = False
MAIL_FROM = 'your email'
MAIL_HOST = 'your email smtp server host'
# Your email smtp server port
MAIL_PORT = 587
MAIL_USER = 'your email'
MAIL_PASS = 'your email password'
# YOur email smtp server port type
MAIL_TLS = True
MAIL_SSL = False
TO_ADDR = 'send to where'        

```

### 数据导出

在指定的数据库中对每个表执行如下命令：
`\copy table_name TO $ABSOLUTE_PATH`  
其中，**$ABSOLUTE_PATH** 为每个表对应输出文件的绝对路径。

### TODO
添加查看爬虫信息的图形化界面
