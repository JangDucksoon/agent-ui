import gradio as gr
import requests

def chat_fn(message, history):
    if not message.strip():
        return []

    payload = {"message": message}
    final_answer = ""

    with requests.post('http://127.0.0.1:8999/chat/stream', json=payload, stream=True) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if not chunk:
                continue

            final_answer += chunk
            yield final_answer

gr.ChatInterface(fn=chat_fn).launch()