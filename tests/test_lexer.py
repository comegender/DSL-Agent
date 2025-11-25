import pytest
from backend.lex import lexer

def test_lexer_keywords():
    """测试关键字识别"""
    script = """
    do login {
        set username = @content@;
        if (username == "admin") {
            speak "登录成功";
            jump main_menu;
        } else {
            call log_error;
        }
    }
    """
    
    lexer.input(script)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value))
    
    # 检查是否正确识别了关键字
    assert ('DO', 'do') in tokens
    assert ('SET', 'set') in tokens
    assert ('IF', 'if') in tokens
    assert ('SPEAK', 'speak') in tokens
    assert ('JUMP', 'jump') in tokens
    assert ('ELSE', 'else') in tokens
    assert ('CALL', 'call') in tokens

def test_lexer_operators():
    """测试运算符识别"""
    script = "a == b; c != d; e > f; g < h; i >= j; k <= l;"
    
    lexer.input(script)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok.type)
    
    assert 'EQEQ' in tokens
    assert 'NOTEQ' in tokens
    assert 'GREATER' in tokens
    assert 'LESS' in tokens
    assert 'GREATEREQ' in tokens
    assert 'LESSEQ' in tokens
    assert 'SEMICOLON' in tokens

def test_lexer_variables():
    """测试变量识别"""
    script = "set money = @money@; set name = @name@; set content = @content@;"
    
    lexer.input(script)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value))
    
    assert ('VARIABLE', '@money@') in tokens
    assert ('VARIABLE', '@name@') in tokens
    assert ('VARIABLE', '@content@') in tokens
    assert ('EQUALS', '=') in tokens

def test_lexer_strings_numbers():
    """测试字符串和数字识别"""
    script = 'speak "Hello World"; set age = 25; set price = 99.9;'
    
    lexer.input(script)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value))
    
    assert ('STRING', 'Hello World') in tokens
    assert ('NUMBER', 25.0) in tokens
    assert ('NUMBER', 99.9) in tokens