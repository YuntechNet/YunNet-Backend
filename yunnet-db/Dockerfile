FROM mariadb:10.4.6-bionic

ENV MYSQL_ROOT_PASSWORD dev

EXPOSE 3306

COPY schema.sql /docker-entrypoint-initdb.d/schema.sql
