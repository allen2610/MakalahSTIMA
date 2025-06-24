import json
import matplotlib.pyplot as plt
import pandas as pd
from study_task import SchedulingProblem

class ResultsAnalyzer:
    
    def __init__(self):
        self.results_data = []
    
    def add_result(self, problem_name, problem, results):
        problem_stats = {
            'name': problem_name,
            'num_subjects': len(problem.tasks),
            'num_days': problem.max_days,
            'total_hours': problem.get_total_required_hours(),
            'max_daily_hours': problem.max_daily_hours,
            'feasible': problem.is_feasible()
        }
        
        for alg_name, result in results.items():
            result_entry = problem_stats.copy()
            result_entry.update({
                'algorithm': result['algorithm'],
                'score': result['score'],
                'success': result['solution'] is not None
            })
            
            if 'statistics' in result:
                result_entry.update(result['statistics'])
            
            self.results_data.append(result_entry)
    
    def generate_comparison_report(self):
        if not self.results_data:
            print("No results data available!")
            return
        
        df = pd.DataFrame(self.results_data)
        
        print("=== ALGORITHM PERFORMANCE ANALYSIS ===\n")
        
        print("1. Overall Performance by Algorithm:")
        print("-" * 40)
        alg_summary = df.groupby('algorithm').agg({
            'score': ['mean', 'std', 'max'],
            'success': 'mean'
        }).round(2)
        print(alg_summary)
        
        print("\n2. Performance by Problem Size:")
        print("-" * 40)
        size_summary = df.groupby(['num_subjects', 'algorithm'])['score'].mean().unstack()
        print(size_summary.round(2))
        
        print("\n3. Success Rate by Algorithm:")
        print("-" * 40)
        success_rate = df.groupby('algorithm')['success'].mean() * 100
        for alg, rate in success_rate.items():
            print(f"{alg}: {rate:.1f}%")
        
        return df
    
    def plot_performance_comparison(self, save_path=None):
        if not self.results_data:
            print("No results data available!")
            return
        
        df = pd.DataFrame(self.results_data)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Algorithm Performance Comparison', fontsize=16)
        
        ax1 = axes[0, 0]
        algorithms = df['algorithm'].unique()
        scores_by_alg = [df[df['algorithm'] == alg]['score'].values for alg in algorithms]
        ax1.boxplot(scores_by_alg, labels=algorithms)
        ax1.set_title('Score Distribution by Algorithm')
        ax1.set_ylabel('Objective Score')
        ax1.tick_params(axis='x', rotation=45)
        
        ax2 = axes[0, 1]
        for alg in algorithms:
            alg_data = df[df['algorithm'] == alg]
            ax2.scatter(alg_data['num_subjects'], alg_data['score'], 
                       label=alg, alpha=0.7)
        ax2.set_title('Performance vs Problem Size')
        ax2.set_xlabel('Number of Subjects')
        ax2.set_ylabel('Objective Score')
        ax2.legend()
        
        ax3 = axes[1, 0]
        success_rates = df.groupby('algorithm')['success'].mean()
        bars = ax3.bar(success_rates.index, success_rates.values)
        ax3.set_title('Success Rate by Algorithm')
        ax3.set_ylabel('Success Rate')
        ax3.set_ylim(0, 1.1)
        
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{height:.2f}', ha='center', va='bottom')
        
        ax4 = axes[1, 1]
        if 'runtime' in df.columns:
            runtime_data = df.dropna(subset=['runtime'])
            if not runtime_data.empty:
                runtime_by_alg = [runtime_data[runtime_data['algorithm'] == alg]['runtime'].values 
                                for alg in algorithms if alg in runtime_data['algorithm'].values]
                runtime_algs = [alg for alg in algorithms if alg in runtime_data['algorithm'].values]
                ax4.boxplot(runtime_by_alg, labels=runtime_algs)
                ax4.set_title('Runtime Comparison')
                ax4.set_ylabel('Runtime (seconds)')
                ax4.tick_params(axis='x', rotation=45)
            else:
                ax4.text(0.5, 0.5, 'No runtime data available', 
                        ha='center', va='center', transform=ax4.transAxes)
                ax4.set_title('Runtime Comparison')
        else:
            ax4.text(0.5, 0.5, 'No runtime data available', 
                    ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('Runtime Comparison')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def analyze_algorithm_scalability(self):
        if not self.results_data:
            print("No results data available!")
            return
        
        df = pd.DataFrame(self.results_data)
        
        print("\n=== SCALABILITY ANALYSIS ===")
        
        size_groups = df.groupby('num_subjects')
        
        for size, group in size_groups:
            print(f"\nProblems with {size} subjects:")
            print("-" * 30)
            
            for alg in group['algorithm'].unique():
                alg_data = group[group['algorithm'] == alg]
                avg_score = alg_data['score'].mean()
                success_rate = alg_data['success'].mean()
                
                if 'runtime' in alg_data.columns and not alg_data['runtime'].isna().all():
                    avg_runtime = alg_data['runtime'].mean()
                    print(f"{alg}: Score={avg_score:.2f}, Success={success_rate:.2f}, Runtime={avg_runtime:.2f}s")
                else:
                    print(f"{alg}: Score={avg_score:.2f}, Success={success_rate:.2f}")
    
    def export_results(self, filename="analysis_results.csv"):
        if not self.results_data:
            print("No results data available!")
            return
        
        df = pd.DataFrame(self.results_data)
        df.to_csv(filename, index=False)
        print(f"Results exported to {filename}")
    
    def find_best_algorithm_by_scenario(self):
        if not self.results_data:
            print("No results data available!")
            return
        
        df = pd.DataFrame(self.results_data)
        
        print("\n=== BEST ALGORITHM BY SCENARIO ===")
        
        scenarios = [
            ("Small Problems (≤5 subjects)", df['num_subjects'] <= 5),
            ("Medium Problems (6-8 subjects)", (df['num_subjects'] >= 6) & (df['num_subjects'] <= 8)),
            ("Large Problems (>8 subjects)", df['num_subjects'] > 8),
            ("Tight Time Constraints", df['total_hours'] / (df['num_days'] * df['max_daily_hours']) > 0.8),
            ("Relaxed Time Constraints", df['total_hours'] / (df['num_days'] * df['max_daily_hours']) <= 0.6)
        ]
        
        for scenario_name, condition in scenarios:
            scenario_data = df[condition]
            if scenario_data.empty:
                continue
                
            best_by_score = scenario_data.groupby('algorithm')['score'].mean().idxmax()
            best_score = scenario_data.groupby('algorithm')['score'].mean().max()
            
            print(f"\n{scenario_name}:")
            print(f"  Best Algorithm: {best_by_score} (avg score: {best_score:.2f})")
            
            # Show all algorithms for this scenario
            scenario_summary = scenario_data.groupby('algorithm').agg({
                'score': 'mean',
                'success': 'mean'
            }).round(2)
            print("  All algorithms:")
            for alg, row in scenario_summary.iterrows():
                print(f"    {alg}: {row['score']:.2f} (success: {row['success']:.2f})")

def run_comprehensive_analysis():
    from problem_generator import ProblemGenerator
    from baseline_algorithms import compare_algorithms
    
    analyzer = ResultsAnalyzer()
    
    # Test different problem types
    problems = {
        "Small": ProblemGenerator.generate_small_problem(),
        "Medium": ProblemGenerator.generate_medium_problem(),
        "Tight_Deadlines": ProblemGenerator.generate_tight_deadlines_problem(),
        "Dependencies": ProblemGenerator.generate_dependency_problem(),
        "Balanced": ProblemGenerator.generate_balanced_problem()
    }
    
    print("Running comprehensive analysis...")
    
    for name, problem in problems.items():
        print(f"\nTesting {name} problem...")
        
        include_bnb = len(problem.tasks) <= 6
        results = compare_algorithms(problem, include_bnb=include_bnb, time_limit=30)
        
        analyzer.add_result(name, problem, results)
    
    df = analyzer.generate_comparison_report()
    analyzer.analyze_algorithm_scalability()
    analyzer.find_best_algorithm_by_scenario()
    analyzer.plot_performance_comparison("algorithm_comparison.png")
    analyzer.export_results("comprehensive_results.csv")
    
    return analyzer

if __name__ == "__main__":
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
        run_comprehensive_analysis()
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Please install missing libraries: pip install matplotlib pandas")