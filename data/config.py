BOT_TOKEN = '5278340360:AAEmA21RWM1dzothCw1IQoAc18Xb6Hjwrdo'

PROJECT_NAME = 'store-bot-example'

WEBHOOK_HOST = f"https://{PROJECT_NAME}.herokuapp.com"
WEBHOOK_PATH = '/webhook/' + BOT_TOKEN
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
DB_URI = "postgres://evhdxwaqxcowbu:35f37f26c91c015af5e4d3eb0d5ec326e1597f178336bffb0755d370680e2d25@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/detshm2lk759f8"

ADMINS = [000000000, 1234567890]
