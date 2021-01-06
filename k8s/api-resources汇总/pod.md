# pod
- 什么是pod
pod是kubernetes中，可创建及管理的最小单元，一个pod中可以有多个containers，containers之间共享同一个网络命名空间、存储,以及在yaml中其他的声明，如:dnsPloicy,就是spec.[]所有同层级的配置都会在多个容器间保持一致

- 启动一个pod
```
vi pod.yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: centos-app
  labels:
    app: centos-app
  namespace: default #可不写默认就是default
spec:
  containers:
  - name: pod-app
    image: centos-ulimit:1.1
    command: ["/bin/sh"]
    args: ["-c", "sh /etc/startup.sh"]
---
kubectl app-ly -f pod.yaml
```
