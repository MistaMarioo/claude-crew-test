from crewai import Agent, Crew, Task
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain_anthropic import ChatAnthropic

class EmailCrew:
    def __init__(self, inputs):
        self.inputs = inputs
        self.llm = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")
        self.search = DuckDuckGoSearchRun()
        self.tool = Tool(
            name="Search",
            func=self.search.run,
            description="useful for when you need to research for info"
        )
        self.setup_agents()
        self.setup_tasks()
        self.crew = Crew(
            agents=[self.researcher, self.writer],
            tasks=[self.task1, self.task2],
            verbose=2
        )

    def setup_agents(self):
        self.researcher = Agent(
            role="Email Research Specialist",
            goal='Research and analyze target audience and content requirements',
            backstory="""You are an expert at researching target audiences and creating
            tailored email content strategies.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.tool]
        )

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

    def setup_tasks(self):
        self.task1 = Task(
            description=f"""Research and analyze the following input:
            {self.inputs}
            
            Provide insights on:
            1. Target audience preferences
            2. Industry context
            3. Key messaging points
            Your final answer must be a detailed analysis report.""",
            agent=self.researcher
        )

        self.task2 = Task(
            description=f"""Using the research insights, create an email that:
            - Matches the specified email type
            - Speaks to the target audience
            - Incorporates the key points
            - Is engaging and conversion-focused
            
            Input details:
            {self.inputs}
            
            Your final answer must be the complete email with subject line.""",
            agent=self.writer
        )

    def run(self):
        return self.crew.kickoff()
