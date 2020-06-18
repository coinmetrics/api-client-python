from datetime import datetime

with open('setup_template.py') as setup_py_file:
    setup_py_content = setup_py_file.read()

now = datetime.now()
setup_py_content = setup_py_content.replace('2020.01.01.00.00.00', f'{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}')

with open('setup.py', 'w') as setup_py_file:
    setup_py_file.write(setup_py_content)
