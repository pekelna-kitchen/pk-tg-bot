# hk-telegram

### install [piku](https://github.com/piku/piku)

```bash
# !! RUN AS ROOT !!

ssh root@YOUR-FRESH-UBUNTU-SERVER
curl https://piku.github.io/get | sh

curl https://raw.githubusercontent.com/piku/piku/master/piku > /bin/piku && chmod 755 /bin/piku
```

### add self-hosted runner

```bash
# !! RUN AS piku !!
su - piku

https://github.com/{YOUR_ACCOUNT}/telegram-bot/settings/actions/runners
```
