# GISM
GISM is the abbreviation of general industrial smart monitoring.
It is designed to complete the task of intelligent detection with YOLO V4.

## Installation

* build docker image

```bash
docker build -t gism:vx.x .
```

* load the docker image

```bash
sh install_gism.sh
```

* run application

```bash
sh run_gism.sh
```

## Code Specification

**file header**

* for python

```python
#!/usr/bin/python3
# -*- coding: UTF-8 -*-
```

**import**

> 单行import 不超过4个&80个字符

**code annotation**

> 使用英语注释

* 单行注释

```python
# 这是单行注释
```

* 单行块注释

```python
"""这是单行块注释"""
```

* 这是多行块注释

```python
"""
这是多行块注释
"""
```

**function**

> 名字小写，单词之间用下划线连接

```python
def load_config():
    pass
```

> 方法注释要详细

```python
def output(label):
    """
    方法功能注释
    :param label: 形式参数
    :return:      返回值
    """
```

> 槽函数的命名用驼峰法

```python
def handleStatus(self, text, value):
    """
    Slot function of the progress bar and the status label state change.
    :param text: The text to be displayed on the status label.
    :param value: The value to be displayed on the process bar.
    :return: None
    """
    self.progressBarStatusLabel.setText(text)
    self.progressBar.setValue(value)
```


## Some References

**TensorRT**

Address£ºhttps://github.com/jkjung-avt/tensorrt_demos

**Docker**

Address£ºhttps://docs.docker.com

**PyQt5**

Adress: https://github.com/PyQt5/PyQt


output方法统一（3哥维度）