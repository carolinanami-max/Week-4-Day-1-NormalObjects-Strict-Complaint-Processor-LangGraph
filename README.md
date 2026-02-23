# NormalObjects - Strict Complaint Processor (Bloyce's Protocol)

## 📋 Project Overview

This project implements a structured, rule-based complaint processing system using LangGraph. Unlike creative agents, this system follows strict workflows and documents every step - exactly as required by "Bloyce's Protocol" at the Downside Up Complaint Bureau.

## 🎯 Learning Objectives

- Build structured agent workflow using LangGraph state machine
- Implement defined nodes and edges for complaint processing
- Create rule-based complaint processing system
- Understand state management in agentic workflows
- Compare structured LangGraph approach with freeform LangChain agents

## 📁 Project Structure
├── normalobjects_langgraph.py
├── comparison.md
├── README.md
└── .env


## ⚙️ Setup Instructions

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository
2. Install required packages
3. Create a `.env` file with your API key



## 🔄 Workflow Steps (Bloyce's Protocol)

The system follows these strict steps:

| Step | Name | Description |
|------|------|-------------|
| 1 | INTAKE | Parse and categorize complaint |
| 2 | VALIDATE | Check against Bloyce's strict rules |
| 3 | INVESTIGATE | Gather evidence (only for valid complaints) |
| 4 | RESOLVE | Propose solution with effectiveness rating |
| 5 | CLOSE | Confirm resolution and log timestamp |

### Categories

- **portal**: Issues with portal timing, location, or behavior
- **monster**: Issues with creature behavior (demogorgons, etc.)
- **psychic**: Issues with psychic abilities or limitations
- **environmental**: Issues with electricity, weather, or physical environment
- **other**: Anything else

### Validation Rules

| Category | Must Reference | Example |
|----------|---------------|---------|
| portal | Specific location OR timing anomalies | "portal opens at different times" |
| monster | Creature behavior or interactions | "demogorgons fight each other" |
| psychic | Specific ability limitations | "can't lift heavy rocks" |
| environmental | Electricity, weather, or physical phenomena | "power lines react strangely" |
| other | Automatically invalid | N/A |

## 🧪 Test Complaints

The system tests 5 sample complaints:

1. ✅ "The Downside Up portal opens at different times each day. Sometimes it's 3pm, sometimes 8pm. How do I predict when?"
2. ✅ "Demogorgons sometimes work together and sometimes fight each other. What's their deal?"
3. ✅ "El can move things with her mind but can't lift heavy rocks. Why the limitation?"
4. ❌ "The portal is weird and I don't like it."
5. ❌ "I found a strange coin in my backyard."

## 📊 Features

- ✅ State machine with 5 nodes
- ✅ Conditional routing for valid/invalid complaints
- ✅ Workflow visualization with emojis
- ✅ Timestamp tracking for closed complaints
- ✅ 30-day follow-up flag for low effectiveness ratings
- ✅ Complete audit trail (workflow_path)

## 🖥️ Running the Program
python normalobjects_langgraph.py


## 📈 Sample Output

### Valid Complaint Path
==================================================
[INTAKE] Processing complaint...
[INTAKE] Categorized as: portal
==================================================
[VALIDATE] Valid: True
==================================================
[INVESTIGATE] Gathering evidence...
==================================================
[RESOLVE] Proposed solution with medium effectiveness rating
==================================================
[CLOSE] Complaint closed at 2026-02-23 17:14:53

🎯 WORKFLOW VISUALIZATION
========================================
✅ intake → ✅ validate → ✅ investigate → ✅ resolve → ✅ close


### Invalid Complaint Path
==================================================
[VALIDATE] Valid: False
==================================================
[ROUTER] Complaint is INVALID → sending to closure

🎯 WORKFLOW VISUALIZATION
========================================
✅ intake → ✅ validate → ⬜ investigate → ⬜ resolve → ✅ close
⚠️ Note: Complaint was rejected at validation


## 🔍 Comparison with LangChain

See `comparison.md` for detailed analysis.

## 🏆 Success Criteria Achieved

- ✓ Successfully built LangGraph state machine
- ✓ Workflow follows all defined steps
- ✓ State is properly managed throughout workflow
- ✓ System handles both valid and invalid complaints
- ✓ Code is well-documented
- ✓ Workflow visualization implemented
- ✓ Complete audit trail available

## 📚 Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [State Management Tutorial](https://python.langchain.com/docs/langgraph/state)
- [Conditional Edges Guide](https://python.langchain.com/docs/langgraph/conditional)

## 👩‍💻 Author

Carolina Nami - Week 4 Day 1 Lab
