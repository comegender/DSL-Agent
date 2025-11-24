from . import yacc
from . import function_interface as fi

d_veriable = {}

def do_statement(body):
    for i in body:
        if i['type'] == 'set_statement':
            set_statement(i['left'], i['right'])
        elif i['type'] == 'speak_statement':
            speak_statement(i['message'])
        elif i['type'] == 'jump_statement':
            jump_statement(i['target'])
        elif i['type'] == 'if_statement':
            if_statement(i['condition'], i['then'], i['else'])
        elif i['type'] == 'call_statement':
            call_statement(i['function'])
        
def call_statement(func_name):
    if func_name == 'getOriginalPassword':
        return fi.getOriginalPassword(d_veriable.get('userName', ''))
    elif func_name == 'AI_Interface':
        s = fi.AI_Interface(d_veriable.get('userInput', ''))
        for i in s:
            body = i['body']
            do_statement(body)
    elif func_name == 'judgePassword':
        return fi.judgePassword(d_veriable.get('userName', ''), d_veriable.get('newPassword', ''))
    elif func_name == 'getUserInformation':
        return fi.getUserInformation(d_veriable.get('userName', ''))
    elif func_name == 'Recharge':
        return fi.Recharge(d_veriable.get('userName', ''), d_veriable.get('recharge_money', 0))
    elif func_name == 'printUserInformation':
        return fi.printUserInformation(d_veriable.get('output', ''))
    elif func_name == 'printRemain':
        return fi.printRemain(d_veriable.get('userName', ''))
    elif func_name == 'Login':
        return fi.Login(d_veriable.get('userName', ''), d_veriable.get('passWord', ''))
    elif func_name == 'Register':
        return fi.Register(d_veriable.get('subUserName', ''), d_veriable.get('subPassWord', ''), d_veriable.get('subPassWord2', ''))
    elif func_name == 'isLogin':
        return fi.isLogin()
    elif func_name == 'writeCA':
        return fi.writeCA(d_veriable.get('userName', ''),d_veriable.get('complaint', ''),d_veriable.get('advice', ''))
    elif func_name == 'EX':
        fi.EX()

def set_statement(var_name, value):
    if type(value) is dict and value.get('type') == 'call_statement':
        value = call_statement(value['function'])
    elif value == '@content@':
        value = fi.getUserInput()
    elif value == '@money@':
        value = float(fi.getUserInput())
    d_veriable[var_name] = value

def speak_statement(message):
    print("🤖："+message)

def jump_statement(target):
    result = yacc.jump_to(target)
    for i in result:
        do_statement(i['body']) 

def if_statement(condition, then_block, else_block):
    if type(condition) is str:
        condition_met = d_veriable.get(condition, False)
    else:
      left = condition['left']
      operation = condition['operation']
      right = condition['right']

      condition_met = False
      if operation == '==':
          condition_met = (d_veriable.get(left) == right)
      elif operation == '!=':
          condition_met = (d_veriable.get(left) != right)
      elif operation == '>':
          condition_met = (d_veriable.get(left) > right)
      elif operation == '<':
          condition_met = (d_veriable.get(left) < right)
      elif operation == '>=':
          condition_met = (d_veriable.get(left) >= right)
      elif operation == '<=':
          condition_met = (d_veriable.get(left) <= right)

    if condition_met:
        do_statement(then_block)
    else:
        do_statement(else_block)

