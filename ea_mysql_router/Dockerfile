FROM oraclelinux:7-slim

ARG KEY=https://repo.mysql.com/RPM-GPG-KEY-mysql
ARG REPO=https://repo.mysql.com

ARG MYSQL_SERVER_PACKAGE_URL=$REPO/yum/mysql-8.0-community/docker/x86_64/mysql-community-server-minimal-8.0.12-1.el7.x86_64.rpm
ARG MYSQL_ROUTER_PACKAGE_URL=$REPO/yum/mysql-tools-community/el/7/x86_64/mysql-router-8.0.12-1.el7.x86_64.rpm

RUN rpmkeys --import $KEY \
    && yum install -y \
      $MYSQL_SERVER_PACKAGE_URL \
      $MYSQL_ROUTER_PACKAGE_URL \
    && yum clean all

RUN yum install -y wget
RUN wget https://dl.influxdata.com/telegraf/releases/telegraf-1.14.5-1.x86_64.rpm
RUN yum install -y telegraf-1.14.5-1.x86_64.rpm

COPY /scripts/entrypoint.sh /run.sh

ENTRYPOINT ["/run.sh"]
HEALTHCHECK \
	CMD mysqladmin --port 6446 --protocol TCP ping 2>&1 | grep Access || exit 1
CMD ["mysqlrouter"]
