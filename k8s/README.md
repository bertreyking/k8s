- [x] master 节点初始化配置及安装
- [x] worker 节点初始化配置及接入
- [x] dashboard 配置 （部署后，chrome无法打开，火狐可以，下附解决方法）
- [x] kubectl 命令tab补全
- [x] etcd Example hardware configurations
- [x] metrics-server_to yaml-dir
- [x] kubectl 只读权限访问cluster
- [x] docker&kk8s_shell使用
- [x] [k8s_api_1.18](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#-strong-api-overview-strong-)
- [x] [ks8_api_1.19](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#-strong-api-overview-strong-)

1. kubectl 命令tab补全
```
rpm -qa | grep bash-completion
yum install -y bash-completion
source /usr/share/bash-completion/bash_completion
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
```
2. dashboard （chrome 无法打开 dashboard）[参考链接](https://github.com/kubernetes/dashboard/issues/2947)

```
- 原因： 浏览器配置不允许使用自签名证书，因为yaml所创建dashboard的secrets中没有证书信息，最终导致无法正常访问
# mkdir /certs

# openssl req -nodes -newkey rsa:2048 -keyout /certs/dashboard.key -out /certs/dashboard.csr -subj "/C=/ST=/L=/O=/OU=/CN=kubernetes-dashboard"

# openssl x509 -req -sha256 -days 365 -in /certs/dashboard.csr -signkey /certs/dashboard.key -out /certs/dashboard.crt

# kubectl create secret generic kubernetes-dashboard-certs --from-file=/certs -n kubernetes-dashboard

# kubectl describe secret kubernetes-dashboard-certs -n kubernetes-dashboard

# kubectl describe secret kubernetes-dashboard-certs -n kubernetes-dashboard                                         
Name:         kubernetes-dashboard-certs
Namespace:    kubernetes-dashboard
Labels:       <none>
Annotations:  <none>
Type:  Opaque
Data
====
dashboard.csr:  907 bytes
dashboard.key:  1704 bytes
dashboard.crt:  1005 bytes

- 另外我的环境需要手动删除下kubernetes-dashboard pod 才可以通过chrome正常访问
```
3. etcd hardware configurations (aws/gce为例)[etcd](https://etcd.io/docs/v3.4.0/op-guide/hardware/#example-hardware-configurations)
```
- Medium cluster
A medium cluster serves fewer than 500 clients, fewer than 1,000 of requests per second, and stores no more than 500MB of data.
Example application workload: A 250-node Kubernetes cluster
注意etcd中，v2的key-value 要比v3 占用更多的计算资源，可以适当进行调整
``` 
| Provider | Type | vCPUs | Memory(GB) | Max concurrent IOPSM | Disk bandwidth(MB/s) |
| -------- | ---- | ----- | ---------- | -------------------- | -------------------- |
| AWS | m4.xlarge | 4 | 16 | 6000 | 93.75 |
| GCE | n1-standard-4 + 150GB PD SSD | 4 | 15 | 4500 | 75 |

4. kubectl 只读权限访问集群
```
- 创建serviceaccount
kubectl create sa test-view
- 创建clusterrole(clusterrole后面使用rolebing和sa关联起来)
kubectl create -f test-view.yaml
- 查看test-view 所对应的tocken(secretName)
kubectl get sa test-view -o json | jq -Mr '.secrets[].name'
- 获取tocken并使用base64转换
kubectl get secrets test-view-token-5n7z4 -o json | jq -Mr '.data.token' | base64 -d
- curl 进行验证tocken的正确性及上面clusterrole的权限是否正确
curl -k https://10.6.x.x:6443/api/v1/nodes -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6Im1hd2VpYmluZy12aWV3LXRva2VuLTVuN3o0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Im1hd2VpYmluZy12aWV3Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiMDRjMjg5M2MtYWZkOS0xMWVhLWExNjYtMDI0MmFjMTIwMDAzIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6bWF3ZWliaW5nLXZpZXcifQ.dFdWY8NrQVvhGJ0JoOmL_px7WEKPEYWJ_Sf5nElkFiOV3uWCHG7OW4x3o4t9HunzsAF7XVUyU9wnr6NTo2iHz_0sQ7cChTyQGSiF1O-MP5L-U_hEszLq0toNW3VDSJj3ZfaRfS0evX4qP_xk0BYiatleTezDj9R0qab3RPXKQXHPmHV40CkIebftjjuTj63NtJAqG6Y7Y8Af1ZwFVhYOGQgks5Owttvz0l0O9hAI21gNfwcauOdESarOfyGgyKGIsAJh_-fC-tcLDtFzCQhk6xwFbeMzpSyVCSGwubQXKUY7rhDiHTx3-YKIJ5lr1XvVQjJ6XU7ycpqq3UhxyklAl8LcrNs2H8XohqplCXXS0SVeV6u8jF3lK63wI-_WcHjlLlVsOKX4yyksXeDUGPuMG8e6Oz-Ae8vSMFK2mvsdLJRsP8GO1-whnvyjEDUZOkFtRoffTZbr1qYHHAMQZRUajKAGTN8-2La9VqpsgDnITFkHU6SsZjZ9qUOKklbhY5oshGXl5X5pJd5j0L3XKW0mtiDN2MKNhiNuY0oLnhrVQCOaK-qmT_pbNuBq7yYHNq7urYuDEvTtP90SDzdOXaIgxup7fdswGQ1DIMtPDRex-yexy1VXXfnxgeXNGFESnBqxcHmB5mLgmwoUvXXLL5vsX90LU_ICb24xAlB6-kr-QHQ" | jq
- 查看get pod请求详细信息
kubectl get pods --v=6
- kubeconfig 中分三部分内容
  cluster: 对应k8s集群
  context: 对应cluster、namespaces、serviceaccout(承上启下)
  preferences: 用户
- 创建一个test-view 的context(对应集群apiserver)
kubectl config set-cluster test-view --server=https://10.6.x.x:6443 --insecure-skip-tls-verify=true
- 创建一个用户及用tocken方式访问集群
kubectl config set-credentials test-view --token="eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6Im1hd2VpYmluZy12aWV3LXRva2VuLTVuN3o0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Im1hd2VpYmluZy12aWV3Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiMDRjMjg5M2MtYWZkOS0xMWVhLWExNjYtMDI0MmFjMTIwMDAzIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6bWF3ZWliaW5nLXZpZXcifQ.dFdWY8NrQVvhGJ0JoOmL_px7WEKPEYWJ_Sf5nElkFiOV3uWCHG7OW4x3o4t9HunzsAF7XVUyU9wnr6NTo2iHz_0sQ7cChTyQGSiF1O-MP5L-U_hEszLq0toNW3VDSJj3ZfaRfS0evX4qP_xk0BYiatleTezDj9R0qab3RPXKQXHPmHV40CkIebftjjuTj63NtJAqG6Y7Y8Af1ZwFVhYOGQgks5Owttvz0l0O9hAI21gNfwcauOdESarOfyGgyKGIsAJh_-fC-tcLDtFzCQhk6xwFbeMzpSyVCSGwubQXKUY7rhDiHTx3-YKIJ5lr1XvVQjJ6XU7ycpqq3UhxyklAl8LcrNs2H8XohqplCXXS0SVeV6u8jF3lK63wI-_WcHjlLlVsOKX4yyksXeDUGPuMG8e6Oz-Ae8vSMFK2mvsdLJRsP8GO1-whnvyjEDUZOkFtRoffTZbr1qYHHAMQZRUajKAGTN8-2La9VqpsgDnITFkHU6SsZjZ9qUOKklbhY5oshGXl5X5pJd5j0L3XKW0mtiDN2MKNhiNuY0oLnhrVQCOaK-qmT_pbNuBq7yYHNq7urYuDEvTtP90SDzdOXaIgxup7fdswGQ1DIMtPDRex-yexy1VXXfnxgeXNGFESnBqxcHmB5mLgmwoUvXXLL5vsX90LU_ICb24xAlB6-kr-QHQ"
- 创建一个context，并将用户和集群关联起来
kubectl config set-context test-view --cluster=test-view --user=test-view
- 查看当前所对应的context(集群)
kubecctl config current-context
- 切换到test-view
kubectl config use-context test-view
- 查看test-view.yaml中所有的资源类型
for x in `cat test-view.yaml  | grep resources -A 17 |awk -F "-" '{print $2}' | sed 's/"/ /g'`;do kubectl get $x --all-namespaces;done
```
5. docker&k8s_shell使用区别-[K8s_Command and Arguments](https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes)
```
- 如果要覆盖docker-image中默认的 Entrypoint 与 Cmd，需要遵循如下规则：
- 如果在yaml配置中没有设置 command 或者 args，那么将使用 Docker 镜像自带的命令及其参数
- 如果在yaml配置中只设置了 command 但是没有设置 args，那么容器启动时只会执行该命令， Docker 镜像中自带的命令及其参数会被忽略
- 如果在yaml配置中只设置了 args，那么 Docker 镜像中自带的命令会使用该新参数作为其执行时的参数
- 如果在yaml配置中同时设置了 command 与 args，那么 Docker 镜像中自带的命令及其参数会被忽略。 容器启动时只会执行配置中设置的命令，并使用配置中设置的参数作为命令的参数
```
6. 执行kubectl get 所有资源类型报错 You must be logged in to the server (Unauthorized) 
```
- 可以执行 kubectl cofnig view 查看kubeconfig
user 那行提示相关key已被删除

- 谁动了你的，kubeconfigfile
- cp /etc/kubernetes/admin.conf /root/.kube/config  直接进行修复
```
