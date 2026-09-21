from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, inference, room_io, TurnHandlingOptions
from livekit.plugins import ai_coustics

load_dotenv(".env.")


# System Prompts
VOICE_INSTRUCTIONS = """You are a helpful voice AI assistant.
You eagerly assist users with their questions by providing information from your extensive knowledge.
Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
You are curious, friendly, and have a sense of humor."""

CHAT_INSTRUCTIONS = """You are Avora, a professional and highly capable AI assistant.
Your goal is to be helpful, precise, and insightful.
You use clean Markdown formatting to make your responses easy to read.
You maintain a professional yet friendly tone, similar to Claude.
When providing code, use proper language blocks.
When listing items, use clear bullet points.
Your responses should be comprehensive but avoid unnecessary fluff."""

# Shared Model Config
MODEL_ID = "google/gemma-4-31b-it"

class Assistant(Agent):
    def __init__(self, instructions=VOICE_INSTRUCTIONS) -> None:
        super().__init__(
            instructions=instructions,
        )


server = AgentServer()

@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3", language="multi"),
        llm=inference.LLM(model=MODEL_ID),
        tts=inference.TTS(
            model="inworld/inworld-tts-2",
            voice="Ashley",
        ),
        turn_handling=TurnHandlingOptions(
            turn_detection=inference.TurnDetector(),
        ),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=ai_coustics.audio_enhancement(model=ai_coustics.EnhancerModel.QUAIL_VF_S),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)