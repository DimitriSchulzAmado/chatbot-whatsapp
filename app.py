import time
import random

from flask import Flask, request, jsonify
from services.waha import Waha
from bot.ai_bot import AIBot


app = Flask(__name__)

@app.route('/api/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['payload']['from']
    received_message = data['payload']['body']
    is_group = '@g.us' in chat_id
    is_status = 'status@broadcast' in chat_id
    
    if is_group or is_status:
        return jsonify({'status': 'success', 'message': 'Group/status message ignored'}), 200
    
    waha = Waha()
    ai_bot = AIBot()

    waha.start_typing(chat_id=chat_id)

    response = ai_bot.invoke(user_message=received_message)
    waha.send_message(
        chat_id=chat_id,
        message=response,
    )
    waha.stop_typing(chat_id=chat_id)

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
