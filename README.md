# Former2

    Ondrej Sika <ondrej@ondrejsika.com>
    https://gitlab.sikahq.com/ondrej/former2
    https://github.com/former2/former2

Simple form backend for static sites.

## Build

```
docker build -t former2/former2
```

## Run

```
docker run -p 80:80 former2/former2 \
  --smtp-server smtp.example.com \
  --smtp-port 587 \
  --smtp-tls \
  --smtp-username noreply@example.com \
  --smtp-password password \
  --smtp-email noreply@example.com \
  --notify-to alice@example.com,bob@example.com  
```