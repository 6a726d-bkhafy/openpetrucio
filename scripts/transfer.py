import mysql.connector

from mysql.connector import Error

class Converter(mysql.connector.conversion.MySQLConverter):

    def row_to_python(self, row, fields):
        row = super(Converter, self).row_to_python(row, fields)

        def to_unicode(col):
            if isinstance(col, bytearray):
                return col.decode('utf-8')
            return col

        return[to_unicode(col) for col in row]

try:
    con_proxy=mysql.connector.connect(converter_class=Converter,host='192.168.1.113',database='petrucio_db',user='transfer',password='Gtq62fp@31415')
    con_ptr=mysql.connector.connect(host='localhost',database='petrucio_db',user='petrucio',password='Gtq62fp@31415')
    cursor_proxy=con_proxy.cursor()
    cursor_ptr=con_ptr.cursor()
    
    cursor_proxy.execute('select host,mac_1,mac_2,ip,dns,uplink,type,emp from main;')
    line=cursor_proxy.fetchall()
    list_host=[]
    list_mac1=[]
    list_mac2=[]
    list_ip=[]
    list_dns=[]
    list_uplink=[]
    list_type=[]
    list_emp=[]
    for i in line:
        list_host.append(str(i[0]))
        list_mac1.append(str(i[1]))
        list_mac2.append(str(i[2]))
        list_ip.append(str(i[3]))
        list_dns.append(str(i[4]))
        list_uplink.append(str(i[5]))
        list_type.append(str(i[6]))
        list_emp.append(str(i[7]))

    for host,mac1,mac2,ip,dns,uplink,typeid,emp in zip(list_host,list_mac1,list_mac2,list_ip,list_dns,list_uplink,list_type,list_emp):
        cursor_ptr.execute('insert into pages_hosts (ip,hostname,host_type,mac_1,mac_2,uplink,dns,empresa,office,os) values ('+"'"+ip+"'"+','+"'"+host+"'"+','+"'"+typeid+"'"+','+"'"+mac1+"'"+','+"'"+mac2+"'"+','+"'"+uplink+"'"+','+"'"+dns+"'"+','+"'"+emp+"'"+','+"'"+'-'+"'"+','+"'"+'-'+"'"+');')
        con_ptr.commit()

except Error as e:
    print('erro com mysql.connector: ',e)