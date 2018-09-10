# Site poller

Simple generic lambda fucntion triggered by cloudwatch events.

## Prerequisites

* Python 2.7

**Environment vaiables:**
* `CHANNEL="#devops"`
* `WEBHOOK_URL="https://hooks.slack.com/services/TXXXXXX/BXXXXXX/xxxxx"`

Set webhook_url and CHANNEL to the one provided by Slack when you [create the webhook]( https://my.slack.com/services/new/incoming-webhook/).

## Install dependencies

Python dependencies must be installed in the project root folder. This is required by amazon lambda. Files are not checked in to repo but must be uploaded to aws.

`pip install requests -t <project folder>`

On Mac, if python was installed by Homebrew, the abvoe will not work. Please add `setup.cfg` to project root with below content

```
[install]
prefix= 
```

## Zip before upload

Files in teh artifact zip need to be in root folder.

`zip -rq ../lamdba_$(date +%Y%m%d-%H%M%S).zip *`
