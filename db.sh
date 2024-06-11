MYSQL_ROOT_PASSWORD=<senha_do_usuario_root_do_MySQL>
MYSQL_DATABASE_NAME=petrucio_db
MYSQL_USER_NAME=petrucio
MYSQL_USER_PASSWORD=<senha_do_usuario_petrucio>

#Executar os comandos do MySQL
mysql -u root -p${MYSQL_ROOT_PASSWORD} <<EOF
CREATE DATABASE ${MYSQL_DATABASE_NAME};
CREATE USER ${MYSQL_USER_NAME}@localhost IDENTIFIED BY '${MYSQL_USER_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE_NAME}.* TO ${MYSQL_USER_NAME}@localhost;
FLUSH PRIVILEGES;
EOF

echo "Comandos do MySQL concluídos."