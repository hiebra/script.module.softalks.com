import os
if os.name == 'posix' and (pydev := os.getenv('PYDEVD')):
    import ast
    import traceback
    try:
        pydev = ast.literal_eval(pydev)
        port = pydev.get('port', 5678)
        try:
            import subprocess
            subprocess.check_call(f'nc -vz localhost 5678'.split())
            try:
                import sys
                if 'pydevd.py' not in subprocess.check_output(f'ps -p {os.getpid()} -o args='.split()).decode('utf-8'):
                    sys.path.append(f'{pydev["eclipse path"]}/plugins/org.python.pydev.core_{pydev["version"]}/pysrc')
                    import pydevd  # @UnresolvedImport
                    pydevd.settrace()
                    print('Remote debugging session started. Press F8 for jumping to the first user defined breakpoint or F6 for debugging from the import statement loading this module')
            except:
                traceback.print_exc()
        except:
            pass
    except:
        traceback.print_exc()        