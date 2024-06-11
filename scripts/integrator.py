import mysql.connector
import subprocess
import paramiko
import time

from mysql.connector import Error

try:
    con_proxy=mysql.connector.connect(host='192.168.1.113',database='proxy_db',user='alpha',password='Gtq62fp@31415')
    con_ptr=mysql.connector.connect(host='localhost',database='petrucio_db',user='petrucio',password='Gtq62fp@31415')
    cursor_proxy=con_proxy.cursor()
    cursor_ptr=con_ptr.cursor()
    cursor_proxy.execute('select hostname,mac_1,mac_2,id,host_type from main;')
    line=cursor_proxy.fetchall()
    list_hostname_proxy=[]
    list_mac1_proxy=[]
    list_mac2_proxy=[]
    list_id_proxy=[]
    list_type_proxy=[]
    for i in line:
        list_hostname_proxy.append(i[0])
        list_mac1_proxy.append(i[1])
        list_mac2_proxy.append(i[2])
        list_id_proxy.append(str(i[3]))
        list_type_proxy.append(i[4])
    cursor_ptr.execute('select id,hostname,mac_1,mac_2,ip,uplink,host_type from pages_hosts;')
    line=cursor_ptr.fetchall()
    list_id_ptr=[]
    list_hostname_ptr=[]
    list_mac1_ptr=[]
    list_mac2_ptr=[]
    list_ip_ptr=[]
    list_uplink_ptr=[]
    list_type_ptr=[]
    for i in line:
        list_id_ptr.append(str(i[0]))
        list_hostname_ptr.append(i[1])
        list_mac1_ptr.append(i[2])
        list_mac2_ptr.append(i[3])
        list_ip_ptr.append(i[4])
        list_uplink_ptr.append(i[5])
        list_type_ptr.append(i[6])
    for mac in list_mac1_proxy:
        if mac not in list_mac1_ptr:
            cursor_proxy.execute('delete from main where mac_1='+"'"+mac+"'"+';')
            con_proxy.commit()
    for hostname_ptr,mac1_ptr,mac2_ptr,ip_ptr,uplink_ptr,id_ptr,type_ptr in zip(list_hostname_ptr,list_mac1_ptr,list_mac2_ptr,list_ip_ptr,list_uplink_ptr,list_id_ptr,list_type_ptr):
        if (mac1_ptr not in list_mac1_proxy):
            cursor_proxy.execute('insert into main (hostname,mac_1,mac_2,status,id,host_type) values ('+"'"+hostname_ptr+"'"+','+"'"+mac1_ptr+"'"+','+"'"+mac2_ptr+"'"+',0,'+id_ptr+','+"'"+type_ptr+"'"+');')
            con_proxy.commit()
        else:
            for hostname_proxy,mac1_proxy,mac2_proxy,id_proxy,type_proxy in zip(list_hostname_proxy,list_mac1_proxy,list_mac2_proxy,list_id_proxy,list_type_proxy):
                if mac1_ptr==mac1_proxy:
                    if hostname_ptr!=hostname_proxy or mac2_ptr!=mac2_proxy or id_ptr!=id_proxy or type_ptr!=type_proxy:
                        cursor_proxy.execute('update main set hostname='+"'"+hostname_ptr+"'"+',mac_2='+"'"+mac2_ptr+"'"+',id='+id_ptr+',host_type='+"'"+type_ptr+"'"+' where mac_1='+"'"+mac1_ptr+"'"+';')
                        con_proxy.commit()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.1.113", username="root", password="Gtq62fp@31415")
    stdin, stdout, stderr = ssh.exec_command("python3 /etc/petrucio_proxy/petrucio_proxy.py")
    stdout.readlines()
    stdout.channel.close()
    exit_status = stdout.channel.recv_exit_status()
    ssh.close()


    cursor_proxy.execute('select mac_1,mac_2,ip,uplink,status from main;')      
    line=cursor_proxy.fetchall()  
    list_mac1_proxy=[]
    list_mac2_proxy=[]
    list_ip_proxy=[]
    list_uplink_proxy=[]
    list_status_proxy=[]
    for i in line:
        list_mac1_proxy.append(i[0])
        list_mac2_proxy.append(i[1])
        list_ip_proxy.append(i[2])
        list_uplink_proxy.append(str(i[3]))
        list_status_proxy.append(i[4])
    for mac1_proxy,mac2_proxy,ip_proxy,uplink_proxy,status_proxy in zip(list_mac1_proxy,list_mac2_proxy,list_ip_proxy,list_uplink_proxy,list_status_proxy):
        for mac1_ptr,mac2_ptr,ip_ptr,uplink_ptr in zip(list_mac1_ptr,list_mac2_ptr,list_ip_ptr,list_uplink_ptr):
            if mac1_proxy==mac1_ptr and status_proxy==1:
                if ip_proxy!=ip_ptr or uplink_proxy!=uplink_ptr:
                    cursor_ptr.execute('update pages_hosts set ip='+"'"+ip_proxy+"'"+',uplink='+"'"+uplink_proxy+"'"+' where mac_1='+"'"+mac1_ptr+"'"+';')
    
    cursor_proxy.execute('select ip,mac,dns,scan_time from unknow;')
    line=cursor_proxy.fetchall()
    list_ip=[]
    list_mac=[]
    list_dns=[]
    list_scan=[]
    for i in line:
        list_ip.append(i[0])
        list_mac.append(i[1])
        list_dns.append(i[2])
        list_scan.append(i[3])
    cursor_ptr.execute('delete from pages_unknow where mac=mac')
    con_ptr.commit()
    for ip,mac,dns,scan in zip(list_ip,list_mac,list_dns,list_scan):
        cursor_ptr.execute('insert into pages_unknow (ip,mac,dns,scan_time) values ('+"'"+ip+"'"+','+"'"+mac+"'"+','+"'"+dns+"'"+','+"'"+scan+"'"+');')
        con_ptr.commit()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.1.113", username="root", password="Gtq62fp@31415")
    stdin, stdout, stderr = ssh.exec_command("source /etc/petrucio_proxy/venv/bin/activate && python3 /etc/petrucio_proxy/snmp.py")
    exit_status = stdout.channel.recv_exit_status()

    stdout.channel.close()
    ssh.close()

    time.sleep(50)

    if exit_status == 0:
        cursor_proxy.execute('select switch_id,port,hostname,ip,mac_1 from switch;')
        line = cursor_proxy.fetchall()
        list_id = []
        list_port = []
        list_host = []
        list_ip = []
        list_mac = []
        for i in line:
            list_id.append(str(i[0]))
            list_port.append(str(i[1]))
            list_host.append(i[2])
            list_ip.append(i[3])
            list_mac.append(i[4])
        cursor_ptr.execute('delete from pages_switch where mac_1=mac_1')
        con_ptr.commit()
        for id_proxy, port, host, ip, mac in zip(list_id, list_port, list_host, list_ip, list_mac):
            cursor_ptr.execute('insert into pages_switch (switch_id,port,hostname,ip,mac_1) values ('+id_proxy+','+port+','+"'"+host+"'"+','+"'"+ip+"'"+','+"'"+mac+"'"+');')
            con_ptr.commit()

    cursor_ptr.execute('select uplink,mac_1 from pages_hosts;')
    line=cursor_ptr.fetchall()
    list_uplink_hosts=[]
    list_mac_hosts=[]
    for i in line:
        list_uplink_hosts.append(i[0])
        list_mac_hosts.append(i[1])
    cursor_ptr.execute('select port,mac_1,switch_id from pages_switch;')
    line=cursor_ptr.fetchall()
    list_uplink_sw=[]
    list_mac_sw=[]
    list_id_sw=[]
    for i in line:
        list_uplink_sw.append(i[0])
        list_mac_sw.append(i[1])
        list_id_sw.append(i[2])
    for uplink_sw,mac_sw,id_sw in zip(list_uplink_sw,list_mac_sw,list_id_sw):
        for uplink_hosts,mac_hosts in zip(list_uplink_hosts,list_mac_hosts):
            if mac_sw==mac_hosts:
                query="select hostname from pages_hosts where id={}".format(id_sw)
                cursor_ptr.execute(query)
                line=cursor_ptr.fetchall()
                for i in line:
                    sw_name=i[0]
                uplink_desc="{} | Port {}".format(sw_name,uplink_sw)
                query="update pages_hosts set uplink='{}' where mac_1='{}';".format(uplink_desc,mac_hosts)
                cursor_ptr.execute(query)
                con_ptr.commit()

except Error as e:
    print('Error not expected for mysql.connector: ',e)
