import paramiko
import random
import string

# данные для подключения по SSH
hostname = 'your_hostname'
port = 22
username = 'username'

# Сгенерировать случайный пароль из 12 символов
new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Вывести пароль на экран
print("Новый пароль:", new_password)


password = 'old_password\n'
new_pass = new_password + '\n'

#процесс смены пароля пользователя
cmd = 'passwd'
prompts = [password, new_pass, new_pass]

with paramiko.SSHClient() as client:
    try:
        client.load_system_host_keys()
        client.connect(hostname, port, username, password.strip())
    except paramiko.ssh_exception.SSHException:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, password.strip())

    stdin, stdout, stderr = client.exec_command('passwd')

    for prompt in prompts:
        stdin.write(prompt)
    stdin.flush()

    stdout.channel.set_combine_stderr(True)
    print(stdout.read().decode())
