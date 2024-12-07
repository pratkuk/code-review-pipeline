from typing import List, Dict, Callable
import time

class Agent:
    def __init__(self, name: str, process_fn: Callable):
        self.name = name
        self.process = process_fn
        
    def run(self, input_data: Dict) -> Dict:
        return self.process(input_data)

class Pipeline:
    def __init__(self, name: str):
        self.name = name
        self.agents: List[Agent] = []
        self.quality_threshold = 0.8
        self.max_iterations = 3
        
    def add_agent(self, agent: Agent):
        self.agents.append(agent)
        
    def run(self, initial_input: Dict) -> Dict:
        current_output = initial_input
        iterations = 0
        
        while iterations < self.max_iterations:
            print(f"\nIteration {iterations + 1} for pipeline {self.name}")
            
            for agent in self.agents:
                current_output = agent.run(current_output)
                print(f"{agent.name} output: {current_output}")
                
                if "quality_score" in current_output:
                    if current_output["quality_score"] >= self.quality_threshold:
                        print(f"Quality threshold met: {current_output['quality_score']}")
                        return current_output
            
            iterations += 1
            time.sleep(1)
        return current_output

def code_reviewer(input_data: Dict) -> Dict:
    code = input_data.get('code', '')
    review_points = []
    
    if 'if' in code:
        review_points.append("Contains conditional logic")
    if 'for' in code or 'while' in code:
        review_points.append("Contains loops")
    if 'def' in code:
        review_points.append("Contains function definitions")
    if '#' in code:
        review_points.append("Contains comments")
    
    return {
        "code": code,
        "review": review_points,
        "metadata": input_data
    }

def quality_assessor(input_data: Dict) -> Dict:
    review = input_data.get('review', [])
    code = input_data.get('code', '')
    
    # Simple scoring based on review points
    score = len(review) * 0.2
    if len(code.split('\n')) > 5:
        score += 0.2
    
    return {**input_data, "quality_score": score}

def create_pipeline(name: str) -> Pipeline:
    pipeline = Pipeline(name)
    pipeline.add_agent(Agent("CodeReviewer", code_reviewer))
    pipeline.add_agent(Agent("QualityAssessor", quality_assessor))
    return pipeline