import config
from classes import *
from Lexer import lex

levmax = 3          #最大嵌套层数
tokenptr = 0        #token数组下标
lastsym = []        #上一个单词
sym = []            #当前单词
allpcode = []       #pcode表
alltoken = []       #单词表
allsymtab = []      #符号表
errorinfo = [0]     #错误信息表
nummax = 10000000000000000000   #最大整数
#语句开始符号集合
stafirset = [SymType.callsy.value, SymType.beginsy.value, SymType.ifsy.value,
             SymType.whilesy.value, SymType.readsy.value, SymType.writesy.value]
#声明开始符号集合
decfirset = [SymType.constsy.value, SymType.varsy.value, SymType.procsy.value]
#因子开始符号集合
facfirset = [SymType.idsy.value, SymType.intsy.value, SymType.lcurvesy.value]
#逻辑运算符集合
logoprset = [SymType.equalsy.value, SymType.nequalsy.value, SymType.lesssy.value,
             SymType.lequalsy.value, SymType.moresy.value, SymType.mequalsy.value]
#错误信息
errormsg = [
	"", "常数说明中应是'='而不是':='", "常数说明中'='后应为数字",
	"常数说明中标识符后应为'='", "const,var,procedure后应为标识符",
	"漏掉逗号或分号", "过程说明后的符号不正确", "应为语句开始符号",
	"程序体内语句部分后的符号不正确", "程序结尾应为句号", "语句之间漏了分号",
	"标识符未说明", "不可向常量或过程赋值", "赋值语句中应为赋值运算符':='",
    "call后应为标识符", "call后标识符属性应为过程,不可调用常量或变量",
	"条件语句中缺失then", "应为分号或end", "while型循环语句中缺失do",
	"语句后的符号不正确", "应为关系运算符", "表达式内不可有过程标识符",
	"缺失右括号", "因子后不可为此符号", "表达式不能以此符号开始",
    "repeat循环语句中缺失until", "代码太长，无法编译", "RuntimeError，地址偏移越界",
    "Read语句括号内不是标识符", "这个数太大，超过10^19", "缺失左括号",
    "句号后面有多余代码", "嵌套层数过多"
]

#报错函数
def ERROR(n):
    global errorinfo, sym, lastsym
    errorinfo[0] = 2
    j = sym.column
    i = sym.line
    last = [5, 16, 1, 18, 10]
    if n in last:
        j = lastsym.column
        i = lastsym.line
    errorinfo.append('错误编号：'+str(n)+'  '+errormsg[n]+'  '+str(j)+' in line '+str(i))


#检测后继符号合法性
#set1：当前语法成分合法的后继符号
#set2：停止符号集合
#n：错误编号
def isLegal(set1, set2, n):
    global sym
    if sym.st not in set1 :
        ERROR(n)
        while sym.st not in set1 and sym.st not in set2 :
            getsym()
    return

#新增一条Pcode操作指令
def gen(F, L, A):
    allpcode.append(PerPcode(F,L,A))

#读入下一个单词
def getsym():
    global sym, alltoken, tokenptr, lastsym
    lastsym = sym
    sym = alltoken[tokenptr]
    if tokenptr+1 >= len(alltoken) :
        return
    tokenptr+=1

#查找标识符在符号表中的位置，从tx开始倒序查找标识符
def position(id):
    global allsymtab
    l = len(allsymtab)
    for i in range(l-1,-1,-1):
        if allsymtab[i].name == id :
            return i
    return 0

#<常量定义> ::= <标识符>=<无符号整数>
def conDefine(level, address):
    global alltoken, tokenptr, allsymtab
    if sym.st == SymType.idsy.value :
        name = sym.value
        getsym()
        if sym.st == SymType.equalsy.value or sym.st == SymType.assignsy.value :
            if sym.st == SymType.assignsy.value :
                ERROR(1)    #错误处理：应是=而不是:=

            getsym()
            if sym.st == SymType.intsy.value :
                #填写符号表
                allsymtab.append(PerSymbol(1,sym.value,level,address[0],name))
                getsym()
            else :  #错误处理：=后应为数
                ERROR(2)
        else :  #错误处理：标识符后应为=
            ERROR(3)
    else :  #错误处理：const,var,procedure后应为标识符
        ERROR(4)
    return

#<变量说明部分>::= var<标识符>{,<标识符>};
def varDefine(level, address):
    if sym.st == SymType.idsy.value :
        allsymtab.append(PerSymbol(2,0,level,address[0],sym.value))
        address[0] += 1
        getsym()
    else :  #错误处理：const,var,procedure后应为标识符
        ERROR(4)
    return

#<表达式> ::= [+|-]<项>{<加法运算符><项>}
def expression(level, fsys):
    tmp = []
    tmp.extend(fsys)
    tmp.append(SymType.addsy.value)
    tmp.append(SymType.subsy.value)

    if sym.st == SymType.addsy.value or sym.st == SymType.subsy.value :
        addop = sym.st
        getsym()
        term(level, tmp)
        if addop == SymType.subsy.value :
            gen(Operator.OPR.value,0,1) #负号
    else :
        term(level, tmp)

    while sym.st == SymType.addsy.value or sym.st == SymType.subsy.value :
        addop = sym.st
        getsym()
        term(level, tmp)
        if addop == SymType.addsy.value :
            gen(Operator.OPR.value,0,2) #加法指令
        else :
            gen(Operator.OPR.value,0,3) #减法指令
    return

#<项> ::= <因子>{<乘法运算符><因子>}
def term(level, fsys):
    tmp = []
    tmp.extend(fsys)
    tmp.append(SymType.mulsy.value)
    tmp.append(SymType.divsy.value)

    factor(level, tmp)
    while (sym.st == SymType.mulsy.value or sym.st == SymType.divsy.value) :
        mulop = sym.st
        getsym()
        factor(level, tmp)
        if mulop == SymType.mulsy.value :
            gen(Operator.OPR.value,0,4) #乘法指令
        else :
            gen(Operator.OPR.value,0,5) #除法指令
    return

#<因子> ::= <标识符>|<无符号整数>|'('<表达式>')'
def factor(level, fsys):
    global facfirset, nummax
    isLegal(facfirset, fsys, 24)
    while sym.st in facfirset:
        if sym.st == SymType.idsy.value :    #因子为常量or变量
            i = position(sym.value)
            if i == 0:
                ERROR(11)
            else :
                t = allsymtab[i].type
                if t == 1 :
                    gen(Operator.LIT.value,0,allsymtab[i].value)
                elif t == 2 :
                    gen(Operator.LOD.value,level-allsymtab[i].level,allsymtab[i].address)
                elif t == 3 :   #错误处理：表达式内不可有过程标识符
                    ERROR(21)
            getsym()
        elif sym.st == SymType.intsy.value :    #因子为一个数
            if sym.value > nummax :
                ERROR(29)
            gen(Operator.LIT.value,0,sym.value)
            getsym()
        elif sym.st == SymType.lcurvesy.value : #因子为表达式，递归调用
            getsym()
            tmp = []
            tmp.extend(fsys)
            tmp.append(SymType.rcurvesy.value)
            expression(level, tmp)

            if sym.st == SymType.rcurvesy.value :
                getsym()
            else :
                ERROR(22)
        tmp = []
        tmp.append(SymType.lcurvesy.value)
        isLegal(fsys, tmp, 23)
    return

#<条件语句> ::= if<条件>then<语句>[else<语句>]
def condition(level, fsys):
    global logoprset
    if sym.st == SymType.oddsy.value :
        getsym()
        expression(level, fsys)
        gen(Operator.OPR.value,0,6)
    else :
        tmp = []
        tmp.extend(fsys)
        tmp.extend(logoprset)
        expression(level, tmp)
        if (sym.st not in logoprset) :
            ERROR(20)   #错误处理：应该为关系运算符
        else :
            relop = sym.st
            getsym()
            expression(level, fsys)
            if relop == SymType.equalsy.value :
                gen(Operator.OPR.value,0,8)
            elif relop == SymType.nequalsy.value :
                gen(Operator.OPR.value,0,9)
            elif relop == SymType.lesssy.value :
                gen(Operator.OPR.value,0,10)
            elif relop == SymType.mequalsy.value :
                gen(Operator.OPR.value,0,11)
            elif relop == SymType.moresy.value :
                gen(Operator.OPR.value,0,12)
            elif relop == SymType.lequalsy.value :
                gen(Operator.OPR.value,0,13)

#<语句> ::= <赋值语句>|<条件语句>|<当型循环语句>
#|<过程调用语句>|<读语句>|<写语句>|<复合语句>|<重复语句>|<空>
def statement(level, fsys):
    global allsymtab, allpcode
    if sym.st == SymType.idsy.value :
        i = position(sym.value)
        if (i==0):  #错误处理：标识符未说明
            ERROR(11)
        elif allsymtab[i].type != 2 :
            ERROR(12)   #错误处理：不可向常量或过程赋值
            i = 0
        getsym()
        if sym.st == SymType.assignsy.value :
            getsym()
        else :  #错误处理：应为赋值运算符:=
            ERROR(13)
        expression(level, fsys)
        if i != 0 :
            gen(Operator.STO.value, level - allsymtab[i].level, allsymtab[i].address)
    elif sym.st == SymType.callsy.value :
        getsym()
        if sym.st != SymType.idsy.value :
            ERROR(14)
        else :
            i = position(sym.value)
            if i == 0:
                ERROR(11)
            else :
                if allsymtab[i].type == 3 :
                    gen(Operator.CAL.value, level-allsymtab[i].level,allsymtab[i].address)
                else :
                    ERROR(15)
            getsym()
    elif sym.st == SymType.ifsy.value :
        getsym()
        tmp = []
        tmp.extend(fsys)
        tmp.append(SymType.thensy.value)
        tmp.append(SymType.dosy.value)
        condition(level, tmp)
        if sym.st == SymType.thensy.value :
            getsym()
        else :
            ERROR(16)
        cx1 = len(allpcode)
        gen(Operator.JPC.value,0,0)
        tmp2 = []
        tmp2.extend(fsys)
        tmp2.append(SymType.elsesy.value)
        statement(level, tmp2)
        if (sym.st == SymType.elsesy.value):
            getsym()
            cx2 = len(allpcode)
            gen(Operator.JMP.value,0,0)
            allpcode[cx1].A = len(allpcode)
            statement(level, fsys)
            allpcode[cx2].A = len(allpcode)
        else :
            allpcode[cx1].A = len(allpcode)
    elif sym.st == SymType.beginsy.value :
        getsym()
        tmp = []
        tmp.extend(fsys)
        tmp.append(SymType.semicolonsy.value)
        tmp.append(SymType.endsy.value)
        statement(level, tmp)
        while sym.st in stafirset or sym.st == SymType.idsy.value or sym.st == SymType.semicolonsy.value :
            if sym.st == SymType.semicolonsy.value :
                getsym()
            else :  #错误处理：语句间漏分号
                ERROR(10)
            statement(level, tmp)
        if sym.st == SymType.endsy.value :
            getsym()
        else :  #错误处理：缺少end
            ERROR(17)
    elif sym.st == SymType.whilesy.value :
        cx1 = len(allpcode)
        getsym()
        tmp = []
        tmp.extend(fsys)
        tmp.append(SymType.dosy.value)
        condition(level, tmp)
        cx2 = len(allpcode)
        gen(Operator.JPC.value,0,0)
        if sym.st == SymType.dosy.value :
            getsym()
        else :
            ERROR(18)
        statement(level, fsys)
        gen(Operator.JMP.value,0,cx1)
        allpcode[cx2].A = len(allpcode)
    elif sym.st == SymType.readsy.value :
        getsym()
        if sym.st == SymType.lcurvesy.value :
            while 1 :
                getsym()
                if sym.st == SymType.idsy.value :
                    i = position(sym.value)
                    if i == 0 :
                        ERROR(11)
                    else :
                        if allsymtab[i].type != 2 :
                            ERROR(12)
                            i = 0
                        else :
                            gen(Operator.RED.value,level-allsymtab[i].level,allsymtab[i].address)
                else :
                    ERROR(28)
                getsym()
                if sym.st != SymType.commasy.value :
                    break
        else :
            ERROR(30)

        if sym.st != SymType.rcurvesy.value :
            ERROR(22)
        getsym()
    elif sym.st == SymType.writesy.value :
        getsym()
        if sym.st == SymType.lcurvesy.value :
            tmp = []
            tmp.extend(fsys)
            tmp.append(SymType.rcurvesy.value)
            tmp.append(SymType.commasy.value)
            while 1:
                getsym()
                expression(level, tmp)
                gen(Operator.WRT.value,0,0)
                if sym.st != SymType.commasy.value:
                    break

            if sym.st != SymType.rcurvesy.value :
                ERROR(22)

            getsym()
        else :
            ERROR(30)
    elif sym.st == SymType.repeatsy.value :
        cx1 = len(allpcode)
        getsym()
        tmp = []
        tmp.extend(fsys)
        tmp.append(SymType.semicolonsy.value)
        tmp.append(SymType.untilsy.value)
        statement(level, tmp)
        while sym.st in stafirset or sym.st == SymType.idsy.value or sym.st == SymType.semicolonsy.value :
            if sym.st == SymType.semicolonsy.value :
                getsym()
            else :
                ERROR(5)
            tmp3 = []
            tmp3.extend(fsys)
            tmp3.append(SymType.semicolonsy.value)
            tmp3.append(SymType.untilsy.value)
            statement(level, tmp3)
        if sym.st == SymType.untilsy.value :
            getsym()
            condition(level, fsys)
            gen(Operator.JPC.value,0,cx1)
        else :  #错误处理：缺少until
            ERROR(25)
        tmp = []
        isLegal(fsys, tmp, 19)  #检测语句正确性
    return

#<分程序> ::= [<常量说明部分>][<变量说明部分>][<过程说明部分>]<语句>
def block(level, fsys):
    global levmax, allpcode, allsymtab
    address = [3]   #三个空间存放：静态链SL、动态链DL和返回地址RA
    tx0 = len(allsymtab)-1
    allsymtab[-1].address = len(allpcode)   #记录当前代码层开始位置
    gen(Operator.JMP.value, 0, 0);  #产生跳转指令，跳转位置未知暂时填0

    if level > levmax:  #嵌套层数过多
        ERROR(32)

    while 1 :

        while sym.st == SymType.constsy.value :
            getsym()
            conDefine(level,address)
            while sym.st == SymType.commasy.value :
                getsym()
                conDefine(level,address)
            if sym.st == SymType.semicolonsy.value :
                getsym()
            else :  #缺少分号
                ERROR(5)

        while sym.st == SymType.varsy.value :
            getsym()
            varDefine(level,address)
            while sym.st == SymType.commasy.value :
                getsym()
                varDefine(level,address)
            if sym.st == SymType.semicolonsy.value :
                getsym()
            else :  #缺少分号
                ERROR(5)

        while sym.st == SymType.procsy.value :  #处理过程声明
            getsym()
            if sym.st == SymType.idsy.value :
                #添加符号表
                allsymtab.append(PerSymbol(3,0,level,address[0],sym.value))
                getsym()
            else :  #procedure后应为标识符
                ERROR(4)

            if sym.st == SymType.semicolonsy.value :
                getsym()
            else :
                ERROR(5)

            tmp = []
            tmp.extend(fsys)
            tmp.append(SymType.semicolonsy.value)
            block(level+1, tmp)

            if sym.st == SymType.semicolonsy.value :
                getsym()
                tmp2 = []
                tmp2.extend(stafirset)
                tmp2.append(SymType.idsy.value)
                tmp2.append(SymType.procsy.value)
                tmp2.append(SymType.pointsy.value)
                isLegal(tmp2, fsys, 6)
            else :
                ERROR(5)

        tmp3 = []
        tmp3.extend(stafirset)
        tmp3.append(SymType.idsy.value)
        tmp3.append(SymType.pointsy.value)
        tmp3.append(SymType.eofsy.value)
        isLegal(tmp3, decfirset, 7)

        if sym.st not in decfirset :
            break


    allpcode[allsymtab[tx0].address].A = len(allpcode)
    allsymtab[tx0].address = len(allpcode)

    #添加生成指令，为被调用的过程开辟dx单元的数据区
    gen(Operator.INT.value, 0, address[0])
    tmp = []
    tmp.extend(fsys)
    tmp.append(SymType.semicolonsy.value)
    tmp.append(SymType.endsy.value)
    statement(level, tmp)
    gen(Operator.OPR.value, 0, 0)   #添加释放指令，过程出口需要释放数据段

    allsymtab=allsymtab[:tx0+1]
    tmp2 = []
    isLegal(fsys, tmp2, 8)
    return

class prog:
    def __init__(self):
        return

    def start(self):
        global allpcode, alltoken, tokenptr, allsymtab, sym, errorinfo, lastsym
        tokenptr = 0
        lastsym = []
        sym = []
        allpcode = []
        allsymtab = []
        errorinfo = config.get_errorinfo()
        if errorinfo[0] > 0 :
            return
        allpcode = []
        allsymtab.append(PerSymbol(3,0,0,0,'main'))
        alltoken = config.get_alltoken()
        # for i in alltoken :
        #     print(i.__dict__)
        getsym()
        bfset = []
        bfset.extend(stafirset)
        bfset.extend(decfirset)
        bfset.append(SymType.pointsy.value)
        bfset.append(SymType.eofsy.value)
        block(0, bfset)
        if (sym.st == SymType.pointsy.value):
            getsym()
            if (sym.st != SymType.eofsy.value):
                 ERROR(31)
        else:
            ERROR(9)
        if len(allpcode) > 1000 :
            ERROR(26)
        # for i in allsymtab :
        #     print(i.__dict__)
        # for i in allpcode :
        #     print(i.__dict__)
        # for i in errorinfo :
        #     print(i)

        config.set_errorinfo(errorinfo)
        config.set_allpcode(allpcode)
        return
