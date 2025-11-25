import pytest
from unittest.mock import patch, MagicMock
from backend.test_script import get_script, get_script_en
from backend.yacc import get_tree, jump_to

def test_get_script():
    """测试获取脚本内容"""
    # 测试已知脚本
    login_script = get_script("登录")
    assert "do login {" in login_script
    assert "set userName = @content@;" in login_script
    
    # 测试不存在的脚本
    unknown_script = get_script("nonexistent")
    assert unknown_script == ""

def test_get_script_en():
    """测试获取英文脚本映射"""
    # 测试已知映射
    login_script = get_script_en("login")
    assert "do login {" in login_script
    
    # 测试不存在的映射
    unknown_script = get_script_en("nonexistent")
    assert unknown_script == ""

def test_get_tree():
    """测试语法树生成"""
    with patch('backend.yacc.test_script.get_script', return_value="""
    do test {
        speak "test";
    }
    """):
        tree = get_tree("test")
        assert isinstance(tree, list)
        assert len(tree) == 1
        assert tree[0]['task'] == 'test'

def test_jump_to():
    """测试跳转功能"""
    with patch('backend.yacc.test_script.get_script_en', return_value="""
    do target {
        speak "jumped";
    }
    """):
        result = jump_to("target")
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['task'] == 'target'