import pytest
from unittest.mock import patch, MagicMock
from backend.function_interface import (
    Login, Register, isLogin, getUserInput,
    getOriginalPassword, Recharge
)

def test_get_user_input(monkeypatch):
    """测试用户输入获取"""
    monkeypatch.setattr('builtins.input', lambda _: 'test input')
    assert getUserInput() == 'test input'

def test_login_success():
    """测试登录成功情况"""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'username': '111', 'password': '111111'}
    
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    
    with patch('backend.function_interface.mysql.connector.connect', return_value=mock_connection):
        result = Login('111', '111111')
        assert result is True
        assert isLogin() is True

def test_login_failure():
    """测试登录失败情况"""
    # 模拟密码错误
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'username': '111', 'password': '123456'}
    
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    
    with patch('backend.function_interface.mysql.connector.connect', return_value=mock_connection):
        result = Login('test', 'wrongpass')
        assert result is False
        assert isLogin() is False

def test_register_success():
    """测试注册成功情况"""
    # 模拟数据库无此用户
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None  # 无此用户
    
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    
    with patch('backend.function_interface.mysql.connector.connect', return_value=mock_connection):
        result = Register('newuser', '123456', '123456')
        assert result is True
        mock_cursor.execute.assert_called()  # 应该执行插入语句

def test_recharge():
    """测试充值功能"""
    # 模拟数据库查询和更新
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'username': 'test', 'remain': 100.0}
    
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    
    with patch('backend.function_interface.mysql.connector.connect', return_value=mock_connection):
        result = Recharge('test', 50)
        assert result is True
        # 修正：检查是否执行了带加法运算的更新语句
        mock_cursor.execute.assert_any_call(
            "UPDATE users SET remain = remain + %s WHERE username = %s", 
            (50, 'test')  # 注意：这里传入的是充值金额50，不是总余额150
        )