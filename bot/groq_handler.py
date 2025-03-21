from groq import Groq
import os
import time
import openai

from dotenv import load_dotenv

from bot.utils.logger import groq_logger as logger

load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')


openrouter_client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    default_headers={
        "X-Title: Zearry"
    }
)

groq_audio_client = Groq(api_key=GROQ_API_KEY)


logger.info("API clients init")

def getResponse(prompt, user_input, context=None):

    if(os.getenv("DEV") == "true"):
        return f"This is a test response just to check if the bot is working fine that includes both the input and the output, the user input is: {user_input}"
    
    else:
        messages = [{"role" : "system", "content" : prompt}]

        start_time = time.time()

        if context:
            recent_msgs = list(context)

            logger.info(f"using {len(recent_msgs)} recent messages for context")

            

            messages.append({"role" : "assistant", "content" : context})

        messages.append({"role" : "user", "content" : user_input})        

        try:
            response = openrouter_client.chat.completion.create(
                model="openai/gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )


            if hasattr(response, "choices") and len(response.choices) > 0:
                response_text = response.choices[0].message.content
            if isinstance(response, dict) and "choices" in response:
                response_text = response["choices"][0]["message"]["content"]

            elif isinstance(response, str):
                response_text = response
            
            elapsed_time = time.time() - start_time

            logger.info(
                f'API response received in {elapsed_time:.2f}s: "{response_text}"'
            )

            return response_text
        
        except Exception as e:
            logger.error(f"Error in getResponse: {e}")

            logger.info("attempting to fallback to groq")

            groq_client = openai.OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=GROQ_API_KEY
            )

            response = groq_client.chat.completions.create(
                model="gemma2-9b-it",
                messages=messages,
                temperature=0.7,
                max_tokens=150,
            )

            response_text = response.choices[0].message.content
            elapsed_time = time.time() - start_time

            logger.info(f"fallback response received in {elapsed_time:.2f}s: {response_text}")

            return response_text