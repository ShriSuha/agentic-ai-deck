"""Crew definition. Add agents and tasks here, and describe them in config/."""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, llm, task, tool

from starter.guardrail.answer_check import check_answer
from starter.llm import local_llm
from starter.tools.read_card import ReadCardTool
from starter.tools.search_cards import SearchCardsTool


@CrewBase
class StarterCrew:
    """One agent: answer a question from the model cards."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @llm
    def local(self):
        return local_llm()

    @tool
    def search_cards(self):
        return SearchCardsTool()

    @tool
    def read_card(self):
        return ReadCardTool()

    @agent
    def card_guide(self) -> Agent:
        return Agent(config=self.agents_config["card_guide"])

    @task
    def answer_question(self) -> Task:
        return Task(
            config=self.tasks_config["answer_question"],
            guardrail=check_answer,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            cache=True,
            verbose=True,
        )
