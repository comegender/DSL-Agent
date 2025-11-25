from unittest.mock import patch
import pytest
import sys
import os
import logging
from datetime import datetime

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def reset_global_state():
    """自动重置全局状态，确保测试独立性"""
    from backend.script_achieve import d_veriable
    from backend.function_interface import ISLOGIN
    
    # 保存初始状态
    initial_vars = d_veriable.copy()
    initial_login = ISLOGIN
    
    yield  # 测试执行
    
    # 恢复初始状态
    d_veriable.clear()
    d_veriable.update(initial_vars)
    ISLOGIN = initial_login

@pytest.fixture
def mock_db_connection():
    """创建数据库连接模拟"""
    from unittest.mock import MagicMock
    
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    
    with patch('backend.function_interface.mysql.connector.connect', return_value=mock_connection):
        yield (mock_connection, mock_cursor)


def pytest_configure(config):
    """配置日志"""
    log_dir = "test_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"test_{timestamp}.log")
    
    # 配置 logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        filename=log_file,
        filemode='w',
        encoding='utf-8'
    )
    
    # 添加控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(console_handler)

def pytest_runtest_logreport(report):
    """记录每个测试用例的结果"""
    if report.when == 'call':
        logger = logging.getLogger('pytest')
        test_name = report.nodeid
        status = report.outcome.upper()
        
        logger.info(f"Test: {test_name} - {status}")
        
        if report.failed:
            logger.error(f"Test failed: {test_name}")
            logger.error(f"Error details:\n{report.longreprtext}")