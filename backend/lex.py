import ply.lex as lex
import AI_api

# 词法分析器部分
tokens = (
    # 关键字
    'DO', 'CALL', 'SET', 'IF', 'ELSE', 'RESPONSE', 'SPEAK', 'JUMP',
    
    # 标识符和变量
    'ID', 'VARIABLE',
    
    # 常量
    'STRING', 'NUMBER',
    
    # 运算符
    'EQUALS', 'EQEQ', 'GREATER', 'LESS', 'GREATEREQ', 'LESSEQ', 'NOTEQ',
    
    # 分隔符
    'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'SEMICOLON', 'NEWLINE',
)

# 忽略空格和制表符（缩进处理单独处理）
t_ignore = ' \t\n'

# 关键字定义
reserved = {
    'do': 'DO',
    'call': 'CALL',
    'set': 'SET',
    'if': 'IF',
    'else': 'ELSE',
    'response': 'RESPONSE',
    'speak': 'SPEAK',
    'jump': 'JUMP',
}

# 运算符和分隔符
t_EQUALS = r'='
t_EQEQ = r'=='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQ = r'>='
t_LESSEQ = r'<='
t_NOTEQ = r'!='
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'

# 变量（如@money@）
def t_VARIABLE(t):
    r'@[a-zA-Z_][a-zA-Z0-9_]*@'
    return t

# 字符串（带双引号）
def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # 去除引号
    return t


# 数字（整数和浮点数）
def t_NUMBER(t):
    r'\d+\.?\d*'
    try:
        t.value = float(t.value)
    except ValueError:
        print(f"无效的数字: {t.value}")
        t.value = 0
    return t

# 标识符（会检查是否为关键字）
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # 检查是否为关键字
    return t

# 错误处理
def t_error(t):
    print(f"非法字符 '{t.value[0]}' 在行 {t.lexer.lineno}")
    t.lexer.skip(1)

# 构建词法分析器
lexer = lex.lex()

lexer.input(
    '''
do change_password {
    set a=b;
}
    '''
)

# while True:
#     tok = lexer.token()
#     if not tok: break      # No more input
#     print(tok)
