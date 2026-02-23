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

# NODE 4: Resolution - Propose a fix based on evidence
def resolve_node(state: ComplaintState) -> ComplaintState:
    """
    Step 4: Problem solver - proposes solution based on evidence
    """
    print("\n" + "="*50)
    print("[RESOLVE] Proposing resolution...")
    print("="*50)
    
    category = state["category"]
    complaint = state["complaint"]
    evidence = state["evidence"]
    
    # Create resolution prompt
    resolution_prompt = f"""
    You are a Downside Up resolution specialist. Propose a solution for this {category} complaint.
    
    Complaint: {complaint}
    
    Investigation Evidence: {evidence}
    
    Bloyce's Protocol Resolution Rules:
    
    1. Resolutions must be specific to {category} complaint type
    2. Must reference established Downside Up procedures or protocols
    3. Environmental or monster complaints MAY require escalation to specialized teams
    4. Each resolution MUST include an effectiveness rating: high, medium, or low
    
    Format your response exactly like this:
    
    Resolution: [Your proposed solution]
    
    Effectiveness Rating: [high/medium/low]
    
    Specialized Team Needed: [yes/no] - Only yes for environmental or monster if needed
    
    Explanation: [Brief explanation of why this solution fits the evidence]
    """
    
    # Ask the AI for resolution
    response = llm.invoke([HumanMessage(content=resolution_prompt)])
    resolution_text = response.content.strip()
    
    # Parse the response to extract rating
    lines = resolution_text.split('\n')
    rating = "medium"  # default
    for line in lines:
        if "Effectiveness Rating:" in line:
            rating = line.replace("Effectiveness Rating:", "").strip().lower()
            break
    
    print(f"[RESOLVE] Proposed solution with {rating} effectiveness rating")
    print(f"[RESOLVE] First line: {lines[0] if lines else 'No resolution provided'}")
    
    # Update the state
    new_state = {
        **state,
        "resolution": resolution_text,
        "effectiveness_rating": rating,
        "workflow_path": state.get("workflow_path", []) + ["resolve"],
        "status": "resolve"
    }
    
    return new_state


# NODE 5: Closure - Confirm resolution and check satisfaction
def close_node(state: ComplaintState) -> ComplaintState:
    """
    Step 5: Customer service - confirms resolution and checks satisfaction
    """
    print("\n" + "="*50)
    print("[CLOSE] Finalizing complaint...")
    print("="*50)
    
    category = state["category"]
    resolution = state["resolution"]
    rating = state["effectiveness_rating"]
    
    from datetime import datetime
    
    # Create closure prompt
    closure_prompt = f"""
    You are a Downside Up closure specialist. Finalize this {category} complaint.
    
    Resolution applied: {resolution}
    Effectiveness rating: {rating}
    
    Bloyce's Protocol Closure Rules:
    
    1. Confirm the resolution was applied
    2. Attempt customer satisfaction verification
    3. Note if this needs 30-day follow-up (low effectiveness ratings require this)
    
    Format your response exactly like this:
    
    Resolution Confirmed: [yes/no]
    
    Customer Satisfaction: [satisfied/unsatisfied/attempted but no response]
    
    Thirty Day Follow-up Needed: [yes/no] - yes if effectiveness rating is "low"
    
    Closing Notes: [Brief final notes]
    """
    
    # Ask the AI for closure
    response = llm.invoke([HumanMessage(content=closure_prompt)])
    closure_text = response.content.strip()
    
    # Check if follow-up is needed based on rating
    follow_up_needed = rating == "low"
    
    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"[CLOSE] Complaint closed at {current_time}")
    print(f"[CLOSE] 30-day follow-up needed: {follow_up_needed}")
    
    # Update the state
    new_state = {
        **state,
        "customer_satisfied": "satisfied" in closure_text.lower(),
        "timestamp": current_time,
        "workflow_path": state.get("workflow_path", []) + ["close"],
        "status": "closed"
    }
    
    # Print summary
    print("\n" + "="*50)
    print("COMPLAINT PROCESSING COMPLETE")
    print("="*50)
    print(f"Category: {category}")
    print(f"Effectiveness Rating: {rating}")
    print(f"30-day Follow-up: {'YES' if follow_up_needed else 'NO'}")
    print(f"Workflow Path: {' → '.join(state.get('workflow_path', []) + ['close'])}")
    print("="*50)
    
    return new_state

# STEP 3: Build the Graph - Connect all nodes into a workflow
from langgraph.graph import StateGraph, END


def build_complaint_graph():
    """
    Build the workflow graph connecting all nodes
    """
    print("Building Bloyce's Protocol workflow...")
    
    # Create the graph with our state structure
    workflow = StateGraph(ComplaintState)
    
    # Add all nodes (workstations)
    workflow.add_node("intake", intake_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("investigate", investigate_node)
    workflow.add_node("resolve", resolve_node)
    workflow.add_node("close", close_node)
    
    print("✓ All nodes added to graph")
    
    # Define the entry point (where work starts)
    workflow.set_entry_point("intake")
    print("✓ Entry point set to 'intake'")
    
    # Add basic linear edges (conveyor belts)
    # Intake always goes to validate
    workflow.add_edge("intake", "validate")
    print("✓ Added edge: intake → validate")
    
    # We'll add conditional routing for validation next
    # For now, let's add the happy path for valid complaints
    workflow.add_edge("investigate", "resolve")
    workflow.add_edge("resolve", "close")
    workflow.add_edge("close", END)
    print("✓ Added edges: investigate → resolve → close → END")
    
    return workflow

# ============================================
# STEP 3: Build the Graph - Connect all nodes
# ============================================

from langgraph.graph import StateGraph, END

# Conditional routing function - decides where to go after validation
def route_after_validation(state: ComplaintState) -> str:
    """
    Decision point: Based on validation result, either:
    - Investigate (if valid)
    - Close with rejection (if invalid)
    """
    print("\n" + "="*50)
    print("[ROUTER] Checking validation result...")
    print("="*50)
    
    if state.get("is_valid", False):
        print("[ROUTER] Complaint is VALID → proceeding to investigation")
        return "investigate"
    else:
        print("[ROUTER] Complaint is INVALID → sending to closure with rejection")
        return "close"

# Function to build the workflow graph
def build_complaint_graph():
    """
    Build the workflow graph connecting all nodes
    """
    print("Building Bloyce's Protocol workflow...")
    
    # Create the graph with our state structure
    workflow = StateGraph(ComplaintState)
    
    # Add all nodes (workstations)
    workflow.add_node("intake", intake_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("investigate", investigate_node)
    workflow.add_node("resolve", resolve_node)
    workflow.add_node("close", close_node)
    
    print("✓ All nodes added to graph")
    
    # Define the entry point (where work starts)
    workflow.set_entry_point("intake")
    print("✓ Entry point set to 'intake'")
    
    # Add edges
    # Intake always goes to validate
    workflow.add_edge("intake", "validate")
    print("✓ Added edge: intake → validate")
    
    # CONDITIONAL EDGE: After validate, router decides next step
    workflow.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "investigate": "investigate",
            "close": "close"
        }
    )
    print("✓ Added conditional edge: validate → [investigate OR close]")
    
    # Happy path for valid complaints
    workflow.add_edge("investigate", "resolve")
    workflow.add_edge("resolve", "close")
    print("✓ Added edges: investigate → resolve → close")
    
    # Close always goes to end
    workflow.add_edge("close", END)
    print("✓ Added edge: close → END")
    
    # Compile the graph
    app = workflow.compile()
    print("✓ Graph compiled successfully!")
    print("\n" + "="*50)
    print("BLOYCE'S PROTOCOL IS READY")
    print("="*50)
    
    return app