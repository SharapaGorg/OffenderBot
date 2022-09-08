from aiogram.utils import executor
from utils import startup
from controller import dp

# activate commands (do not delete)
import handlers

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=startup)