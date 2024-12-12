"""
This agent will send a message to agent Bob as soon as its starts.
"""
from uagents import Agent, Context, Model
from typing import List, Any, Optional
import datetime

class MessageModel(Model):
    id: int
    heart_rate: int
    blood_oxygen: float
    hrv: Optional[float]  # HRV can be None
    glucose_level: Optional[float]  # Glucose level can be None
    latitude: float
    longitude: float
    timestamp: datetime

# health data on a 30-second interval for driver emergencies
health_data = [
    # Case 1: Hypoglycemia emergency
    [
        {
            "id": 1,
            "heart_rate": 110 + i * 2,  # Gradual increase in heart rate
            "blood_oxygen": 95.0 - i * 0.5,  # Gradual decrease in oxygen
            "hrv": 25.0 - i * 0.5,  # Gradual decrease in HRV
            "glucose_level": 55.0 + i * 1.5,  # Gradual recovery of glucose level
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timestamp": datetime.datetime.now() + datetime.timedelta(seconds=i * 30)
        } for i in range(10)
    ],
    # Case 2: Cardiac arrest symptoms
    [
        {
            "id": 2,
            "heart_rate": 200 - i * 5,  # Gradual decrease in heart rate
            "blood_oxygen": 85.0 + i * 0.5,  # Gradual recovery of oxygen
            "hrv": 5.0 + i * 0.5,  # Gradual increase in HRV
            "glucose_level": None,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "timestamp": datetime.datetime.now() + datetime.timedelta(seconds=i * 30)
        } for i in range(10)
    ],
    # Case 3: Respiratory distress
    [
        {
            "id": 3,
            "heart_rate": 120 - i * 2,  # Gradual decrease in heart rate
            "blood_oxygen": 78.0 + i * 1.0,  # Gradual recovery of oxygen
            "hrv": 15.0 + i * 0.5,  # Gradual increase in HRV
            "glucose_level": None,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "timestamp": datetime.datetime.now() + datetime.timedelta(seconds=i * 30)
        } for i in range(10)
    ]
]

data_master_agent = Agent(name="data_master", seed="data_master")
dr_emergent_address = "dr_emergent"
def pick_case(case_number: int) -> List:
    return health_data[case_number]



@data_master_agent.on_interval(period=30.0)
async def send_message(ctx: Context):
    """Send a message to agent Dr.Emergent by specifying its address"""

    await ctx.send(dr_emergent_address, MessageModel(message=health_data))
    ctx.logger.info(f"Message has been sent to Dr.Emergent")

if __name__ == "__main__":
    data_master_agent.run()
    