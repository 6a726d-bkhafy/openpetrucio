#!/bin/bash

# Instalação de pacotes
yum install -y python3
yum install -y python3-pip
pip3 install virtualenv
yum install -y git
yum install -y mariadb-server
systemctl start mariadb

# Criação do ambiente virtual e instalação do Django
mkdir -p /etc/petrucio/venv
virtualenv /etc/petrucio/venv
source /etc/petrucio/venv/bin/activate
pip3 install django
django-admin startproject core

# Transferência do diretório do GitHub para o servidor ainda n configurada

# Instalação de pacotes adicionais do Django
yum install -y mariadb-devel
pip3 install mysqlclient
pip3 install django-crispy-forms
pip3 install mysql-connector-python==8.0.17
pip3 install paramiko
pip3 install pysnmp
