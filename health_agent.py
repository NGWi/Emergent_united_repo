from uagents import Agent, Context

class HealthAnalyzerAgent:
    def __init__(self):
        # Initialize the uAgent
        self.agent = Agent(name="health_analyzer", private_key="your_private_key_here")

        # Register the message handler for health data
        @self.agent.on_event("health_data")
        async def analyze_health_data(ctx: Context, payload: dict):
            """
            Analyze health data and provide a comparison to average ranges.
            Notify the livekit agent with the result.
            """
            user_metrics = payload.get("metrics", {})
            averages = {
                "heart_rate": 72,  # Example averages
                "blood_pressure": "120/80",
                "temperature": 98.6,
            }

            analysis_results = {}
            for metric, user_value in user_metrics.items():
                avg_value = averages.get(metric)
                if avg_value:
                    analysis_results[metric] = {
                        "user_value": user_value,
                        "average_value": avg_value,
                        "status": "above" if user_value > avg_value else "below" if user_value < avg_value else "normal",
                    }

            # Log and notify the livekit agent
            ctx.logger.info(f"Health analysis results: {analysis_results}")
            await ctx.send("livekit_agent", {"analysis": analysis_results})

    def start(self):
        """
        Start the agent to listen for events.
        """
        self.agent.run()
