 A script that waits for a specific service to be up and running before it returns. A typical usecase would be for services that needs to be started in a certain order. A typical scanrio for this is synchronising Docker containers. 

### Example
```
$ waitforservice -n google -u http://www.google.com -c 10 -s 2000
```
Tries to get a 200 response from the given URL by trying it 10 times with 2s inbetween

### Usage
```
  usage: waitforservice [-h] -n [NAME] -u [URL] [-c [COUNT]] [-s [SLEEP]]

  optional arguments:
    -h, --help            show this help message and exit
    -n [NAME], --name [NAME]
                        the name of the service to wait for
    -u [URL], --url [URL]
                        the url ex: tcp://<host>:<port> or http://...
    -c [COUNT], --count [COUNT]
                        the nr of times to try. less than 1 means forever.
                        default = 100
    -s [SLEEP], --sleep [SLEEP]
                        sleep time in ms between tries. default = 1s
```
