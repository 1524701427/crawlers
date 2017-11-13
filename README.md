# crawlers

![build](https://api.travis-ci.org/keepalive555/export.svg?branch=master)

## 爬虫集合

工程收集了笔者日常工作生活中，用到的一些爬虫案例，实现比较简单，并未用到一些复杂的爬虫技术。不积跬步无以至千里，希望自己可以完成量到质的成长。

### 环境配置

- 下载代码

`git clone`远程仓库中的代码至本地：

```bash
git clone git@github.com:keepalive555/crawlers.git
```

- 安装虚拟环境

```bash
cd crawlers/
virtualenv env && source env/bin/active
```

- 安装依赖库

```bash
pip install -r requirements.txt -i http://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com
```

***注意：*** `html`解析库`lxml`是由`c`语言编写的，用`pip`安装需要一些依赖库，如下：

- Debian/Ubuntu

```bash
sudo apt-get install libxml2-dev libxslt-dev python-dev
```

- CentOS

```bash
sudo yum install libxml2 libxmls-devel libxslt-devel python-devel
```

### 配置文件

根据模板生成配置文件：`cp config_sample.py config.py`

用编辑器打开`config.py`添加配置项。

```python
QQ_MAIL_ACCOUNT = ''  #  腾讯企业邮发件账户
QQ_MAIL_PASSWORD = ''  # 腾讯企业邮发件密码
RECEIPTS = ['demo@qq.com']  # 收件人列表

ITJUZI_USER = ''  # IT桔子用户名
ITJUZI_PASSWORD = '' # ITt桔子用户密码
```

### 运行爬虫

```bash
mkdir -p ~/log
cd cralwers && ../env/bin/python export.py  # 爬取影视剧信息
cd cralwers && ../env/bin/python itjuzi.py  # 爬去It桔子项目信息
```

在服务器上运行爬虫，使用`supervisor`或者`nohup`。
