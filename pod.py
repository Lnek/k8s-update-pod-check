#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import random
import time

LOG_FILE = "tmp.log"


def write_file(file_name, value):
    with open("./" + file_name, "a") as file:
        file.write(value)


def create_pod(filename):
    cmd = 'kubectl apply -f ./' + filename
    write_file(LOG_FILE, str(time.time()) + " " + os.popen(cmd).read())


def delete_pod(pod_name):
    cmd = "kubectl delete po " + pod_name
    write_file(LOG_FILE, str(time.time()) + " " + os.popen(cmd).read())


def get_pod(pod_name):
    cmd = "kubectl get po " + pod_name + " -o wide"
    write_file(LOG_FILE, str(time.time()) + " " + os.popen(cmd).read())


def loop_cmd():
    filename = str(random.randrange(2 << 32))
    podname = "test-nginx-" + filename
    config = "apiVersion: v1 \n\
kind: Pod\n\
metadata:\n\
  name: " + podname + "\n\
  labels:\n\
    app: nginx\n\
spec:\n\
  containers:\n\
  - name: nginx\n\
    image: nginx:1.7.9\n\
    ports:\n\
    - containerPort: 80"
    write_file(filename, config)
    create_pod(filename)
    time.sleep(random.randrange(10))
    os.remove("./" + filename)
    get_pod(podname)
    delete_pod(podname)


# TODO: deployment 通过service name
def export_deployment_service(deployment_name):
    cmd = "kubectl expose deploment " + deployment_name + " --type=NodePort --name=example-service"
    write_file(LOG_FILE, str(time.time()) + " " + os.popen(cmd).read())


def get_node_port():
    cmd = "kubectl describe services example-service"
    ack = os.popen(cmd).read()
    for i in ack.split('\n'):
        print(i)

def create_by_deployment():
    filename = "nginx-deployment"
    # podname = "nginx"
    config = "apiVersion: apps/v1\n\
kind: Deployment\n\
metadata:\n\
  name: nginx-deployment\n\
spec:\n\
  selector:\n\
    matchLabels:\n\
      app: nginx\n\
  replicas: 2\n\
  template:\n\
    metadata:\n\
      labels:\n\
        app: nginx\n\
    spec:\n\
      containers:\n\
      - name: nginx\n\
        image: nginx:1.7.9\n\
        ports:\n\
        - containerPort: 80"
    write_file(filename, config)
    create_pod(filename)
    os.remove("./" + filename)


def main():
    while True:
        loop_cmd()

main()