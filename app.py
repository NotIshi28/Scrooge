from bot.bot_handler import InputHandler
from bot.speech_handler import SpeechHandler
import sys
import time
from flask import Flask, jsonify
from bot.utils.logger import app_logger as logger
import threading
import os

print('Bot is running')
input_handler = None

bot_thread = None
is_running = False

print('Server is running')
app = Flask(__name__)

def create_handler():
    global input_handler
    if input_handler is not None:
        try:
            input_handler.stop()
        except:
            pass
    input_handler = InputHandler()
    return input_handler

def bot_worker():
    try:
        input_handler.mainLoop()
    except Exception as e:
        logger.error(f"Error in bot_worker: {e}")
        input_handler.stop()


@app.route('/api',methods=['GET'])
def hello_world():
    return jsonify({"message": "hello world"})

stop_threads = False

input_handler = InputHandler()




@app.route('/api/start', methods=['GET', 'POST'])
def start_service():
    global bot_thread, is_running, input_handler, stop_threads
    
    if is_running:
        return jsonify({"status": "info", "message": "Service already running"})
    
    try:
        
        logger.info("Starting service...")
        
        # if input_handler is not None:
        #     try:
        #         # input_handler.stop()
        #     except:
        #         pass
        input_handler.start()
                    
        # bot_thread = threading.Thread(target=input_handler.mainLoop)
        # bot_thread.daemon = True
        # bot_thread.start()

        input_handler.is_running = True
        
        def announce():
            sh = SpeechHandler()
            sh.speak("Service started")
        announce()
        
        logger.info("Service successfully started")
        return jsonify({"status": "success", "message": "Service started"})
    
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        return jsonify({"status": "error", "message": f"Failed to start service: {str(e)}"})

@app.route('/api/stop',methods=['GET', 'POST'])
def stop_service():
    global is_running, bot_thread, input_handler, stop_threads
    print("milgyi request")
    if not input_handler.is_running:
        return jsonify({"status": "info", "message": "Service already stopped"})
    
    try:
        logger.info("Stopping service...")
        
        
        if input_handler is not None:
            input_handler.stop()
        
        if bot_thread and bot_thread.is_alive():
            logger.info("Waiting for bot thread to finish...")
            bot_thread.join(timeout=5)

            if bot_thread.is_alive():
                logger.info("Bot thread did not finish in time, stopping it...")
                stop_threads = True
            
        is_running = False
        input_handler.is_running = False
        bot_thread = None

        input_handler = None

        def announce():
            sh = SpeechHandler()
            sh.speak("Service stopped")
        threading.Thread(target=announce).start()
        
        logger.info("Service successfully stopped")
        return jsonify({"status": "success", "message": "Service stopped"})
    
    except Exception as e:
        logger.error(f"Error stopping service: {e}")
        return jsonify({"status": "error", "message": f"Error stopping service: {str(e)}"})

@app.route('/api/status',methods=['GET', 'POST'])
def return_status():
    global is_running, input_handler
    try:
        if input_handler is None:
            return jsonify({
                "status": "stopped"
            })
        else:
            return jsonify({
                "status": "running" if input_handler.getStatus() else "stopped"
            })
    except Exception as e:
        logger.error(f"Error in status endpoint: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        })

@app.route('/api/settings',methods=['GET'])
def view_settings():
    sh = SpeechHandler()

    return 'Settings'



if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    logger.info(f"Starting Flask server on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)    