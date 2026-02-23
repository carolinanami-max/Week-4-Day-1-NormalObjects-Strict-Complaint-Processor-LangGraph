import os
from dotenv import load_dotenv
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Load environment variables from .env file
load_dotenv()

# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

# Define the state structure for the complaint processing workflow
class ComplaintState(TypedDict):
    # Input
    complaint: str  # The original complaint text
    
    # To be filled during workflow
    category: str  # portal, monster, psychic, environmental, or other
    is_valid: bool  # True or False after validation
    validation_message: str  # Why it's valid or invalid
    evidence: str  # Findings from investigation
    resolution: str  # Proposed solution
    effectiveness_rating: str  # high, medium, or low
    customer_satisfied: bool  # Did customer confirm resolution worked?
    
    # Tracking
    workflow_path: List[str]  # Records each step taken
    status: str  # Current status (intake, validate, investigate, resolve, close)
    timestamp: str  # When complaint was closed

    # NODE 1: Intake - Parse and categorize the complaint
def intake_node(state: ComplaintState) -> ComplaintState:
    """
    Step 1: The receptionist - reads complaint and decides category
    """
    print("\n" + "="*50)
    print("[INTAKE] Processing complaint...")
    print("="*50)
    
    # Get the complaint from the current state
    complaint = state["complaint"]
    
    print(f"Complaint: {complaint}")
    
    # Create a prompt for the AI to categorize the complaint
    categorization_prompt = f"""
    Categorize this Downside Up complaint into exactly ONE of these categories:
    
    - portal: Issues with portal timing, location, or behavior
    - monster: Issues with creature behavior (demogorgons, etc.)
    - psychic: Issues with psychic abilities or limitations
    - environmental: Issues with electricity, weather, or physical environment
    - other: Anything else
    
    Complaint: {complaint}
    
    Respond with ONLY the category name (portal, monster, psychic, environmental, or other).
    """
    
    # Ask the AI to categorize
    response = llm.invoke([HumanMessage(content=categorization_prompt)])
    category = response.content.strip().lower()
    
    print(f"[INTAKE] Categorized as: {category}")
    
    # Update the state with new information
    new_state = {
        **state,  # Keep all existing information
        "category": category,
        "workflow_path": state.get("workflow_path", []) + ["intake"],
        "status": "intake"
    }
    
    return new_state