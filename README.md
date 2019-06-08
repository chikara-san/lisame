# lisame

The lisame is a reference implementation to open your home doors with SESAME smart lock system from 
the LINE text messaging service. The author uses heroku for his web server to bridge SESAME and LINE, but it can
be another service if you would like. 

- SESAME https://ameblo.jp/candyhouse-inc/
- LINE https://developers.line.biz/en/
- Heroku https://heroku.com

## Prerequisite

 - Git basic knowledge
 - curl usage
 
 
### Sesame API KEY and your sesame device ID

First obtain your SESAMEs API KEY for your account. 
https://docs.candyhouse.co/#tutorial-1-api-postman 
Next you can get device id(s) with next command
```bash
curl -H "Authorization: <YOUR API KEY>" https://api.candyhouse.co/public/sesames
```
The response from API is like this. devece_ids are needed for the configuration. Note them. 
```json
[
    {
        "device_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX",
        "serial": "XXXXXXXXXXXX",
        "nickname": "Sesame man"
    },
    {
        "device_id": "YYYYYYYY-YYYY-YYYY-YYYY-YYYYYYYYYYY",
        "serial": "YYYYYYYYYYYY",
        "nickname": "Sesame lady"
    }
    ...
]
```

### Heroku sign up

Heroku is an application platform. Sign up from next: https://signup.heroku.com/
and install Heroku CLI https://devcenter.heroku.com/articles/heroku-cli

```bash
$ heroku login

heroku: Press any key to open up the browser to login or q to exit:
Opening browser to https://cli-auth.heroku.com/auth/browser/XXXX
Logging in... done
Logged in as <YOUR MAIL ADDRESS>
```
```bash
$ heroku create <YOUR APP NAME>

Creating <YOUR APP NAME>... done
https://<YOUR APP NAME>.herokuapp.com/ | https://git.heroku.com/<YOUR APP NAME>.git
```

```bash
$ heroku plugins:install heroku-config

```
### Line developer registration

Register as LINE developers. https://developers.line.biz/en/.

- Create a channel as a Messaging API.
- Turn on "Webhook URL". Also fill the Web hook URL as `https://<YOUR APP NAME>.herokuapp.com/callback`
- Note Channel secret key for the configuration

Also, the channel access token set to the Line channel. This is used in the configuration

### LINE bot 

Find your LINE bot with QR code from Add friends icon the top right from the entry page of LINE app. 

## deployment

```bash
$ git clone
$ cd lisame
```

Set environment variable to .env in the top directory. 
```editorconfig
LINE_CHANNEL_SECRET=
LINE_CHANNEL_ACCESS_TOKEN=
AUTH_KEY=
KEYWORD="Open sesame" # Your preference keyword to open your home door
ENDPOINTS=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX;YYYYYYYY-YYYY-YYYY-YYYY-YYYYYYYYYYY # device_ids of SESAME smart locks
```
To deploy your configuration and code to Heroku, put the next commands and it's end of all preparation!
```bash
$ heroku git:clone -a <YOUR APP NAME>
$ cd <YOUR APP NAME>
$ heroku login
$ heroku config:push
$ git push heroku master 
```

