import google.generativeai as genai
import os

# ඔබේ API Key එක මෙහි ඇතුළත් කරන්න
api_key = "AIzaSyBi6ly3f3tDo8-97Y4VznhBfw80qrGodMo"
genai.configure(api_key=api_key)

print("ලබාගත හැකි Models ලැයිස්තුව:\n")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Name: {m.name}")
except Exception as e:
    print(f"Error: {e}")