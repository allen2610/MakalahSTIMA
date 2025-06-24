import random
import time
import json
from study_task import StudyTask, SchedulingProblem
from baseline_algorithms import compare_algorithms
from results_analyzer import ResultsAnalyzer

class ComprehensiveTestSuite:    
    def __init__(self):
        self.results = []
        self.analyzer = ResultsAnalyzer()
    
    def generate_test_problems(self):
        problems = {}
        
        problems.update(self._generate_scale_problems())
        problems.update(self._generate_deadline_pressure_problems())
        problems.update(self._generate_priority_problems())
        problems.update(self._generate_difficulty_problems())
        problems.update(self._generate_realistic_scenarios())
        problems.update(self._generate_stress_tests())
        
        return problems
    
    def _generate_scale_problems(self):
        problems = {}
        
        problems["XS_Scale"] = self._create_problem(
            num_subjects=3,
            days=5,
            daily_hours=6,
            base_hours=2,
            hour_variance=1
        )
        
        problems["S_Scale"] = self._create_problem(
            num_subjects=4,
            days=7,
            daily_hours=8,
            base_hours=4,
            hour_variance=2
        )
        
        problems["M_Scale"] = self._create_problem(
            num_subjects=6,
            days=14,
            daily_hours=8,
            base_hours=6,
            hour_variance=3
        )
        
        problems["L_Scale"] = self._create_problem(
            num_subjects=8,
            days=21,
            daily_hours=10,
            base_hours=8,
            hour_variance=4
        )
        
        problems["XL_Scale"] = self._create_problem(
            num_subjects=10,
            days=28,
            daily_hours=12,
            base_hours=10,
            hour_variance=5
        )
        
        return problems
    
    def _generate_deadline_pressure_problems(self):
        problems = {}
        
        problems["Low_Pressure"] = self._create_problem(
            num_subjects=5,
            days=21,  
            daily_hours=6,
            base_hours=4,
            hour_variance=2,
            deadline_factor=0.8  
        )
        
        problems["Med_Pressure"] = self._create_problem(
            num_subjects=5,
            days=14,
            daily_hours=8,
            base_hours=5,
            hour_variance=2,
            deadline_factor=0.9 
        )
        
        problems["High_Pressure"] = self._create_problem(
            num_subjects=5,
            days=10,
            daily_hours=10,
            base_hours=6,
            hour_variance=2,
            deadline_factor=0.95  
        )
        
        problems["Extreme_Pressure"] = self._create_problem(
            num_subjects=4,
            days=6,
            daily_hours=12,
            base_hours=8,
            hour_variance=1,
            deadline_factor=0.98  
        )
        
        return problems
    
    def _generate_priority_problems(self):
        problems = {}
        
        problems["All_High_Priority"] = self._create_problem(
            num_subjects=5,
            days=14,
            daily_hours=8,
            base_hours=5,
            hour_variance=2,
            priority_pattern="high"
        )
        
        problems["Mixed_Priority"] = self._create_problem(
            num_subjects=6,
            days=14,
            daily_hours=8,
            base_hours=5,
            hour_variance=2,
            priority_pattern="mixed"
        )
        
        problems["One_Critical"] = self._create_problem(
            num_subjects=5,
            days=14,
            daily_hours=8,
            base_hours=5,
            hour_variance=2,
            priority_pattern="one_critical"
        )
        
        return problems
    
    def _generate_difficulty_problems(self):
        problems = {}
        
        problems["All_Easy"] = self._create_problem(
            num_subjects=6,
            days=14,
            daily_hours=8,
            base_hours=4,
            hour_variance=2,
            difficulty_pattern="easy"
        )
        
        problems["All_Hard"] = self._create_problem(
            num_subjects=4,
            days=14,
            daily_hours=8,
            base_hours=6,
            hour_variance=2,
            difficulty_pattern="hard"
        )
        
        problems["Mixed_Difficulty"] = self._create_problem(
            num_subjects=5,
            days=14,
            daily_hours=8,
            base_hours=5,
            hour_variance=3,
            difficulty_pattern="mixed"
        )
        
        return problems
    
    def _generate_realistic_scenarios(self):
        problems = {}
        
        problems["Midterm_Period"] = SchedulingProblem(
            tasks=[
                StudyTask(1, "Calculus Exam", 12, 7, 5, 9, 1, []),
                StudyTask(2, "Physics Exam", 10, 8, 5, 8, 1, []),
                StudyTask(3, "Chemistry Lab Report", 6, 5, 3, 6, 2, []),
                StudyTask(4, "English Essay", 4, 10, 2, 4, 3, []),
                StudyTask(5, "History Reading", 3, 12, 2, 3, 3, [])
            ],
            max_days=14,
            max_daily_hours=10,
            min_session_hours=1
        )
        
        problems["Final_Period"] = SchedulingProblem(
            tasks=[
                StudyTask(1, "Advanced Math", 20, 14, 5, 10, 1, []),
                StudyTask(2, "Organic Chemistry", 18, 12, 5, 9, 1, []),
                StudyTask(3, "Computer Science", 15, 10, 4, 7, 2, []),
                StudyTask(4, "Statistics", 12, 13, 4, 6, 2, []),
                StudyTask(5, "Literature Analysis", 8, 11, 3, 5, 3, []),
                StudyTask(6, "Philosophy Essay", 6, 9, 2, 4, 3, [])
            ],
            max_days=21,
            max_daily_hours=12,
            min_session_hours=1
        )
        
        problems["Regular_Semester"] = SchedulingProblem(
            tasks=[
                StudyTask(1, "Weekly Math Homework", 4, 7, 3, 6, 1, []),
                StudyTask(2, "Programming Project", 8, 14, 4, 7, 2, []),
                StudyTask(3, "Reading Assignment", 3, 10, 2, 3, 3, []),
                StudyTask(4, "Lab Preparation", 2, 5, 3, 5, 2, []),
                StudyTask(5, "Essay Writing", 5, 12, 2, 4, 3, [])
            ],
            max_days=14,
            max_daily_hours=6,
            min_session_hours=1
        )
        return problems
    
    def _generate_stress_tests(self):
        problems = {}
        problems["Minimal_Time"] = SchedulingProblem(
            tasks=[
                StudyTask(1, "Quick Review", 1, 2, 3, 3, 1, []),
                StudyTask(2, "Brief Study", 1, 3, 2, 4, 2, [])
            ],
            max_days=3,
            max_daily_hours=2,
            min_session_hours=1
        )
        
        problems["Single_Large_Task"] = SchedulingProblem(
            tasks=[
                StudyTask(1, "Massive Project", 60, 21, 5, 8, 1, [])
            ],
            max_days=21,
            max_daily_hours=8,
            min_session_hours=1
        )
        
        return problems
    
    def _create_problem(self, num_subjects, days, daily_hours, base_hours, hour_variance, 
                       deadline_factor=0.85, priority_pattern="random", difficulty_pattern="random"):
        subjects = ["Math", "Physics", "Chemistry", "Biology", "English", "History", 
                   "Geography", "Art", "Music", "Computer Science", "Economics", "Psychology"]
        
        tasks = []
        total_available_time = days * daily_hours
        
        for i in range(num_subjects):
            hours = max(1, base_hours + random.randint(-hour_variance, hour_variance))
            
            latest_deadline = int(days * deadline_factor)
            deadline = random.randint(max(2, latest_deadline - 3), latest_deadline)
            
            if priority_pattern == "high":
                priority = random.randint(4, 5)
            elif priority_pattern == "mixed":
                priority = random.randint(1, 5)
            elif priority_pattern == "one_critical":
                priority = 5 if i == 0 else random.randint(2, 4)
            else:  
                priority = random.randint(2, 5)
            
            if difficulty_pattern == "easy":
                difficulty = random.randint(1, 4)
            elif difficulty_pattern == "hard":
                difficulty = random.randint(7, 10)
            elif difficulty_pattern == "mixed":
                difficulty = random.randint(1, 10)
            else:
                difficulty = random.randint(3, 8)
            
            preferred_time = random.randint(1, 3)
            
            tasks.append(StudyTask(
                subject_id=i+1,
                name=f"{subjects[i % len(subjects)]}_{i+1}",
                required_hours=hours,
                deadline=deadline,
                priority=priority,
                difficulty=difficulty,
                preferred_time=preferred_time,
                dependencies=[]
            ))
        
        return SchedulingProblem(
            tasks=tasks,
            max_days=days,
            max_daily_hours=daily_hours,
            min_session_hours=1
        )
    
    def run_comprehensive_tests(self, save_results=True):
        problems = self.generate_test_problems()
        
        print(f"Running comprehensive tests on {len(problems)} problem instances...")
        print("=" * 60)
        
        for problem_name, problem in problems.items():
            print(f"\nTesting: {problem_name}")
            print(f"  Subjects: {len(problem.tasks)}, Days: {problem.max_days}")
            print(f"  Total hours: {problem.get_total_required_hours()}, Available: {problem.max_days * problem.max_daily_hours}")
            print(f"  Feasible: {problem.is_feasible()}")
            
            include_bnb = len(problem.tasks) <= 7  # Limit B&B to smaller problems
            time_limit = 60 if len(problem.tasks) <= 5 else 30  # Shorter time for larger problems
            
            try:
                start_time = time.time()
                results = compare_algorithms(problem, include_bnb=include_bnb, time_limit=time_limit)
                
                if time.time() - start_time > 120:  # 2 minute limit per problem
                    print(f"  Warning: Test took {time.time() - start_time:.1f} seconds")
                
                self.analyzer.add_result(problem_name, problem, results)
                
                best_score = max(r['score'] for r in results.values())
                best_alg = max(results.keys(), key=lambda k: results[k]['score'])
                print(f"  Best: {results[best_alg]['algorithm']} ({best_score:.1f})")
                
            except KeyboardInterrupt:
                print(f"  Interrupted - skipping {problem_name}")
                continue
            except Exception as e:
                print(f"  Error: {str(e)}")
                continue
        
        print("\n" + "=" * 60)
        print("COMPREHENSIVE ANALYSIS")
        print("=" * 60)
        
        df = self.analyzer.generate_comparison_report()
        self.analyzer.analyze_algorithm_scalability()
        self.analyzer.find_best_algorithm_by_scenario()
        
        if save_results:
            self.analyzer.plot_performance_comparison("comprehensive_comparison.png")
            self.analyzer.export_results("comprehensive_results.csv")
            
            # Save detailed results
            with open("detailed_test_results.json", "w") as f:
                json.dump(self.analyzer.results_data, f, indent=2)
            
            print(f"\nResults saved to:")
            print(f"  - comprehensive_comparison.png")
            print(f"  - comprehensive_results.csv") 
            print(f"  - detailed_test_results.json")
        
        return self.analyzer

def main():
    test_suite = ComprehensiveTestSuite()
    analyzer = test_suite.run_comprehensive_tests()
    
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    
    if analyzer.results_data:
        import pandas as pd
        df = pd.DataFrame(analyzer.results_data)
        
        print(f"\nTotal test cases: {len(df)}")
        print(f"Algorithms tested: {', '.join(df['algorithm'].unique())}")
        print(f"Problem sizes: {df['num_subjects'].min()}-{df['num_subjects'].max()} subjects")
        print(f"Success rate by algorithm:")
        
        for alg in df['algorithm'].unique():
            alg_data = df[df['algorithm'] == alg]
            success_rate = alg_data['success'].mean() * 100
            avg_score = alg_data['score'].mean()
            print(f"  {alg}: {success_rate:.1f}% success, {avg_score:.1f} avg score")

if __name__ == "__main__":
    main()