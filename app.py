from bot.bot_handler import InputHandler
import sys
import time

print(sys.argv[1])

if sys.argv[1] == 'bot':
    print('Bot is running')
    from bot.bot_handler import InputHandler
    input_handler = InputHandler()
    while True:
        input_handler.handleConversation()
        print("hlo")