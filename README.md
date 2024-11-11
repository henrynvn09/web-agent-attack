# web-agent-attack

## command to run

```
docker build -t bruin-market:latest . && docker stop bruin-market-app && docker rm bruin-market-app && docker run --name bruin-market-app -p 80:80 -d bruin-market:latest
```

## the exploit works

- the WebAgent visit bruin profile after login, the `hiddenForm` will be sent after 5s to [this web hook](https://webhook.site/#!/view/2828acd1-f052-4cc0-9110-10b63244bfae/6b43652f-a28a-4cd1-9755-86d535909529/1)
