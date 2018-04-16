# Third party integrations

## Setup Github OAuth2 App Integration (Recommended)

Navigate to: [Github - New Application](https://github.com/settings/applications/new) and enter similar values to:

* Enter Application Name: `MyGitcoinApp`
* Homepage URL: `http://localhost`
* Application description: `My Gitcoin App`
* Authorization callback URL: `http://localhost:8000/` (required)

The authorization callback URL should match your `BASE_URL` value in `web/app/app/.env`

Update the `web/app/app/.env` file to include the values provided by Github:

```shell
GITHUB_CLIENT_ID=xxxx
GITHUB_CLIENT_SECRET=xxx
GITHUB_APP_NAME=MyGitcoinApp
```

Restart your `web` container to apply the changes via:  `docker-compose restart web`

## Setup Github User Integration (Recommended)

Navigate to: [Github - New Token](https://github.com/settings/tokens/new)
At minimum, select `user` scope.

Update the `web/app/app/.env` file to include the values provided by Github:

```shell
GITHUB_API_TOKEN=xxx
GITHUB_API_USER=xxx
```

## Gitcoinbot Installation Instructions

### This integration requires the Github OAuth2 App Integration

Navigate to: [Gitcoinbot Github App](https://github.com/apps/gitcoinbot)
Copy the application ID found on the page as the `GITCOINBOT_APP_ID` environment variable.

The following environment variables must be set for gitcoinbot to work correctly:

```shell
GITHUB_API_USER=gitcoinbot  # Github Profile name of the bot. Defaults to: gitcoinbot
GITCOINBOT_APP_ID=APP_ID_FROM_ABOVE  # Defaults to empty.
GITCOIN_BOT_CERT_PATH=RELATIVE_PATH_TO_CERT_FILE  # Defaults to empty.
```

#### Example

```shell
GITHUB_API_USER=gitcoinbot  # Github Profile name of the bot. Defaults to: gitcoinbot
GITCOINBOT_APP_ID=7735  # Gitcoin Bot App ID
GITCOIN_BOT_CERT_PATH=app/gitcoin_bot_secret.pem  # If pem file is located at web/app/app/gitcoin_bot_secret.pem
```

Aside from these environment variables, the settings page of the gitcoin bot application must have the correct url for webhook events to post to. It should be set to `https://gitcoin.co/payload` based on urls.py line 131.

After running the migrations and deploying the gitcoin.co website, gitcoinbot will begin to receive webhook events from any repository that it is installed into. This application will then parse through the comments and respond if it is called with @gitcoinbot + registered action call.

## Rollbar Integration

Error tracking is entirely optional and primarily for internal staging and production tracking.
If you would like to track errors of your local environment, setup an account at: [Rollbar.com](https://rollbar.com)

Once you have access to your project access tokens, you can enable rollbar error tracking for both the backend and frontend by adding the following environment variables to `web/app/app/.env`:

```shell
ROLLBAR_CLIENT_TOKEN=post_client_item
ROLLBAR_SERVER_TOKEN=post_server_item
```