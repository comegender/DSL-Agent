import pytest
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import patch, MagicMock
from backend.function_interface import Login, Recharge, Register
from backend.script_achieve import set_statement, d_veriable

# 线程本地存储，用于保存每个线程的模拟数据
thread_local = threading.local()

def generate_test_users(count):
    """生成测试用户数据"""
    return [
        (f"test_user_{i}", f"password_{i}") 
        for i in range(count)
    ]

# ------------------------------
# 测试 1: 并发登录 - 最终修复版本
# ------------------------------
def test_concurrent_login():
    """测试并发登录功能（修复线程本地数据传递问题）"""
    user_count = 5  # 先减少数量便于调试
    concurrent_users = 3
    test_users = generate_test_users(user_count)
    
    # 模拟数据库连接和游标
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # 存储实际执行的SQL查询，用于调试
    executed_queries = []
    
    # ------------------------------
    # 核心修复：根据实际SQL格式进行匹配
    # ------------------------------
    def mock_execute(query, params=None):
        # 记录实际执行的查询
        executed_queries.append((query, params))
        
        # 从当前线程的本地存储中获取测试用户列表
        local_test_users = getattr(thread_local, 'test_users', [])
        
        # 调试信息
        current_thread = threading.current_thread().name
        print(f"Thread {current_thread}: SQL查询 -> '{query}'")
        print(f"Thread {current_thread}: 参数 -> {params}")

        # 根据实际观察到的SQL格式进行匹配
        # 实际SQL: SELECT username, password FROM users WHERE username = %s
        if ("SELECT username, password FROM users WHERE username = %s" in query and 
            params and len(params) == 1):
            
            username = params[0]
            print(f"Thread {current_thread}: 尝试验证用户 '{username}'")
            
            # 在本地用户列表中查找用户
            for user, pwd in local_test_users:
                if user == username:
                    # 找到用户，返回用户信息（包括密码）
                    thread_local.fetchone_result = {'username': username, 'password': pwd}
                    print(f"Thread {current_thread}: 用户存在 '{username}'")
                    return
            
            # 用户不存在
            thread_local.fetchone_result = None
            print(f"Thread {current_thread}: 用户不存在 '{username}'")
        
        else:
            # 其他SQL查询，默认返回None
            thread_local.fetchone_result = None
            print(f"Thread {current_thread}: 不匹配的SQL查询")

    def mock_fetchone():
        """从当前线程的本地存储中获取查询结果"""
        result = getattr(thread_local, 'fetchone_result', None)
        print(f"Thread {threading.current_thread().name}: fetchone 返回 {result}")
        return result

    # 替换 execute 和 fetchone 方法
    mock_cursor.execute.side_effect = mock_execute
    mock_cursor.fetchone.side_effect = mock_fetchone

    with patch('backend.function_interface.mysql.connector.connect', return_value=mock_connection):
        # 重置全局登录状态
        from backend.function_interface import ISLOGIN
        ISLOGIN = False
        
        start_time = time.time()

        # ------------------------------
        # 改进的Wrapper函数
        # ------------------------------
        def login_task_wrapper(user_credentials, all_users):
            """
            登录任务的包装函数。
            """
            username, password = user_credentials
            # 每个线程都需要完整的用户列表来进行验证
            thread_local.test_users = all_users
            # 重置线程本地的fetchone结果
            thread_local.fetchone_result = None

            print(f"Thread {threading.current_thread().name}: 开始处理用户 '{username}'")
            result = Login(username, password)
            print(f"Thread {threading.current_thread().name}: 登录结果 '{username}' -> {result}")
            return result

        # 并发登录测试
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            # 提交任务时，传递用户凭证和完整的用户列表
            futures = [
                executor.submit(login_task_wrapper, user_cred, test_users)
                for user_cred in test_users
            ]
            
            success_count = 0
            error_messages = []
            for i, future in enumerate(as_completed(futures)):
                try:
                    result = future.result()
                    if result:
                        success_count += 1
                        print(f"任务 {i}: 成功")
                    else:
                        print(f"任务 {i}: 失败")
                except Exception as e:
                    error_messages.append(str(e))
                    print(f"任务 {i}: 异常 - {e}")

            end_time = time.time()
            duration = end_time - start_time

            # 打印调试信息
            print(f"\n=== 调试信息 ===")
            print(f"执行的SQL查询:")
            for i, (query, params) in enumerate(executed_queries):
                print(f"{i+1}. {query} | 参数: {params}")

            # 打印测试结果
            print(f"\n并发登录测试:")
            print(f"总用户数: {user_count}")
            print(f"并发数: {concurrent_users}")
            print(f"成功数: {success_count}")
            print(f"成功率: {success_count/user_count*100:.2f}%")
            print(f"总耗时: {duration:.2f}秒")
            if error_messages:
                print(f"错误信息: {', '.join(list(set(error_messages)))}")

            assert success_count == user_count, f"登录成功率错误：预期 {user_count}，实际 {success_count}"

# ------------------------------
# 测试 2: 充值压力 - 最终修复版本
# ------------------------------
def test_recharge_stress():
    """测试充值功能压力（修复线程本地数据传递问题）"""
    test_user = "stress_test_user"
    test_password = "test_pass"
    initial_balance = 0.0
    
    # 生成 10 个随机金额（先减少数量便于调试）
    recharge_amounts = [round(random.uniform(10, 100), 2) for _ in range(10)]
    concurrent_recharges = 5
    
    # 模拟数据库连接和游标
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # 存储执行的SQL查询
    executed_queries = []
    
    # 模拟用户数据库
    mock_users_db = {}
    
    # ------------------------------
    # 改进的线程安全模拟逻辑
    # ------------------------------
    def mock_execute(query, params=None):
        # 记录查询
        executed_queries.append((query, params))
        
        print(f"执行SQL: '{query}'")
        print(f"参数: {params}")

        # 根据实际SQL格式进行匹配
        if query and params:
            # 用户存在性检查（注册时）
            if ("SELECT username FROM users WHERE username = %s" in query and 
                len(params) == 1):
                username = params[0]
                if username in mock_users_db:
                    thread_local.fetchone_result = {'username': username}
                else:
                    thread_local.fetchone_result = None
            
            # 用户注册
            elif ("INSERT INTO users (username, password, remain)" in query and 
                  len(params) == 3):
                username, password, remain = params
                mock_users_db[username] = {
                    'password': password,
                    'remain': remain
                }
                print(f"注册用户: {username}")
                thread_local.fetchone_result = None
            
            # 登录查询 - 根据实际格式匹配
            elif ("SELECT username, password FROM users WHERE username = %s" in query and 
                  len(params) == 1):
                username = params[0]
                if username in mock_users_db:
                    user_data = mock_users_db[username]
                    thread_local.fetchone_result = {
                        'username': username, 
                        'password': user_data['password']
                    }
                    print(f"登录查询成功: {username}")
                else:
                    thread_local.fetchone_result = None
                    print(f"登录查询失败: 用户不存在")
            
            # 余额查询
            elif ("SELECT username, remain FROM users WHERE username = %s" in query and 
                  len(params) == 1):
                username = params[0]
                if username in mock_users_db:
                    user_data = mock_users_db[username]
                    thread_local.fetchone_result = {
                        'username': username, 
                        'remain': user_data['remain']
                    }
                    print(f"余额查询成功: {username} -> {user_data['remain']}")
                else:
                    thread_local.fetchone_result = None
            
            # 充值更新
            elif ("UPDATE users SET remain = %s WHERE username = %s" in query and 
                  len(params) == 2):
                new_balance, username = params
                if username in mock_users_db:
                    mock_users_db[username]['remain'] = new_balance
                    mock_cursor.rowcount = 1
                    print(f"充值成功: {username} -> {new_balance}")
                else:
                    mock_cursor.rowcount = 0
                thread_local.fetchone_result = None
            
            else:
                thread_local.fetchone_result = None
        else:
            thread_local.fetchone_result = None

    def mock_fetchone():
        result = getattr(thread_local, 'fetchone_result', None)
        print(f"fetchone 返回: {result}")
        return result

    # 替换 execute 和 fetchone 方法
    mock_cursor.execute.side_effect = mock_execute
    mock_cursor.fetchone.side_effect = mock_fetchone

    with patch('backend.function_interface.mysql.connector.connect', return_value=mock_connection):
        # 先注册用户
        print("=== 注册用户 ===")
        register_result = Register(test_user, test_password, test_password)
        print(f"注册结果: {register_result}")

        # 登录测试
        print("=== 登录测试 ===")
        login_result = Login(test_user, test_password)
        print(f"登录结果: {login_result}")

        # 调试信息
        print(f"\n=== 调试信息 ===")
        print(f"执行的SQL查询:")
        for i, (query, params) in enumerate(executed_queries):
            print(f"{i+1}. {query} | 参数: {params}")
        
        print(f"模拟数据库中的用户: {list(mock_users_db.keys())}")
        if test_user in mock_users_db:
            print(f"用户数据: {mock_users_db[test_user]}")

        assert login_result, "登录失败"
        
        # 如果登录成功，进行充值测试
        start_time = time.time()

        def recharge_task_wrapper(amount):
            """充值任务的包装函数"""
            return Recharge(test_user, amount)

        # 并发充值测试
        with ThreadPoolExecutor(max_workers=concurrent_recharges) as executor:
            futures = [
                executor.submit(recharge_task_wrapper, amount)
                for amount in recharge_amounts
            ]
            
            success_count = 0
            error_messages = []
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        success_count += 1
                except Exception as e:
                    error_messages.append(str(e))

            end_time = time.time()
            duration = end_time - start_time

            # 打印测试结果
            print(f"\n充值压力测试:")
            print(f"总充值次数: {len(recharge_amounts)}")
            print(f"并发数: {concurrent_recharges}")
            print(f"成功数: {success_count}")
            print(f"成功率: {success_count/len(recharge_amounts)*100:.2f}%")
            print(f"总耗时: {duration:.2f}秒")
            if test_user in mock_users_db:
                print(f"最终余额: {mock_users_db[test_user]['remain']}")
            if error_messages:
                print(f"错误信息: {', '.join(list(set(error_messages)))}")

            assert success_count == len(recharge_amounts), "部分充值失败"

# ------------------------------
# 测试 3: 脚本执行压力（保持不变）
# ------------------------------
def test_script_execution_stress():
    """测试脚本执行压力"""
    script_executions = 100
    concurrent_executions = 15
    
    def execute_test_script(index):
        d_veriable.clear()
        set_statement(f"test_var_{index}", f"value_{index}")
        return d_veriable.get(f"test_var_{index}") == f"value_{index}"
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=concurrent_executions) as executor:
        futures = [executor.submit(execute_test_script, i) for i in range(script_executions)]
        
        success_count = 0
        for future in as_completed(futures):
            if future.result():
                success_count += 1
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n脚本执行压力测试:")
    print(f"总执行次数: {script_executions}")
    print(f"并发数: {concurrent_executions}")
    print(f"成功数: {success_count}")
    print(f"成功率: {success_count/script_executions*100:.2f}%")
    print(f"总耗时: {duration:.2f}秒")
    
    assert success_count == script_executions

if __name__ == "__main__":
    pytest.main(["-v", "test_stress.py"])