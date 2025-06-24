"""
Branch and Bound algorithm implementation for study scheduling
"""

import heapq
import time
import copy
from study_task import ScheduleNode

class BranchAndBoundScheduler:
    """Branch and Bound algorithm for optimal study scheduling"""
    
    def __init__(self, problem):
        self.problem = problem
        self.best_solution = None
        self.best_score = float('-inf')
        self.nodes_explored = 0
        self.nodes_pruned = 0
        self.start_time = None
        
    def solve(self, time_limit=300):
        """
        Main solving method with optional time limit in seconds
        Returns the best solution found
        """
        self.start_time = time.time()
        
        # Initialize with root node
        root = ScheduleNode(current_day=1, assignments={}, 
                           remaining_tasks=copy.deepcopy(self.problem.tasks))
        root.calculate_upper_bound(self.problem)
        
        # Priority queue (max-heap using negative values)
        priority_queue = [(-root.upper_bound, 0, root)]
        node_counter = 1
        
        print(f"Starting Branch and Bound search...")
        print(f"Problem: {len(self.problem.tasks)} subjects, {self.problem.max_days} days")
        
        # For larger problems, use a more aggressive approach
        max_queue_size = 1000 if len(self.problem.tasks) > 5 else 10000
        
        while priority_queue and self._within_time_limit(time_limit):
            # Extract node with highest upper bound
            neg_bound, _, current_node = heapq.heappop(priority_queue)
            self.nodes_explored += 1
            
            if self.nodes_explored % 1000 == 0:
                remaining_hours = sum(t.remaining_hours for t in current_node.remaining_tasks)
                queue_size = len(priority_queue)
                print(f"Explored {self.nodes_explored} nodes, best: {self.best_score:.2f}, day: {current_node.current_day}, remaining: {remaining_hours}h, queue: {queue_size}")
            
            # Pruning check
            if -neg_bound <= self.best_score:
                self.nodes_pruned += 1
                continue
                
            # Check if complete solution
            if self._is_complete_solution(current_node):
                current_node.calculate_objective_score(self.problem)
                if current_node.objective_score > self.best_score:
                    self.best_score = current_node.objective_score
                    self.best_solution = current_node
                    print(f"New best solution found! Score: {self.best_score:.2f}")
                continue
                
            # Generate and process child nodes
            children = self._generate_children(current_node)
            
            # Limit queue size for large problems
            if len(priority_queue) > max_queue_size:
                # Keep only the best nodes
                priority_queue = priority_queue[:max_queue_size//2]
                heapq.heapify(priority_queue)
            
            for child in children:
                if child.is_feasible and child.upper_bound > self.best_score:
                    heapq.heappush(priority_queue, 
                                 (-child.upper_bound, node_counter, child))
                    node_counter += 1
                else:
                    self.nodes_pruned += 1
                    
        elapsed_time = time.time() - self.start_time
        print(f"Search completed in {elapsed_time:.2f} seconds")
        print(f"Nodes explored: {self.nodes_explored}, Nodes pruned: {self.nodes_pruned}")
        
        return self.best_solution
    
    def _within_time_limit(self, time_limit):
        """Check if we're still within the time limit"""
        if time_limit is None:
            return True
        return (time.time() - self.start_time) < time_limit
    
    def _is_complete_solution(self, node):
        """Check if the node represents a complete solution"""
        # Check if all tasks are completed OR we've gone through all days
        all_tasks_done = all(task.remaining_hours <= 0 for task in node.remaining_tasks)
        past_last_day = node.current_day > self.problem.max_days
        
        return all_tasks_done or past_last_day
    
    def _generate_children(self, node):
        """Generate all possible child nodes for the next day"""
        children = []
        next_day = node.current_day
        
        if next_day > self.problem.max_days:
            return children
            
        # Get subjects that still need study hours and satisfy dependencies
        available_subjects = [task for task in node.remaining_tasks 
                            if task.remaining_hours > 0 and 
                            self._dependencies_satisfied(task, node)]
        
        # Always create a "skip day" option
        skip_child = self._create_skip_day_child(node)
        children.append(skip_child)
        
        if not available_subjects:
            return children
        
        # For larger problems, be more selective about combinations
        if len(self.problem.tasks) > 5:
            # Generate only high-priority combinations
            selected_combinations = self._generate_smart_combinations(available_subjects, next_day)
        else:
            # For smaller problems, generate all combinations
            combinations = self._generate_daily_combinations(available_subjects, 
                                                           self.problem.max_daily_hours)
            non_empty_combinations = [c for c in combinations if c]
            non_empty_combinations.sort(key=lambda x: self._calculate_combination_priority(x), 
                                      reverse=True)
            selected_combinations = non_empty_combinations[:20]  # Limit to top 20
        
        for combination in selected_combinations:
            child = self._create_child_node(node, next_day, combination)
            if child.is_feasible:
                children.append(child)
                
        return children
    
    def _generate_smart_combinations(self, subjects, day):
        """Generate smart combinations for larger problems"""
        combinations = []
        
        # Sort subjects by urgency and priority
        subjects_by_priority = sorted(subjects, 
                                    key=lambda s: (s.deadline - day, -s.priority, -s.difficulty))
        
        # Strategy 1: Focus on most urgent subject
        if subjects_by_priority:
            urgent_subject = subjects_by_priority[0]
            max_hours = min(urgent_subject.remaining_hours, self.problem.max_daily_hours)
            for hours in range(self.problem.min_session_hours, max_hours + 1):
                combinations.append([(urgent_subject.subject_id, hours)])
        
        # Strategy 2: Balance 2 subjects
        if len(subjects_by_priority) >= 2:
            s1, s2 = subjects_by_priority[0], subjects_by_priority[1]
            for h1 in range(self.problem.min_session_hours, 
                           min(s1.remaining_hours, self.problem.max_daily_hours - self.problem.min_session_hours) + 1):
                remaining_hours = self.problem.max_daily_hours - h1
                max_h2 = min(s2.remaining_hours, remaining_hours)
                if max_h2 >= self.problem.min_session_hours:
                    for h2 in range(self.problem.min_session_hours, max_h2 + 1):
                        combinations.append([(s1.subject_id, h1), (s2.subject_id, h2)])
        
        # Strategy 3: Complete a subject if possible
        for subject in subjects_by_priority:
            if subject.remaining_hours <= self.problem.max_daily_hours:
                combinations.append([(subject.subject_id, subject.remaining_hours)])
        
        # Remove duplicates and sort by priority
        unique_combinations = []
        seen = set()
        for combo in combinations:
            combo_tuple = tuple(sorted(combo))
            if combo_tuple not in seen:
                seen.add(combo_tuple)
                unique_combinations.append(combo)
        
        unique_combinations.sort(key=lambda x: self._calculate_combination_priority(x), reverse=True)
        return unique_combinations[:15]  # Return top 15 combinations
    
    def _generate_daily_combinations(self, subjects, max_hours):
        """Generate all valid study hour combinations for a day"""
        combinations = []
        
        def backtrack(current_combo, remaining_hours, subject_index):
            if subject_index >= len(subjects):
                # Only add non-empty combinations here
                if current_combo:
                    combinations.append(current_combo.copy())
                return
                
            subject = subjects[subject_index]
            max_allocatable = min(remaining_hours, subject.remaining_hours)
            
            # Try not studying this subject today
            backtrack(current_combo, remaining_hours, subject_index + 1)
            
            # Try studying this subject for different hours
            for hours in range(self.problem.min_session_hours, 
                             max_allocatable + 1):
                if hours <= remaining_hours:
                    current_combo.append((subject.subject_id, hours))
                    backtrack(current_combo, remaining_hours - hours, 
                             subject_index + 1)
                    current_combo.pop()
                
        backtrack([], max_hours, 0)
        
        return combinations
    
    def _calculate_combination_priority(self, combination):
        """Calculate priority score for a combination"""
        if not combination:
            return 0
        
        score = 0
        for subject_id, hours in combination:
            task = next((t for t in self.problem.tasks if t.subject_id == subject_id), None)
            if task:
                urgency = 1.0 / max(1, task.deadline - 1)  # Higher urgency = higher score
                score += task.priority * urgency * hours
        return score
    
    def _create_child_node(self, parent, day, combination):
        """Create a child node with the given day assignment"""
        child = ScheduleNode(current_day=day + 1, 
                           assignments=copy.deepcopy(parent.assignments),
                           remaining_tasks=copy.deepcopy(parent.remaining_tasks))
        
        # Apply the combination to the child node
        if combination:
            child.assignments[day] = combination
        
        # Update remaining hours for affected subjects
        for subject_id, hours in combination:
            for task in child.remaining_tasks:
                if task.subject_id == subject_id:
                    task.remaining_hours -= hours
                    break
                    
        # Calculate scores and bounds
        child.calculate_objective_score(self.problem)
        child.calculate_upper_bound(self.problem)
        child.is_feasible = self._check_feasibility(child)
        
        return child
    
    def _create_skip_day_child(self, parent):
        """Create a child node that skips the current day"""
        child = ScheduleNode(current_day=parent.current_day + 1,
                           assignments=copy.deepcopy(parent.assignments),
                           remaining_tasks=copy.deepcopy(parent.remaining_tasks))
        
        child.calculate_objective_score(self.problem)
        child.calculate_upper_bound(self.problem)
        child.is_feasible = self._check_feasibility(child)
        
        return child
    
    def _dependencies_satisfied(self, task, node):
        """Check if all dependencies for a task are satisfied"""
        for dep_id in task.dependencies:
            for dep_task in node.remaining_tasks:
                if dep_task.subject_id == dep_id and dep_task.remaining_hours > 0:
                    return False
        return True
    
    def _check_feasibility(self, node):
        """Check if the current node can lead to a feasible solution"""
        remaining_days = self.problem.max_days - node.current_day + 1
        total_remaining_hours = sum(task.remaining_hours 
                                  for task in node.remaining_tasks)
        
        # Check if enough time remains
        if total_remaining_hours > remaining_days * self.problem.max_daily_hours:
            return False
            
        # Check deadline feasibility
        for task in node.remaining_tasks:
            if task.remaining_hours > 0:
                days_until_deadline = task.deadline - node.current_day + 1
                if days_until_deadline <= 0:
                    return False  # Past deadline
                if task.remaining_hours > days_until_deadline * self.problem.max_daily_hours:
                    return False
                    
        return True
    
    def get_statistics(self):
        """Get algorithm performance statistics"""
        return {
            "nodes_explored": self.nodes_explored,
            "nodes_pruned": self.nodes_pruned,
            "best_score": self.best_score,
            "runtime": time.time() - self.start_time if self.start_time else 0
        }