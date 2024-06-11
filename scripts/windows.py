import subprocess

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output, error

computer_ips = ['endereço_IP_1', 'endereço_IP_2', ...]
share_name = 'compartilhamento'
username = 'nome_de_usuario'
password = 'senha'
output_dir = '/etc/petrucio/office'
output_file = output_dir + '/result.txt'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(output_file, 'w') as file:
    for computer_ip in computer_ips:
        print(f'Consultando o registro em {computer_ip}...')

        smb_command = f'smbclient //{computer_ip}/{share_name} -U {username}%{password} -c "reg query \\"HKLM\\\\Software\\\\Microsoft\\\\Windows NT\\\\CurrentVersion\\" /v \\"ProductName\\";quit"'
        output, error = run_command(smb_command)
        output = output.decode('utf-8')

        file.write(f'Resultado da consulta de registro em {computer_ip}:\n{output}\n')

with open(output_file, 'r') as file:
    print(file.read())
