import pytest
from unittest.mock import patch, MagicMock
from backend.AI_api import get_response

def test_ai_api_basic():
    """测试AI接口基本功能"""
    # 模拟AI API返回
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "登录"
    
    with patch('backend.AI_api.client.chat.completions.create', return_value=mock_response):
        result = get_response("我想登录系统")
        assert result == "登录"

def test_ai_api_recognize_recharge():
    """测试AI识别充值意图"""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "充值"
    
    with patch('backend.AI_api.client.chat.completions.create', return_value=mock_response):
        result = get_response("我要给账户充钱")
        assert result == "充值"

def test_ai_api_recognize_help():
    """测试AI识别帮助意图"""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "使用帮助"
    
    with patch('backend.AI_api.client.chat.completions.create', return_value=mock_response):
        result = get_response("我需要帮助，不知道怎么操作")
        assert result == "使用帮助"

def test_ai_api_unknown_intent():
    """测试AI处理未知意图"""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "default"
    
    with patch('backend.AI_api.client.chat.completions.create', return_value=mock_response):
        result = get_response("这个功能怎么用啊")
        assert result == "default"