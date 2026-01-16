import gradio as gr
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:5000/simon")
SESSION_ID = "gradio-session"

def chat(message, history):
    """
    Send message to /simon endpoint and return response
    """
    try:
        response = requests.post(
            API_URL,
            json={
                "message": message,
                "session_id": SESSION_ID
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get("reply", "No response")
            
            # Display actions if any
            actions = data.get("actions", [])
            if actions:
                reply += f"\n\n**Actions**: {actions}"
            
            return reply
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Connection error: {str(e)}. Make sure the API server is running on {API_URL}"

# Create Gradio interface
with gr.Blocks(title="AI Chat Interface") as demo:
    gr.Markdown("# AI Chat Interface")
    gr.Markdown("Chat with your autonomous AI assistant powered by DeepSeek")
    
    chatbot = gr.Chatbot(
        height=500,
        bubble_full_width=False,
    )
    
    msg = gr.Textbox(
        placeholder="Type your message here...",
        show_label=False,
        container=False
    )
    
    clear = gr.Button("Clear Chat")
    
    msg.submit(chat, [msg, chatbot], [chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    print(f"Connecting to API at: {API_URL}")
    print("Starting Gradio interface...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
