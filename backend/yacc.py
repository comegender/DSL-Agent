import ply.yacc as yacc
import warnings
from . import AI_api
from . import test_script
from .lex import tokens

def p_script(p):
    '''script : do_module
              | script do_module'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_do_module(p):
    '''do_module : DO ID LBRACE c RBRACE'''
    task_name = p[2]
    p[0] = {
        'type': 'do_statement',
        'task': task_name,
        'body': p[4]  # 代码块内容，一个语句列表
    }

def p_c(p):
    '''c : statement
         | c statement'''
    if len(p) == 2:  # 只有一个语句
        p[0] = [p[1]]
    else:  # 多条语句：c + statement
        p[0] = p[1] + [p[2]]

def p_statement_set(p):
    '''statement : SET ID EQUALS expr SEMICOLON'''
    p[0] = {
        'type': 'set_statement',
        'left': p[2],
        'operation': '=',
        'right': p[4]
    }

def p_statement_speak(p):
    '''statement : SPEAK STRING SEMICOLON'''
    p[0] = {
        'type': 'speak_statement',
        'message': p[2]
    }

def p_statement_jump(p):
    '''statement : JUMP ID SEMICOLON'''
    p[0] = {
        'type': 'jump_statement',
        'target': p[2]
    }

def p_statement_if(p):
    '''statement : IF LPAREN condition RPAREN LBRACE c RBRACE'''
    p[0] = {
        'type': 'if_statement',
        'condition': p[3],       
        'then': p[6],            
        'else': []               
    }

def p_statement_if_else(p):
    '''statement : IF LPAREN condition RPAREN LBRACE c RBRACE ELSE LBRACE c RBRACE'''
    p[0] = {
        'type': 'if_statement',
        'condition': p[3],
        'then': p[6],
        'else': p[10]
    }

def p_condition_compare(p):
    '''condition : expr EQEQ expr
                 | expr NOTEQ expr
                 | expr GREATER expr
                 | expr LESS expr
                 | expr GREATEREQ expr
                 | expr LESSEQ expr'''
    p[0] = {
        'left': p[1],
        'operation': p[2],
        'right': p[3]
    }

def p_statement_call(p):
    '''statement : CALL ID SEMICOLON'''
    p[0] = {
        'type': 'call_statement',
        'function': p[2]
    }


def p_condition_expr(p):
    '''condition : expr'''
    p[0] = p[1] 

def p_expr_id(p):
    '''expr : ID'''
    p[0] = p[1]

def p_expr_call(p):
    '''expr : CALL ID'''
    p[0] = {
        'type': 'call_statement',
        'function': p[2]
    }

def p_expr_literal(p):
    '''expr : STRING
            | VARIABLE
            | NUMBER'''
    p[0] = p[1]


# ========== 构建解析器 ==========
parser = yacc.yacc()

def print_tree(x):
    resp = AI_api.get_response(x)
    s=test_script.get_script(resp)

    # ========== 执行解析 ==========
    result = parser.parse(s)

    # ========== 打印语法树 ==========
    print("🔍 生成的语法树结构如下：")
    import pprint
    pprint.pprint(result, indent=2)
    warnings.filterwarnings("ignore")


def jump_to(x):
    s=test_script.get_script_en(x)
        # ========== 执行解析 ==========
    result = parser.parse(s)

    # ========== 打印语法树 ==========
    print("🔍 生成的语法树结构如下：")
    import pprint
    pprint.pprint(result, indent=2)
    warnings.filterwarnings("ignore")

if __name__ == "__main__":
    print_tree()