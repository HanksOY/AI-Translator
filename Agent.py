import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# --- Load environment files (robust to CWD changes) ---
env_main = find_dotenv(".env", usecwd=True)
if not env_main:
    env_main = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_main, override=True)

env_local = find_dotenv(".env.local", usecwd=True)
if env_local:
    load_dotenv(dotenv_path=env_local, override=True)

# --- Validate required variables early ---
REQUIRED_VARS = [
    "ASSEMBLYAI_API_KEY",
    "GOOGLE_API_KEY",
    "CARTESIA_API_KEY",
    "LIVEKIT_URL",
    "LIVEKIT_API_KEY",
    "LIVEKIT_API_SECRET",
    "PINECONE_API_KEY",
    "ASSISTANT_NAME",
    "TAVUS_API_KEY",
    "TAVUS_REPLICA_ID",
]

missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
if missing:
    raise RuntimeError(
        "Missing required environment variables:\n  - "
        + "\n  - ".join(missing)
        + "\n\nMake sure your .env or .env.local files are being picked up, "
        + "or export them in your shell before running."
    )

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RoomOutputOptions
from livekit.plugins import (
    google,
    cartesia,
    noise_cancellation,
    assemblyai,
    silero,
    tavus,
)
from livekit.agents.llm import function_tool

# Pinecone client (use the *actual* key from env)
from pinecone import Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create / reference the Assistant by name from env
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME")
assistant = pc.assistant.Assistant(assistant_name=ASSISTANT_NAME)

@function_tool
async def ask_knowledge_base(question: str) -> str:
    """
    Query the Pinecone knowledge base for relevant information.
    This uses the Pinecone Assistant named in ASSISTANT_NAME.
    """
    try:
        # Avoid importing a specific Message class; send a simple dict.
        resp = assistant.chat(messages=[{"role": "user", "content": question}])
        # Defensive extraction of text
        if hasattr(resp, "message") and getattr(resp.message, "content", None):
            return resp.message.content
        # Some SDKs return dict-like data:
        msg = getattr(resp, "get", lambda *_: None)("message") if hasattr(resp, "get", None) else None
        if isinstance(msg, dict) and "content" in msg:
            return msg["content"]
        # Fallback stringify
        return str(resp)
    except Exception as e:
        # Don't crash the session if Pinecone is misconfigured or down.
        return f"[KB error] {type(e).__name__}: {e}"

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are **Kelly**, the official cPort translator agent.

Your role is to provide real-time, two-way spoken translation between two languages specified by the user.

### Instructions:
1. **Opening Line**
On activation, always say:
“Welcome to cPort! I'm Kelly. Please specify what two languages you need to translate.”

2. **Language Setup**
After the user provides two languages (e.g., English and French), confirm by saying:
“Great! Please speak anything you want to translate.”

3. **Translation Mode**
- From this point onward, only perform translation even though users are asking questions or making comments.
- If User A speaks in Language 1, translate it into Language 2 with voice in real time. 
- If User B speaks in Language 2, translate it into Language 1 with voice in real time. 
- This is an example: For example: User A says in English: "What's your name?" You translate into French: "Comment tu t'appelles?" 
  User B answers the question from User A in French: "Je m'appelle Pierre. Comment ça va?" You translate into English: "My name is Pierre. How are you?"
  User A responds in English: "I'm good, thank you!" You translate into French: "Je vais bien, merci!" So on and so forth.
- Continue this seamless two-way translation without interruption.

4. **Behavior Rules**
- Do **not** ask questions, make comments, or provide answers, explanations or solutions by yourself during translation. Remember, you are a translator only.
- The only exception: if speech is unclear or inaudible, politely say:
  “Could you please repeat that?”

5. **Mode Persistence**
- Remain strictly in translation mode once setup is complete.
- Provide clear, natural, and accurate real-time spoken translations only.
""",
            tools=[ask_knowledge_base],
        )

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=assemblyai.STT(
            api_key=os.getenv("ASSEMBLYAI_API_KEY"),
            end_of_turn_confidence_threshold=0.7,
            min_end_of_turn_silence_when_confident=160,
            max_turn_silence=2400,
        ),
        llm=google.LLM(
            model="gemini-1.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
        ),
        tts=cartesia.TTS(
            model="sonic-2",
            voice="f786b574-daa5-4673-aa0c-cbe3e8534c02",
            api_key=os.getenv("CARTESIA_API_KEY"),
        ),
        vad=silero.VAD.load(),  # Voice activity detection (VAD) detects periods of silence
        turn_detection="stt",   # Know when to start listening and when to respond
    )


    replica_id = os.getenv("TAVUS_REPLICA_ID")

    avatar = tavus.AvatarSession(
        api_key=os.getenv("TAVUS_API_KEY"),
        replica_id=replica_id,
        )  

     # Start the avatar and wait for it to join
    await avatar.start(session, room=ctx.room)

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
        room_output_options=RoomOutputOptions(audio_enabled=False),  # Audio is forwarded to the avatar, so we disable room output audio
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
