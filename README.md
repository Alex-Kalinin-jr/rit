## Microservice MONGODB+FASTAPI+TELEGRAM BOT example

Small microservice app for interaction between telegram bot and mongoDB

- Go to **develop** branch
- Go into bot directory
- Toucn **.env** file and fill it with content:

TELEGRAM_TOKEN="your-telegram-bot-token"<br>
NGROK_AUTHTOKEN="your-ngrok-token"

- Launch **make up**
- Enjoy. You can pass to bot the next data:
{<br>
"dt_from":"2022-09-01T00:00:00",<br>
"dt_upto":"2022-12-31T23:59:00",<br>
"group_type":"month"<br>
}<br>
where **dt_from** is start date for aggregation of paid sums, **dt_upto** is end date for aggregation, **group_type** is type of aggregation with possible values: **day**, **month**, **hour**.

Mongo is automatically filled up with example dataset from ***.bson** file and
in telegram you will recieve aggregated datasets.

- for tests launch **make test** while app is running.
