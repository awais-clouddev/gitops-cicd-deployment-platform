# Kubernetes Runtime Evidence

## Cluster

```text
Context: kind-gitops-platform
NAME                            STATUS   ROLES           AGE    VERSION
gitops-platform-control-plane   Ready    control-plane   170m   v1.37.0
gitops-platform-worker          Ready    <none>          170m   v1.37.0
gitops-platform-worker2         Ready    <none>          170m   v1.37.0
```

## Development Workloads

```text
NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/helpdesk-api        1/1     1            1           144m
deployment.apps/helpdesk-frontend   1/1     1            1           58m
deployment.apps/helpdesk-gateway    1/1     1            1           144m
deployment.apps/helpdesk-redis      1/1     1            1           144m

NAME                                 READY   AGE
statefulset.apps/helpdesk-postgres   1/1     144m
```

## Development Pods

```text
NAME                                 READY   STATUS    RESTARTS   AGE
helpdesk-api-6598d76fbd-xdftl        1/1     Running   0          61m
helpdesk-frontend-55c7647457-xznqv   1/1     Running   0          58m
helpdesk-gateway-9f786cc94-nwswz     1/1     Running   0          67m
helpdesk-postgres-0                  1/1     Running   0          67m
helpdesk-redis-58785f44df-w4lw7      1/1     Running   0          67m
```

## Services

```text
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
helpdesk-api        ClusterIP   10.96.47.110    <none>        8000/TCP   144m
helpdesk-frontend   ClusterIP   10.96.98.111    <none>        8080/TCP   144m
helpdesk-gateway    ClusterIP   10.96.101.118   <none>        80/TCP     144m
helpdesk-postgres   ClusterIP   10.96.93.200    <none>        5432/TCP   144m
helpdesk-redis      ClusterIP   10.96.65.161    <none>        6379/TCP   144m
```

## Running Images

```text
helpdesk-api-6598d76fbd-xdftl => ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-api@sha256:d0e5362a68e06846429aae6fda6020a7e2f94d74bc9cfc4325b4a2d229a2e4b3 
helpdesk-frontend-55c7647457-xznqv => ghcr.io/awais-clouddev/gitops-cicd-deployment-platform-frontend@sha256:d3d2169eb6e7a5e385a78c31ef7395c9ccfacc84b3ac9d039b42bea97f5313d4 
helpdesk-gateway-9f786cc94-nwswz => nginx:alpine 
helpdesk-postgres-0 => postgres:17 
helpdesk-redis-58785f44df-w4lw7 => redis:8-alpine 
```

## Release Traceability


- Running release SHA: `3bf1dffef919c85a7a74399ea16cacc403ce9f0b`

## Argo CD

```text
NAME                   SYNC STATUS   HEALTH STATUS
helpdesk-development   Synced        Healthy
```
