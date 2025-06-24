from study_task import StudyTask, SchedulingProblem
from branch_bound_scheduler import BranchAndBoundScheduler
from baseline_algorithms import compare_algorithms
import json

def create_sample_problem():    
    tasks = [
        StudyTask(
            subject_id=1,
            name="Mathematics",
            required_hours=8,
            deadline=10,
            priority=5,
            difficulty=8,
            preferred_time=1,  # Morning
            dependencies=[]
        ),
        StudyTask(
            subject_id=2,
            name="Physics",
            required_hours=6,
            deadline=8,
            priority=4,
            difficulty=7,
            preferred_time=1,  # Morning
            dependencies=[]
        ),
        StudyTask(
            subject_id=3,
            name="Chemistry",
            required_hours=5,
            deadline=7,
            priority=3,
            difficulty=6,
            preferred_time=2,  # Afternoon
            dependencies=[]
        ),
        StudyTask(
            subject_id=4,
            name="English",
            required_hours=4,
            deadline=12,
            priority=2,
            difficulty=4,
            preferred_time=3,  # Evening
            dependencies=[]
        ),
        StudyTask(
            subject_id=5,
            name="History",
            required_hours=3,
            deadline=9,
            priority=2,
            difficulty=3,
            preferred_time=3,  # Evening
            dependencies=[]
        )
    ]
    
    problem = SchedulingProblem(
        tasks=tasks,
        max_days=14,
        max_daily_hours=8,
        min_session_hours=1
    )
    
    return problem

def print_schedule(solution, problem):
    if solution is None:
        print("No solution found!")
        return
    
    print(f"\n=== STUDY SCHEDULE ===")
    print(f"Total Score: {solution.objective_score:.2f}")
    print(f"=" * 50)
    
    subject_names = {task.subject_id: task.name for task in problem.tasks}
    
    for day in sorted(solution.assignments.keys()):
        print(f"\nDay {day}:")
        daily_total = 0
        for subject_id, hours in solution.assignments[day]:
            subject_name = subject_names.get(subject_id, f"Subject {subject_id}")
            print(f"  {subject_name}: {hours} hours")
            daily_total += hours
        print(f"  Total: {daily_total} hours")
    
    print(f"\n=== COMPLETION STATUS ===")
    for task in solution.remaining_tasks:
        completion = task.get_completion_percentage()
        status = "✓ COMPLETED" if task.is_completed() else f"✗ {completion:.1f}% done"
        print(f"{task.name}: {status}")

def save_results_to_json(results, filename="scheduling_results.json"):
    json_results = {}
    
    for alg_name, result in results.items():
        json_results[alg_name] = {
            'algorithm': result['algorithm'],
            'score': result['score'],
            'assignments': result['solution'].assignments if result['solution'] else {},
        }
        
        if 'statistics' in result:
            json_results[alg_name]['statistics'] = result['statistics']
    
    with open(filename, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"Results saved to {filename}")

def main():
    print("=== Study Scheduling Optimization System ===\n")
    
    problem = create_sample_problem()
    print(f"Problem created: {problem}")
    print(f"Total required hours: {problem.get_total_required_hours()}")
    print(f"Available hours: {problem.max_days * problem.max_daily_hours}")
    print(f"Problem feasible: {problem.is_feasible()}\n")
    
    print("Option 1: Branch and Bound only")
    print("-" * 40)
    bnb_scheduler = BranchAndBoundScheduler(problem)
    bnb_solution = bnb_scheduler.solve(time_limit=30)  # 30 second limit
    
    if bnb_solution:
        print_schedule(bnb_solution, problem)
        stats = bnb_scheduler.get_statistics()
        print(f"\nAlgorithm Statistics:")
        print(f"Nodes explored: {stats['nodes_explored']}")
        print(f"Nodes pruned: {stats['nodes_pruned']}")
        print(f"Runtime: {stats['runtime']:.2f} seconds")
    
    print("\n" + "="*60 + "\n")
    
    print("Option 2: Algorithm Comparison")
    print("-" * 40)
    results = compare_algorithms(problem, include_bnb=True, time_limit=30)
    
    print(f"\n=== ALGORITHM COMPARISON ===")
    print(f"{'Algorithm':<15} {'Score':<10} {'Status'}")
    print("-" * 35)
    
    for alg_name, result in results.items():
        status = "Success" if result['solution'] else "Failed"
        print(f"{result['algorithm']:<15} {result['score']:<10.2f} {status}")
    
    best_alg = max(results.keys(), key=lambda k: results[k]['score'])
    best_solution = results[best_alg]['solution']
    
    print(f"\n=== BEST SOLUTION ({results[best_alg]['algorithm']}) ===")
    print_schedule(best_solution, problem)
    
    save_results_to_json(results)

if __name__ == "__main__":
    main()