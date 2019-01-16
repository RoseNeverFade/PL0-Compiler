import config
import sys
from classes import *

inps = ''       #读入pl0代码
alltoken = []   #存储词法分析的结果
inpl = 0        #pl0代码的长度
line = 1        #记录每个字符的行号
column = 0      #记录每个字符的列号
#保留字数组
reword = ['if', 'then', 'else', 'repeat', 'until', 'while', 'do', 'read', 'write', 'call', 'begin',
          'end', 'const', 'var', 'procedure', 'odd']

inpc = 0        #遍历pl0代码时的下标
char = ''       #保存当前读入的字符
token = ''      #保存当前读入的单词
outp = []       #暂时保存词法分析的结果
sum = 0         #单词数量
errorinfo = [0] #错误信息

#报错函数
def ERROR(j, i, estr):
    global errorinfo
    errorinfo[0] = 1
    errorinfo.append(str(estr)+'  '+str(j)+' in line '+str(i))

#读入下一个字符
def getchar():
    global inpc, char
    char = inps[inpc]
    inpc += 1

#跳过空字符
def getnbc():
    global inpc, inpl, line, column
    while inpc < inpl and inps[inpc].isspace() :
        if inps[inpc] == '\n':
            line += 1
            column = inpc+1
        inpc += 1

#将char中的字符拼到token中
def cat():
    global token, char
    token += char

#退读一个字符
def ungetch():
    global char, inpc
    inpc -= 1
    char = inps[inpc-1]

#查看token中的单词是否是保留字
def reserve():
    global token
    l = len(reword)
    for i in range(l):
        if (token == reword[i]):
            return i+3
    return SymType.idsy.value

#读取一个单词
def getsym():
    global token, char, inpc, line, column
    getnbc()

    if inpc >= inpl :
        return 0
    token = ''
    getchar()

    if char.isalpha() :         #保留字或标识符
        while char.isalpha() or char.isdigit() :
            cat()
            getchar()
        ungetch()
        C = reserve()
        outp.append([C, line, token, inpc-column])
    elif char.isdigit():        #数字
        while char.isdigit():
            cat()
            getchar()
        ungetch()
        outp.append([SymType.intsy.value, line, int(token), inpc-column])
    elif char == '+' :
        outp.append([SymType.addsy.value, line, char, inpc-column])
    elif char == '-' :
        outp.append([SymType.subsy.value, line, char, inpc-column])
    elif char == '*' :
        outp.append([SymType.mulsy.value, line, char, inpc-column])
    elif char == '/' :
        outp.append([SymType.divsy.value, line, char, inpc-column])
    elif char == '<' :
        cat()
        getchar()
        if char == '=' :
            cat()
            outp.append([SymType.lequalsy.value, line, token, inpc-column])
        elif char == '>':
            cat()
            outp.append([SymType.nequalsy.value, line, token, inpc-column])
        else :
            ungetch()
            outp.append([SymType.lesssy.value, line, token, inpc-column])
    elif char == '>' :
        cat()
        getchar()
        if char == '=' :
            cat()
            outp.append([SymType.mequalsy.value, line, token, inpc-column])
        else :
            ungetch()
            outp.append([SymType.moresy.value, line, token, inpc-column])
    elif char == '=' :
        outp.append([SymType.equalsy.value, line, char, inpc-column])
    elif char == ':' :
        cat()
        getchar()
        if char == '=':
            cat()
            outp.append([SymType.assignsy.value, line, token, inpc-column])
        else :
            ERROR(inpc-column, line, ': is an illegal word.')
    elif char == '(' :
        outp.append([SymType.lcurvesy.value, line, char, inpc-column])
    elif char == ')' :
        outp.append([SymType.rcurvesy.value, line, char, inpc-column])
    elif char == ',' :
        outp.append([SymType.commasy.value, line, char, inpc-column])
    elif char == ';' :
        outp.append([SymType.semicolonsy.value, line, char, inpc-column])
    elif char == '.' :
        outp.append([SymType.pointsy.value, line, char, inpc-column])
    elif char == '\0' :
        outp.append([SymType.eofsy.value, line, char, inpc-column])
        return 0
    else :
        ERROR(inpc-column, line, char+' can not be identified.')
        return 0
    return 1

class lex:
    def __init__(self):
        return

    def start(self):
        global inps, inpl, inpc, char, token, sum, outp, errorinfo, line, column
        line = 1
        column = 0
        inpc = 0
        char = ''
        token = ''
        outp = []
        alltoken = []
        sum = 0
        errorinfo = [0]
        inps = config.get_pl0code()
        inps += '\0'
        inpl = len(inps)
        while getsym() :
            sum += 1
        outl = len(outp)
        for i in range(outl):
            alltoken.append(Token(outp[i][0], outp[i][1], outp[i][2], outp[i][3]))

        config.set_alltoken(alltoken)
