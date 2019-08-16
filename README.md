*MTrack* is a simple time tracking tool that we use in our technical team in [Quera](https://quera.ir).

## Installation

For installing or updating, run the following commands:

```bash
git clone git@github.com:mjnaderi/mtrack.git
cd mtrack
sudo pip3 install . 
```

## Usage

To start timer:

```
$ mtr PROJECT_NAME
```

Press `Ctrl+C` to stop timer.

For getting a report of a month:

```
$ mtr PROJECT_NAME --report 1398 1
```

For printing current installed version:

```bash
$ mtr --version
```

## TODO

- Display icon in systray
