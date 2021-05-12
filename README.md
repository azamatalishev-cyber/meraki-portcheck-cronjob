# meraki_portcycle_cronjob

## SOURCES
`bootstrap.sh`

[Git - When to Merge vs. When to Rebase – DerekGourlay.com | bash](https://www.derekgourlay.com/blog/git-when-to-merge-vs-when-to-rebase/) 

[How do I clone a subdirectory only of a Git repository? - Stack Overflow](https://stackoverflow.com/questions/600079/how-do-i-clone-a-subdirectory-only-of-a-git-repository/13738951#13738951)

[partial-clone.md](https://gist.github.com/nharrer/33b1535b4630387ff2be3116513baa0b)

[What's the best practice to "git clone" into an existing folder? - Stack Overflow](https://stackoverflow.com/questions/5377960/whats-the-best-practice-to-git-clone-into-an-existing-folder)

[Bring your monorepo down to size with sparse-checkout - The GitHub Blog](https://github.blog/2020-01-17-bring-your-monorepo-down-to-size-with-sparse-checkout/)

[Private Git Repositories: Part 2A - Repository SSH Keys](https://www.openshift.com/blog/private-git-repositories-part-2a-repository-ssh-keys?extIdCarryOver=true&sc_cid=701f2000001OH7iAAG)

[How to configure multiple deploy keys for different private github repositories on the same computer without using ssh-agent](https://gist.github.com/gubatron/d96594d982c5043be6d4)

[linux - How to compare two strings in dot separated version format in Bash? - Stack Overflow](https://stackoverflow.com/questions/4023830/how-to-compare-two-strings-in-dot-separated-version-format-in-bash)

[How to convert a string to lower case in Bash? - Stack Overflow](https://stackoverflow.com/questions/2264428/how-to-convert-a-string-to-lower-case-in-bash)

[linux - Extract file basename without path and extension in bash - Stack Overflow](https://stackoverflow.com/questions/2664740/extract-file-basename-without-path-and-extension-in-bash/2664746#2664746)

`main.py`

[Pipenv: Python Dev Workflow for Humans — pipenv 2020.11.16.dev0 documentation](https://pipenv.pypa.io/en/latest/)

[Stop using sudo pip install - DEV](https://dev.to/elabftw/stop-using-sudo-pip-install-52mn)

[homebrew - How to install specific version of python on OS X - Ask Different](https://apple.stackexchange.com/questions/237430/how-to-install-specific-version-of-python-on-os-x/319675#319675)

[A launchd Tutorial](https://www.launchd.info/)

[Exit Codes With Special Meanings](https://tldp.org/LDP/abs/html/exitcodes.html)

[Logging in Python – Real Python](https://realpython.com/python-logging/)

[logging - Making Python loggers output all messages to stdout in addition to log file - Stack Overflow](https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file)

## Setup
### python
```bash
brew install pyenv
pyenv install 3.7.3
pyenv local 3.7.3
ln -s ~/.pyenv/versions/3.7.3/bin/python3.7 /usr/local/bin/python3.7
```
### pipenv
```bash
# new install w/requirements.txt
pipenv install

# updated Pipfile/requirements.txt
pipenv sync

# switched python versions/debugging
pipenv --rm
pipenv install
```

### requirements.txt
* If `pipenv` is overkill or QA is finished, `requirements.txt` can be used to install dependencies as the current user
    * Avoid [sudo pip install](https://dev.to/elabftw/stop-using-sudo-pip-install-52mn)
    ```bash
    python -m pip install -r requirements.txt
    ```
    * This ensures that the packages get installed for the [correct version of Python](https://stackoverflow.com/questions/2812520/dealing-with-multiple-python-versions-and-pip)
* Virtual environment usage

    `TODO`

### Credentials
* **1Password**: `Cisco Meraki API token` && `Dead Man's Snitch URL`
* `.env` dotfile with `decouple`
    * Create an `.env` file (ignored in repo) in working directory and fill out env vars
    ```bash
    API_KEY='${api_key}'
    SNITCH_URL='${snitch_url}'
    ```
* Environment variable credentials
    ```bash
    export API_KEY='${api_key}'
    export SNITCH_URL='${snitch_url}'
    ```

## Usage
```bash
# activate virtualenv
$ pipenv shell

# run python script
(meraki_portcylcle_cronjob) $ python main.py

# script output
2020-12-15 16:19:31       meraki:     INFO > Meraki dashboard API session initialized with these parameters: {'version': '1.4.0', 'api_key': '************************************bf9e', 'base_url': 'https://api.meraki.com/api/v1', 'single_request_timeout': 60, 'certificate_path': '', 'requests_proxy': '', 'wait_on_rate_limit': True, 'nginx_429_retry_wait_time': 60, 'action_batch_retry_wait_time': 60, 'retry_4xx_error': False, 'retry_4xx_error_wait_time': 60, 'maximum_retries': 2, 'simulate': False, 'be_geo_id': None, 'caller': None}
2020-12-15 16:19:31       meraki:     INFO > GET https://api.meraki.com/api/v1/devices/Q2VX-K5M5-7ZV6/switch/ports/statuses
2020-12-15 16:19:31       meraki:     INFO > GET https://n349.meraki.com/api/v1/devices/Q2VX-K5M5-7ZV6/switch/ports/statuses
2020-12-15 16:19:32       meraki:     INFO > switch, getDeviceSwitchPortsStatuses - 200 OK
2020-12-15 16:19:32       meraki:     INFO > POST https://n349.meraki.com/api/v1/devices/Q2VX-K5M5-7ZV6/switch/ports/cycle
2020-12-15 16:19:33       meraki:     INFO > switch, cycleDeviceSwitchPorts - 200 OK

# deactivate virtualenv
(meraki_portcylcle_cronjob) $ exit

# create and start launchdaemon
$ sudo ./cron.sh

# validate plist
$ plutil -lint /Library/LaunchDaemons/meraki_portcycle.plist
/Library/LaunchDaemons/meraki_portcycle.plist: OK
$ defaults read /Library/LaunchDaemons/meraki_portcycle.plist
{
    Label = "meraki_portcycle";
    ProgramArguments =     (
        "/usr/local/bin/python3.7",
        "/usr/local/bin/meraki-portcycle"
    );
    RunAtLoad = 1;
    StandardErrorPath = "/Users/ghadmin/meraki_portcycle_cronjob/logs/meraki_portcycle_stderr.log";
    StandardOutPath = "/Users/ghadmin/meraki_portcycle_cronjob/logs/meraki_portcycle_stdout.log";
    StartInterval = 1800;
    UserName = ghadmin;
}
```
**NOTE**
Assuming that the PLIST was successfully created and launched, check:
* `logs` directory 
* `#dead_mans_snitch` Slack channel
* email alerts (e.g., `[REPORTING] meraki_cronjob is reporting again`)

## Troubleshooting
* Python
    * Set shebang (intepreter) in `main.py`
    * Verify all dependencies are present for specific version of Python (see: [Setup](#setup))
* LaunchDaemon
    * Check the logs (uncomment `StandardOutPath` and `StandardErrorPath` lines in `cron.sh`)
    ```bash
    # system.log
    sudo tail -F /var/log/system.log | grep --line-buffered "com.apple.xpc.launchd\[" | grep "meraki_portcycle"

    # stderr/stdout.log(s)
    tail -f logs/meraki_portcycle_stderr.log
    ```

## TODO
### main.py
* Add average Kbps logic to `main` function and/or look into getting a status check in Verkada API
    * Can leave current check in-place, but if it's at the threshold, verify how long Kbps has been low
* Document vanilla ~~`requirements.txt`~~ && `venv`

### cron.sh
* Add cron job then setup functions based on OS
