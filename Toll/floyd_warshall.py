import numpy as np

def floyd_warshall(matrix):
    """
    Computes shortest paths between all city pairs.
    
    Args:
        matrix (np.ndarray): N x N cost matrix from build_matrix()
    
    Returns:
        np.ndarray: Optimized cost matrix
        np.ndarray: Next node matrix for path reconstruction
    """
    n = len(matrix)
    dist = np.copy(matrix)
    next_node = np.full((n, n), -1)  # For path reconstruction
    
    # Initialize next_node for direct paths
    for i in range(n):
        for j in range(n):
            if i != j and not np.isinf(matrix[i][j]):
                next_node[i][j] = j
    
    # Floyd-Warshall core algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if np.isfinite(dist[i][k]) and np.isfinite(dist[k][j]) and dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
    
    return dist, next_node
def reconstruct_path(start_idx, end_idx, next_node, cities):
    """
    Converts next_node matrix into human-readable path.
    
    Args:
        start_idx (int): Index of origin city in `cities` list
        end_idx (int): Index of destination city
        next_node (np.ndarray): Next node matrix from floyd_warshall()
        cities (list): List of city names
    
    Returns:
        list: Sequence of cities in optimal path, e.g., ["Mumbai", "Pune", "Bangalore"]
    """
    if next_node[start_idx][end_idx] == -1:
        return []  # No path exists
    
    path = [cities[start_idx]]
    steps = 0
    max_steps = len(cities)
    
    while start_idx != end_idx:
        if steps >= max_steps:
            return []  # Prevent infinite loop
        start_idx = next_node[start_idx][end_idx]
        path.append(cities[start_idx])
        steps += 1
    
    return path
