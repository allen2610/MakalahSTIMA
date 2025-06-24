import random
import copy
from study_task import ScheduleNode

class GreedyScheduler:
    def __init__(self, problem):
        self.problem = problem
    
    def solve(self):
        tasks = copy.deepcopy(self.problem.tasks)
        schedule = {}
        
        for day in range(1, self.problem.max_days + 1):
            daily_hours = 0
            daily_assignments = []
            
            available_tasks = [t for t in tasks if t.remaining_hours > 0 and t.deadline >= day]
            available_tasks.sort(key=lambda t: (t.deadline - day, -t.priority))
            
            for task in available_tasks:
                if daily_hours >= self.problem.max_daily_hours:
                    break
                
                hours_to_allocate = min(
                    task.remaining_hours,
                    self.problem.max_daily_hours - daily_hours,
                    self.problem.max_daily_hours  
                )
                
                if hours_to_allocate >= self.problem.min_session_hours:
                    daily_assignments.append((task.subject_id, hours_to_allocate))
                    task.remaining_hours -= hours_to_allocate
                    daily_hours += hours_to_allocate
            
            if daily_assignments:
                schedule[day] = daily_assignments
        
        solution = ScheduleNode(current_day=self.problem.max_days + 1,
                              assignments=schedule,
                              remaining_tasks=tasks)
        solution.calculate_objective_score(self.problem)
        
        return solution


class RandomScheduler:    
    def __init__(self, problem):
        self.problem = problem
    
    def solve(self, seed=42):
        random.seed(seed)
        tasks = copy.deepcopy(self.problem.tasks)
        schedule = {}
        
        for day in range(1, self.problem.max_days + 1):
            daily_hours = 0
            daily_assignments = []
            
            available_tasks = [t for t in tasks if t.remaining_hours > 0 and t.deadline >= day]
            
            while available_tasks and daily_hours < self.problem.max_daily_hours:
                task = random.choice(available_tasks)
                
                max_allocatable = min(
                    task.remaining_hours,
                    self.problem.max_daily_hours - daily_hours
                )
                
                if max_allocatable >= self.problem.min_session_hours:
                    hours_to_allocate = random.randint(self.problem.min_session_hours, 
                                                     max_allocatable)
                    
                    daily_assignments.append((task.subject_id, hours_to_allocate))
                    task.remaining_hours -= hours_to_allocate
                    daily_hours += hours_to_allocate
                
                available_tasks = [t for t in available_tasks if t.remaining_hours > 0]
            
            if daily_assignments:
                schedule[day] = daily_assignments
        
        solution = ScheduleNode(current_day=self.problem.max_days + 1,
                              assignments=schedule,
                              remaining_tasks=tasks)
        solution.calculate_objective_score(self.problem)
        
        return solution


class RoundRobinScheduler:    
    def __init__(self, problem):
        self.problem = problem
    
    def solve(self):
        tasks = copy.deepcopy(self.problem.tasks)
        schedule = {}
        
        for day in range(1, self.problem.max_days + 1):
            daily_hours = 0
            daily_assignments = []
            
            available_tasks = [t for t in tasks if t.remaining_hours > 0 and t.deadline >= day]
            task_index = 0
            
            while available_tasks and daily_hours < self.problem.max_daily_hours:
                if task_index >= len(available_tasks):
                    task_index = 0
                
                task = available_tasks[task_index]
                
                hours_to_allocate = min(
                    max(self.problem.min_session_hours, 1),
                    task.remaining_hours,
                    self.problem.max_daily_hours - daily_hours
                )
                
                if hours_to_allocate >= self.problem.min_session_hours:
                    daily_assignments.append((task.subject_id, hours_to_allocate))
                    task.remaining_hours -= hours_to_allocate
                    daily_hours += hours_to_allocate
                
                task_index += 1
                
                available_tasks = [t for t in available_tasks if t.remaining_hours > 0]
                if task_index >= len(available_tasks):
                    task_index = 0
            
            if daily_assignments:
                schedule[day] = daily_assignments
        
        solution = ScheduleNode(current_day=self.problem.max_days + 1,
                              assignments=schedule,
                              remaining_tasks=tasks)
        solution.calculate_objective_score(self.problem)
        
        return solution


def compare_algorithms(problem, include_bnb=True, time_limit=60):
    results = {}
    
    print("Running Greedy algorithm...")
    greedy = GreedyScheduler(problem)
    greedy_solution = greedy.solve()
    results['greedy'] = {
        'solution': greedy_solution,
        'score': greedy_solution.objective_score,
        'algorithm': 'Greedy'
    }
    
    print("Running Random algorithm...")
    random_scheduler = RandomScheduler(problem)
    random_solution = random_scheduler.solve()
    results['random'] = {
        'solution': random_solution,
        'score': random_solution.objective_score,
        'algorithm': 'Random'
    }
    
    print("Running Round Robin algorithm...")
    rr = RoundRobinScheduler(problem)
    rr_solution = rr.solve()
    results['round_robin'] = {
        'solution': rr_solution,
        'score': rr_solution.objective_score,
        'algorithm': 'Round Robin'
    }
    
    if include_bnb:
        print("Running Branch and Bound algorithm...")
        from branch_bound_scheduler import BranchAndBoundScheduler
        bnb = BranchAndBoundScheduler(problem)
        bnb_solution = bnb.solve(time_limit=time_limit)
        results['branch_bound'] = {
            'solution': bnb_solution,
            'score': bnb_solution.objective_score if bnb_solution else 0,
            'algorithm': 'Branch and Bound',
            'statistics': bnb.get_statistics()
        }
    
    return results