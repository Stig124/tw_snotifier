# TW-S(napshot)notifier

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

Following the openSUSE Tumbleweed update rate can be difficult, this solves this issue by sending a notification if a new update is available

#### NOTE : The RSS feed used is only actualised at 00:00+0000 (UTC) ([Check in your timezone](https://worldti.me/1006O)) every day, if there is a snapshot in the middle of the day, the script will not pick it up before midnight UTC

## Getting Started <a name = "getting_started"></a>


### Prerequisites

You must run `openSUSE Tumbleweed` and have `python3`, `pip3` and `python-dbus` installed

To install this, you can use OpenSUSE Zypper patterns :

```bash
sudo zypper in -t pattern devel_basis devel_python3
sudo zypper in python38-dbus-python
```

Install `pipenv`

```bash
pip3 install --user pipenv
```


### Installing

Clone the repository

```bash
git clone https://github.com/Stig124/tw_snotifier.git
cd tw_snotifier
```

Activate the environnement

```bash
pipenv install
```

Make the wrapper script executable

```bash
sudo chmod +x launch.sh
```

And simply run the wrapper script

```bash
./launch.sh
```

![Update available](https://i.imgur.com/frDLUCT.png)

![No update available](https://i.imgur.com/Z3ynIID.png)

## Usage <a name = "usage"></a>


You can add it to your `crontab` for periodic launch

`crontab -e`

Every boot :

```cron
@reboot /dir/launch.sh # Replace /dir/ by the script directory
```

or at midnight UTC ([Check in your timezone](https://worldti.me/1006O)) :

For exemple in UTC+1 with DST : *(the number to change is the one before the asterixs in 24h form)*

```
0 2 * * * /dir/launch.sh # Same here
```

You can modifiy the notification timeout *(must stay in seconds)* in the main.py file, lines :


- `118` : for the no update available timeout *(default : 10min (600s))*
- `121` : When update is available *(default : 1h (3600s))*

And

- the icon by changing accordingly the `path1` *(complete path to the folder where the icon is located)* and `icon1` *(which is path + icon name)*
- the app name using `app_name` variable
- the notifications titles, using both `titler` variables in lines `117` and `120`

## LICENSE

This program is released under the GNU General Public License (GPL) v2.0 only
