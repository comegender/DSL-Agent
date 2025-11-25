import pytest
from backend.yacc import parser

def test_parse_simple_script():
    """测试解析简单脚本"""
    script = """
    do greet {
        speak "Hello, welcome!";
        jump ask;
    }
    """
    
    result = parser.parse(script)
    assert isinstance(result, list)
    assert len(result) == 1
    
    module = result[0]
    assert module['type'] == 'do_statement'
    assert module['task'] == 'greet'
    assert len(module['body']) == 2
    
    # 检查第一个语句
    assert module['body'][0]['type'] == 'speak_statement'
    assert module['body'][0]['message'] == 'Hello, welcome!'
    
    # 检查第二个语句
    assert module['body'][1]['type'] == 'jump_statement'
    assert module['body'][1]['target'] == 'ask'

def test_parse_if_statement():
    """测试解析条件语句"""
    script = """
    do check_login {
        if (is_login == true) {
            speak "已登录";
        } else {
            speak "未登录";
            jump login;
        }
    }
    """
    
    result = parser.parse(script)
    assert len(result) == 1
    
    module = result[0]
    assert module['task'] == 'check_login'
    assert len(module['body']) == 1
    
    if_stmt = module['body'][0]
    assert if_stmt['type'] == 'if_statement'
    assert if_stmt['condition']['operation'] == '=='
    assert len(if_stmt['then']) == 1
    assert len(if_stmt['else']) == 2

def test_parse_set_statement():
    """测试解析变量赋值语句"""
    script = """
    do set_values {
        set username = @content@;
        set age = 25;
        set balance = call get_balance;
    }
    """
    
    result = parser.parse(script)
    assert len(result) == 1
    
    module = result[0]
    assert len(module['body']) == 3
    
    # 检查第一个赋值语句
    set_stmt1 = module['body'][0]
    assert set_stmt1['type'] == 'set_statement'
    assert set_stmt1['left'] == 'username'
    
    # 检查第二个赋值语句
    set_stmt2 = module['body'][1]
    assert set_stmt2['left'] == 'age'
    assert set_stmt2['right'] == 25.0
    
    # 检查第三个赋值语句
    set_stmt3 = module['body'][2]
    assert set_stmt3['left'] == 'balance'
    assert set_stmt3['right']['type'] == 'call_statement'