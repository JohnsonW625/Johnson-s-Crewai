#!/usr/bin/env python3
"""
A CrewAI example where a twin agent representing "Johnson Wang", a Harvard student, 
answers questions about his background and expertise.

Author: Johnson
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileWriterTool, FileReadTool

# Read API keys from the environment. 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # Optional: for web search


if not OPENAI_API_KEY:
    print("⚠️  OPENAI_API_KEY not found in environment. Set OPENAI_API_KEY before running for real runs.")
if not SERPER_API_KEY:
    print("⚠️  SERPER_API_KEY not found in environment. Web search may be disabled or limited.")

def create_twin_agent():
    return Agent(
        role='The little me of myself',
        goal='Provide short paragraph about the question asked on Johnson behalf given his information',
        backstory="""You are Johnson Wang, a student currently studying at Harvard, who is excel in academics and passionate about AI.""",
        verbose=True,
        allow_delegation=False,
        tools=[FileReadTool(file_path='./information.txt')]  # Tool to read files
    )

def create_writer_agent():
    return Agent(
        role='Formal Response Writer',
        goal='Take a draft first-person response and produce a concise, formal, and polished reply suitable for sending',
        backstory="""You are a professional writer who converts short, candid draft replies into formal, concise messages in first-person voice.
        Expect input that contains a short 'answer' and 'support' section. Produce a final first-person message (2-4 sentences) and optionally a short formal paragraph of context if requested.""",
        verbose=True,
        allow_delegation=False,
        tools=[FileWriterTool()]  # Tool to write files
    )

def create_johnson_response_task(agent, question):
    """Create a research task for the research agent."""
    return Task(
        description=f"""Question: {question}

        Your task (on behalf of Johnson Wang):
        1. Read `information.txt` to learn Johnson's background and perspective.
        2. Produce a concise first-person answer (2-3 sentences) that Johnson could send in reply.
        3. Provide a short supporting paragraph (3-4 sentences) that explains the reasoning or details.

        Keep the reply honest, try not to invent ideas that is out of the scope of Johnson's knowledge (PhD level knowledge).
        """,

        expected_output="""A short structured text containing the the answer to the question
        """,
        agent=agent
    )

def create_writing_task(agent, draft_output):
    """Create a writing task for the writer agent using the twin agent's draft output.

    draft_output is expected to be a small structured object or text containing at least
    an 'answer' (2-3 sentences) and optional 'support' notes.
    """
    description = (
        "You are given a short draft response (from Johnson's twin agent).\n\n"
        "Input (draft) to use:\n" + str(draft_output) + "\n\n"
        "Your task:\n"
        "1. Convert the draft into a concise, formal, first-person reply (2-4 sentences).\n"
        "2. Preserve the factual content and citations from the draft; do not invent facts.\n"
        "3. Optionally provide a single short formal context paragraph if needed.\n"
        "4. Save the final reply as 'johnson_reply.md' and return a short confirmation.\n"
    )

    expected = (
        "A formal first-person reply saved to 'johnson_reply.md' and a short status message."
    )

    return Task(description=description, expected_output=expected, agent=agent)

def main():
    """Main runner: collect a question, create agents/tasks, run the crew, and report results."""
    print("🚀 Welcome to Chat use Johnson - a master student at Harvard studying AI and biology")
    print("=" * 50)

    # Get question from user input
    question = input("Enter a question you'd like Johnson to answer: ")
    if not question.strip():
        question = "Explain my background in 3 sentences"
        print(f"Using default question: {question}")

    print(f"\n📚 Question: {question}")
    print("=" * 50)

    # Create agents
    print("\n🤖 Creating AI agents...")
    researcher = create_twin_agent()
    writer = create_writer_agent()

    # Create tasks
    print("📋 Setting up tasks...")
    research_task = create_johnson_response_task(researcher, question)

    # Create a placeholder draft that would be replaced by the twin agent's real output
    draft_placeholder = "{'answer': '<short answer>', 'support': '<supporting paragraph>'}"
    writing_task = create_writing_task(writer, draft_placeholder)

    # Create crew
    print("👥 Assembling the crew...")
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,  # Tasks will be executed in sequence
        verbose=True
    )

    # Execute the crew
    print("\n🎯 Starting crew execution...")
    print("=" * 50)

    try:
        result = crew.kickoff()

        print("\n✅ Crew execution completed!")
        print("=" * 50)
        print("📄 Final Result:")
        print(result)

        # Check if the article or reply file was created
        if os.path.exists('johnson_reply.md'):
            print("\n📝 Reply successfully saved to 'johnson_reply.md'")
            with open('johnson_reply.md', 'r') as f:
                content = f.read()
                print(f"📊 Reply length: {len(content)} characters")
        elif os.path.exists('ai_studio_article.md'):
            print("\n📝 Article successfully saved to 'ai_studio_article.md'")
            with open('ai_studio_article.md', 'r') as f:
                content = f.read()
                print(f"📊 Article length: {len(content)} characters")
        else:
            print("\n⚠️  No output file found. The agents may not have used the file tools.")

    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("\n💡 Note: This example requires valid API keys to function properly.")
        print("Please set your OPENAI_API_KEY environment variable.")


if __name__ == "__main__":
    main()

