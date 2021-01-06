# volume(持久化)

我们带着两个问题去学习k8s中的volume(卷)
1. 容器中应用数据如何持久化(容器消亡后数据随之丢失)
2. pod内多个容器之间数据如何共享

# 什么是volume(卷)
- 卷的核心就是存放数据的一个目录，其生命周期要比pod/容器长，因为pod/容器重启，卷依然存在所谓的持久化也将不复存在，也就没有意义
- 卷在pod和容器内如何定义
```
1. pod内： .spec.volumes. 字段声明pod要使用的volume
2. containers内： .spec.containers[*].volumeMounts 字段声明卷在容器中的挂载位置
3. docker 镜像位于文件系统层次结构的根部,各个卷则挂载在镜像内的指定路径上.卷不能挂载到其他卷上,也不能与其他卷有硬链接.Pod 配置中的每个容器必须单独指定各个卷的挂载位置
```

# volume(卷)支持的类型-常用

1. 需要第三方存储资源环境
- cephfs/cephrbd
- vsphereVolume
- portworxVolume
- iscsi 
- nfs
2. kubernetes原生态
- emptyDir
```
1. pod调度至节点后,其卷被创建,容器间以读写的形式访问该卷,当pod被调度至其他节点后该卷数据被永久删除
2. 容器崩溃可能不会导致Pod被从节点上移除，因此容器崩溃期间emptyDir卷中的数据是安全的
3. yaml示例
---
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir: {}
---
```
- hostPath
```
1. 将主机上的文件系统以及文件或目录挂载到pod内
2. 场景
- 运行一个需要访问docker内部机制的容器；可使用hostPath挂载/var/lib/docker路径
- 在容器中运行cAdvisor时，以hostPath方式挂载 /sys
- 允许Pod指定给定的hostPath在运行Pod之前是否应该存在，是否应该创建以及应该以什么方式存在
3. path 文件系统、文件或目录必须指定外，hostpath 的type有多种可以按需指定
- 空: 空字符串（默认）用于向后兼容，这意味着在安装 hostPath 卷之前不会执行任何检查
- DirectoryOrCreate: 路径不存在时，会按照需求自动创建，权限为0755，与kubelet相同的组和属主信息
- Directory: 路径必须存在，否则pod无法正常启动
- FileOrCreate: 文件不存在时，会按照需求自动创建，权限为0644，与kubelet相同的组和属主信息(前提父目录要存在)
- File: 文件必须存在，否则pod无法正常启动
- Socket: 在给定路径上必须存在的 UNIX 套接字
- CharDevice: 在给定路径上必须存在的字符设备
- BlockDevice: 在给定路径上必须存在的块设备
当使用这种类型的卷时要小心因为：
具有相同配置的多个 Pod 会由于节点上文件的不同 而在不同节点上有不同的行为
下层主机上创建的文件或目录只能由root用户写入,你需要在特权容器中以root身份运行进程，或者修改主机上的文件权限以便容器能够写入 hostPath卷
3. yaml示例-type是directory
---
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      path: /data        #宿主上目录位置
      type: Directory    #此字段为可选
---
4. yaml示例-type是directoryorcreate、fileorcreate
---
apiVersion: v1
kind: Pod
metadata:
  name: test-webserver
spec:
  containers:
  - name: test-webserver
    image: k8s.gcr.io/test-webserver:latest
    volumeMounts:
    - mountPath: /var/local/aaa
      name: mydir
    - mountPath: /var/local/aaa/1.txt
      name: myfile
  volumes:
  - name: mydir
    hostPath:
      path: /var/local/aaa
      type: DirectoryOrCreate
  - name: myfile
    hostPath:
      path: /var/local/aaa/1.txt
      type: FileOrCreate
---
```
- configMap
- persistentVolumeClaim
- secret
- subPath
- local

