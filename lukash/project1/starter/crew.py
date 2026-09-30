"""Crew definition. Add agents and tasks here, and describe them in config/."""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, llm, task, tool

from starter.llm import local_llm
from starter.tools.vector_search import VectorSearchTool
from starter.tools.entry_lister import ListEntriesTool, ModelDetailsTool
from starter.tools.keyword_search import KeywordSearchTool

@CrewBase
class StarterCrew:
    """Independent researchers verify relevant model cards before summarization."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @llm
    def local(self):
        return local_llm()

    @tool
    def vector_search(self):
        return VectorSearchTool()

    @tool
    def keyword_search(self):
        return KeywordSearchTool()

    @tool
    def get_all_entries(self):
        return ListEntriesTool()

    @tool
    def get_model_details(self):
        return ModelDetailsTool()

    @agent
    def vector_searcher(self) -> Agent:
        return Agent(config=self.agents_config["vector_searcher"])

    @agent
    def keyword_searcher(self) -> Agent:
        return Agent(config=self.agents_config["keyword_searcher"])

    @agent
    def headline_hunter(self) -> Agent:
        return Agent(config=self.agents_config["headline_hunter"])

    @agent
    def writer(self) -> Agent:
        return Agent(config=self.agents_config["writer"])

    @task
    def research_vector(self) -> Task:
        return Task(config=self.tasks_config["research_vector"])

    @task
    def research_keywords(self) -> Task:
        return Task(config=self.tasks_config["research_keywords"])

    @task
    def research_titles(self) -> Task:
        return Task(config=self.tasks_config["research_titles"])

    @agent
    def editor(self) -> Agent:
        return Agent(config=self.agents_config["editor"])

    @task
    def edit_task(self) -> Task:
        return Task(config=self.tasks_config["edit_task"])

    @task
    def write_task(self) -> Task:
        return Task(config=self.tasks_config["write_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
