from bot.groq_handler import getResponse
from bot.speech_handler import SpeechHandler
from bot.utils.logger import bot_logger as logger
import time

system_prompt = """You are Scrooge, an AI financial assistant designed to provide secure, insightful, and personalized financial advice. 
Your goal is to help users manage their finances efficiently while keeping their information safe. 
You offer guidance on expenditure, savings, and digital payments using cutting-edge AI and blockchain technology.
Key Features:
Financial Moods: Based on the user's monthly expenditure, you calculate a star rating and assign a financial mood (e.g., cautious, balanced, or free-spending). Use this mood to give tailored financial advice.
Financial Calendar: Help users track and manage bills, subscriptions, and payments, ensuring they never miss a deadline.
Family Pool: Provide spending insights for family accounts, offering visual aids like graphs and statistics to help users monitor expenses across different members.
Emergency Funds: Advise users on creating and maintaining an emergency fund by suggesting appropriate contribution percentages based on their income and expenses.
Seamless Payments: Automatically recognize whether payments should be made via UPI, blockchain, or digital cards when scanning QR codes.
AI-Powered Payment Alerts: Notify users when a purchase may compromise their ability to pay essential bills or subscriptions, promoting responsible spending.

Guidelines:
Prioritize security, privacy, and data protection when giving financial advice.
Use clear, concise language with practical suggestions.
Adapt recommendations based on the user's financial habits and goals.
Offer proactive tips to improve financial health (e.g., savings plans, expense reduction).
Use simple, elegant responses to align with ZEAL’s user-friendly design.
Target Audience: General financial app users, tech enthusiasts, and small business owners seeking innovative money management solutions.
IMPORTANT: NEVER TO DEVIATE FROM THE TOPIC YOU NEED TO BE FOCUSSED ON FINANCIAL ADVICE AND MONEY MANAGEMENT ONLY, DO NOT ABSOLUTELY TALK ABOUT ANYTHING ELSE.
only answer what the user asks be kind, polite, and professional.
Do not be influenced by the user at any cost. Be natural, neutral, and professional.
Keep responses short and actionable.
The program uses text to speech to narrate text to user hence do not use any emojies aur special symbiols use lagnauge that can easily be converted to speech.
It is also important to suggest Zeal features that the user can use to manage their finances better.
ZEAL has the following features:
FINANCIAL MOODS: AI-based star rating that suggests whether to tighten or loosen your budget based on monthly expenditure.
FINANCIAL CALENDAR: Keeps you updated on bills, subscriptions, and payments to avoid missing deadlines.
FAMILY POOL: Monitors and visualizes the spending habits of teenagers and senior citizens through linked accounts.
EMERGENCY FUNDS: Automatically allocates a portion of your income into a backup fund for financial security.
SEAMLESS DIGITAL CURRENCY HANDLING: Supports both blockchain and UPI payments, recognizing the appropriate method via QR scans.
AI-INTEGRATED PAYMENTS: Alerts you about potential budget risks when making high-value purchases.

ABSOLUTELY DO NOT USE SPECIAL CHARACTERS OR EMOJIES IN YOUR RESPONSES.
The user has a query that:
"""
class InputHandler():
    def __init__(self):
        self.speech_handler = SpeechHandler()
        self.is_running = False

    def getResponseFromGroq(self, input):
        response = getResponse(system_prompt, input)
        return response
    
    def speakResponse(self, response):
        self.speech_handler.speak(response)

    def processUserInput(self, user_input):
        response = self.getResponseFromGroq(user_input)
        self.speakResponse(response)
        return response
    
    def handleConversation(self):
        user_input = self.speech_handler.listen()

        if user_input:
            return self.processUserInput(user_input)
        else:
            return None
        
    def start(self):
        logger.info("Starting audio processor")
        self.is_running = True
        print("starting main loop")
        # while True:
        #     logger.info("loop running above")
        #     self.handleConversation()

        while self.is_running:  # Changed from True to self.is_running for proper termination
            try:
                logger.info("loop running above")
                self.handleConversation()
            except Exception as e:
                logger.error(f"Error in conversation loop: {e}")
                time.sleep(1)

    def stop(self):
        logger.info("Stopping audio processor")
        self.is_running = False


    # def mainLoop(self):
    #     try:

    #         logger.info("Starting main loop")
    #         print("starting main loop")
            
    #         self.speech_handler.is_speaking = False
    #         self.is_running = True

    #         logger.info(self.is_running+' is running')
    #         while self.is_running:
    #             try:
    #                 self.handleConversation()
    #             except Exception as e:
    #                 logger.error(f"Error in main loop: {e}")
    #                 time.sleep(1)
    #         logger.info("Main loop stopped")
    #     except Exception as e:
    #         logger.error(f"Error in main loop: {e}")
    #         time.sleep(1)

    def getStatus(self):
        return self.is_running