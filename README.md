# Avora AI - Real-Time Voice Assistant

Avora AI is an enterprise-grade, real-time interactive voice assistant built on the LiveKit architecture, integrating advanced speech recognition, large language models, and neural text-to-speech synthesis based on your implementation.

## System Architecture

The application relies on the following core components and service providers defined in your source code:
- **Core Framework**: LiveKit Agents framework (`AgentServer`, `AgentSession`) for real-time WebRTC room management and session handling.
- **Speech-to-Text (STT)**: Deepgram Nova-3 model (`deepgram/nova-3`) configured for multi-language transcription.
- **Large Language Model (LLM)**: Google Gemma model (`google/gemma-4-31b-it`) optimized for conversational agent responses.
- **Text-to-Speech (TTS)**: Inworld TTS engine (`inworld/inworld-tts-2`) utilizing the Ashley voice profile for synthetic speech generation.
- **Acoustic Enhancement**: Integrated noise cancellation through AI-driven audio processing models (`ai_coustics`).

## Technical Specifications

- **Language**: Python
- **Core Dependencies**: 
  - `livekit`
  - `livekit-agents`
  - `python-dotenv`

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/MuhammadAdeel107/Avora-Ai.git](https://github.com/MuhammadAdeel107/Avora-Ai.git)
   cd Avora-Ai
