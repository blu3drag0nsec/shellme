# shellme

```bash
usage: genshellme.py [-h] [-p PORT] [-d DEVICE] [-i IP] [-path PATH]

Generate a shellme file

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT
  -d DEVICE, --device DEVICE
  -i IP, --ip IP
  -path PATH, --path PATH
```

Examples:

```bash
/blu3/hackz/genshellme.py -i 0.tcp.eu.ngrok.io -p 18825
File created at: /dev/shm/shellme
```

```bash
/blu3/hackz/genshellme.py -i eth0                      
File created at: /dev/shm/shellme
```

```bash
/blu3/hackz/genshellme.py -i eth0 -p 1337 -path ./generated
File created at: ./generated/shellme
```
