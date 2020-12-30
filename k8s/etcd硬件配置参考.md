# etcd hardware configurations (aws/gce为例)[etcd](https://etcd.io/docs/v3.4.0/op-guide/hardware/#example-hardware-configurations)

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
