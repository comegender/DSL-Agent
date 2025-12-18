MODE = 3

def set_mode(x):
    global MODE
    MODE = x

def get_mode():
    return MODE

f = open("./脚本语言设计.md", "r", encoding='utf-8').read()
s=f.split('### ')[8:]
d1={}
de1={}
d2={}
de2={}
d3={}
de3={}

for i in range(len(s)):
    s[i]=s[i].split("```")

for i in s:
    d1[i[0].strip()]=i[1][9:]
    
for i in d1:
    ss = d1[i].split(' ')
    de1[ss[1]]=d1[i]

f=open("./hospital.script", "r", encoding='utf-8').read()
s=f.split('#')
for i in range(len(s)):
    s[i] = s[i].strip()
    ss=s[i].split(' ')
    de2[ss[1]]=s[i]
d2["挂号"]=de2["register_patient"]
d2["查询"]=de2["query_info"]
d2["取消"]=de2["cancel_registration"]
d2["退出"]=de2["exit"]
d2["默认"]=de2["default"]
f=open("./restaurant.script", "r", encoding='utf-8').read()
s=f.split('#')
for i in range(len(s)):
    s[i] = s[i].strip()
    ss=s[i].split(' ')
    de3[ss[1]]=s[i]
d3["点餐"]=de3["order_food"]
d3["菜单"]=de3["show_menu"]
d3["结账"]=de3["checkout"]
d3["帮助"]=de3["help_info"]
d3["退出"]=de3["exit"]
d3["默认"]=de3["default"]


def get_script(name):
    if MODE==1:
        d=d1
    elif MODE==2:
        d=d2
    elif MODE==3:
        d=d3
    return d.get(name, "")

def get_script_en(name):
    if MODE==1:
        de=de1
    elif MODE==2:
        de=de2
    elif MODE==3:
        de=de3
    return de.get(name, "")