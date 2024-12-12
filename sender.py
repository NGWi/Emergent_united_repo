async def send_health_data(agent: HealthAnalyzerAgent):
    health_data = {
        "heart_rate": 72,
        "blood_pressure": "120/80",
        "temperature": 98.6,
    }
    await agent.handle_health_data_event(Context(), health_data)
