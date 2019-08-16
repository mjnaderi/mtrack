*MTrack* is a simple time tracking tool that we use in our engineering team in [Quera](https://quera.ir).

## Installation

For installing or updating, run the following commands:

```bash
git clone git@github.com:mjnaderi/mtrack.git
cd mtrack
sudo pip3 install . 
```

## Usage

Start timer:

```
$ mtr PROJECT_NAME
```

Press `Ctrl+C` to stop timer.

Getting report for a Jalali month:

```
$ mtr PROJECT_NAME --report 1398 1
```

Printing current installed version:

```bash
$ mtr --version
```

## TODO

- Display icon in systray
