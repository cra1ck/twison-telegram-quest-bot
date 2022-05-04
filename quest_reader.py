import json

print("Input quest name:")
input_file = str(input())
with open(input_file, "r") as read_file:
    data = json.load(read_file)


print('Quest name:', data['name'], '\n')
pid = 1
current_scene = pid - 1

while True:

    message = data['passages'][current_scene]['text']
    message = message.partition('[')[0]
    print(message, '\n')

    n = 0
    try:
        for n in range(len(data['passages'][current_scene]['links'])):
            print(n + 1, data['passages'][current_scene]['links'][n]['name'])
    except KeyError:
        print('Game over!')
        break

    print('\n')
    while True:
        choice = int(input())
        try:
            print('\n')
            #print(data['passages'][current_scene]['links'][choice-1]['pid'])
            pid = int(data['passages'][current_scene]['links'][choice-1]['pid'])
            break
        except IndexError:
            continue
    current_scene = pid - 1

input()
