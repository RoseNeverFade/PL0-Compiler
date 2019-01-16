import config
from Lexer import lex
from program import prog
from interpret import interp
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from mwin import Ui_Dialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#操作码映射数组
mappf = ['', 'INT', 'CAL', 'LIT', 'LOD', 'STO', 'JMP', 'JPC', 'OPR', 'RED', 'WRT']

class MainUi(QtWidgets.QMainWindow, Ui_Dialog):
    state = 0
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.state = 0
        self.pctable.setColumnCount(3)
        self.pctable.setColumnWidth(0,60)
        self.pctable.setColumnWidth(1,60)
        self.pctable.setColumnWidth(2,60)
        self.pctable.setHorizontalHeaderItem(0,QTableWidgetItem('F'))
        self.pctable.setHorizontalHeaderItem(1,QTableWidgetItem('L'))
        self.pctable.setHorizontalHeaderItem(2,QTableWidgetItem('A'))
        return

    def br(self):   #浏览按钮
        fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "浏览", "./","PL0 Files (*.pl0);;TXT Files (*.txt)")
        with open(fileName, 'r') as infi :
            tmp = infi.read()
            #生成行号
            inps = '  1: '
            l = len(tmp)
            linenum = 1
            for i in range(l) :
                inps += tmp[i]
                if tmp[i] == '\n' :
                    linenum += 1
                    for j in range(3-len(str(linenum))) :
                        inps += ' '
                    inps += str(linenum)
                    inps += ': '

            self.pltxt.setPlainText(inps)
        self.state = 0
        config.set_allpcode([])
        config.set_output('')
        config.set_errorinfo([0])

        #消除行号
        tmp = self.pltxt.toPlainText()
        ct = 5
        pl0 = ''
        for i in tmp :
            if ct > 0 :
                ct -= 1
                continue
            if i == '\n' :
                ct = 5
            pl0 += i

        config.set_pl0code(pl0)
        self.intxt.setPlainText('')
        self.outtxt.setPlainText('')
        self.pctable.setRowCount(0)
        return

    def compile(self):  #编译按钮
        tmp = self.pltxt.toPlainText()

        #消除行号
        ct = 5
        pl0 = ''
        for i in tmp :
            if ct > 0 :
                ct -= 1
                continue
            if i == '\n' :
                ct = 5
            pl0 += i

        #如果没有行号
        if tmp[:5] != '  1: ' :
            pl0 = tmp

        config.set_pl0code(pl0)
        config.set_errorinfo([0])
        config.set_alltoken([])
        config.set_allpcode([])
        config.set_output('')
        lexer = lex()
        lexer.start()
        program = prog()
        program.start()
        pcode = config.get_allpcode()
        l = len(pcode)

        outstr = ''
        errorinfo = config.get_errorinfo()
        lener = len(errorinfo)
        if errorinfo[0] == 1 :
            outstr += '词法错误：\n'
            for i in  range(1,lener):
                outstr += errorinfo[i]+'\n'
            self.pctable.setRowCount(0)
            self.state = 0
        elif errorinfo[0] == 2 :
            outstr += '语法错误：\n'
            for i in range(1,lener) :
                outstr += errorinfo[i]+'\n'
            self.pctable.setRowCount(0)
            self.state = 0
        else :
            outstr += '编译成功！PCode指令如右表所示。'
            self.pctable.setRowCount(l)
            self.state = 1
            for i in range(l) :
                self.pctable.setVerticalHeaderItem(i,QTableWidgetItem(str(i)))
                self.pctable.setItem(i,0,QTableWidgetItem(mappf[pcode[i].F]))
                self.pctable.setItem(i,1,QTableWidgetItem(str(pcode[i].L)))
                self.pctable.setItem(i,2,QTableWidgetItem(str(pcode[i].A)))
                #self.pctable.itemAt(i,0).setTextAlignment(0x4|0x80)
                # self.pctable.item(i,1).setTextAlignment(0x4|0x80)
                # self.pctable.item(i,3).setTextAlignment(0x4|0x80)
        self.outtxt.setPlainText(outstr)

        return

    def inte(self):     #解释按钮
        if self.state == 0:
            self.outtxt.setPlainText('请先完成编译，再进行解释。')
            return
        config.set_input(self.intxt.toPlainText())
        intepretor =  interp()
        intepretor.start()
        output = config.get_output()
        self.outtxt.setPlainText(output)
        return

app = QtWidgets.QApplication(sys.argv)
w = MainUi()
w.setWindowTitle('PL0')
w.show()
sys.exit(app.exec_())
