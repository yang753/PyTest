import re


def match(regex: str, input: str):
    regex = '(' + regex + ')'
    pattern = re.compile(regex)
    result = pattern.findall(input)
    match = ""
    for x in result:
        for y in x:
            if re.match(regex, y):
                match = y
                return match
    return match

def test(regex: str, input: str):
    matchStr = match(regex, strs)
    if matchStr!="":
        print(strs.replace(matchStr, '<' + matchStr + '>'))
    else:
        print(input)


if __name__ == '__main__':
    # regex = '请?(帮|给|替)?我?(想|要|想要)?(把|给|将)?的?(海尔|智能)?(茶吧机|热饮机|饮水机)的?(取水|上水|出水|右取水|加热壶取水|加热壶上水)(功能|模式|开关)?(打开|开开|开启|启动|开始)'
    # regex = '开始'
    # strs = '开始'

    strs="垃圾处理停下"
    regex="'(垃圾|厨余垃圾|食物垃圾)(处理|研磨|清理)(关闭|终止|结束|关停|关一下|停用|禁用|不启用|停止|不要开|中止|停|不要|关门|不要用|停下|停掉|关电|中断|退出|闭了|别开开|关机|闭上|关|关小|取消|别打开|关了|别启用|关掉|别要|关上|别开|不运行|取消掉)'"
    test(regex, strs)
