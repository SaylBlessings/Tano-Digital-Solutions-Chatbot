import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from twilio.rest import Client

# Initialize Flask app
app = Flask(__name__)

class Chatbot:
    """WhatsApp Chatbot for Tano Digital Solutions Company Information"""
    CHATBOT_NAME = "Tano Digital Solutions Chatbot"
    
    def __init__(self):
        self.info_responses = {
            "about": "Tano Digital Solutions is a leading technology company based in Zimbabwe. We specialize in providing innovative solutions in software development, web development, and IT consulting services.",
            "services": "At Tano Digital Solutions, we offer a wide range of services including software development, web development, mobile app development, digital marketing, and IT consulting.",
            "contact": "You can reach us at Tano Digital Solutions via email at info@tanodigital.co.zw or by phone at +263 123 456 789. Our office is located at 123 Main Street, Harare, Zimbabwe."
        }
         
        self.gen_ai = genai.configure(api_key="AIzaSyAQc54eHT-3cms9WgB8cM4N1d6j3lhvPDg")
        # Initialize Twilio client
        self.twilio_client = Client("AC3c625c0fd94f88258708dcb626e3cf41 ", "c5aa6c81ba92e0daad34a6d36cf1165a ")
    
    def get_info_response(self, query):
        """Get company information based on user query"""
        query = query.lower()
        if query in self.info_responses:
            return self.info_responses[query]
        else:
            # Search for company information on the internet using Gemini API
            # You need to replace "YOUR_GEMINI_API_KEY_HERE" with your actual Gemini API key
            internet_info = self.gemini_api.search(query)
            # Generate additional information using Generative AI
            additional_info = self.gen_ai.generate_info(query)
            return internet_info + "\n" + additional_info

chatbot = Chatbot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Handle incoming messages and provide Tano Digital Solutions company information.
    """
    incoming_msg = request.values.get('Body', '').lower()

    # Get company information response based on user query
    response = chatbot.get_info_response(incoming_msg)

    # Prepare Twilio response
    resp = MessagingResponse()
    resp.message(response)

    return str(resp)

if __name__ == '__main__':
    app.run(debug=False)
