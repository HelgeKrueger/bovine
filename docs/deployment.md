# Deployment

To run bovine as on a webserver, the following information might be useful. I currently have no idea how resource intensive Bovine is. Deployment is currently causing the most load on the server. Of course, I'm not popular, so this might not be a good measure.

I put the source code into `/opt/bovine` as user `bovine` in group `bovine`

## Systemd unit

```
[Unit]
Description=Bovine
After=network.target

[Service]
User=bovine
Group=bovine
Restart=always
Type=simple
WorkingDirectory=/opt/bovine
Environment="DOMAIN=$MY_DOMAIN"
Environment="ACCESS_TOKEN=$MY_TOKEN"
ExecStart=/usr/local/bin/poetry run hypercorn bovine_blog:app --bind unix:/run/bovine.sock

[Install]
WantedBy=multi-user.target
```

You have to update `$MY_DOMAIN` and `$MY_TOKEN`. The token is the one used in buffalo
to access the client to server endpoints.
Under ubuntu place this file in `/etc/systemd/system/` and
then reload systemd via `systemctl daemon-reload`.

## Nginx

Nginx can then be configured via

```
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

**FIXME**: For this to work, I had to run `chmod 777 /tmp/bovine.sock`. My internet research shows that it shoud be in `/run`. But no clue how to get this working.

**FIXME**: Should I add `proxy_buffering`?
