from pysnmp.hlapi import *
import os
import xml.etree.ElementTree as et
import mysql.connector
from mysql.connector import Error
import socket

def snmp_get(host, community, oid):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)))
        )

        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            else:
                for varBind in varBinds:
                    port=(' = '.join([x.prettyPrint() for x in varBind]))
                    return port

def host_verify(list_port_db,list_host_db,list_ip_db,list_mac_db,list_id_db,sw_id,port,host,ip,mac,list_mac):
    for port_db,host_db,ip_db,mac_db,id_db in zip(list_port_db,list_host_db,list_ip_db,list_mac_db,list_id_db):
        if port_db==port:
            if mac_db not in list_mac:
                query="delete from switch where port='{}' and switch_id='{}';".format(port,sw_id)
                cursor.execute(query)
                con.commit()
            if host_db!=host or ip_db!=ip or mac_db!=mac:
                query="update switch set hostname='{}',ip='{}',mac_1='{}' where port='{}' and switch_id='{}';".format(host,ip,mac,port,sw_id)
                cursor.execute(query)
                con.commit()

con=mysql.connector.connect(host='localhost',database='proxy_db',user='root',password='Gtq62fp@31415')
cursor=con.cursor()

file=et.parse('/etc/petrucio_proxy/scan.xml')
root=file.getroot()
list_attrib=[]
for i in root.iter('address'):
    list_attrib.append(i.attrib)
counter=0
list_mac_range=[]
list_ip_range=[]
for attrib in list_attrib:
    if counter%2==0:
        ip_attrib=str(attrib)
        ip_attrib=ip_attrib.split("'")
        list_ip_range.append(ip_attrib[3])
    else:
        mac_attrib=str(attrib)
        mac_attrib=mac_attrib.split("'")
        list_mac_range.append(mac_attrib[3])
    counter+=1
while len(list_ip_range)>len(list_mac_range):
        list_ip_range.pop()
list_mac=[]
list_host=[]
list_ip=[]
for mac in list_mac_range:
    query="select hostname,ip,mac_1 from main where mac_1='{}' or mac_2='{}';".format(mac,mac)
    cursor.execute(query)
    line=cursor.fetchall()
    for i in line:
        list_host.append(i[0])
        list_ip.append(i[1])
        list_mac.append(i[2])
for mac,ip in zip(list_mac_range,list_ip_range):
    if mac not in list_mac:
        list_host.append('UNKNOW')
        list_ip.append(ip)
        list_mac.append(mac)

list_mac_dec=[]
list_1=[]
list_2=[]
for mac in list_mac:
    mac = mac.split(':')
    for hexa in mac:
        dec = int(hexa, 16)
        list_2.append(str(dec))
    mac_dec = '.'.join(list_2)
    list_mac_dec.append(mac_dec)
    list_2 = []

try:
    cursor.execute("select mac_1 from main where host_type='FIREWALL';")
    line=cursor.fetchall()
    for i in line:
        mac_fw=(i[0])
    cursor.execute("select id,ip from main where host_type='SWITCH';")
    line=cursor.fetchall()
    list_sw_ip=[]
    list_sw_id=[]
    for i in line:
        list_sw_ip.append(i[1])
        list_sw_id.append(i[0])
    cursor.execute("select mac_1 from main where host_type='ACCESS POINT';")
    line=cursor.fetchall()
    list_ap_mac_1=[]
    for i in line:
        list_ap_mac_1.append(i[0])
    list_downlink=[]
    list_uplink=[]
    for sw_ip,sw_id in zip(list_sw_ip,list_sw_id):
        print(sw_ip)
        list_port=[]
        list_port_2=[]
        list_port_sw=[]
        list_ap_ip=[]
        list_ap_host=[]
        list_ap_mac=[]
        list_port_ap=[]
        list_port_out=[]
        try:
            for i in list_mac_dec:
                if __name__ == '__main__':
                    host = sw_ip
                    community = 'FRO'
                    oid = '1.3.6.1.2.1.17.7.1.2.2.1.2.1.'+i
                    timeout=5
                    socket.setdefaulttimeout(timeout)
                    port_snmp=snmp_get(host, community, oid)
                    port_snmp=port_snmp.split('=')
                    list_port_2.append(port_snmp[1])
            for i in list_port_2:
                result=i.lstrip()
                list_port.append(result)
            query="select port,hostname,ip,mac_1,switch_id from switch where switch_id='{}';".format(sw_id)
            cursor.execute(query)
            line=cursor.fetchall()
            list_port_db=[]
            list_host_db=[]
            list_ip_db=[]
            list_mac_db=[]
            list_id_db=[]
            for i in line:
                list_port_db.append(i[0])
                list_host_db.append(i[1])
                list_ip_db.append(i[2])
                list_mac_db.append(i[3])
                list_id_db.append(i[4])
            list_id_up=[]
            list_port_up=[]
            list_uplink_in=[]
            for port,mac in zip(list_port,list_mac):
                if mac==mac_fw:
                    port_up=port
            list_sw_port=[]
            for port,host,ip,mac in zip(list_port,list_host,list_ip,list_mac):
                counter=list_port.count(port)
                if counter==1:
                    if mac not in list_mac_db:
                        query="insert into switch (switch_id,port,hostname,ip,mac_1) values ('{}','{}','{}','{}','{}');".format(sw_id,port,host,ip,mac)
                        cursor.execute(query)
                        con.commit()
                    else:
                        host_verify(list_port_db,list_host_db,list_ip_db,list_mac_db,list_id_db,sw_id,port,host,ip,mac,list_mac)
                elif (port!=port_up) and (ip in list_sw_ip) and (port!='No Such Instance currently exists at this OID'):
                    query="select mac_1 from switch where switch_id='{}';".format(sw_id)
                    cursor.execute(query)
                    line=cursor.fetchall()
                    list_mac_sw=[]
                    for i in line:
                        list_mac_sw.append(i[0])
                    if mac not in list_mac_sw:
                        query="insert into switch (switch_id,port,hostname,ip,mac_1) values ({},{},'{}','{}','{}');".format(sw_id,port,host,ip,mac)
                        cursor.execute(query)
                        con.commit()
                    else:
                        host_verify(list_port_db,list_host_db,list_ip_db,list_mac_db,list_id_db,sw_id,port,host,ip,mac,list_mac)
                    list_sw_port.append(mac)
                    list_port_sw.append(port)
                
                elif (port!=port_up) and (mac in list_ap_mac_1) and (port!='No Such Instance currently exists at this OID'):
                    query="select ip,hostname from main where mac_1='{}';".format(mac)
                    cursor.execute(query)
                    line=cursor.fetchall()
                    for i in line:
                        list_ap_ip.append(i[0])
                        list_ap_host.append(i[1])
                    list_ap_mac.append(mac)
                    list_port_ap.append(port)
                elif port!=port_up and (port!='No Such Instance currently exists at this OID'):
                    list_port_out.append(port)
                print(list_ap_host)
                print(list_port_out)
            
            for port,host,ip,mac in zip(list_port_ap,list_ap_host,list_ap_ip,list_ap_mac):
                if port not in list_port_sw:
                    if mac not in list_mac_sw:
                        query="insert into switch (switch_id,port,hostname,ip,mac_1) values ({},{},'{}','{}','{}');".format(sw_id,port,host,ip,mac)
                        cursor.execute(query)
                        con.commit()
                    else:
                        query="update switch set port={},hostname='{}',ip='{}',mac_1='{}' where switch_id={};".format(port,host,ip,mac,sw_id)
                        cursor.execute(query)
                        con.commit()
            
            list_hub=[]
            for i in list_port_out:
                if (i not in list_port_sw) and (i not in list_port_ap) and (i not in list_hub):
                    list_hub.append(i)
            for port in list_hub:
                if port not in list_port_db:
                    query="insert into switch (switch_id,port,hostname,ip,mac_1) values ({},{},'HUB','-','-');".format(sw_id,port)
                    cursor.execute(query)
                    con.commit() 
                else:
                    query="update switch set hostname='HUB',ip='-',mac_1='-' where switch_id={} and port={};".format(sw_id,port)
                    cursor.execute(query)
                    con.commit()
            
            list_uplink_in.append(port_up)
            list_uplink_in.append(sw_id)
            list_uplink.append(list_uplink_in)
            list_sw_port.append(sw_id)
            list_downlink.append(list_sw_port)

        except socket.timeout:
            continue 
        except:
            continue

    
    list_downlink=sorted(list_downlink,key=len,reverse=True)
    for list_sw in list_downlink:
        up_id=list_sw[-1]
        list_sw.pop()
        print(list_downlink)
        if list_downlink==[]:
            continue
        query='select hostname,ip,mac_1 from main where id={};'.format(up_id)
        cursor.execute(query)
        line=cursor.fetchall()
        for i in line:
            hostname=i[0]
            ip=i[1]
            mac=i[2]
        for i in list_sw:
            query="select id from main where mac_1='{}' or mac_2='{}';".format(i,i)
            cursor.execute(query)
            line=cursor.fetchall()
            for i in line:
                sw_id=i[0]
            for i in list_uplink:
                port=i[0]
                sw_id_2=i[1]
                if sw_id==sw_id_2:
                    query="select mac_1 from switch where switch_id='{}';".format(sw_id)
                    cursor.execute(query)
                    line=cursor.fetchall()
                    list_mac_sw=[]
                    for i in line:
                        list_mac_sw.append(i[0])
                    if mac not in list_mac_sw:
                        query="insert into switch (switch_id,port,hostname,ip,mac_1) values ({},{},'{}','{}','{}');".format(sw_id,port,hostname,ip,mac)
                        cursor.execute(query)
                        con.commit()
                    else:
                        query="update switch set hostname='{}',ip='{}',mac_1='{}' where switch_id={} and port={};".format(hostname,ip,mac,sw_id,port)
                        cursor.execute(query)
                        con.commit()


except Error as e:
    print(e)

