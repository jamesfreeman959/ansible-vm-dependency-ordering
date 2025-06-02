from ansible.errors import AnsibleFilterError

def graph_topology_sort(graph):
    """
    Perform a topological sort on a graph represented by a dictionary.
    
    Args:
        graph (dict): A dictionary where each key is a node, and the value
                      is a list of dependencies that must precede the node.
                      
    Returns:
        list: A list of nodes sorted in dependency-resolved order.
    
    Raises:
        AnsibleFilterError: If a cyclic dependency is detected.
    """
    sorted_items = []  # List to hold sorted nodes
    visited = {}       # Tracks visitation status of each node
    
    def visit(node):
        """
        Recursive helper function to visit nodes using Depth-First Search.
    	- Depth-First Search (DFS):
	 	  - The algorithm uses DFS to visit each node recursively.
	 	  - Nodes are marked temporarily during the exploration of dependencies.
	 	- Cycle detection:
	 	  - If a node is encountered again while marked as temporarily visited, this indicates a cyclic dependency, and the algorithm raises an error.
	 	- Ordering:
          - Each node is appended to sorted_items after all its dependencies have been resolved, ensuring dependencies appear before dependent nodes.
        
        Args:
            node (str): Current node to visit.
            
        Raises:
            AnsibleFilterError: If a cyclic dependency is detected.
        """
        if node in visited:
            if visited[node] == 'temporary':
                # A node visited temporarily again means a cycle
                raise AnsibleFilterError(f"Cyclic dependency detected: {node}")
            return  # Already permanently visited; nothing to do
        
        visited[node] = 'temporary'  # Mark node as temporarily visited
        
        # Recursively visit dependencies first
        for dependency in graph.get(node, []):
            visit(dependency)
        
        visited[node] = 'permanent'  # Mark node as permanently visited
        sorted_items.append(node)    # Append node after its dependencies
    
    # Visit all nodes in the graph to ensure comprehensive coverage
    for node in graph:
        visit(node)
    
    return sorted_items  # Return list of nodes sorted correctly

class FilterModule(object):
    def filters(self):
        return {'graph_topology_sort': graph_topology_sort}