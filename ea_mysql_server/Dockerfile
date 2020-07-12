FROM oraclelinux:7-slim

ARG MYSQL_SERVER_PACKAGE=mysql-community-server-minimal-8.0.20
ARG MYSQL_SHELL_PACKAGE=mysql-shell-8.0.20

# Install server
RUN yum install -y https://repo.mysql.com/mysql-community-minimal-release-el7.rpm \
      https://repo.mysql.com/mysql-community-release-el7.rpm \
  && yum-config-manager --enable mysql80-server-minimal \
  && yum install -y \
      $MYSQL_SERVER_PACKAGE \
      $MYSQL_SHELL_PACKAGE \
      libpwquality \
  && yum clean all \
  && mkdir /docker-entrypoint-initdb.d

RUN yum install -y wget
RUN wget https://dl.influxdata.com/telegraf/releases/telegraf-1.14.5-1.x86_64.rpm
RUN yum install -y telegraf-1.14.5-1.x86_64.rpm

COPY scripts/docker-entrypoint.sh /entrypoint.sh

COPY scripts/healthcheck.sh /healthcheck.sh

ENTRYPOINT ["/entrypoint.sh"]
HEALTHCHECK CMD /healthcheck.sh

CMD ["mysqld"]
