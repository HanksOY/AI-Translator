from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io
from livekit.plugins import noise_cancellation, silero, google, elevenlabs, openai
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv(".env")

import os
print(f"ELEVEN_API_KEY loaded: {bool(os.environ.get('ELEVEN_API_KEY'))}")
print(f"ELEVEN_API_KEY length: {len(os.environ.get('ELEVEN_API_KEY', ''))}")
print(f"GOOGLE_API_KEY loaded: {bool(os.environ.get('GOOGLE_API_KEY'))}")
print(f"OPENAI_API_KEY loaded: {bool(os.environ.get('OPENAI_API_KEY'))}")

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a professional translator conducting a translation between two languages.
            The LangGraph workflow will drive the conversation flow.
            Simply translate the content as they come from the graph.
            Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
            Be conversational, professional, and helpful throughout the translation process.""",
        )

server = AgentServer()

@server.rtc_session() # Register the next function as a WebRTC session handler. LiveKit will now know: Every time a user joins a room → run my_agent. Without this decorator, LiveKit would never call your function.
# Async is mainly for handling multiple “waiting things” (I/O tasks) at the same time:
# receiving audio packets from WebRTC (continuous), sending audio to ElevenLabs STT (streaming) and receiving partial transcripts, running VAD + turn detection continuously, calling Gemini (network) and waiting for tokens, calling ElevenLabs TTS (network) and receiving audio chunks, playing TTS audio while still listening for interruptions (“barge-in”), timers / keepalives / reconnect
# ctx: LiveKit’s object that represents one live voice call — it’s how your code knows which user and which audio stream it should attach the AI to. It is automatically created by LiveKit and passed into your function
async def my_agent(ctx: agents.JobContext): 
    session = AgentSession(
        stt=openai.STT(
            model="gpt-4o-mini-transcribe-2025-12-15",
            detect_language=True,
        ),
        llm=google.LLM(
            model="gemini-2.0-flash",
        ),
        tts=elevenlabs.TTS(
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel - or choose another voice
            model="eleven_turbo_v2_5",  # Latest fast multilingual model
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    # Start a live call: keep listening, transcribing, replying, speaking… until the user leaves. If you removed await, it would mean:“Start attaching… but immediately continue and exit the function, so the agent gets cleaned up / ends.”
    await session.start(
        room=ctx.room, 
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)