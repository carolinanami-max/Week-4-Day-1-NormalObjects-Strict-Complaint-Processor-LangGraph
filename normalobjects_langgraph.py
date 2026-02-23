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

# Define the state structure - like a form that gets filled step by step
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