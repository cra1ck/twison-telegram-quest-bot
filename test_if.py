import re

test_dict = {'var':'3'}

def operations(text, test_dict):
    var_pattern = r'<<if\s+\$(\w*)\s*.*?>>'
    op_pattern = r'<<if\s+\$\w*\s+(.*?)\s.*?>>'
    val_pattern = r'<<if\s+\$\w*\s+.*?\s(.*?)>>'
    var_list = re.findall(var_pattern, text)
    op_list = re.findall(op_pattern, text)
    val_list = re.findall(val_pattern, text)
    ##verification
    try:
        if(op_list[0] == 'eq'):
            for name in test_dict.items():
                if(var_list[0] == name[0]):
                    if(name[1] == val_list[0]):
                        return True
    except:
        return None
    return False

def if_else(text):
    i = 0
    a = 0
    b = 0
    ex = []
    tmp = text
    for match in re.finditer(r'<<if.*?>>|<<else>>|<</if>>', tmp):
        if(re.fullmatch(r'<<if.*?>>', match[0])):
            i = i + 1
            if(i == 1):
                a = match.start()
        elif(match[0] == '<</if>>'):
            i = i - 1
        if(i == 0):
            b = match.end()
            break
    return tmp[a:b]




text = 'Каждый охотник <<if $var eq 3>>знает где<<if $var eq 3>>  сидит фазан<<if $var eq 3>> или ещё кого-то<</if>><</if>> сидит курочка <</if>>, а хочет есть<<if $var eq 3>>, например оленины <</if>>nigga'

def macro(text):
    while if_else(text):
        if(not operations(if_else(text), test_dict)):
            tmp = text.split(if_else(text))
            text = ''.join(tmp)
            return text
        res_list = text.split(if_else(text))
        res_list.append(res_list[1])
        res_list[1] = if_else(text)
        res_list[1] = re.sub(r'<<if.*?>>', '', res_list[1], 1)
        res_list[1] = re.sub(r'<</if>>', '', res_list[1], 1)
        text = ''.join(res_list)
    return text

while if_else(text):
    text = macro(text)

print(text)
