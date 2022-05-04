import re
## Macro to set variables
#  return dict with names and values of variables
#

def macro_set(text):
    var = {}
    text = ''.join(text.split()) ## remove all spaces
    set_pattern = '<<set\$\w*=\w*>>'
    match = re.findall(set_pattern, text)
    name = []
    value = []
    name_pattern = '\$\w*'
    value_pattern = '=\w*'
    for i in range(len(match)):
        tmp_name = re.findall(name_pattern, match[i])
        tmp_value = re.findall(value_pattern, match[i])
        name.append(str(tmp_name[0][1:]))
        value.append(str(tmp_value[0][1:]))
        var[name[i]] = value[i]
    return var

## Macro to print values of variables inside the text
#  return string
#
def macro_print(text, var):
    var_name = []
    pattern = '<<print\s*\$\w*>>'
    match = re.findall(pattern, text)
    tmp = re.findall(pattern, text)
    tmp = ''.join(tmp)
    tmp = re.findall(r'\$\w*', tmp)
    for i in range(len(match)):
        var_name.append(str(tmp[i][1:]))
        pattern = f'<<print\s*\${var_name[i]}\s*>>'
        result = re.sub(pattern, var.get(var_name[i]), text)
        text = result
    return text

