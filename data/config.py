BOT_TOKEN = '5349137146:AAEhEOYgN0BZYq9Pao2otgGHBiejz9WrUgc'

PROJECT_NAME = 'tg-bot-delivery'

WEBHOOK_HOST = f"https://{PROJECT_NAME}.herokuapp.com"
WEBHOOK_PATH = '/webhook/' + BOT_TOKEN
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
DB_URI = "postgres://yeltmzlfdttraj:09503e6d76ea6183612ed1e57e1373d1e23c4c31ac5459910dd9bd464958a02b@ec2-52-30-67-143.eu-west-1.compute.amazonaws.com:5432/dgbgiq2gihjue"

ADMINS = [000000000, 1234567890]
