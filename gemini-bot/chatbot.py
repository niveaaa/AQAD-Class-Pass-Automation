import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDJThh_yBZxBxo5LT2O8IcXE6NZ15Kf7sE")

model = genai.GenerativeModel('gemini-1.5-flash')

#response = model.generate_content("Write a story about an AI and magic")
#print(response.text)

chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)

while True: 
    response = chat.send_message(input("Send Message: "))
    print(response.text)
