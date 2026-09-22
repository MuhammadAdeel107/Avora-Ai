"""
Avora AI - Voice Assistant Interface
A clean, self-contained Gradio 6.x app: sidebar with brand/status/voice
controls/mic/chat, and a center panel with an animated voice visualizer.
"""

import gradio as gr
from dotenv import load_dotenv

load_dotenv(".env")


# =========================================================
# BACKEND LOGIC
# =========================================================

def toggle_voice(is_running: bool):
    """Flip voice-listening state and update status texts + button label."""
    is_running = not is_running

    if is_running:
        return (
            True,
            "LISTENING",
            "Avora is listening. You can speak now.",
            "⏸  PAUSE VOICE",
        )

    return (
        False,
        "READY",
        "Voice assistant is paused.",
        "●  START VOICE",
    )


def send_message(message: str, history: list):
    """Append the user's message + a placeholder agent reply to the chat."""
    if not message or not message.strip():
        return history, ""

    history = history or []
    history.append({"role": "user", "content": message})
    history.append(
        {"role": "assistant", "content": "Your LiveKit agent response will appear here."}
    )

    return history, ""


def clear_chat():
    return [], ""


# =========================================================
# CSS  (kept simple + specific to avoid clashing with Gradio's own DOM)
# =========================================================

CSS = r"""
:root {
    --avora-bg: #ffffff;
    --avora-sidebar: #f8f9fb;
    --avora-panel: #ffffff;
    --avora-border: #e5e7eb;
    --avora-text: #171717;
    --avora-muted: #737780;
    --avora-accent: #6366f1;
    --avora-accent-2: #8b5cf6;
}

.dark {
    --avora-bg: #101114;
    --avora-sidebar: #17181c;
    --avora-panel: #202126;
    --avora-border: #303137;
    --avora-text: #f5f5f5;
    --avora-muted: #9a9ca5;
}

.avora-shell {
    display: flex;
    gap: 0;
    min-height: 88vh;
    background: var(--avora-bg);
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid var(--avora-border);
}

.avora-sidebar {
    background: var(--avora-sidebar) !important;
    border-right: 1px solid var(--avora-border) !important;
    padding: 20px 16px !important;
}

.avora-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 16px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--avora-border);
}

.avora-brand-icon {
    width: 38px;
    height: 38px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 11px;
    background: linear-gradient(135deg, var(--avora-accent), var(--avora-accent-2));
    color: white;
    font-size: 18px;
}

.avora-brand-name {
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: var(--avora-text);
}

.avora-brand-sub {
    margin-top: 2px;
    color: var(--avora-muted);
    font-size: 10px;
    letter-spacing: 1.2px;
}

.avora-label {
    color: var(--avora-muted) !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1.2px !important;
    margin: 14px 0 6px 0 !important;
}

.avora-voice-btn {
    background: linear-gradient(135deg, var(--avora-accent), var(--avora-accent-2)) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
}

.avora-center {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    background: radial-gradient(circle at center, rgba(99,102,241,0.06), transparent 55%);
    padding: 24px;
}

.avora-center h1 {
    margin: 0 0 4px 0;
    color: var(--avora-text);
    font-size: 26px;
    font-weight: 700;
    text-align: center;
}

.avora-center p {
    margin: 0 0 20px 0;
    color: var(--avora-muted);
    font-size: 12px;
    text-align: center;
}

.avora-visualizer {
    width: min(38vw, 320px);
    aspect-ratio: 1 / 1;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.avora-ring {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(99,102,241,0.18);
}
.avora-ring.r1 { width: 100%; height: 100%; }
.avora-ring.r2 { width: 78%;  height: 78%;  }
.avora-ring.r3 { width: 56%;  height: 56%;  }

.avora-core {
    width: 30%;
    aspect-ratio: 1;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(145deg, #ffffff, #eef0f7);
    border: 1px solid #dfe3ec;
    box-shadow: 0 12px 40px rgba(99,102,241,0.15);
    font-size: 34px;
    z-index: 2;
}

.dark .avora-core {
    background: linear-gradient(145deg, #2a2c34, #16171b);
    border-color: rgba(255,255,255,0.12);
}

.avora-visualizer.listening .avora-ring {
    animation: avoraPulse 1.8s ease-in-out infinite;
}
.avora-visualizer.listening .avora-ring.r2 { animation-delay: 0.15s; }
.avora-visualizer.listening .avora-ring.r3 { animation-delay: 0.3s; }
.avora-visualizer.listening .avora-core {
    animation: avoraCore 0.9s ease-in-out infinite alternate;
}

@keyframes avoraPulse {
    0%   { transform: scale(0.92); opacity: 0.3; }
    50%  { transform: scale(1.06); opacity: 0.9; }
    100% { transform: scale(0.92); opacity: 0.3; }
}
@keyframes avoraCore {
    from { transform: scale(0.97); }
    to   { transform: scale(1.05); }
}

.avora-status-line {
    margin-top: 18px;
    color: var(--avora-muted);
    font-size: 10px;
    letter-spacing: 2px;
}

.avora-info {
    margin-top: auto;
    padding-top: 14px;
    color: var(--avora-muted);
    font-size: 10px;
    line-height: 1.5;
    border-top: 1px solid var(--avora-border);
}
"""

# JS: mic control via the browser's built-in SpeechRecognition API,
# and a tiny helper to toggle the pulsing ring animation + dark mode.
VOICE_JS = r"""
() => {
    const textarea = document.querySelector(".avora-chat-input textarea");
    const visualizer = document.querySelector(".avora-visualizer");

    if (!window.avoraVoice) {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        window.avoraVoice = { recognition: SR ? new SR() : null, running: false };

        if (window.avoraVoice.recognition) {
            const r = window.avoraVoice.recognition;
            r.continuous = true;
            r.interimResults = true;
            r.lang = "en-US";

            r.onresult = (event) => {
                if (!textarea) return;
                let text = "";
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) text += event.results[i][0].transcript + " ";
                }
                if (text.trim()) {
                    textarea.value = text.trim();
                    textarea.dispatchEvent(new Event("input", { bubbles: true }));
                }
            };
            r.onerror = () => { window.avoraVoice.running = false; };
            r.onend = () => { if (window.avoraVoice.running) { try { r.start(); } catch (e) {} } };
        }
    }

    const v = window.avoraVoice;
    if (!v.recognition) {
        alert("Speech recognition isn't supported in this browser. Try Chrome or Edge.");
        return;
    }

    if (!v.running) {
        v.running = true;
        if (visualizer) visualizer.classList.add("listening");
        try { v.recognition.start(); } catch (e) {}
    } else {
        v.running = false;
        if (visualizer) visualizer.classList.remove("listening");
        try { v.recognition.stop(); } catch (e) {}
    }
}
"""

THEME_JS = r"""
() => {
    document.querySelector(".avora-shell").classList.toggle("dark");
}
"""


# =========================================================
# UI
# =========================================================

with gr.Blocks(title="Avora AI") as demo:
    voice_state = gr.State(False)

    with gr.Row(elem_classes="avora-shell"):

        # ---------------- SIDEBAR ----------------
        with gr.Column(scale=0, min_width=280, elem_classes="avora-sidebar"):

            gr.HTML(
                """
                <div class="avora-brand">
                    <div class="avora-brand-icon">✦</div>
                    <div>
                        <div class="avora-brand-name">AVORA</div>
                        <div class="avora-brand-sub">AI VOICE ASSISTANT</div>
                    </div>
                </div>
                """
            )

            gr.Markdown("STATUS", elem_classes="avora-label")
            status = gr.Textbox(value="READY", show_label=False, interactive=False)
            status_message = gr.Markdown("Press Start Voice to begin.")

            gr.Markdown("VOICE", elem_classes="avora-label")
            voice_button = gr.Button("●  START VOICE", elem_classes="avora-voice-btn")

            gr.Markdown("MICROPHONE", elem_classes="avora-label")
            microphone = gr.Audio(sources=["microphone"], type="filepath", show_label=False)

            gr.Markdown("CHAT", elem_classes="avora-label")
            chatbot = gr.Chatbot(show_label=False, height=220)

            with gr.Row():
                text_input = gr.Textbox(
                    placeholder="Message...",
                    show_label=False,
                    scale=4,
                    elem_classes="avora-chat-input",
                )
                send_button = gr.Button("Send", scale=1)

            clear_button = gr.Button("Clear chat", size="sm")

            gr.Markdown("APPEARANCE", elem_classes="avora-label")
            theme_button = gr.Button("☾  Dark mode")

            gr.HTML(
                """
                <div class="avora-info">
                    <b>Avora AI</b><br>
                    Personal voice assistant<br>
                    LiveKit · Deepgram · Gemma · Inworld
                </div>
                """
            )

        # ---------------- CENTER ----------------
        with gr.Column(scale=1, elem_classes="avora-center"):
            gr.HTML(
                """
                <h1>Your AI Assistant</h1>
                <p>Speak naturally and let Avora help.</p>
                <div class="avora-visualizer">
                    <div class="avora-ring r1"></div>
                    <div class="avora-ring r2"></div>
                    <div class="avora-ring r3"></div>
                    <div class="avora-core">🎙</div>
                </div>
                <div class="avora-status-line">AVORA VOICE ENGINE</div>
                """
            )

    # ---------------- EVENTS ----------------
    voice_button.click(
        fn=toggle_voice,
        inputs=[voice_state],
        outputs=[voice_state, status, status_message, voice_button],
        js=VOICE_JS,
    )

    send_button.click(
        fn=send_message,
        inputs=[text_input, chatbot],
        outputs=[chatbot, text_input],
    )
    text_input.submit(
        fn=send_message,
        inputs=[text_input, chatbot],
        outputs=[chatbot, text_input],
    )
    clear_button.click(fn=clear_chat, outputs=[chatbot, text_input])

    theme_button.click(fn=None, js=THEME_JS)


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        theme=gr.themes.Base(),
        css=CSS,
    )