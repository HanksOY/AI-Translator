import os
from dotenv import load_dotenv

load_dotenv()

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    cartesia,
    noise_cancellation,
    assemblyai,
    silero,
)



class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI language translator. ")


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=assemblyai.STT(
        end_of_turn_confidence_threshold=0.7,
        min_end_of_turn_silence_when_confident=160,
        max_turn_silence=2400,
        ),
        llm=google.LLM(model="gemini-1.5-flash"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(), #Voice activity detection (VAD) detects periods of silence in user input
        turn_detection="stt",# know when to start listening and when to respond
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
            ws_url=os.getenv("LIVEKIT_URL"),
        )
    )