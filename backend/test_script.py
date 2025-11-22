f = open("./脚本语言设计.md", "r", encoding='utf-8').read()
s=f.split('### ')[9:]
d={}

for i in range(len(s)):
    s[i]=s[i].split("```")

for i in s:
    d[i[0].strip()]=i[1][9:]

def get_script(name):
    return d.get(name, "")
