# 镜像搬运工(来源: gcr.io/google_containers/)

- [cAdvisor](https://github.com/google/cadvisor/releases)
```
docker pull skyking116/cadvisor:v0.36.0
docker pull skyking116/cadvisor:v0.35.0
docker pull skyking116/cadvisor:v0.34.0
```
- [kubernetes-1.18.0](https://console.cloud.google.com/gcr/images/google-containers)
```
docker pull skyking116/kube-apiserver:v1.18.0
docker pull skyking116/kube-controller-manager:v1.18.0
docker pull skyking116/kube-proxy:v1.18.0 
docker pull skyking116/kube-scheduler:v1.18.0 
```
- [kubernetes-1.18.4](https://console.cloud.google.com/gcr/images/google-containers)
```
sudo docker pull skyking116/kube-apiserver:v1.18.4
sudo docker pull skyking116/kube-controller-manager:v1.18.4
sudo docker pull skyking116/kube-scheduler:v1.18.4
sudo docker pull skyking116/kube-proxy:v1.18.4
sudo docker pull skyking116/pause:3.2
sudo docker pull skyking116/etcd:3.4.3-0
sudo docker pull skyking116/coredns:1.6.7
```
- [kubeadm、kubectl]
```
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
       http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
```
