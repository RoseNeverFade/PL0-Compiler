from enum import Enum

class Token:    #每个单词
    st = -1     #类号
    line = -1   #行号
    value = ''  #值
    column = -1 #列号

    def __init__(self, s, l, v, c):
        self.st = s
        self.line = l
        self.value = v
        self.column = c


class PerSymbol:    #每个符号表项
    type = 0        #种类
    value = 0       #值
    level = -1      #嵌套层数
    address = -1    #地址
    name = ''       #名字

    def __init__(self, t, v, l, a, n):
        self.type = t
        self.value = v
        self.level = l
        self.address = a
        self.name = n

class PerPcode:     #每条pcode指令
    F = 0   #操作码
    L = 0   #层数差
    A = 0

    def __init__(self, f, l, a):
        self.F = f
        self.L = l
        self.A = a

SymType = Enum('SymType', (
    'idsy', 'intsy', 'ifsy', 'thensy', 'elsesy', 'repeatsy', 'untilsy',
    'whilesy', 'dosy', 'readsy', 'writesy', 'callsy', 'beginsy',
    'endsy', 'constsy', 'varsy', 'procsy', 'oddsy', 'addsy', 'subsy', 'mulsy',
    'divsy', 'equalsy', 'nequalsy', 'lesssy', 'lequalsy', 'moresy', 'mequalsy',
    'lcurvesy', 'rcurvesy', 'assignsy', 'commasy', 'semicolonsy', 'pointsy', 'eofsy'
))

Operator = Enum('Operator', ('INT', 'CAL', 'LIT', 'LOD', 'STO', 'JMP', 'JPC', 'OPR', 'RED', 'WRT'))
