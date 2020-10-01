
# yaml文件示例 
- 新增每个资源类型的具体输出
- 新增参考资料

1. Cronjob 输出：
```
- 查看job数
[root@k8s-master01 yaml]# kubectl get jobs -n test-tenant                        
NAME                             COMPLETIONS   DURATION   AGE
centos-cronjob-echo-1577800320   4/4           10s        10m
centos-cronjob-echo-1577800380   4/4           8s         9m8s
centos-cronjob-echo-1577800440   4/4           8s         8m8s
- 查看pod数
[root@k8s-master01 yaml]# kubectl get pods -n test-tenant  | grep cronjob
centos-cronjob-echo-1577799420-2rtcd   0/1     Completed   0          2m20s
centos-cronjob-echo-1577799420-8l4sl   0/1     Completed   0          2m26s
centos-cronjob-echo-1577799420-g55fb   0/1     Completed   0          2m20s
centos-cronjob-echo-1577799420-l94bg   0/1     Completed   0          2m26s
centos-cronjob-echo-1577799480-4tscg   0/1     Completed   0          82s
centos-cronjob-echo-1577799480-n6q8f   0/1     Completed   0          86s
centos-cronjob-echo-1577799480-swf9s   0/1     Completed   0          82s
centos-cronjob-echo-1577799480-x8bc5   0/1     Completed   0          86s
centos-cronjob-echo-1577799540-f7qsx   0/1     Completed   0          22s
centos-cronjob-echo-1577799540-jwc2p   0/1     Completed   0          22s
centos-cronjob-echo-1577799540-x26bq   0/1     Completed   0          26s
centos-cronjob-echo-1577799540-xl8ht   0/1     Completed   0          26s
- 查看pod_log
[root@k8s-master01 yaml]# kubectl logs -f centos-cronjob-echo-1577799540-xl8ht -n test-tenant 
This is a Test cronjob！
- 查看master节点是否有污点
[root@k8s-master01 yaml]# kubectl get nodes k8s-master01 --show-labels            
NAME           STATUS   ROLES    AGE   VERSION   LABELS
k8s-master01   Ready    master   38d   v1.16.2   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-master01,kubernetes.io/os=linux,node-role.kubernetes.io/master=
- 打污点
[root@k8s-master01 yaml]# kubectl taint node k8s-master01 node-role.kubernetes.io=master:NoSchedule
node/k8s-master01 tainted
- 取消污点
[root@k8s-master01 yaml]# kubectl taint node k8s-master01 node-role.kubernetes.io=master:NoSchedule-
node/k8s-master01 untainted

- completions: 4 job完成总数
- parallelism: 2 job的并发数
- successfulJobsHistoryLimit：保留已完成job数量，默认是3
- failedJobsHistoryLimit: 1 保留失败job数量，默认是1
- 4个节点、1个master节点(默认有污点)、get pods 正好是12个

```
2. Daemonset 输出：
```
- 查看daemonset状态
[root@k8s-master01 ~]# kubectl get ds -n test-tenant 
NAME                    DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
centos-daemonset-echo   4         4         0       4            0           <none>          14m
- 查看daemonset pods
[root@k8s-master01 ~]# kubectl get pods -n test-tenant | grep daemonset
centos-daemonset-echo-cxbhv            0/1     Completed          10         26m
centos-daemonset-echo-h6vj9            0/1     CrashLoopBackOff   10         26m
centos-daemonset-echo-jdq8n            0/1     CrashLoopBackOff   9          26m
centos-daemonset-echo-tzbdw            0/1     CrashLoopBackOff   9          26m
- 查看pod_logs（因为yaml只定义了echo，所以执行完后主进程退出，kubelet随即认为容器异常并kill掉容器，所以get pods显示CrashLoopBackOff），这里有牵扯出pod的health_check
[root@k8s-master01 ~]# kubectl logs -f centos-daemonset-echo-tzbdw -n test-tenant 
This is a DaemonSet's Instance!
```
3. sts & pv/pvc 输出:
```
- 创建pv/pvc/sts
[root@k8s-master01 yaml]# kubectl apply -f centos-sts-echo.yaml 
persistentvolume/webindex created
persistentvolumeclaim/webindex-tmpfile created
statefulset.apps/centos-sts-echo created
- 查看pv/pvc/sts/pods资源
[root@k8s-master01 yaml]# kubectl get pv 
NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                          STORAGECLASS   REASON   AGE
webindex   10Gi       RWX            Retain           Bound    test-tenant/webindex-tmpfile                           4m8s
[root@k8s-master01 yaml]# kubectl get pvc -n test-tenant 
NAME               STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
webindex-tmpfile   Bound    webindex   10Gi       RWX                           4m14s
[root@k8s-master01 yaml]# kubectl get sts -n test-tenant   
NAME              READY   AGE
centos-sts-echo   3/3     5m6s
[root@k8s-master01 yaml]# kubectl get pod -n test-tenant  | grep sts
centos-sts-echo-0                      1/1     Running     0          4m48s
centos-sts-echo-1                      1/1     Running     0          4m45s
centos-sts-echo-2                      1/1     Running     0          4m42s
- 登陆worker节点，查看文件是否持久化(tmp/为空，所以/testvol目录下为空，我们手动创建并查看)
- worker01节点中的9e25498c0b54容器
[root@k8s-worker01 ~]# docker ps | grep sts | grep -v POD
9e25498c0b54        ceb10bf48bb5                 "/bin/sh -c 'while t…"   7 minutes ago       Up 7 minutes                            k8s_centos-sts-echo_centos-sts-echo-2_test-tenant_b580feb1-6ebd-4335-a27b-94abe34e593b_0
8b71f3887cbb        ceb10bf48bb5                 "/bin/sh -c 'while t…"   7 minutes ago       Up 7 minutes                            k8s_centos-sts-echo_centos-sts-echo-0_test-tenant_1453ee85-d58f-4a9e-b184-da1312e4b417_0
[root@k8s-worker01 ~]# docker exec -it 9e25498c0b54 /bin/bash 
[root@centos-sts-echo-2 /]# cd tmp/
[root@centos-sts-echo-2 tmp]# ll
bash: ll: command not found
[root@centos-sts-echo-2 tmp]# ls -l
total 0
[root@centos-sts-echo-2 tmp]# touch testfile
[root@centos-sts-echo-2 tmp]# hostname
centos-sts-echo-2
- worker01节点中8b71f3887cbb容器
[root@k8s-worker01 ~]# docker exec -it 8b71 touch /tmp/testfile2
[root@k8s-worker01 ~]# docker exec -it 8b71 ls -l /tmp 
total 0
-rw-r--r--. 1 root root 0 Jan  3 07:56 testfile
-rw-r--r--. 1 root root 0 Jan  3 08:00 testfile2
- worker节点
[root@k8s-worker01 testvol]# ll
total 0
-rw-r--r--. 1 root root 0 Jan  3 15:56 testfile
[root@k8s-worker01 testvol]# hostname
k8s-worker01
[root@k8s-worker01 testvol]#
- 测试得出 多个容器是可以读写的，因为pv/pvc的accessMode为RWX
```
4. deplopy_Metrics-server
```
- kubectl 部署
[root@k8s-master01 ~]# kubectl apply -f https://raw.githubusercontent.com/bertreyking/repos/master/k8s/yaml/metrics-server.yaml      
clusterrole.rbac.authorization.k8s.io "system:aggregated-metrics-reader" apply
clusterrolebinding.rbac.authorization.k8s.io "metrics-server:system:auth-delegator" apply
rolebinding.rbac.authorization.k8s.io "metrics-server-auth-reader" apply
apiservice.apiregistration.k8s.io "v1beta1.metrics.k8s.io" apply
serviceaccount "metrics-server" apply
deployment.apps "metrics-server" apply
service "metrics-server" apply
clusterrole.rbac.authorization.k8s.io "system:metrics-server" apply
clusterrolebinding.rbac.authorization.k8s.io "system:metrics-server" apply

- helm 部署
[root@k8s-master01 ~]# helm install stable/metrics-server -n kube-system --generate-name
NAME: metrics-server-1591771682
LAST DEPLOYED: Wed Jun 10 14:48:18 2020
NAMESPACE: kube-system
STATUS: deployed
REVISION: 1
NOTES:
The metric server has been deployed. 

In a few minutes you should be able to list metrics using the following
command:

  kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes"

- helm部署后，需要修改下deployment
pod.container cmd或args需要加上以下参数
    - --kubelet-insecure-tls
    - --kubelet-preferred-address-types=InternalIP

- 通过lables查看某个pod的计算资源利用率
[root@k8s-master01 ~]# kubectl get pods --show-labels
NAME                                READY   STATUS    RESTARTS   AGE     LABELS
nginx-6db489d4b7-x8lrk              1/1     Running   0          4h11m   pod-template-hash=6db489d4b7,run=nginx
nginx-deployment-5d9ff489f5-hms2q   1/1     Running   2          75d     app=nginx,pod-template-hash=5d9ff489f5
nginx-deployment-5d9ff489f5-tdlx4   1/1     Running   2          158d    app=nginx,pod-template-hash=5d9ff489f5
traefik-59f9f94958-lqdvb            1/1     Running   2          43d     app=traefik,pod-template-hash=59f9f94958
whoami-5ff9b84c7d-hnnlp             1/1     Running   2          160d    app=whoami,pod-template-hash=5ff9b84c7d
whoami-5ff9b84c7d-jw5pp             1/1     Running   2          75d     app=whoami,pod-template-hash=5ff9b84c7d
[root@k8s-master01 ~]# kubectl top pods -l app=whoami
NAME                      CPU(cores)   MEMORY(bytes)   
whoami-5ff9b84c7d-hnnlp   0m           0Mi             
whoami-5ff9b84c7d-jw5pp   0m           0Mi 
```
- 参考资料 
[Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)
[StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
[Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#resources)
[issues_188](https://github.com/kubernetes-sigs/metrics-server/issues/188)
[metrics-server](https://github.com/kubernetes-sigs/metrics-server)
