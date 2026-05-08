# UFWUI

## A web UI to manage A linux server's Uncomplicated Firewall (UFW) in a comfertable web UI this also expoes a API

## `How to run :-`

- ### **Docker Run :-**
  
  ```bash
  docker run -d \
  --name ufwui \
  --network host \
  --privileged \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  -v /etc/ufw:/etc/ufw \
  --restart unless-stopped \
  192.168.1.100:3002/dev-mir2011/ufwui:latest
  ```

- ### **Docker Compose :-**
  
  ```yaml
    services:
    ufwui:
        image: 192.168.1.100:3002/dev-mir2011/ufwui:latest
        container_name: ufwui

        network_mode: host

        privileged: true

        cap_add:
        - NET_ADMIN
        - NET_RAW

        volumes:
        - /etc/ufw:/etc/ufw

        restart: unless-stopped
  ```
