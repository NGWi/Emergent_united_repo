import logging

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from uagents import Agent, Context
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import openai, deepgram, silero
from prompts.base import SYSTEM_PROMPT

load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("voice-agent")

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def health_analysis(ctx: Context, health_data: dict):
    """
    Analyze health data against average ranges and notify the livekit agent.
    """
    # Example average health ranges (replace with actual data)
    average_ranges = {
        "heart_rate": (60, 100),
        "blood_pressure": ((90, 120), (60, 80)),  # systolic and diastolic
    }

    analysis_results = {}

    # Compare health data to average ranges
    for metric, value in health_data.items():
        if metric == "heart_rate":
            analysis_results[metric] = average_ranges[metric][0] <= value <= average_ranges[metric][1]
        elif metric == "blood_pressure":
            systolic, diastolic = value
            sys_ok = average_ranges[metric][0][0] <= systolic <= average_ranges[metric][0][1]
            dia_ok = average_ranges[metric][1][0] <= diastolic <= average_ranges[metric][1][1]
            analysis_results[metric] = sys_ok and dia_ok

    # Notify the livekit agent with the analysis
    logger.info(f"Health analysis results: {analysis_results}")
    await ctx.emit("health_analysis_results", {"results": analysis_results})

async def entrypoint(ctx: JobContext):
    
    # Initialize uAgent for health analysis
    health_agent = Agent(name="HealthAnalyzer", on_startup=lambda _: logger.info("HealthAnalyzer started"))

    @health_agent.on_event("health_data")
    async def on_health_data(ctx: Context, payload: dict):
        await health_analysis(ctx, payload)
    
    # Start the health agent
    health_agent.start()
    health_data = {"heart_rate": 70, "blood_pressure": "120/80", "temperature": 98.6}
    health_analysis_result = await health_agent.handle_health_data_event(Context(), health_data)
    logger.info(f"Health analysis result: {health_analysis_result}")
    # Append the health agent to the initial context
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=SYSTEM_PROMPT+f"Health analysis result: {health_analysis_result}",
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)


    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")

    assistant = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
    )

    assistant.start(ctx.room, participant)

    # The agent should be polite and greet the user when it joins :)
    await assistant.say("Hey, how can I help you today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
