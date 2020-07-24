# YouTube Downloader over Tor Proxy
This script uses a Tor proxy to download YouTube videos using the [youtube-dl](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#readme) command line tool.

This will allow you to bypass download restrictions of YouTube for downloading large datasets.

## Requirements
1. Python 3.7+
2. youtube-dl 
3. tor 

## Setup Tor
You must first download and configure [Tor](https://www.torproject.org/) to run on commandline.

```brew install tor``` (MacOS)
```sudo apt-get install tor``` (Linux)

Once Tor has installed you must copy the example ```torrc``` configuration file.

```cp /usr/local/etc/tor/torrc.sample /usr/local/etc/tor/torrc```

Create a password to access the local Tor proxy (remember this password for later) using:

```tor --hash-password **your_password_here**```

Copy the hash output from the terminal (it should look like this: ```16:E3EAD3E61428CHSO20EA72221528EE489BDD9D21E937331E1D810694B2```)

Edit the ```torrc``` file:

```sudo nano /usr/local/etc/tor/torrc```

Locate the line ```#HashedControlPassword```, remove the comment mark (#) and paste in the output from the previous step. The line should now look like:

```HashedControlPassword 16:E3EAD3E61428CHSO20EA72221528EE489BDD9D21E937331E1D810694B2```

Remove the comment mark (#) from the ```ControlPort``` line.
```
ControlPort 9051
```

Close and save your file (```ctrl+x```) then ```Y``` <- if you are using nano to edit the file.

Congrats - you're ready to start running your Tor proxy.

## Starting Tor
You must start the Tor proxy before you run the python script. To start the Tor proxy, run:

```tor```

## Config Setup
Create a ```config.json``` file by copying and renaming the ```config.example.json```.

```
{
  "tor_password": "enter_your_password_here",
  "verbose_logging": false
}
```

### Verbose logging
If you find you're having issues running the tool, enable youtube-dl verbose logging to see what the issue is.

You can do this by editing the ```config.json``` and changing the ```verbose_logging``` to ```[True/False]```

## Managing your dataset
The script uses three files (below) to manage the state of downloading your dataset.

| File                      | Description                                                             |
|---------------------------|-------------------------------------------------------------------------|
| dataset\.csv              | List of YouTube Ids in your dataset                                     |
| completed\_downloads\.csv | After each file is downloaded the YouTube ID will be added to this file |
| error\_files\.csv         | If a file fails to download the YouTube ID will be added to this file   |

Start by adding YouTube Ids to the ```dataset.csv``` file. This file will be used by the script to download the YouTube videos into the ```/videos``` folder.

Files will be downloaded as ```.mp4``` format.

### Dataset.csv
Each line should be a new YouTube ID found at the end of a youtube link i.e. https://www.youtube.com/watch?v=dQw4w9WgXcQ (dQw4w9WgXcQ - YouTube Id)
```
nQPXu-T9uWc
bX2KCrEAc5w
```

## Running
Start the script using ```python downloader.py```

## FAQ
### SocketError
```SocketError: [Errno 61] Connection refused``` - Check that you have Tor running and configured correctly. This is due to either tor not running, incorrect password, or ControlPort hasn't been commented out.

### IncorrectPassword
```IncorrectPassword: Authentication failed: Password did not match HashedControlPassword value from configuration``` - Check that your script is using the plain text password that you set when you configured the Tor password (see above)
