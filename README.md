# hk-telegram

### install [piku](https://github.com/piku/piku)

piku requires own user public key in authorized_keys to bind it with GH action runner in the end.

```bash

# ssh-keygen -o
cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys
```

```bash
sudo -i

curl https://piku.github.io/get | sh
./piku-bootstrap install --no-interactive
curl https://raw.githubusercontent.com/piku/piku/master/piku > /usr/bin/piku && chmod 755 /usr/bin/piku
```

### add self-hosted runner

Open [runners page](https://github.com/pekelna-kitchen/telegram-bot/settings/actions/runners) to get API key and instructions.


### install project dependencies

```bash
sudo apt-get install postgresql
```

### after piku app init, configure env variables

```bash
piku config:set TG_TOKEN=
piku config:set DATABASE_URL=
```
