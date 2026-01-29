#!/usr/bin/env python3
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv
load_dotenv()

client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_ENDPOINT"],
    credential=DefaultAzureCredential()
)

with client:
    # List handoff-service versions
    print("Checking handoff-service agent...")
    agents = list(client.agents.list_versions(agent_name="handoff-service"))
    for a in agents:
        print(f"  Found: {a.id}")
    
    # Test the conversations API locally
    print("\nTesting Conversations API...")
    openai_client = client.get_openai_client()
    try:
        conv = openai_client.conversations.create(
            items=[{"type": "message", "role": "user", "content": "test"}]
        )
        print(f"  Conversation created: {conv.id}")
        
        resp = openai_client.responses.create(
            conversation=conv.id,
            extra_body={"agent": {"name": "handoff-service", "type": "agent_reference"}},
            input=""
        )
        print(f"  Response: {resp.output_text[:200]}...")
    except Exception as e:
        print(f"  Conversations API error: {e}")
