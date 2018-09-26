# krok
*as in ngrok*

Expose your local TCP server as Kubernetes service in remote cluster.


## Usage

Giving we want to create service in `namespace` with name `service_name` on port `service_port` forwarding all traffic from it to `local_host` (usually 127.0.0.1) and `local_port`.

1. Install krok client: `pip install krok`

2. Install krok server: `kubectl -n <namespace> run --image=smpio/krok-server krok`

3. Run krok: `krok -n <namespace> -l <local_host> -p <local_port> <service_name> <service_port>`

Note: `local_host` can be any host reachable from your machine, but usually `127.0.0.1` is the most useful.


## How it works

We have running krok server in the pod `krok_pod` in `namespace`. The server is simple OpenSSH server that allows to forward incoming connections.

Krok client is simple script that automates the following steps:

1. Run `kubectl port-forward <krok_pod> :22`. It will listen on random `local_ssh_port` forwarding all connections to krok's OpenSSH server on `krok_pod`.

2. Run `ssh -N -R *:0:<local_host>:<local_port> -p <local_ssh_port> krok@localhost`. This causes krok's OpenSSH server on `krok_pod` to listen on random `pod_port` forwarding all connections to `local_host:local_port` using SSH tunnel.

3. Create or update service `service_name` with port `service_port` and targetPort `pod_port`, with selector matching `krok_pod`.

In the result, all connections to `service_name:service_port` will be forwarded to `krok_pod`, then to your local machine via SSH tunnel forwarded by `kubectl port-forward`, and then forwarded by SSH client to `local_host:local_port`.
