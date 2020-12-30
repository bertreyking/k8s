1. kubectl 命令tab补全

```
rpm -qa | grep bash-completion
yum install -y bash-completion
source /usr/share/bash-completion/bash_completion
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
```
2. kubectl 上下文切换
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
3. kubectl 查询资源报错  You must be logged in to the server (Unauthorized) 
```
- 可以执行 kubectl cofnig view 查看kubeconfig
user 那行提示相关key已被删除

- 谁动了你的，kubeconfigfile
- cp /etc/kubernetes/admin.conf /root/.kube/config  直接进行修复
```
