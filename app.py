from flask import Flask, request, jsonify
import os
import requests
import json
from openai import OpenAI

app = Flask(__name__)

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Webhook is running'})

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get update from Telegram
        update = request.json
        
        # Extract message info
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            user_text = message.get('text', '')
            
            if user_text:
                # Get response from OpenAI
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_text}
                    ],
                    max_tokens=500
                )
                
                ai_response = response.choices[0].message.content
                
                # Send response back to Telegram
                send_message(chat_id, ai_response)
        
        return jsonify({'status': 'success'})
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)}), 500

def send_message(chat_id, text):
    """Send message to Telegram chat"""
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f'Failed to send message: {str(e)}')
        return None

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set up Telegram webhook"""
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook'
    data = {'url': f'{WEBHOOK_URL}/webhook'}
    
    try:
        response = requests.post(url, json=data)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
