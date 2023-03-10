import os
import com.softalks.debuggable  # @UnusedImport
import subprocess
from subprocess import Popen, PIPE

wrotten = 0
delimiter = ' '
encodedDelimiter = '_!_'
encoding = 'utf-8'
pipe = None

def get(*commands, singleton=True):

    def encode(command):
        return command.group(1).replace(' ', encodedDelimiter)

    def encoded(command):
        import re
        command = re.sub('"([^"]*)"', encode, command)
        return command

    def decoded(command):
        command = command.split()
        tokens = []
        for token in command:
            tokens.append(token.replace(encodedDelimiter, ' '))
        return tokens

    def check_output(command):
        command = decoded(command)
        output = subprocess.check_output(command, stdin=pipe)
        lines = output.splitlines()
        result = []
        for line in lines:
            result.append(line.decode(encoding))
        if len(result) == 1 and singleton:
            return result[0]
        return result

    chain = []
    for command in commands:
        chain.append(encoded(command))
    length = len(chain)
    if (length == 1):
        return check_output(chain[0])
    for i in range(length):
        command = chain[i]
        if (i == length - 1):
            return check_output(command)
        else:
            command = decoded(command)
            global pipe
            pipe = Popen(command, stdin=pipe, stdout=PIPE).stdout

def lines(*commands):
    return get(*commands, singleton=False)

    
def paging():
    from os import getppid
    ppid = getppid()
    siblings = lines(f'ps -o ppid= -o args -A', f'awk "$1 == {ppid}{{print $2}}"')
    for sibling in siblings:
        if (sibling == 'more' or sibling.startswith('more ')):
            return True
    return False

tty = get(f'ps -p {os.getpid()} -o tty=')
if tty.startswith('tty'):
    columns = int(get('tput cols'))
    static = True
elif tty == '?':
    columns = 120
    static = True
else:
    static = False
    
def write(value, **parameters):
    '''
    :note: dasdfadf
    :summary: te cagas 
    :param value:
    '''
    if static:
        global columns
    else:
        columns = int(get('tput cols'))
    value = str(value)
    length = len(value)
    global wrotten
    needed = length if wrotten == 0 else length + len(delimiter)
    if columns - wrotten < needed:
        value = f'\n{value}'
        wrotten = length
    elif wrotten > 0:
        value = delimiter + value
        wrotten += length + 1
    else:
        wrotten += length
    print(value, end='', **parameters)