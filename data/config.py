BOT_TOKEN = '5278340360:AAEmA21RWM1dzothCw1IQoAc18Xb6Hjwrdo'

PROJECT_NAME = 'store-bot-example'

WEBHOOK_HOST = f"https://{PROJECT_NAME}.herokuapp.com"
WEBHOOK_PATH = '/webhook/' + BOT_TOKEN
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
DB_URI = "postgres://xmgdswtykrnjpa:6e3bade32ee29a658bca98af21a8916896e5c33b383c4048153107fbec8365d2@ec2-176-34-211-0.eu-west-1.compute.amazonaws.com:5432/dfqijgrnpc42tk"

ADMINS = [000000000, 1234567890]
