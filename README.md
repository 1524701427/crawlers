# export

## 爬去一些网站数据的爬虫集合

> **安装运行**

- 安装虚拟环境

```shell
virtualenv env && source env/bin/active
```

- 安装第三方库

```shell
pip install -r requirements.txt -i http://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com
```

- 配置文件config.py

```
QQ_MAIL_ACCOUNT = '' #  腾讯企业邮发件账户
QQ_MAIL_PASSWORD = '' # 腾讯企业邮发件密码
RECEIPTS = ['demo@qq.com'] # 收件人列表
```

- 运行脚本

```shell
python export.py
``` 
