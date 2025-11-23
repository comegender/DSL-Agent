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
        return fi.getOriginalPassword()
    elif func_name == 'getUserInput':
        return fi.getUserInput()
    elif func_name == 'AI_Interface':
        return fi.AI_Interface()
    elif func_name == 'judgePassword':
        return fi.judgePassword()
    elif func_name == 'getUserInformation':
        return fi.getUserInformation()
    elif func_name == 'Recharge':
        return fi.Recharge()

def set_statement(var_name, value):
    if type(value) is dict and value.get('type') == 'call_statement':
        value = call_statement(value['function'])
    elif value == '@content@':
        value = fi.getUserInput()
    elif value == '@money@':
        value = float(fi.getUserInput())
    d_veriable[var_name] = value

def speak_statement(message):
    print("🤖:"+message)

def jump_statement(target):
    result = yacc.jump_to(target)
    # print(result)
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

