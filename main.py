# main.py
from crewai import Agent, Crew, Task  # Import core CrewAI components
from langchain_community.tools import DuckDuckGoSearchRun  # Import search tool
from langchain.agents import Tool  # Import Tool class for creating tools
from langchain_anthropic import ChatAnthropic  # Import Anthropic's ChatAnthropic

class EmailCrew:
    def __init__(self, inputs):
        # Initialize the language model with Claude 3
        self.llm = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")
        
        # Initialize the search tool
        self.search = DuckDuckGoSearchRun()
        
        # Create a tool wrapper for the search functionality
        self.tool = Tool(
            name="Search",
            func=self.search.run,
            description="useful for when you need to research for info"
        )
        
        # Initialize researcher agent
        self.researcher = Agent(
            role="Email Research Specialist",
            goal='Research and analyze target audience and content requirements',
            backstory="""You are an expert at researching target audiences and creating
            tailored email content strategies.""",
            verbose=True,  # Print detailed output for debugging
            allow_delegation=False,  # Don't allow task delegation
            llm=self.llm,
            tools=[self.tool]
        )

        # Initialize writer agent
        self.writer = Agent(
            role='Email Content Strategist',
            goal='Craft compelling email content',
            backstory="""You are an expert email copywriter who creates engaging
            and conversion-focused emails.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.tool]
        )

        # Create research task using the provided inputs
        self.task1 = Task(
            description=f"""Research and analyze the following input:
            {inputs}
            
            Provide insights on:
            1. Target audience preferences
            2. Industry context
            3. Key messaging points
            Your final answer must be a detailed analysis report.""",
            agent=self.researcher
        )

        # Create writing task using the provided inputs
        self.task2 = Task(
            description=f"""Using the research insights, create an email that:
            - Matches the specified email type
            - Speaks to the target audience
            - Incorporates the key points
            - Is engaging and conversion-focused
            
            Input details:
            {inputs}
            
            Your final answer must be the complete email with subject line.""",
            agent=self.writer
        )

        # Create the crew with both agents and tasks
        self.crew = Crew(
            agents=[self.researcher, self.writer],
            tasks=[self.task1, self.task2],
            verbose=2  # Detailed output level
        )

    def run(self):
        # Execute all tasks and return the result
        return self.crew.kickoff()

# This code only runs if the file is run directly (not imported)
if __name__ == "__main__":
    test_input = "Test input"
    crew = EmailCrew(test_input)
    print(crew.run())
