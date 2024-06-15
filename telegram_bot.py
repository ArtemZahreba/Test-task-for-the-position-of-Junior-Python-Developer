# Import necessary modules for the bot using aiogram and the main program class
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

from main import MainProgram

# Create an instance of the main program
program = MainProgram()

# Telegram API token
API = '5913335392:AAEpoOAsSO1saRKIHDkb3f-pbYDz5DqUWEc'

# Bot object
bot = Bot(token=API)
# Dispatcher
dp = Dispatcher()


# Handler for the /start command
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Function to send a message in response to the /start command.

    :param message: The incoming message from the user.
    :return: None
    """
    await message.answer(
        '''
Hello!
This is a test task implementation, specifically:

Part 1. Implement a parser for the number of vacancies on the robota.ua website for the keyword "junior".

Part 2. Implement a Telegram bot to get vacancy statistics.
        '''
    )


# Handler for the /get_today_statistic command
@dp.message(Command("get_today_statistic"))
async def get_today_statistic(message: types.Message):
    """
    Function to send a file in response to the /get_today_statistic command.

    :param message: The incoming message from the user.
    :return: None
    """
    # Get the file path from the main program
    file = FSInputFile(
        path=program.get_file()
    )

    # Send the document to the user
    await bot.send_document(
        message.chat.id,
        document=file
    )


# Function to start polling for new updates
async def main():
    """
    Function to start polling for new updates.

    :return: None
    """
    await dp.start_polling(bot)


# Function to start the program
async def run_bot():
    """
    Function to run the main program and the bot concurrently.

    :return: None
    """
    await asyncio.gather(program.run(), main())


if __name__ == "__main__":
    # Run the bot
    asyncio.run(run_bot())
