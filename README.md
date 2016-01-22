# nagios-b2handle-probes
Two tests are available, `check_epic_api.py` and `check_handle_resolution.pl`

##check_epic_api.py

This plugin is a simple CRUD test of the EPIC API service on the specified host and the specified prefix. It creates a handle named NAGIOS-{DATE}-{TIME}, and then tries to read it and update it with a new value, and finally tries to delete it.

It imports the `epicclient` module.

###Required options:

`--username <user>` : The username used to authenticate with the EPIC service

`--url <uri>` : The base uri of the EPIC API service to be tested

`--pass <key>` : The API key of the username

`--prefix <prefix>` : The prefix to be tested


###Optional options
`--debug` : Debug mode

`--help` : Print a help message and exit

`--timeout <timeout>` : Timeout in seconds

###Example:
```
check_epic_api.py \

	--url "https://epic.domain.com/api/v2/handles/" --prefix 12345 \

	--username nagios --pass deadbabe --debug```

