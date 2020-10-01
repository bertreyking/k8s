# Helm_Install
# [JFrog_ChartCenter](https://chartcenter.io/)
# [Helm Hub](https://hub.helm.sh/charts/)

1. 下载helm介质
```
wget https://get.helm.sh/helm-v3.0.2-linux-amd64.tar.gz
```

2. 配置helm
```
tar -zxvf helm-v3.0.2-linux-amd64.tar.gz -C /root && cd /root/helm/302/linux-amd64
mv helm /usr/local/bin/helm
```

3. 部署tiller-仅供参考（如果将tiller部署k8s集群中，那么tiiler将获取k8s的cluster-admin权限，有一定安全隐患。我们考虑将tiller部署在本地节点中。即 tillerless）
```
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl apply -f tiller.yaml
```

4. 在本地节点部署tillerless (个人感觉就是 centos yum源部署在 http/ftp上，所有节点repo文件指向http/ftp yum install即可)
```
[root@k8s-master01 ~]# helm plugin install https://github.com/rimusz/helm-tiller
Installed plugin: tiller
[root@k8s-master01 ~]# helm plugin list 
NAME    VERSION DESCRIPTION                                       
tiller  0.9.3   Start a Tiller server locally, aka Tillerless Helm

By default, the default directories depend on the Operating System. The defaults are listed below:
+------------------+---------------------------+--------------------------------+-------------------------+
| Operating System | Cache Path                | Configuration Path             | Data Path               |
+------------------+---------------------------+--------------------------------+-------------------------+
| Linux            | $HOME/.cache/helm         | $HOME/.config/helm             | $HOME/.local/share/helm |
| macOS            | $HOME/Library/Caches/helm | $HOME/Library/Preferences/helm | $HOME/Library/helm      |
| Windows          | %TEMP%\helm               | %APPDATA%\helm                 | %APPDATA%\helm          |
+------------------+---------------------------+--------------------------------+-------------------------+

[root@k8s-master01 ~]# cd $HOME/.local/share/helm
[root@k8s-master01 helm]# ls -l 
total 0
drwxr-xr-x. 2 root root 25 Jan 20 17:05 plugins
[root@k8s-master01 helm]# cd plugins/
[root@k8s-master01 plugins]# ls -l 
total 0
lrwxrwxrwx. 1 root root 61 Jan 20 17:05 helm-tiller -> /root/.cache/helm/plugins/https-github.com-rimusz-helm-tiller
```

5. 使用helm
```
- helm 查看帮助信息
输出较多，不做展示

- 查看当前的chart 仓库
[root@k8s-master01 ~]# helm repo list 
NAME    URL                                              
stable  https://kubernetes-charts.storage.googleapis.com/

- 添加一个微软的chart仓库
[root@k8s-master01 ~]# helm repo add azure http://mirror.azure.cn/kubernetes/charts/
"stable" has been added to your repositories
[root@k8s-master01 ~]# helm repo list
NAME            URL                                                
stable          https://kubernetes-charts.storage.googleapis.com/ 
azure           http://mirror.azure.cn/kubernetes/charts/

- 删除一个chart 仓库
[root@k8s-master01 ~]# helm repo remove stable
"stable" has been removed from your repositories

- 更新现有repo
[root@k8s-master01 ~]# helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "azure" chart repository
Update Complete. ⎈ Happy Helming!⎈

- helm search repo 查看prometheus相关的chart
[root@k8s-master01 ~]# helm search repo | grep prometheus
stable/helm-exporter                    0.3.2           0.4.0                   Exports helm release stats to prometheus          
stable/prometheus                       10.3.1          2.15.2                  Prometheus is a monitoring system and time seri...
stable/prometheus-adapter               2.0.1           v0.5.0                  A Helm chart for k8s prometheus adapter           
stable/prometheus-blackbox-exporter     2.0.0           0.15.1                  Prometheus Blackbox Exporter                      
stable/prometheus-cloudwatch-exporter   0.5.0           0.6.0                   A Helm chart for prometheus cloudwatch-exporter   
stable/prometheus-consul-exporter       0.1.4           0.4.0                   A Helm chart for the Prometheus Consul Exporter   
stable/prometheus-couchdb-exporter      0.1.1           1.0                     A Helm chart to export the metrics from couchdb...
stable/prometheus-mongodb-exporter      2.4.0           v0.10.0                 A Prometheus exporter for MongoDB metrics         
stable/prometheus-mysql-exporter        0.5.2           v0.11.0                 A Helm chart for prometheus mysql exporter with...
stable/prometheus-nats-exporter         2.3.0           0.6.0                   A Helm chart for prometheus-nats-exporter         
stable/prometheus-node-exporter         1.8.1           0.18.1                  A Helm chart for prometheus node-exporter         
stable/prometheus-operator              8.5.11          0.34.0                  Provides easy monitoring definitions for Kubern...
stable/prometheus-postgres-exporter     1.2.0           0.8.0                   A Helm chart for prometheus postgres-exporter     
stable/prometheus-pushgateway           1.2.13          1.0.1                   A Helm chart for prometheus pushgateway           
stable/prometheus-rabbitmq-exporter     0.5.5           v0.29.0                 Rabbitmq metrics exporter for prometheus          
stable/prometheus-redis-exporter        3.2.1           1.0.4                   Prometheus exporter for Redis metrics             
stable/prometheus-snmp-exporter         0.0.4           0.14.0                  Prometheus SNMP Exporter                          
stable/prometheus-to-sd                 0.3.0           0.5.2                   Scrape metrics stored in prometheus format and ...

- helm search repo 查看prometheus chart的详细信息
[root@k8s-master01 ~]# helm show chart stable/prometheus-operator
apiVersion: v1
appVersion: 0.34.0
dependencies:
- condition: kubeStateMetrics.enabled
  name: kube-state-metrics
  repository: https://kubernetes-charts.storage.googleapis.com/
  version: 2.6.*
- condition: nodeExporter.enabled
  name: prometheus-node-exporter
  repository: https://kubernetes-charts.storage.googleapis.com/
  version: 1.8.*
- condition: grafana.enabled
  name: grafana
  repository: https://kubernetes-charts.storage.googleapis.com/
  version: 4.3.*
description: Provides easy monitoring definitions for Kubernetes services, and deployment
  and management of Prometheus instances.
home: https://github.com/coreos/prometheus-operator
icon: https://raw.githubusercontent.com/prometheus/prometheus.github.io/master/assets/prometheus_logo-cb55bb5c346.png
keywords:
- operator
- prometheus
maintainers:
- name: vsliouniaev
- name: bismarck
- email: gianrubio@gmail.com
  name: gianrubio
name: prometheus-operator
sources:
- https://github.com/coreos/kube-prometheus
- https://github.com/coreos/prometheus-operator
- https://coreos.com/operators/prometheus
version: 8.5.11

- 使用helm 部署datadog
[root@k8s-master01 ~]# helm install azure/datadog --generate-name
NAME: datadog-1579446795
LAST DEPLOYED: Sun Jan 19 23:13:18 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
DataDog agents are spinning up on each node in your cluster. After a few
minutes, you should see your agents starting in your event stream:

    https://app.datadoghq.com/event/stream

- 查看datadog是否部署完成
[root@k8s-master01 ~]# kubectl get all -A  | grep -i datadog    
default                pod/datadog-1579446795-ffw98                                 0/1     ContainerCreating   0          2m23s
default                pod/datadog-1579446795-kube-state-metrics-6988b89c88-4ntnx   0/1     ContainerCreating   0          2m23s
default                pod/datadog-1579446795-pcjmn                                 0/1     ContainerCreating   0          2m23s
default                pod/datadog-1579446795-s985x                                 0/1     ContainerCreating   0          2m23s
default                pod/datadog-1579446795-vk6gp                                 0/1     ContainerCreating   0          2m23s

- 查看log说明在下载镜像，说明helm安装datadog完成
kubectl describe pods datadog-1579446795-ffw98
Events:
  Type    Reason     Age        From                   Message
  ----    ------     ----       ----                   -------
  Normal  Scheduled  <unknown>  default-scheduler      Successfully assigned default/datadog-1579446795-ffw98 to k8s-worker01
  Normal  Pulling    6m59s      kubelet, k8s-worker01  Pulling image "datadog/agent:7"
  
 - 查看安装的list
 [root@k8s-master01 ~]# helm list 
NAME                    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
datadog-1579446795      default         1               2020-01-19 23:13:18.886203327 +0800 CST deployed        datadog-1.39.2  7 

- 卸载datadog
[root@k8s-master01 ~]# helm uninstall datadog-1579446795
release "datadog-1579446795" uninstalled
```

# 参考链接

- [helm官方文档](https://v3.helm.sh/docs/intro/install/)
- [the server could not find the requested resource](https://github.com/helm/helm/issues/6374)
- [chart仓库](https://github.com/BurdenBear/kube-charts-mirror)
- [tillerless](https://medium.com/faun/helm-basics-using-tillerless-dac28508151f)
- [tillerless_github](https://github.com/rimusz/helm-tiller)

