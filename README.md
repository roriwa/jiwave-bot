# jiwave-bot
small discord bot

```text
    _ _                         
   (_|_)                        
    _ ___      ____ ___   _____ 
   | | \ \ /\ / / _` \ \ / / _ \
   | | |\ V  V / (_| |\ V /  __/
   | |_| \_/\_/ \__,_| \_/ \___|
  _/ |                          
 |__/                           
```

# Setup the Bot

[invite the bot](https://discord.com/api/oauth2/authorize?client_id=1011312099940646952&permissions=2128&scope=bot)  
<sup>Note: The Permissions are currently not working perfectly (add admin manually or test a bit)</sup>

## Install Project
```terminal
user@pc:~$ git clone https://github.com/roriwa/jiwave-bot.git
user@pc:~$ cd jiwave-bot
user@pc:~$ scripts/install.sh
```

## Discord-Token setup
either add an environment variable (`DISCORD-TOKEN`)
or create a `DISCORD-TOKEN.txt` file in the project root directory or in the `src/jiwave` directory

## Run the Bot

### Manually (not recommended)

```terminal
user@pc:~$ /path/to/jiwave-bot/src/run.sh
```

### Setup as Service (recommended)
copy this code to `/etc/systemd/system/jiwave-bot.service`
```ini
[Unit]
Description=jiwave-bot
After=network.target

[Service]
Type=simple
Restart=always
User=<username>
ExecStart=/path/to/jiwave-bot/src/run.sh

[Install]
WantedBy=multi-user.target
```
use `systemctl start jiwave-bot` to manually start the bot  
use `systemctl stop jiwave-bot` to manually stop the bot  
use `systemctl enable jiwave-bot` to make the bot run completely automatically  
use `systemctl status jiwave-bot` to check the bot

# Bot Commands

<sub>coming soon...</sub>

# Links for development
[docs: events](https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events)
