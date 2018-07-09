#!/usr/bin/python
# coding:utf-8


import operator

a = [1, 2, 3]

# b = operator.itemgetter(1)  # 定义函数b，获取对象的第1个域的值
print a[-1]
for i in range(len(a) - 1):
    print i
    print a[i]

# b = operator.itemgetter(1, 0)  # 定义函数b，获取对象的第1个域和第0个的值
# print b(a)
