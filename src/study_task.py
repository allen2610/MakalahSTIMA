"""
Data structures for study scheduling problem
"""

class StudyTask:
    """Represents a subject that needs to be studied"""
    
    def __init__(self, subject_id, name, required_hours, deadline, 
                 priority, difficulty, preferred_time, dependencies=None):
        self.subject_id = subject_id
        self.name = name
        self.required_hours = required_hours
        self.deadline = deadline
        self.priority = priority        # 1-5 scale
        self.difficulty = difficulty    # 1-10 scale
        self.preferred_time = preferred_time  # 1=morning, 2=afternoon, 3=evening
        self.dependencies = dependencies or []  # List of prerequisite subject_ids
        self.remaining_hours = required_hours
    
    def __str__(self):
        return f"StudyTask({self.name}, {self.remaining_hours}/{self.required_hours}h, deadline={self.deadline})"
    
    def __repr__(self):
        return self.__str__()
    
    def is_completed(self):
        """Check if the task is completed"""
        return self.remaining_hours <= 0
    
    def get_completion_percentage(self):
        """Get completion percentage"""
        if self.required_hours == 0:
            return 100.0
        return ((self.required_hours - self.remaining_hours) / self.required_hours) * 100


class ScheduleNode:
    """Represents a node in the Branch and Bound search tree"""
    
    def __init__(self, current_day, assignments, remaining_tasks):
        self.current_day = current_day
        self.assignments = assignments    # Dict: {day: [(subject_id, hours)]}
        self.remaining_tasks = remaining_tasks  # List of StudyTask objects
        self.objective_score = 0
        self.upper_bound = 0
        self.is_feasible = True
    
    def calculate_objective_score(self, problem):
        """Calculate the objective function score for this node"""
        score = 0
        weights = problem.weights
        
        for day, day_assignments in self.assignments.items():
            daily_total_hours = sum(hours for _, hours in day_assignments)
            
            for subject_id, hours in day_assignments:
                # Find the corresponding task
                task = None
                for t in problem.tasks:
                    if t.subject_id == subject_id:
                        task = t
                        break
                
                if task is None:
                    continue
                
                # Priority component
                priority_score = weights["priority"] * task.priority
                
                # Time preference bonus
                time_bonus = self._calculate_time_bonus(task, day)
                time_score = weights["time_pref"] * time_bonus
                
                # Balance bonus
                balance_bonus = max(0, 2.0 - (daily_total_hours / problem.max_daily_hours))
                balance_score = weights["balance"] * balance_bonus
                
                # Deadline penalty
                deadline_penalty = self._calculate_deadline_penalty(task, day)
                deadline_score = weights["deadline"] * deadline_penalty
                
                # Total score for this study session
                session_score = (priority_score + time_score + balance_score - deadline_score) * hours
                score += session_score
        
        self.objective_score = score
        return score
    
    def calculate_upper_bound(self, problem):
        """Calculate optimistic upper bound for this node"""
        current_score = self.objective_score
        optimistic_future = 0
        
        weights = problem.weights
        remaining_days = problem.max_days - self.current_day + 1
        
        for task in self.remaining_tasks:
            if task.remaining_hours > 0:
                # More realistic bound - consider deadline pressure
                days_until_deadline = max(1, task.deadline - self.current_day + 1)
                
                # Penalize if we're running out of time
                deadline_factor = 1.0
                if days_until_deadline < remaining_days:
                    deadline_factor = 0.7  # Reduce optimism if deadline is tight
                
                # Optimistic assumptions: good time bonus, good balance, minimal deadline penalty
                max_score_per_hour = (weights["priority"] * task.priority + 
                                    weights["time_pref"] * 1.5 +  # Slightly less optimistic
                                    weights["balance"] * 1.5) * deadline_factor  # Apply deadline factor
                
                optimistic_future += max_score_per_hour * task.remaining_hours
        
        self.upper_bound = current_score + optimistic_future
        return self.upper_bound
    
    def _calculate_time_bonus(self, task, day):
        """Calculate time preference bonus (simplified - assumes optimal time)"""
        # For now, assume optimal time preference
        # In full implementation, this would check actual time slots
        return 2.0  # Maximum bonus
    
    def _calculate_deadline_penalty(self, task, day):
        """Calculate deadline pressure penalty"""
        days_until_deadline = task.deadline - day
        if days_until_deadline <= 0:
            return 10.0  # Heavy penalty for missing deadline
        
        penalty = (task.difficulty / 10.0) * (1.0 / days_until_deadline)
        return max(0, penalty)
    
    def __str__(self):
        return f"ScheduleNode(day={self.current_day}, score={self.objective_score:.2f}, bound={self.upper_bound:.2f})"
    
    def __repr__(self):
        return self.__str__()


class SchedulingProblem:
    """Represents the complete scheduling problem instance"""
    
    def __init__(self, tasks, max_days, max_daily_hours, min_session_hours=1):
        self.tasks = tasks
        self.max_days = max_days
        self.max_daily_hours = max_daily_hours
        self.min_session_hours = min_session_hours
        self.weights = {
            "priority": 3.0, 
            "time_pref": 1.0, 
            "balance": 2.0, 
            "deadline": 4.0
        }
    
    def get_total_required_hours(self):
        """Get total hours required across all tasks"""
        return sum(task.required_hours for task in self.tasks)
    
    def is_feasible(self):
        """Check if the problem is theoretically solvable"""
        total_hours = self.get_total_required_hours()
        available_hours = self.max_days * self.max_daily_hours
        return total_hours <= available_hours
    
    def __str__(self):
        return f"SchedulingProblem({len(self.tasks)} tasks, {self.max_days} days, {self.max_daily_hours}h/day)"