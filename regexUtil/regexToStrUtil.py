# -*- coding:utf-8 -*-
import re


def regexToStr(regex: str):
    regex = regex.replace("/", "|")
    print(regex)
    pattern = re.compile(regex)
    rr=r"[(][\u4E00-\u9FA5A-Za-z0-9|]+[)]"
    pattern = re.compile(rr)
    result=pattern.findall(regex)
    list=[]
    for x in result:
        print(x)
        list.append(x)

    concat("",list)


def concat(ss,li:list):
    if len(li)>=0:
        a=li[0][1:-1].split("|")
        b=[]
        if len(li)>1:
            b=li[1:]
            print(b)
        for x in a:
            if len(b)==0:
                print(ss+x)
            else:
                concat(ss+x,b)


if __name__ == '__main__':
    regex = r"(控湿/控制湿度/操控湿度/湿度操控/湿度控制/管理湿度/湿度管理)(打开/开始/启动/开启/开动/进入/开头/启头/从头/开/启/来点/需要/启用/开下/开了/开/吹/开上/开成/开到/开开/设置/调成/调到/转到/调至/变为/换到/换成/切换为/变为/转为/调为/弄成/改到/改成/转换为/设为/设成/工作/弄成/来点/我需要/需要/运转/运行/开起来/走起来/动起来/吹起来/跑起来/开着/打着/来/换点/换/设置为/来一波/给点/给/供/工作/唤起/唤醒/我要/要)"
    regexToStr(regex)
