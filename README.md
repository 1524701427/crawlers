# export

## 导出影视剧排行的爬虫

> **安装运行**

- 安装虚拟环境

```shell
virtualenv env && source env/bin/active
```

- 安装第三方库

```shell
pip install -r requirements.txt -i http://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com
```

- 运行脚本

```shell
python export.py
```