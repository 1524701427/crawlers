# crawlers

![build](https://travis-ci.org/keepalive555/crawlers.svg?branch=master)

## 爬虫集合

工程收集了笔者日常工作生活中，用到的一些爬虫案例，技术实现比较简单，并未用到一些复杂的爬虫技术。不积跬步无以至千里，希望自己可以通过不断解决现实问题，积攒爬虫经验。
> 爬虫列表如下：
> 
- 花骨朵
- IT桔子
- 铅笔道

## 环境配置

`git clone`远程仓库至本地：

```bash
git clone git@github.com:keepalive555/crawlers.git
```
新建`Python`虚拟运行环境

```bash
cd crawlers/
virtualenv env && source env/bin/active
```

安装`Python`依赖库

```bash
pip install -r requirements.txt -i http://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com
```
> ***注意：*** 
> 
> 工程引用的`html`解析库`lxml`是由`c`语言编写的，用`pip`安装需要首先安装一些`Python`依赖库，如下：
> 
> - Debian/Ubuntu
> 
> ```bash
> sudo apt-get install libxml2-dev libxslt-dev python-dev
> ```
> - CentOS
> 
> ```bash
> sudo yum install libxml2 libxmls-devel libxslt-devel python-devel
> ```

## 配置爬虫

根据模板生成配置文件：`cp config_sample.py config.py`

用编辑器打开`config.py`，配置项如下所示：

```python
QQ_MAIL_ACCOUNT = ''  #  腾讯企业邮发件账户
QQ_MAIL_PASSWORD = ''  # 腾讯企业邮发件密码
RECEIPTS = ['demo@qq.com']  # 收件人列表

ITJUZI_USER = ''  # IT桔子用户名
ITJUZI_PASSWORD = '' # ITt桔子用户密码

QIANBIDAO_USER = ''  # 铅笔道登录用户
QIANDIDAO_PASSWORD = ''  # 铅笔道登录密码
```

### 运行爬虫

```bash
mkdir -p ~/log
cd cralwers && ../env/bin/python export.py  # 爬取花骨朵影视剧信息
cd cralwers && ../env/bin/python itjuzi.py  # 爬取IT桔子项目信息
cd cralwers && ../env/bin/python qianbidao.py  # 爬取铅笔道项目信息
```

在服务器上运行，可以考虑`supervisor`或者`nohup`后台运行。
