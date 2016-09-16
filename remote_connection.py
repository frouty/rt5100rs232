#with this script you can
#execute a command

import paramiko

ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh_client.connect('localhost', username='lof', password='lof')
except paramiko.SSHException:
    print "connection failed"
    quit()
stdin,stdout,stderr=ssh_client.exec_command('ls /etc/')

for line in stdout.readlines():
    print line.strip()


sftp_client = ssh_client.open_sftp()
sftp_file = sftp_client.open('/var/log/Xorg.0.log')
for i,line in enumerate(sftp_file):
    print "{}:{}".format(i,line[:15])
    if i >=9:
        break
sftp_file.close()
sftp_client.close()

ssh_client.close()