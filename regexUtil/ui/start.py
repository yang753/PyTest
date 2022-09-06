import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QInputDialog
import threading
import re
import shutil

from regexUtil.ui.regex import Ui_RegexUtil
from regexUtil.ui.sceneSelect import Ui_sceneDialog

scene = "common"
mainWindos = None
sceneSelectDialog = None
sceneOperate = "select"


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


def match(regexin: str, input: str):
    regexList = regexin.split("\n")
    match = ""
    for regex in regexList:
        a = everMatch(regex, input)
        if (len(a) > len(match)):
            match = a
    return match


def test(regex: str, input: str):
    matchStr = match(regex, input)
    response = input
    if matchStr != "":
        if matchStr == input:
            response = input.replace(matchStr, '<span style="background:#00FF00">' + matchStr + '</span>', 1)
        else:
            response = input.replace(matchStr, '<span style="background:yellow">' + matchStr + '</span>', 1)

    return response


def replace(input: str):
    return input.replace("\t", "").replace("\f", "").replace('<span style="background:#00FF00">', "").replace("</span>",
                                                                                                              "")


def replaceDic(input: str, dic: str):
    if dic == "":
        return input
    dic = dic.split("\n")
    try:
        for x in dic:
            if x.startswith("#") or x.replace(" ", "") == "":
                continue
            a = replace(x).split("---")
            input = input.replace(a[0], a[1])
    except Exception as e:
        print(e)
    ##看下有没有词典没有配置
    dicReg = "({<\\w+>})"
    p = re.compile(dicReg)
    s = p.findall(input)
    if len(s) > 0:
        error = set()
        for a in s:
            error.add(a)
        raise Exception(str(error) + "没有配置字典")
    return input


class RegexUtil(QMainWindow):
    def setUi(self, ui: Ui_RegexUtil):
        self.ui = ui

    def loadResource(self):
        global sceneDialog
        sceneDialog.clearScene()
        list = os.listdir("../resource/")
        for x in list:
            xPath = "../resource/" + x
            if os.path.isdir(xPath):
                sceneDialog.addScene(x)
        sceneDialog.show()

    def selectScene(self):
        global sceneOperate
        sceneOperate = "select"
        self.loadResource()

    def deleteScene(self):
        global sceneOperate
        sceneOperate = "delete"
        self.loadResource()

    def createScene(self):
        global sceneOperate
        sceneOperate = "create"
        self.loadResource()

    def saveScene(self):
        self.saveInput()

    def regexTest(self):
        out = ""
        try:
            regex = replace(self.ui.regular_input.toPlainText())
            dict = self.ui.dic_input.toPlainText()
            regex = replaceDic(regex, dict)
            inputStr = self.ui.str_input.toPlainText()
            if regex == "" or inputStr == "":
                return
            inputList = inputStr.split("\n")
            self.ui.result_output.clear()

            for input in inputList:
                input = replace(input)
                if not input == "":
                    out = out + test(regex, input) + "<br/>"
        except Exception as e:
            out = e
        self.ui.result_output.setText(str(out))

    def saveInput(self):
        global scene
        f = open("../resource/" + scene + "/regular.txt", mode='w', encoding='utf-8')
        f.write(self.ui.regular_input.toPlainText())
        f.close()
        f = open("../resource/" + scene + "/input.txt", mode='w', encoding='utf-8')
        f.write(self.ui.str_input.toPlainText())
        f.close()
        f = open("../resource/" + scene + "/dic.txt", mode='w', encoding='utf-8')
        f.write(self.ui.dic_input.toPlainText())
        f.close()

    def loadConfig(self):
        global scene
        self.ui.userScene.setText(scene)
        print(scene)
        f = open("../resource/" + scene + "/dic.txt", mode='r', encoding='utf-8')
        text = f.read()
        self.ui.dic_input.setText(text)
        f.close()
        f = open("../resource/" + scene + "/regular.txt", mode='r', encoding='utf-8')
        text = f.read()
        self.ui.regular_input.setText(text)
        f.close()
        f = open("../resource/" + scene + "/input.txt", mode='r', encoding='utf-8')
        text = f.read()
        self.ui.str_input.setText(text)
        f.close()

    def closeEvent(self, event):
        self.saveInput()

    def showEvent(self, event):
        self.loadConfig()


class sceneDialog(QDialog):

    def setUi(self, ui: Ui_sceneDialog):
        self.ui = ui

    def addScene(self, scene):
        try:
            self.ui.scene_list.addItem(scene)
        except Exception as e:
            print(e)

    def selectScene(self, select):
        global sceneOperate
        global scene
        self.close()
        if sceneOperate == "select":
            scene = select
            mainWindos.loadConfig()
        elif sceneOperate == "create":
            name,b = QInputDialog.getText(self, "创建", "请输入场景名称")
            list = os.listdir("../resource/")
            sceneNameList=[]
            for x in list:
                xPath = "../resource/" + x
                if os.path.isdir(xPath):
                    sceneNameList.append(x)
            if name in sceneNameList:
                a = QMessageBox.question(self, '提示', name+'已存在', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            else:
                fromPath="../resource/" + select
                toPath="../resource/" + name
                shutil.copytree(fromPath,toPath)
        elif sceneOperate == "delete":
            inUse = mainWindos.ui.userScene.text()
            if select == inUse:
                a = QMessageBox.question(self, '提示', '正在使用，无法删除', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                print("正在使用，无法删除")
            elif select == "common":
                a = QMessageBox.question(self, '提示', 'common 无法删除', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                print("common 无法删除")
            else:
                a = QMessageBox.question(self, '提示', '确认删除' + select + "吗", QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
                if a == QMessageBox.Yes:
                    shutil.rmtree("../resource/" + select)

    def clearScene(self):
        self.ui.scene_list.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = RegexUtil()
    ui = Ui_RegexUtil()  # Ui_MainWindow 即我们用Qt designer设计生成转化出来的类
    myWin.setUi(ui)
    ui.setupUi(myWin)

    sceneSelectDialog = sceneDialog()
    sceneSelect_ui = Ui_sceneDialog()
    sceneSelect_ui.setupUi(sceneSelectDialog)
    sceneSelectDialog.setUi(sceneSelect_ui)

    mainWindos = myWin
    sceneDialog = sceneSelectDialog
    myWin.show()
    sys.exit(app.exec_())
