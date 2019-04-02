# Site poller

Configurable database poller that posts slack message if first row firscifigured query resultset is noand alert slack alerter lambda function

## Prerequisites

* Slack webhook

**Environment vaiables:**
* `CHANNEL="#devops"`
* `WEBHOOK_URL="https://hooks.slack.com/services/TXXXXXX/BXXXXXX/xxxxx"`

Set webhook_url and CHANNEL to the one provided by Slack when you [create the webhook]( https://my.slack.com/services/new/incoming-webhook/).

## Install dependencies

`yarn install`

## Zip before upload

Files in teh artifact zip need to be in root folder.

`zip -rq ../lamdba_db_poll$(date +%Y%m%d-%H%M%S).zip *`
