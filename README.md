DBank Downloader
================

This script will get the DBank's real URL and call wget to download.

Get
---

###You need [python](http://www.python.org) to run this script.

```bash
wget https://raw.github.com/billzhong/dbank/master/dbank.py
```

Usage
-----
```
dbank.py [-h] [--resume] url
```

For example, the url is `http://dl.vmall.com/c0o1b6khfw`:

```bash
python dbank.py http://dl.vmall.com/c0o1b6khfw
```

### --resume

Resume getting a partially-downloaded file.

For example:

```bash
python dbank.py http://dl.vmall.com/ --resume
```

Note
----
Only test in python 2.7.x.

DBank has two type crypts, only test the 'ed' one.



中文
====

本脚本用来获取 DBank 网盘的真实下载地址，并调用 wget 来下载。

获取
----
需要 [Python](http://www.python.org) 环境。

```bash
wget https://raw.github.com/billzhong/dbank/master/dbank.py
```

用法
----

```
dbank.py [-h] [--resume] url
```

例如，需要下载的地址是 `http://dl.vmall.com/c0o1b6khfw` ：

```bash
python dbank.py http://dl.vmall.com/c0o1b6khfw
```

### --resume

继续下载之前未下载完的文件。

例如：

```bash
python dbank.py http://dl.vmall.com/c0o1b6khfw --resume
```

备注
----
仅在 python 2.7.x 试过。

DBank 有两种加密方式，只测试过 'ed' 方式。


