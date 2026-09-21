import asyncio
import gradio as gr
from dotenv import load_dotenv
from livekit.agents import inference, llm
from Avora import MODEL_ID, CHAT_INSTRUCTIONS

load_dotenv(".env")

# Initialize the LLM
# Note: Using the same model ID as Avora.py
llm_instance = inference.LLM(model=MODEL_ID)

# Custom CSS to achieve the "Claude Look"
CLAUDE_CSS = """
.gradio-container {
    background-color: #f9f9f8 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
}

#chatbot-container {
    background-color: transparent !important;
    border: none !important;
}

.chatbot {
    flex-grow: 1 !important;
    max-width: 800px !important;
    margin: 0 auto !important;
}

/* Message Bubbles */
.message {
    border-radius: 15px !important;
    padding: 12px 16px !important;
    line-height: 1.6 !important;
}

.user {
    background-color: #f0f0eb !important;
    color: #333 !important;
    border: 1px solid #e5e5df !important;
}

.bot {
    background-color: transparent !important;
    color: #1a1a1a !important;
    border: none !important;
}

/* Input Area */
#input-container {
    max-width: 800px !important;
    margin: 0 auto !important;
    padding-bottom: 20px !important;
}

.textbox input {
    border-radius: 20px !important;
    border: 1px solid #ddd !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important;
    padding: 12px 20px !important;
}

.footer {
    text-align: center;
    font-size: 12px;
    color: #888;
    margin-top: 10px;
}
"""

async def chat_stream(message, history):
    # Initialize ChatContext with the professional Chat Instructions
    chat_ctx = llm.ChatContext().append(
        role="system",
        text=CHAT_INSTRUCTIONS
    )

    # Add history to context
    for user_msg, bot_msg in history:
        chat_ctx.append(role="user", text=user_msg)
        chat_ctx.append(role="assistant", text=bot_msg)

    # Add current message
    chat_ctx.append(role="user", text=message)

    # Stream the response from Gemma-4
    full_response = ""
    async for chunk in llm_instance.chat(chat_ctx):
        full_response += chunk.choices[0].delta.content or ""
        yield full_response

def launch_voice():
    # This would ideally be a link to your LiveKit room
    # For now, we provide a helpful message or a mock URL
    return "Redirecting to Voice Session... (Ensure Avora.py is running)"

with gr.Blocks() as demo:
    with gr.Column(elem_id="main-column"):
        gr.Markdown(
            "# Avora",
            elem_id="title"
        )

        with gr.Row():
            with gr.Column(scale=1):
                # Sidebar for settings/links
                gr.Markdown("### Controls")
                voice_btn = gr.Button("🎙️ Launch Voice Mode", variant="primary")
                voice_status = gr.Markdown("")

                gr.Markdown(
                    """
                    **Avora Hybrid**
                    - Text Mode: Gemma-4-31B
                    - Voice Mode: LiveKit + Inworld
                    """
                )

        with gr.Column(elem_id="chatbot-container"):
            chatbot = gr.Chatbot(
                label="Conversation",
                elem_id="chatbot",
                show_label=False
            )


            with gr.Row(elem_id="input-container"):
                msg = gr.Textbox(
                    placeholder="Message Avora...",
                    show_label=False,
                    scale=9,
                    container=False
                )
                submit = gr.Button("Send", scale=1)

        gr.Markdown(
            "Powered by Gemma-4 • Built with Gradio & LiveKit",
            elem_classes="footer"
        )

    # Event Handlers
    msg.submit(chat_stream, [msg, chatbot], [chatbot])
    submit.click(chat_stream, [msg, chatbot], [chatbot]).then(
        lambda: "", None, msg # Clear input
    )

    voice_btn.click(launch_voice, None, voice_status)

if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=7860,
        css=CLAUDE_CSS,
        theme=gr.themes.Soft()
    )
