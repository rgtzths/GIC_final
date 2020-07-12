import cherrypy
import docker
import os
from pysnmp.hlapi import *
from influxdb import InfluxDBClient
import datetime
import threading
import time

os.environ["DOCKER_HOST"]="tcp://10.2.0.1:2375"
client=docker.from_env()

nginx_replicas = 2
router_replicas = 2

services = {}

sem = threading.Semaphore()

def insert_snmp_values():
    global services
    global sem
    oids = [
        ("SNMPv2-MIB", "sysUpTime", 0, "sys_uptime"),
        ("UCD-SNMP-MIB", "ssIOSent", 0,"io_sent"),
        ("UCD-SNMP-MIB", "ssIOReceive", 0, "io_received"),
        ("UCD-SNMP-MIB", "ssCpuUser", 0, "cpu_user"),
        ("UCD-SNMP-MIB", "ssCpuSystem", 0, "cpu_system"),
        ("UCD-SNMP-MIB", "ssCpuIdle", 0, "cpu_idle"),
        ("UCD-SNMP-MIB", "memTotalReal", 0, "total_mem"),
        ("UCD-SNMP-MIB", "memAvailReal", 0, "mem_available"),
        ("UCD-SNMP-MIB", "memTotalFree", 0, "mem_free"),
        ("UCD-SNMP-MIB", "dskTotal", 1, "total_disk"),
        ("UCD-SNMP-MIB", "dskUsed", 1, "disk_used"),
        ("UCD-SNMP-MIB", "dskAvail", 1, "disk_used"),
        ("UCD-SNMP-MIB", "dskPercent", 1, "disl_percent")
    ]
    client = InfluxDBClient(host='10.5.0.115', port=8086, database='telegraf')
    while True:
        json_body = []
        sem.acquire()
        for service in services:
            try:
                measurement = {"measurement":"snmp", "tags": {"host": service}, "time": str(datetime.datetime.now())}
                fields = {}
                errorIndication, errorStatus, errorIndex, varBinds = next(
                    getCmd(SnmpEngine(),
                        CommunityData('gicgirs', mpModel=0),
                        UdpTransportTarget((services[service], 161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oids[0][0], oids[0][1], oids[0][2])),
                        ObjectType(ObjectIdentity(oids[1][0], oids[1][1], oids[1][2])),
                        ObjectType(ObjectIdentity(oids[2][0], oids[2][1], oids[2][2])),
                        ObjectType(ObjectIdentity(oids[3][0], oids[3][1], oids[3][2])),
                        ObjectType(ObjectIdentity(oids[4][0], oids[4][1], oids[4][2])),
                        ObjectType(ObjectIdentity(oids[5][0], oids[5][1], oids[5][2])),
                        ObjectType(ObjectIdentity(oids[6][0], oids[6][1], oids[6][2])),
                        ObjectType(ObjectIdentity(oids[7][0], oids[7][1], oids[7][2])),
                        ObjectType(ObjectIdentity(oids[8][0], oids[8][1], oids[8][2])),
                        ObjectType(ObjectIdentity(oids[9][0], oids[9][1], oids[9][2])),
                        ObjectType(ObjectIdentity(oids[10][0], oids[10][1], oids[10][2])),
                        ObjectType(ObjectIdentity(oids[11][0], oids[11][1], oids[11][2])),
                        ObjectType(ObjectIdentity(oids[12][0], oids[12][1], oids[12][2])))
                )

                if errorIndication:
                    print(errorIndication)
                elif errorStatus:
                    print('%s at %s' % (errorStatus.prettyPrint(),
                                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                else:
                    for idx, varBind in enumerate(varBinds):
                        fields[oids[idx][3]] = int(str(varBind[1]))

                measurement["fields"] = fields
                json_body.append(measurement)

            except Exception as e:
                print(e)
                #print("Erro no Ip", services[service])
        sem.release()
        client.write_points(json_body)
        print("Dados SNMP Enviados")
        print(services)
        time.sleep(60)

@cherrypy.expose
class SnmpMonitorAndTriggerGenerator(object):

    def dockerScaleBServiceUp(self, service):
        global nginx_replicas
        global router_replicas
        serviceName="easyAppointments_"+service
        dockerService=client.services.get(serviceName)
        if service == "nginx-proxy":
            if(dockerService.scale(nginx_replicas+1)):
                print("Service "+ service + " scaled up with success. Replicas:", nginx_replicas)
                nginx_replicas += 1
            else:
                print("Service Not Scaled")
        else:
            if(dockerService.scale(router_replicas+1)):
                print("Service "+ service + " scaled up with success. Replicas:", router_replicas)
                router_replicas += 1
            else:
                print("Service Not Scaled")


    def dockerScaleServiceDown(self, service):
        global nginx_replicas
        global router_replicas
        serviceName="easyAppointments_"+service
        dockerService=client.services.get(serviceName)
        if service == "nginx-proxy":
            if nginx_replicas > 2 and  dockerService.scale(nginx_replicas-1):
                print("Service "+ service+" scaled down with success. Replicas:", nginx_replicas)
                nginx_replicas -= 1
            else:
                print("Service Not Scaled")
        else:
            if router_replicas > 2 and dockerService.scale(router_replicas-1):
                print("Service "+ service+" scaled down with success. Replicas:", router_replicas)
                router_replicas -= 1
            else:
                print("Service Not Scaled")

    def updateServices(self, service_name, ip):
        global sem
        sem.acquire()
        if service_name == "easyAppointments_mysql-server-1":
            services["ea-mysql-server1"] = ip
        elif service_name == "easyAppointments_mysql-server-2":
            services["ea-mysql-server2"] = ip
        elif service_name == "easyAppointments_mysql-server-3":
            services["ea-mysql-server3"] = ip
        elif service_name == "easyAppointments_mysql-router":
            services["ea-mysql-router"] = ip
        elif service_name == "easyAppointments_application1":
            services["ea-app1"] = ip
        elif service_name == "easyAppointments_application2":
            services["ea-app2"] = ip
        elif service_name == "easyAppointments_nginx-proxy":
            services["ea-nginx-proxy"] = ip
        else:
            print("Não foi introduzido em lado nenhum")
        sem.release()

    @cherrypy.expose
    def monitor(self, service=None):
        service_name = service.split(".")[0]
        ip = cherrypy.request.remote.ip
        self.updateServices(service_name, ip)

    @cherrypy.expose
    def scale(self, service, value):
        if int(value) == 1:
            self.dockerScaleBServiceUp(service)
        else:
            self.dockerScaleServiceDown(service)


if __name__ == '__main__':
    x = threading.Thread(target=insert_snmp_values)
    x.start()
    cherrypy.server.socket_host = '10.5.0.115'
    cherrypy.config.update({'server.socket_port': 9000})
    cherrypy.quickstart(SnmpMonitorAndTriggerGenerator(), '/')
