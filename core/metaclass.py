# -*- coding: utf-8 -*-

""" 常用的元类。"""


class Final(type):
    """封闭类的Python实现。

        遍历要构造类的基类，判断其中是否有类为封闭类（Final的实例对象）。

    Args:
        cls (str): 要构造类的类名。
        bases (tuple): 继承基类的元组。
        namespace (dict): 要构造类的属性kv字典。

    Returns:
        class : 返回一个不可继承的封闭类。

    Raises:
        TypeError : 继承一个不可继承的类。
    """

    def __init__(self, cls, bases, namespace):
        for base in bases:
            if isinstance(base, Final):
                raise TypeError("final class %s." % base.__name__)
