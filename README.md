## Beacon Machine

> This tool was created for educational purposes. Use it on your own risk.

## Requirements

- python
- uv
- aircrack-ng installed on your system

## How to use

Firstly, your device should be in monitor mode.

```shell
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Check that your monitor in correct country (it matters):

```shell
sudo iw reg set RU
```

### CLI

```shell
uv run beacon_machine <interface> -c <how-many-spots> -ch <channel> (--ssid <name> | --ssid-file <path> | --random-ssid)
```

Examples:

```shell
# One SSID for all APs (no prefix mode)
sudo uv run beacon_machine wlan0mon -c 10 -ch 36 --ssid FreeWiFi

# SSIDs from file (one SSID per line)
sudo uv run beacon_machine wlan0mon -c 10 -ch 36 --ssid-file ssids.txt

# Random SSIDs
sudo uv run beacon_machine wlan0mon -c 10 -ch 36 --random-ssid --random-length 10
```

Supported channels: `1, 6, 11, 36, 40, 44, 48`

Happy hacking! >w<
