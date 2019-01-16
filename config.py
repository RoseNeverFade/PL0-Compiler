class global_var:
    AllToken = []       #所有单词
    AllPcode = []       #所有pcode命令
    errorinfo = [0]     #错误信息
    pl0code = ''        #读取到的pl0代码
    output = ''         #输出信息
    input = ''          #输入信息

def set_input(input):
    global_var.input = input
def get_input():
    return global_var.input
def set_output(output):
    global_var.output = output
def get_output():
    return global_var.output
def set_alltoken(alltoken):
    global_var.AllToken = alltoken
def get_alltoken():
    return global_var.AllToken
def set_pl0code(pl0code):
    global_var.pl0code = pl0code
def get_pl0code():
    return global_var.pl0code
def set_errorinfo(errorinfo):
    global_var.errorinfo = errorinfo
def get_errorinfo():
    return global_var.errorinfo
def set_allpcode(allpcode):
    global_var.allpcode = allpcode
def get_allpcode():
    return global_var.allpcode
