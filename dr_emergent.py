from uagents import Agent, Context, Model, Bureau
from analysis import analyze_biometric_data  # Import the analysis function
from datetime import datetime
from typing import List, Optional
from data_master import data_master_agent
class MessageModel(Model):
    id: int
    heart_rate: int
    blood_oxygen: float
    hrv: Optional[float]  # HRV can be None
    glucose_level: Optional[float]  # Glucose level can be None
    latitude: float
    longitude: float
    timestamp: datetime
    
# Create the Health Monitoring Agent
dr_emergent_agent = Agent(name="dr_emergent", seed="dr_emergent")

@dr_emergent_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Health Monitoring Agent is now active.")

@dr_emergent_agent.on_message(model=MessageModel)  # Expecting a MessageModel as input
async def health_data_handler(ctx: Context, sender: str, data: MessageModel):
    # Analyze the received biometric data
    analysis_results = analyze_biometric_data(data.dict())  # Convert Pydantic model to dict for analysis
    
    # Log the analysis results
    ctx.logger.info(f"Received data from {sender}: {data.dict()}")
    ctx.logger.info(f"Analysis results: {analysis_results}")

    # Here we can implement further actions based on the analysis results
    # For example, sending alerts or notifications if issues are detected

if __name__ == "__main__":
    dr_emergent_agent.run()

