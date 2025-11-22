import backend.yacc as yacc
import backend.AI_api as AI_api

user_input = input("请输入您的问题或需求：")

yacc.print_tree(user_input)