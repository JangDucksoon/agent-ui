import gradio as gr
import requests

def chat_fn(message, history):
    if not message.strip():
        return history, gr.update()

    history = history + [[message, ""]]
    yield history, gr.update(value="")

    payload = {"message": message}
    final_answer = ""

    history[-1][1] = '<div class="typing-indicator"><span></span><span></span><span></span></div>'
    yield history, gr.update()

    with requests.post('http://127.0.0.1:8999/chat/stream', json=payload, stream=True) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if not chunk:
                continue
            final_answer += chunk
            history[-1][1] = f"{final_answer}<br><div class='typing-indicator'><span></span><span></span><span></span></div>"
            yield history, gr.update()

    history[-1][1] = final_answer
    yield history, gr.update()


css = """
.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
}
.typing-indicator span {
  width: 6px;
  height: 6px;
  background: #666;
  border-radius: 50%;
  display: inline-block;
  animation: blink 1.4s infinite both;
}
.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}
.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes blink {
  0%, 80%, 100% { opacity: 0; }
  40% { opacity: 1; }
}
"""

with gr.Blocks(css=css) as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    msg.submit(chat_fn, inputs=[msg, chatbot], outputs=[chatbot, msg])

demo.launch()
