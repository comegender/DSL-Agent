f = open("./脚本语言设计.md", "r", encoding='utf-8').read()
s=f.split('### ')[8:]
d={}
de={}

for i in range(len(s)):
    s[i]=s[i].split("```")

for i in s:
    d[i[0].strip()]=i[1][9:]
    
for i in d:
    ss = d[i].split(' ')
    de[ss[1]]=d[i]

def get_script(name):
    return d.get(name, "")

def get_script_en(name):
    return de.get(name, "")