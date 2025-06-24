"""
Problem instance generator for testing different scenarios
"""

import random
from study_task import StudyTask, SchedulingProblem

class ProblemGenerator:
    """Generate various test problems for algorithm evaluation"""
    
    @staticmethod
    def generate_small_problem(seed=42):
        """Generate a small problem (3-5 subjects, 1 week)"""
        random.seed(seed)
        
        subjects = ["Math", "Physics", "Chemistry", "English"]
        tasks = []
        
        for i, subject in enumerate(subjects[:4]):
            tasks.append(StudyTask(
                subject_id=i+1,
                name=subject,
                required_hours=random.randint(3, 6),
                deadline=random.randint(5, 7),
                priority=random.randint(2, 5),
                difficulty=random.randint(3, 8),
                preferred_time=random.randint(1, 3),
                dependencies=[]
            ))
        
        return SchedulingProblem(
            tasks=tasks,
            max_days=7,
            max_daily_hours=6,
            min_session_hours=1
        )
    
    @staticmethod
    def generate_medium_problem(seed=42):
        """Generate a medium problem (6-8 subjects, 2 weeks)"""
        random.seed(seed)
        
        subjects = ["Math", "Physics", "Chemistry", "Biology", "English", "History", "Geography", "Art"]
        tasks = []
        
        for i, subject in enumerate(subjects[:6]):
            tasks.append(StudyTask(
                subject_id=i+1,
                name=subject,
                required_hours=random.randint(4, 10),
                deadline=random.randint(8, 14),
                priority=random.randint(1, 5),
                difficulty=random.randint(2, 9),
                preferred_time=random.randint(1, 3),
                dependencies=[]
            ))
        
        return SchedulingProblem(
            tasks=tasks,
            max_days=14,
            max_daily_hours=8,
            min_session_hours=1
        )
    
    @staticmethod
    def generate_large_problem(seed=42):
        """Generate a large problem (10+ subjects, 3-4 weeks)"""
        random.seed(seed)
        
        subjects = ["Math", "Physics", "Chemistry", "Biology", "English", "History", 
                   "Geography", "Art", "Music", "Computer Science", "Economics", "Psychology"]
        tasks = []
        
        for i, subject in enumerate(subjects[:10]):
            tasks.append(StudyTask(
                subject_id=i+1,
                name=subject,
                required_hours=random.randint(5, 15),
                deadline=random.randint(15, 28),
                priority=random.randint(1, 5),
                difficulty=random.randint(1, 10),
                preferred_time=random.randint(1, 3),
                dependencies=[]
            ))
        
        return SchedulingProblem(
            tasks=tasks,
            max_days=28,
            max_daily_hours=10,
            min_session_hours=1
        )
    
    @staticmethod
    def generate_tight_deadlines_problem(seed=42):
        """Generate a problem with very tight deadlines"""
        random.seed(seed)
        
        subjects = ["Exam1", "Exam2", "Exam3", "Assignment1", "Assignment2"]
        tasks = []
        
        for i, subject in enumerate(subjects):
            tasks.append(StudyTask(
                subject_id=i+1,
                name=subject,
                required_hours=random.randint(6, 12),
                deadline=random.randint(3, 6),  # Very tight deadlines
                priority=random.randint(4, 5),  # High priority
                difficulty=random.randint(6, 10),  # High difficulty
                preferred_time=random.randint(1, 3),
                dependencies=[]
            ))
        
        return SchedulingProblem(
            tasks=tasks,
            max_days=7,
            max_daily_hours=12,  # Long study days needed
            min_session_hours=1
        )
    
    @staticmethod
    def generate_dependency_problem(seed=42):
        """Generate a problem with subject dependencies"""
        random.seed(seed)
        
        tasks = [
            StudyTask(1, "Basic Math", 4, 8, 4, 5, 1, []),
            StudyTask(2, "Advanced Math", 6, 12, 5, 8, 1, [1]),  # Depends on Basic Math
            StudyTask(3, "Physics Basics", 5, 10, 4, 6, 1, [1]),  # Depends on Basic Math
            StudyTask(4, "Advanced Physics", 7, 14, 5, 9, 1, [2, 3]),  # Depends on both math courses
            StudyTask(5, "Chemistry", 4, 9, 3, 5, 2, []),
            StudyTask(6, "English", 3, 11, 2, 3, 3, [])
        ]
        
        return SchedulingProblem(
            tasks=tasks,
            max_days=14,
            max_daily_hours=8,
            min_session_hours=1
        )
    
    @staticmethod
    def generate_balanced_problem(seed=42):
        """Generate a well-balanced, realistic problem"""
        random.seed(seed)
        
        tasks = [
            StudyTask(1, "Calculus", 12, 14, 5, 8, 1, []),
            StudyTask(2, "Physics", 10, 12, 4, 7, 1, []),
            StudyTask(3, "Programming", 8, 10, 4, 6, 2, []),
            StudyTask(4, "Statistics", 6, 11, 3, 5, 2, []),
            StudyTask(5, "English Essay", 4, 8, 2, 4, 3, []),
            StudyTask(6, "History Project", 5, 13, 2, 3, 3, [])
        ]
        
        return SchedulingProblem(
            tasks=tasks,
            max_days=14,
            max_daily_hours=8,
            min_session_hours=1
        )

def test_all_problems():
    """Test all generated problems"""
    from baseline_algorithms import compare_algorithms
    
    problems = {
        "Small": ProblemGenerator.generate_small_problem(),
        "Medium": ProblemGenerator.generate_medium_problem(),
        "Large": ProblemGenerator.generate_large_problem(),
        "Tight Deadlines": ProblemGenerator.generate_tight_deadlines_problem(),
        "Dependencies": ProblemGenerator.generate_dependency_problem(),
        "Balanced": ProblemGenerator.generate_balanced_problem()
    }
    
    for name, problem in problems.items():
        print(f"\n=== Testing {name} Problem ===")
        print(f"Subjects: {len(problem.tasks)}")
        print(f"Days: {problem.max_days}")
        print(f"Total required hours: {problem.get_total_required_hours()}")
        print(f"Available hours: {problem.max_days * problem.max_daily_hours}")
        print(f"Feasible: {problem.is_feasible()}")
        
        # Run comparison (without B&B for large problems to save time)
        include_bnb = len(problem.tasks) <= 6  # Only run B&B for smaller problems
        results = compare_algorithms(problem, include_bnb=include_bnb, time_limit=30)
        
        print(f"\nResults:")
        for alg_name, result in results.items():
            status = "✓" if result['solution'] else "✗"
            print(f"  {result['algorithm']}: {status} Score: {result['score']:.2f}")

if __name__ == "__main__":
    test_all_problems()