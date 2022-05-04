import re


text = '<<set $gold=100>>\n<<set $infl = 10>>\n'
print(f'Not formated text:\n{text}')

text = ''.join(text.split())
print(f'Formated text:\n{text}\n')

set_pattern = "<<set\$\w*=\w*>>"
match = re.findall(set_pattern, text)
print(f'FIND IN TEXT:\n{match}')

var = {}

names = []
name_pattern = "\$\w*"
for i in range(len(match)):
    name = (re.findall(name_pattern, match[i]))
    names.append(str(name[0])[1:])
print(f'VAR:\n{names}')
value = []
val_pattern = "=\w*"
for i in range(len(match)):
    val = re.findall(val_pattern, match[i])
    value.append(str(val[0])[1:])
print(f'VAL:\n{value}')

for i in range(len(match)):
    var[names[i]] = value[i]
print(f'RESULT: {var}')


## print some variables
#
#
def print_macro(text):
    pattern = '<<print\s*\$\w*>>'
    var_name = str((re.findall(r'\$\w*', text))[0][1:])
    result = re.sub(pattern, var.get(var_name), text)
    return result

text = 'I have <<print $infl>> golden coins'
print(print_macro(text))


