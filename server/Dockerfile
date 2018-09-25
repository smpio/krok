FROM alpine

RUN set -xe \
    && apk add --no-cache openssh \
    && ssh-keygen -A \
    && echo -e "PermitRootLogin no\nPermitEmptyPasswords yes\nGatewayPorts yes\nClientAliveInterval 1\nClientAliveCountMax 10" > /etc/ssh/sshd_config \
    && echo "krok::1000:1000:krok user:/tmp:/sbin/nologin" >> /etc/passwd

EXPOSE 22

ENTRYPOINT ["/usr/sbin/sshd", "-D", "-e"]
