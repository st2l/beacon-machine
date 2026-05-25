## Beacon Machine

> This tool was created in educational purposes. Use it on your own risk.


## Requirements

- python
- aircrack-ng installed on your system

## How to use

Firstly, your device should be in monitor mode.

```shell
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Check that your monitor in correct country (it mattters):
```shell
sudo iw reg set RU
```

```shell
sudo uv run beacon_machine.py <interface> -c <how-many-spots> -p <prefix-for-each-network> -ch <channel-on-which-deploy>
```

Happy hacking! >w<
