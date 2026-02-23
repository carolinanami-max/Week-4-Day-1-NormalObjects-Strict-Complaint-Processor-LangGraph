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


# NODE 2: Validation - Check complaint against Bloyce's strict rules
def validate_node(state: ComplaintState) -> ComplaintState:
    """
    Step 2: Security guard - checks if complaint follows the rules
    """
    print("\n" + "="*50)
    print("[VALIDATE] Checking complaint against Bloyce's Protocol...")
    print("="*50)
    
    category = state["category"]
    complaint = state["complaint"]
    
    # Create a validation prompt based on the category rules from the lab
    validation_prompt = f"""
    You are Bloyce's strict complaint validator. Check if this complaint follows these rules:
    
    Category: {category}
    Complaint: {complaint}
    
    Validation rules from Bloyce's Protocol:
    
    1. PORTAL complaints (category: portal):
       - Must reference specific location OR timing anomalies
       - Example: "portal opens at different times" → VALID
       - Example: "portal location changed" → VALID
       - Example: "portal is weird" → INVALID (too vague)
    
    2. MONSTER complaints (category: monster):
       - Must describe creature behavior or interactions
       - Example: "demogorgons fight each other" → VALID
       - Example: "creature appeared" → INVALID (no behavior described)
    
    3. PSYCHIC complaints (category: psychic):
       - Must reference specific ability limitations or malfunctions
       - Example: "can't lift heavy rocks" → VALID
       - Example: "powers are weird" → INVALID (too vague)
    
    4. ENVIRONMENTAL complaints (category: environmental):
       - Must mention electricity, weather, or observable physical phenomena
       - Example: "power lines react strangely" → VALID
       - Example: "weather is bad" → INVALID (too vague)
    
    5. OTHER complaints (category: other):
       - Automatically INVALID (requires manual review)
    
    Return your response in this exact format:
    Valid: [YES/NO]
    Message: [Brief explanation following the rules]
    """
    
    # Ask the AI to validate
    response = llm.invoke([HumanMessage(content=validation_prompt)])
    result = response.content.strip()
    
    # Parse the response
    lines = result.split('\n')
    is_valid = 'YES' in lines[0].upper()
    validation_message = lines[1].replace('Message:', '').strip() if len(lines) > 1 else "No message provided"
    
    print(f"[VALIDATE] Valid: {is_valid}")
    print(f"[VALIDATE] Message: {validation_message}")
    
    # Update the state
    new_state = {
        **state,
        "is_valid": is_valid,
        "validation_message": validation_message,
        "workflow_path": state.get("workflow_path", []) + ["validate"],
        "status": "validate"
    }
    
    return new_state

# NODE 3: Investigation - Gather evidence based on complaint type
def investigate_node(state: ComplaintState) -> ComplaintState:
    """
    Step 3: Detective - gathers evidence before proposing solution
    Only runs if complaint is valid
    """
    print("\n" + "="*50)
    print("[INVESTIGATE] Gathering evidence...")
    print("="*50)
    
    category = state["category"]
    complaint = state["complaint"]
    
    # Create investigation prompt based on category
    investigation_prompt = f"""
    You are a Downside Up investigator. Gather evidence for this {category} complaint.
    
    Complaint: {complaint}
    
    Based on Bloyce's Protocol, investigate according to these rules:
    
    - PORTAL issues: Investigate temporal patterns, location consistency, and environmental factors
    - MONSTER issues: Gather behavioral data, interaction patterns, and environmental triggers
    - PSYCHIC issues: Document ability specifications, tested limitations, and contextual factors
    - ENVIRONMENTAL issues: Analyze power line activity, atmospheric conditions, and anomaly correlation
    - OTHER issues: Note that these require manual review
    
    Provide a detailed investigation report with:
    1. Key findings (what did you discover?)
    2. Evidence gathered (specific observations)
    3. Patterns identified (if any)
    
    Keep the report concise but professional.
    """
    
    # Ask the AI to investigate
    response = llm.invoke([HumanMessage(content=investigation_prompt)])
    evidence = response.content.strip()
    
    print(f"[INVESTIGATE] Evidence gathered:")
    print(f"{evidence[:200]}...")  # Show first 200 chars only
    
    # Update the state
    new_state = {
        **state,
        "evidence": evidence,
        "workflow_path": state.get("workflow_path", []) + ["investigate"],
        "status": "investigate"
    }
    
    return new_state