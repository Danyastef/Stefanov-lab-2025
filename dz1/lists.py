n = int(input())
result = []
commands = []
if n < 1:
    print('Error')
else:
    for i in range(n):
        command = input().strip()
        commands.append(command)
    for command in commands:
        command = command.split(' ')
        if command[0] == 'insert':
            if 0 <= int(command[1]) <= len(result):
                result.insert(int(command[1]), int(command[2]))
            else:
                print('Error')
                break
        elif command[0] == 'print':
            print(result)
        elif command[0] == 'remove':
            if int(command[1]) in result:
                result.remove(int(command[1]))
            else:
                print('Error')
                break
        elif command[0] == 'append':
            result.append(int(command[1]))
        elif command[0] == 'sort':
            result.sort()
        elif command[0] == 'pop':
            if result:
                result.pop()
            else:
                print('Error')
                break
        elif command[0] == 'reverse':
            result.reverse()
        else:
            print('Error')
            break