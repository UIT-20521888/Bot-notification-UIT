import asyncio
import telegram
from datetime import date



my_token = '5637440964:AAFGSkLJY2OFKniBsrlkc-UJcAxqcxWNiss'
my_id = "5739747518"

bot = telegram.Bot(my_token)
async def send_message(text_message):    
    '''send message'''
    async with bot:
        await bot.send_message(text=text_message, chat_id=my_id)


if __name__ == '__main__':
    today = date.today()
    content = 'Today\'s date: ' + str(today.strftime("%b-%d-%Y"))
    # print(content)
    asyncio.run(send_message(content))