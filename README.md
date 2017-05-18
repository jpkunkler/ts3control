# ts3control
A command line tool to control a teamspeak 3 query instance.

You no longer need any web interface to start, stop, create, delete and manage all your TeamSpeak 3 servers.
Do it all, right from your command line!

## Requirements
##### Python-ts3
- Follow installation instructions on https://github.com/nikdoof/python-ts3

## Installation
1. Clone this repository 
2. Open credentials.py and adjust settings to your teamspeak 3 instance
3. Create alias for this script by adding ```alias ts3='python /path/to/ts3control.py```

## Usage
To start a control session, type ts3 (if you created the above alias) followed by:

- -h for help on all functions
- -list: Lists status for all servers
- -list -s {online|offline|all}: Select which servers you want to be listed by status
- -list -s clients: Lists all currently connected clients

