from typing import List, Optional
from .models import db, Problem
from .templates import ProblemTemplate, BasicsProblemTemplate


class ProblemRepository:
    def __init__(self):
        self.template_map = {
            "BASICS": BasicsProblemTemplate
        }

    def create_problem(self, topic: str, difficulty: int) -> Problem:
        template_class = self.template_map.get(topic, ProblemTemplate)
        template = template_class(topic, difficulty)
        problem_data = template.generate()

        problem = Problem(
            topic=topic,
            week=1,  # TODO: Get from TOPICS constant
            difficulty=difficulty,
            description=problem_data["description"],
            test_cases=problem_data["test_cases"],
            starter_code=problem_data["starter_code"]
        )
        db.session.add(problem)
        db.session.commit()
        return problem

    def get_problems_by_topic(self, topic: str) -> List[Problem]:
        return Problem.query.filter_by(topic=topic).all()

    def get_problem_by_id(self, problem_id: int) -> Optional[Problem]:
        return db.session.get(Problem, problem_id)
