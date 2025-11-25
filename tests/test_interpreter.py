import pytest
from backend.script_achieve import do_statement, set_statement, d_veriable
from unittest.mock import patch

def test_set_statement():
    """测试变量赋值"""
    # 重置全局变量字典
    d_veriable.clear()
    
    # 测试基本赋值
    set_statement('name', 'test_user')
    assert d_veriable['name'] == 'test_user'
    
    # 测试数字赋值
    set_statement('age', 25)
    assert d_veriable['age'] == 25
    
    # 测试模拟用户输入
    with patch('backend.function_interface.getUserInput', return_value='12345'):
        set_statement('password', '@content@')
        assert d_veriable['password'] == '12345'

def test_do_statement_speak(capsys):
    """测试speak语句执行"""
    statements = [
        {
            'type': 'speak_statement',
            'message': 'Test message'
        }
    ]
    
    do_statement(statements)
    captured = capsys.readouterr()
    assert '🤖：Test message' in captured.out

def test_do_statement_if():
    """测试if语句执行"""
    d_veriable.clear()
    d_veriable['score'] = 85
    
    # 测试条件为真的情况
    true_block = [
        {'type': 'speak_statement', 'message': 'Passed'}
    ]
    
    false_block = [
        {'type': 'speak_statement', 'message': 'Failed'}
    ]
    
    if_stmt = {
        'type': 'if_statement',
        'condition': {
            'left': 'score',
            'operation': '>=',
            'right': 60
        },
        'then': true_block,
        'else': false_block
    }
    
    with patch('backend.script_achieve.speak_statement') as mock_speak:
        do_statement([if_stmt])
        mock_speak.assert_called_with('Passed')
        assert mock_speak.call_count == 1

def test_jump_statement(monkeypatch):
    """测试跳转语句"""
    # 模拟跳转目标的解析结果
    def mock_jump_to(target):
        return [
            {
                'body': [
                    {'type': 'speak_statement', 'message': f'Jumped to {target}'}
                ]
            }
        ]
    
    monkeypatch.setattr('backend.script_achieve.yacc.jump_to', mock_jump_to)
    
    with patch('backend.script_achieve.speak_statement') as mock_speak:
        jump_stmt = {
            'type': 'jump_statement',
            'target': 'test_target'
        }
        do_statement([jump_stmt])
        mock_speak.assert_called_with('Jumped to test_target')