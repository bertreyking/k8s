1. 镜像文件 [下载链接](https://github.com/bertreyking/repos/releases)
```
docker load -i dashboard-v2.0.0-beta8.tar.gz
docker load -i metrics-scraper-v1.0.2.tar.gz
```
2. dashboard_yaml文件
```
- yaml 中已包含service account 及 clusterrole 等资源，无需重新创建
- 原文件不支持nodePort，仅做了支持nodePort访问的修改
```
3. dashboard （chrome 无法打开 dashboard）[参考链接](https://github.com/kubernetes/dashboard/issues/2947)
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

[k8s for dashboard](https://github.com/kubernetes/dashboard)

[参考blog](https://www.replex.io/blog/how-to-install-access-and-add-heapster-metrics-to-the-kubernetes-dashboard)
