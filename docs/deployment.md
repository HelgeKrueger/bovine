# Deployment

To run bovine as on a webserver, the following information might be useful. I currently have no idea how resource intensive Bovine is. Deployment is currently causing the most load on the server. Of course, I'm not popular, so this might not be a good measure.

I put the source code into `/opt/bovine` as user `bovine` in group `bovine`

## Systemd unit

```ini
[Unit]
Description=Bovine
After=network.target

[Service]
User=bovine
Group=bovine
Restart=always
Type=simple
WorkingDirectory=/opt/bovine/bovine_blog
Environment="DOMAIN=$MY_DOMAIN"
Environment="ACCESS_TOKEN=$MY_TOKEN"
LimitAS=infinity
LimitRSS=infinity
LimitCORE=infinity
LimitNOFILE=65536
ExecStart=/usr/local/bin/poetry run hypercorn bovine_blog:app --bind unix:/run/bovine.sock

[Install]
WantedBy=multi-user.target
```

You have to update `$MY_DOMAIN` and `$MY_TOKEN`. The token is the one used in buffalo
to access the client to server endpoints.
Under ubuntu place this file in `/etc/systemd/system/` and
then reload systemd via `systemctl daemon-reload`.

The settings starting with `Limit` are not fine tuned. In particular, the number of allowed file connections is needed in order to handle the many `GET` requests from fellow Fediverse servers, when somebody announces your content.

The default value of the number of allowed open files can be viewed on your system with `ulimit -n`. Having too low number of open files leads to errors such as

```
[2023-02-07 19:16:10,518] ERROR    asyncio      socket.accept() out of system resource
socket: <asyncio.TransportSocket fd=3, family=AddressFamily.AF_UNIX, type=SocketKind.SOCK_STREAM, proto=0, laddr=/tmp/bovine.sock>
Traceback (most recent call last):
  File "/usr/lib/python3.10/asyncio/selector_events.py", line 159, in _accept_connection
    conn, addr = sock.accept()
  File "/usr/lib/python3.10/socket.py", line 293, in accept
OSError: [Errno 24] Too many open files
```

## Nginx

Nginx can then be configured via in `sites-available`

```nginx
	location / {
		proxy_set_header Host $http_host;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
		proxy_set_header Upgrade $http_upgrade;
		proxy_redirect off;
		proxy_buffering off;
		proxy_pass http://unix:/run/bovine.sock;
	}
```

Furthermore, one needs to do the usual gymnastics to get SSL working.

Finally, one needs to edit the nginx config, i.e. `/etc/nginx/nginx.conf` and increase the number of worker connections, e.g.

```nginx
events {
        worker_connections 4096;
}
```

This is again necessary to handle the many get requests that occur if somebody announces your content. The corresponding error message is

```
2023/02/11 13:21:46 [alert] 650#650: 768 worker_connections are not enough
```

**FIXME**: For this to work, I had to run `chmod 777 /tmp/bovine.sock`. My internet research shows that it shoud be in `/run`. But no clue how to get this working.

**FIXME**: Should I add `proxy_buffering`?
