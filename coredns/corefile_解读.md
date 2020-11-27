# coredns插件配置文件corefile解读

- 示例配置文件
```
 Corefile: |
    .:53 {
        errors
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
          pods insecure
          upstream 
          fallthrough in-addr.arpa ip6.arpai
          ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
          policy sequential
        }
        cache 30
        loop
        reload
        loadbalance
    }
metadata:
  name: coredns
  namespace: kube-system
```
- 中文解读
```
errors: 错误日志会以标准输出的方式打印到容器日志

health: CoreDNS的健康状况

kubernetes: kubernetes插件是CoreDNS中用来替代kube-dns的模块，将service的域名转为IP的工作由该插件完成

其中常用的参数作用如下：
- pods POD-MODES: 用于设置Pod的A记录处理模式，如1-2-3-4.ns.pod.cluster.local. in A 1.2.3.4。pods disabled为默认值，表示不为pod提供dns记录
- pods insecure会一直返回对应的A记录，而不校验ns
- pods verified会校验ns是否正确，如果该ns下有对应的pod，则返回A记录

- upstream [ADDRESS..]: 定义用于解析外部hosts的上游dns服务器。如果不指定，则CoreDNS会自行处理，例如使用后面会介绍到的proxy插件
- fallthrough [ZONE..]: 如果指定此选项，则DNS查询将在插件链上传递，该插件链可以包含另一个插件来处理查询，例如in-addr.arpa

prometheus: CoreDNS对外暴露的监控指标，默认为http://localhost:9153/metrics

forward [from to]: 任何不属于Kubernetes集群内部的域名，其DNS请求都将指向forword指定的 DNS 服务器地址（from一般为"."，代表所有域名，to可以为多个，如111.114.114.114 8.8.8.8；
需要注意的是，新版本的CoreDNS已forward插件替代proxy插件，不过使用方法是一致的，如果你的集群是proxy，建议改为forward插件，性能更好

reload: 允许自动加载变化了的Corefile，建议配置，这样CoreDNS可以实现热更新
```
# 参考链接如下：
[kubernetes_coredns](https://kubernetes.io/zh/docs/tasks/administer-cluster/dns-custom-nameservers/)
[ucloud_coredns](https://docs.ucloud.cn/uk8s/administercluster/custom_dns_service)
