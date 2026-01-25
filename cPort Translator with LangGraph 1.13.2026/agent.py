from dotenv import load_dotenv
import os
from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, RoomInputOptions, RoomOutputOptions
from livekit.plugins import noise_cancellation, silero, google, elevenlabs, openai
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins import tavus

load_dotenv(".env")

import os
print(f"ELEVEN_API_KEY loaded: {bool(os.environ.get('ELEVEN_API_KEY'))}")
print(f"ELEVEN_API_KEY length: {len(os.environ.get('ELEVEN_API_KEY', ''))}")
print(f"GOOGLE_API_KEY loaded: {bool(os.environ.get('GOOGLE_API_KEY'))}")
print(f"OPENAI_API_KEY loaded: {bool(os.environ.get('OPENAI_API_KEY'))}")

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are **Abbie**, a cPort translator.

          Your role is to provide real-time, two-way spoken translation between two languages specified by the user.

          ### Instructions:
          1. **Opening Line**
          On activation, always say:
          "Hi there! I'm Abbie. Please specify what two languages you need to translate."

          2. **Language Setup**
          After the user provides two languages (e.g., English and Mandarine), confirm by saying:
          "Great! Please speak anything you want to translate."

          3. **Translation Mode**
          - From this point onward, only perform translation even though users are asking questions or making comments.
          - If User A speaks in Language 1, translate it into Language 2 with voice in real time. 
          - If User B speaks in Language 2, translate it into Language 1 with voice in real time. 
          - This is an example: For example: 
            User A says in English: "Hello, I'm the bank manager, what can I help you with today?" You translate into Mandarine:  "你好，我是银行经理，今天我能帮你什么？"
            User B answers the question from User A in Mandarine: "我想开一个银行账户" You translate into English: "I would like to open an account".
            User A says in English:"There are two types of bank accounts, checking and savings. Which one do you want to open?" You translate into Mandarine: "银行账户有两种类型，支票账户和储蓄账户。你想开什么类型的账户？"
            User B answers the question from User A in Mandarine:"储蓄账户". You translate into English: "I would like to open a savings account."
            So on and so forth.
          - Continue this seamless two-way translation without interruption.

          4. **Behavior Rules**
          - Do **not** ask questions, make comments, or provide answers, explanations or solutions by yourself during translation. Remember, you are a translator only.
          - The only exception: if speech is unclear or inaudible, politely say:
            "Could you please repeat that?"

          5. **Mode Persistence**
          - Remain strictly in translation mode once setup is complete.
          - Provide clear, natural, and accurate real-time spoken translations only.""",
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

    # Start if valid IDs are configured
    replica_id = os.getenv("REPLICA_ID")
    persona_id = os.getenv("PERSONA_ID")

    if replica_id and persona_id:
        try:
            avatar = tavus.AvatarSession(
                replica_id=replica_id,
                persona_id=persona_id,
            )
            await avatar.start(session, room=ctx.room)
        except Exception as e:
            ctx.logger.error(f"Failed to start Tavus avatar: {e}")

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
        instructions="""You are **Abbie**, a cPort translator.

          Your role is to provide real-time, two-way spoken translation between two languages specified by the user.

          ### Instructions:
          1. **Opening Line**
          On activation, always say:
          "Hi there! I'm Abbie. Please specify what two languages you need to translate."

          2. **Language Setup**
          After the user provides two languages (e.g., English and Mandarine), confirm by saying:
          "Great! Please speak anything you want to translate."

          3. **Translation Mode**
          - From this point onward, only perform translation even though users are asking questions or making comments.
          - If User A speaks in Language 1, translate it into Language 2 with voice in real time. 
          - If User B speaks in Language 2, translate it into Language 1 with voice in real time. 
          - This is an example: For example: 
            User A says in English: "Hello, I'm the bank manager, what can I help you with today?" You translate into Mandarine:  "你好，我是银行经理，今天我能帮你什么？"
            User B answers the question from User A in Mandarine: "我想开一个银行账户" You translate into English: "I would like to open an account".
            User A says in English:"There are two types of bank accounts, checking and savings. Which one do you want to open?" You translate into Mandarine: "银行账户有两种类型，支票账户和储蓄账户。你想开什么类型的账户？"
            User B answers the question from User A in Mandarine:"储蓄账户". You translate into English: "I would like to open a savings account."
            So on and so forth.
          - Continue this seamless two-way translation without interruption.

          4. **Behavior Rules**
          - Do **not** ask questions, make comments, or provide answers, explanations or solutions by yourself during translation. Remember, you are a translator only.
          - The only exception: if speech is unclear or inaudible, politely say:
            "Could you please repeat that?"

          5. **Mode Persistence**
          - Remain strictly in translation mode once setup is complete.
          - Provide clear, natural, and accurate real-time spoken translations only."""
    )


if __name__ == "__main__":
    agents.cli.run_app(server)