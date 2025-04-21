from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Vrecruite():
	"""Vrecruite crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	
	@agent
	def skill_scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['skill_scraper'],
			verbose=True
		)
	
	@agent
	def talent_acquisition_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['talent_acquisition_specialist'],
			verbose=True
		)

	@agent
	def senior_recruiter(self) -> Agent:
		return Agent(
			config=self.agents_config['senior_recruiter'],
			verbose=True
		)
	
	@agent
	def formatter(self) -> Agent:
		return Agent(
			config=self.agents_config['formatter'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	
	@task
	def skill_scraper_task(self) -> Task:
		return Task(
			config=self.tasks_config['skill_scraper_task'],
		)

	@task
	def talent_acquisition_task(self) -> Task:
		return Task(
			config=self.tasks_config['talent_acquisition_task'],
		)

	@task
	def recruiting_task(self) -> Task:
		return Task(
			config=self.tasks_config['recruiting_task'],
		)
	
	@task
	def formatting_task(self) -> Task:
		return Task(
			config=self.tasks_config['formatting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Vrecruite crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
