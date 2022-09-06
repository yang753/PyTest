# -*- coding:utf-8 -*-
import re
def everMatch(regex: str, input: str):
    ##因为以下这个bug所以要先给括号内文字|拆分由多到少排序
    ##regex = "(垃圾|厨余垃圾|食物垃圾)(处理|研磨|清理)(关闭|终止|结束|关停|关一下|停用|禁用|不启用|停止|不要开|中止|停|不要|关门|不要用|停下|停掉|关电|中断|退出|闭了|别开开|关机|闭上|关|关小|取消|别打开|关了|别启用|关掉|别要|关上|别开|不运行|取消掉)"
    ##regex = "(垃圾|厨余垃圾|食物垃圾)(处理|研磨|清理)(停|停下|停掉)"
    ##结果为垃圾处理停
    regexCC=r'([\u4e00-\u9fa5a-zA-Z|0-9]*)'
    patternCC = re.compile(regexCC)
    resultCC = patternCC.findall(regex)
    for x in resultCC:
        if x !="":
            sp=x.split("|")
            sp=sorted(sp,key=len)
            sp.reverse()
            s1 = '|'.join(str(n) for n in sp)
            regex=regex.replace(x,s1)

    regex1 = '(' + regex + ')'
    pattern = re.compile(regex1)
    result = pattern.findall(input)
    match = ""
    for x in result:
        for y in x:
            if re.match(regex1, y):
                return y
    if match == "" and input.__contains__(regex):
        return regex
    return ""

strs = "垃圾处理停下"
regex = "(垃圾|厨余垃圾|食物垃圾)(处理|研磨|清理)(关闭|终止|结束|关停|关一下|停用|禁用|不启用|停止|不要开|中止|停|不要|关门|不要用|停下|停掉|关电|中断|退出|闭了|别开开|关机|闭上|关|关小|取消|别打开|关了|别启用|关掉|别要|关上|别开|不运行|取消掉)"
regex = "(垃圾|厨余垃圾|食物垃圾)(处理|研磨|清理)(停|停下|停掉)"
print(everMatch(regex, strs))