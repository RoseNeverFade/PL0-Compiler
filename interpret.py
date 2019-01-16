import config
from classes import *
from Lexer import lex
from program import prog

bp = 1
s = [0 for i in range(5000)]    #模拟栈式计算机
input = []
inpc = 0
times = 0
output = ''
errormsg = ''

def ERROR(str):
    global errormsg
    errormsg = str

def base(l):    #通过过程基址求上一层过程基址
    global bp, s
    bb = bp
    while l>0 :
        bb = s[bb]
        l-=1
    return bb

def work(): #解释程序
    global bp, s, output, input, inpc, times
    pcd = config.get_allpcode()
    top = 0
    i = 0
    bp = 1

    while 1 :
        times += 1
        if times > 5000 :
            ERROR('程序可能存在死循环，请检查程序！')
            return 0
        p = pcd[i]
        i += 1
        if p.F == Operator.LIT.value :  #取常量置于栈顶
            top += 1
            s[top] = p.A
        elif p.F == Operator.OPR.value :    #计算
            if p.A == 0 :   #函数调用返回
                top = bp - 1
                i = s[top+3]
                bp = s[top+2]
            elif p.A == 1 : #负号
                s[top]=-s[top]
            elif p.A == 2 : #加
                top -= 1
                s[top] += s[top+1]
            elif p.A == 3 : #减
                top -= 1
                s[top] -= s[top+1]
            elif p.A == 4 : #乘
                top -= 1
                s[top] *= s[top+1]
            elif p.A == 5 : #除
                top -= 1
                s[top] //= s[top+1]
            elif p.A == 6 : #奇偶判断
                s[top] %= 2
            elif p.A == 8 : #判断相等
                top -= 1
                s[top] = int(s[top] == s[top+1])
            elif p.A == 9 : #判断不等
                top -= 1
                s[top] = int(s[top] != s[top+1])
            elif p.A == 10 :    #判断小于
                top -= 1
                s[top] = int(s[top] < s[top+1])
            elif p.A == 11 :    #判断大于等于
                top -= 1
                s[top] = int(s[top] >= s[top+1])
            elif p.A == 12 :    #判断大于
                top -= 1
                s[top] = int(s[top] > s[top+1])
            elif p.A == 13 :    #判断小于等于
                top -= 1
                s[top] = int(s[top] <= s[top+1])
        elif p.F == Operator.LOD.value :    #取变量值置于栈顶
            top += 1
            s[top] = s[base(p.L) + p.A]
        elif p.F == Operator.STO.value :    #栈顶值存于变量
            s[base(p.L) + p.A] = s[top]
            top -= 1
        elif p.F == Operator.CAL.value :    #调用过程
            s[top+1] = base(p.L)
            s[top+2] = bp
            s[top+3] = i
            bp = top + 1
            i = p.A
        elif p.F == Operator.INT.value :    #分配空间，指针+a
            top += p.A
        elif p.F == Operator.JMP.value :    #无条件跳转至a
            i = p.A
        elif p.F == Operator.JPC.value :    #条件跳转至a
            if s[top] == 0 :
                i = p.A
            top -= 1
        elif p.F == Operator.RED.value :    #读数据
            if inpc >= len(input) :
                ERROR('运行时错误：未输入的参数数量不足。')
                return 0
            s[base(p.L) + p.A] = input[inpc]
            inpc += 1
        elif p.F == Operator.WRT.value :    #写数据
            output += str(s[top])
            output += '\n'
            top += 1

        if i == 0 :
            break
    return 1

def trim(s):
    if len(s) == 0:
        return s
    elif s[0] == ' ':
        return (trim(s[1:]))
    elif s[-1] == ' ':
        return (trim(s[:-1]))
    return s


class interp:
    def __init__(self):
        return

    def start(self):
        global bp, s, output, input, inpc, times, errormsg
        times = 0
        bp = 1
        s = [0 for i in range(5000)]
        string = config.get_input()
        string = trim(string)
        string = string.strip('\n')
        input = []
        if len(string) > 0 :
            input.extend(list(map(int, string.split(' '))))
        inpc = 0
        output = ''
        if work() == 0 :
            config.set_output(errormsg)
            return
        output = '解释成功:\n' + output
        config.set_output(output)
        return
