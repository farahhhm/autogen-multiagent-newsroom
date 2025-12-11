import asyncio
from autogen import AssistantAgent, GroupChat, GroupChatManager, register_function, UserProxyAgent 

config_list = [
    {
        "model": "llama3.1:8b",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
    }
]

# Tool: Simulate fetching news data
def fetch_news_data(topic: str) -> str:
    """Tool: Simulate fetching news data for a topic. Returns fake data."""
    return f"Fake news data for {topic}: Fact 1. Fact 2. Fact 3. Fact 4. Fact 5."

# ===== TEAM 1: Reporter Team (Tool Usage Pattern) =====
# Reporter Agent (uses the tool)
reporter = AssistantAgent(
    name="Reporter",
    system_message="You are a reporter. Use the fetch_news_data tool to get news data. Upon receiving the tool response, output ONLY the data content as a single block of text and then the word 'TERMINATE'. Do not add any extra commentary or JSON/dictionary wrappers.",
    llm_config={"config_list": config_list, "temperature": 0.0},
)

# User Proxy Agent (executes the tool)
user_proxy = UserProxyAgent(
    name="UserProxy",
    system_message="You execute functions and manage the conversation flow.",
    code_execution_config=False,
    llm_config=None,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
)

# Register the tool
register_function(
    fetch_news_data,
    caller=reporter,
    executor=user_proxy,
    name="fetch_news_data",
    description="Fetch news data for a given topic."
)

# ===== TEAM 2: Editorial Desk (Reflection Pattern) =====
# Writer Agent 
writer = AssistantAgent(
    name="Writer",
    system_message=(
        "You are a newsletter writer. Your task is to write a single, complete newsletter introduction (150 words max) using the provided data. "
        "Send the draft to the Critic for review. "
        "If the Critic says 'APPROVE', you MUST respond with ONLY the word 'TERMINATE' and nothing else. "
        "Do not thank anyone, do not say goodbye, do not add any commentary after approval. Just say 'TERMINATE'."
    ),
    llm_config={"config_list": config_list, "temperature": 0.3},
)

# Critic Agent 
critic = AssistantAgent(
    name="Critic",
    system_message=(
        "You are a critic. Review the Writer's draft for quality, conciseness, and use of data. "
        "If the draft is good, say 'APPROVE' and NOTHING else. "
        "If revisions are needed, provide brief constructive criticism. "
        "After you say 'APPROVE', you MUST NOT respond again under any circumstances."
    ),
    llm_config={"config_list": config_list, "temperature": 0.3},
)

# Create GroupChat for Team 2 (Reflection is limited)
editorial_team = GroupChat(
    agents=[writer, critic],
    messages=[],
    max_round=10,  # Increased to allow for conversation
    speaker_selection_method="round_robin"
)

# ===== MAIN EXECUTION =====
async def main():
    """Main function to run the newsroom system."""
        
    topic = input("Enter news topic (press Enter for 'AI News'): ").strip()
    if not topic:
        topic = "AI News"
    print(f"\n{'='*70}")
    print(f"NEWSROOM SYSTEM - Topic: {topic}")
    print(f"{'='*70}\n")
        
    # ===== STEP 1: Run Team 1 (Reporter + Tool) =====
    print("TEAM 1: Reporter Team (Fetching News Data)")
    print("-" * 70)
        
    # Execution is synchronous
    chat_result_team1 = user_proxy.initiate_chat(
        reporter,
        message=f"Please fetch news data for the topic: {topic}",
        max_turns=5
    )
        
    # Extract news data from Team 1 output
    news_data = "No data retrieved."
    for msg in reversed(chat_result_team1.chat_history):
        content = msg.get("content", "")
        # Look for the last message from the Reporter that contains the data
        if msg.get("name") == "Reporter" and "Fact" in content:
            # Clean the Reporter's output to get just the data
            clean_data = content.replace("TERMINATE", "").strip().strip('{}[]"')
            if "data" in clean_data.lower():
                # If the LLM still includes the data key, extract the value
                try:
                    import json
                    data_part = clean_data[clean_data.find('{'):clean_data.rfind('}')+1]
                    data_dict = json.loads(data_part)
                    news_data = data_dict.get("data", clean_data)
                except:
                    # Fallback for simple string output
                    news_data = clean_data.split(':', 1)[-1].strip() if ':' in clean_data else clean_data
            else:
                news_data = clean_data
            break
            
    # Simplify the extracted data for Team 2 to prevent misinterpretation
    if "Fact 1. Fact 2." in news_data:
        news_data = f"Fake news data for {topic}: Fact 1. Fact 2. Fact 3. Fact 4. Fact 5."
            
    print(f"\n{'='*70}")
    print(f"TEAM 1 OUTPUT (News Data):")
    print(f"{'='*70}")
    print(news_data)
    print()
        
    # ===== STEP 2: Run Team 2 (Editorial Desk) =====
    print(f"\n{'='*70}")
    print("TEAM 2: Editorial Desk (Writer + Critic Reflection)")
    print("-" * 70)
        
    
    def is_group_chat_termination(msg):
        content = msg.get("content", "").upper()
        # Stop if the message contains 'APPROVE' or 'TERMINATE'
        # Also stop if the message is just pleasantries after approval
        return "APPROVE" in content or "TERMINATE" in content
        
    # Create GroupChatManager with custom termination
    editorial_manager = GroupChatManager(
        groupchat=editorial_team,
        llm_config={"config_list": config_list, "temperature": 0.3},
        is_termination_msg=is_group_chat_termination
    )
        
    # Writer initiates the editorial process (synchronous)
    writer.initiate_chat(
        editorial_manager,
        message=f"Please write a newsletter introduction using this news data:\n\n{news_data}",
        max_turns=10
    )
        
    # ===== STEP 3: Display Final Output =====
    print(f"\n{'='*70}")
    print("FINAL NEWSLETTER INTRODUCTION:")
    print(f"{'='*70}")
        
    if editorial_team.messages:
        # Find the last Writer message before the Critic's APPROVE
        final_intro = "No final approved draft found."
        
        # Iterate through messages to find the approval point
        for i in range(len(editorial_team.messages) - 1, -1, -1):
            msg = editorial_team.messages[i]
            content = msg.get("content", "")
            sender = msg.get("name", "")
            
            # If we find APPROVE from Critic, get the previous Writer message
            if "APPROVE" in content.upper() and sender == "Critic":
                # Look backwards for the last Writer message
                for j in range(i - 1, -1, -1):
                    prev_msg = editorial_team.messages[j]
                    if prev_msg.get("name") == "Writer":
                        prev_content = prev_msg.get("content", "")
                        # Skip messages that are just TERMINATE or pleasantries
                        if "TERMINATE" not in prev_content and len(prev_content.strip()) > 20:
                            final_intro = prev_content
                            break
                break
        
        
        final_intro = final_intro.replace("[Rest of the newsletter content will follow]", "").strip()
        print(final_intro)
    else:
        print("No output generated.")
        
    print(f"\n{'='*70}")
    print("NEWSROOM SYSTEM COMPLETE")
    print(f"{'='*70}\n")
    
    
    return

if __name__ == "__main__":
    asyncio.run(main())