import mysql.connector
from mysql.connector import Error
from . import AI_api as ai
from . import yacc

ISLOGIN = False

def getUserInput():
    userinput = input("👤：")
    return userinput

def getOriginalPassword(username):
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='AI',
            password='123456',
            database='your_database'
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if not result:
            print(f"用户 {username} 不存在，无法获取密码")
            return None

        return result['password']

    except Exception as e:
        print(f"数据库错误: {e}")
        return None

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

def AI_Interface(x):
    r = ai.get_response(x)
    return yacc.get_tree(r)

def judgePassword(username, new_password):
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='AI',
            password='123456',
            database='your_database'
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if not result:
            print(f"用户 {username} 不存在，无法判断密码")
            return False

        original_password = result['password']

        return new_password == original_password

    except Error as e:
        print(f"数据库错误: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

def getUserInformation(username):
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='AI',
            password='123456',
            database='your_database'
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT username, remain FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if not result:
            print(f"用户 {username} 不存在，无法获取用户信息")
            return None

        return {
            'username': result['username'],
            'ramain': result['remain']
        }

    except Exception as e:
        print(f"数据库错误: {e}")
        return None

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

def Recharge(username, x):

    if not isinstance(x, (int, float)):
        print(f"错误：充值金额必须是数字，但传入的是 {type(x)} 类型")
        return False


    if isinstance(x, int):
        x = float(x)
    else:
        if isinstance(x, float):
            x_str = "{:.10f}".format(x).rstrip('0').rstrip('.') if '.' in "{:.10f}".format(x) else str(x)
            if '.' in x_str:
                decimal_part = x_str.split('.')[1]
                if len(decimal_part) > 2:
                    print(f"错误：充值金额小数位不能超过两位，但传入的是 {x}（小数位有 {len(decimal_part)} 位）")
                    return False

    x = float(x)

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='AI',
            password='123456',
            database='your_database'
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT username, balance FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if not result:
            print(f"错误：用户 '{username}' 不存在，无法充值")
            return False

        current_balance = result['balance']


        new_balance = current_balance + x

        cursor.execute("UPDATE users SET balance = %s WHERE username = %s", (new_balance, username))

        connection.commit()

        return True

    except Error as e:
        print(f"数据库错误: {e}")
        if connection is not None and connection.is_connected():
            connection.rollback()
        return False

    except Exception as e:
        print(f"未知错误: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
        
def printUserInformation(output):
    print("🤖：用户信息如下：")
    print(f"用户名: {output['username']}")
    print(f"余额: {output['ramain']} 元")

def printRemain(username):
    import mysql.connector
    from mysql.connector import Error

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='AI',
            password='123456',
            database='your_database'
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT username, balance FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if not result:
            print(f"错误：用户 '{username}' 不存在，无法获取余额")
            return

        remain = result['balance']
        print(f"🤖:用户 {username} 的余额为：{remain}")

    except Error as e:
        print(f"数据库错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

def Login(username, password):

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='AI',
            password='123456',
            database='your_database'
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if not result:
            print(f"🤖:登录失败：用户 '{username}' 不存在")
            return False

        stored_password = result['password']

        if password == stored_password:
            global ISLOGIN
            ISLOGIN = True
            return True
        else:
            print(f"🤖:登录失败：用户 '{username}' 密码错误")
            return False

    except Error as e:
        print(f"数据库错误: {e}")
        return False
    except Exception as e:
        print(f"未知错误: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

def Register(sub_username, sub_password, sub_password_2):
    import mysql.connector
    from mysql.connector import Error

    if sub_password != sub_password_2:
        print("🤖:注册失败：两次输入的密码不一致")
        return False

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='AI',
            password='123456',
            database='your_database'
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT username FROM users WHERE username = %s", (sub_username,))
        existing_user = cursor.fetchone()

        if existing_user:
            print(f"🤖:注册失败：用户名 '{sub_username}' 已存在，请选择其他用户名")
            return False

        insert_query = """
        INSERT INTO users (username, password, balance)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (sub_username, sub_password, 0))  # 余额初始化为 0

        connection.commit()
        print(f"🤖:注册成功：用户 '{sub_username}' 已创建")
        return True

    except Error as e:
        print(f"数据库错误: {e}")
        if connection is not None and connection.is_connected():
            connection.rollback()
        return False
    except Exception as e:
        print(f"未知错误: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

def isLogin():
    global ISLOGIN
    return ISLOGIN

def writeCA(username, complaint, advice):
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='AI',
            password='123456',
            database='your_database'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO complaints (username, complaint, advise)
                VALUES (%s, %s, %s)
            """

            record = (username, complaint, advice)
            cursor.execute(insert_query, record)

            connection.commit()

    except Error as e:
        print(f"数据库操作出错: {e}")

    finally:
        # 5. 关闭游标和连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def EX():
    print("🤖:感谢使用，再见！")
    import sys
    sys.exit(0)