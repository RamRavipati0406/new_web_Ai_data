# fix_graph_depth.py
# Fix the depth values in the existing graph using BFS from seed topics

import pickle
import json
import networkx as nx
from collections import deque

# Seed topics (should be at depth 0)
SEED_TOPICS = [
    "Engineering",
    "Mechanical Engineering",
    "Electrical Engineering",
    "Civil Engineering",
    "Chemical Engineering",
    "Computer Engineering",
    "Industrial Engineering",
    "Aerospace Engineering",
    "Biomedical Engineering",
    "Environmental Engineering",
    "Systems Engineering",
    "Systems Theory",
    "Control Theory",
    "Robotics",
    "Automation",
    "Cybernetics",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Neural Network",
    "Natural Language Processing",
    "Computer Vision",
    "Reinforcement Learning",
    "Data Science",
    "Computational Engineering",
    "Software Engineering",
    "Information Technology"
]

print("Loading graph...")
G = pickle.load(open('engineering_graph.gpickle', 'rb'))

print(f"Original graph: {len(G.nodes())} nodes, {len(G.edges())} edges")
print(f"Original depth distribution: {{}}")
old_depths = {}
for node in G.nodes():
    d = G.nodes[node].get('depth', -1)
    old_depths[d] = old_depths.get(d, 0) + 1
for d in sorted(old_depths.keys()):
    print(f"  Depth {d}: {old_depths[d]} nodes")

# Correct depths using BFS from seed topics
print("\nRecalculating depths using BFS from seed topics...")
new_depth = {}
visited = set()
queue = deque()

# Initialize seed topics at depth 0
for topic in SEED_TOPICS:
    if topic in G.nodes():
        new_depth[topic] = 0
        visited.add(topic)
        queue.append((topic, 0))

# BFS to assign depths
while queue:
    current, current_depth = queue.popleft()
    
    # Add successors (outgoing edges = links this page points to)
    for successor in G.successors(current):
        if successor not in visited:
            new_depth[successor] = current_depth + 1
            visited.add(successor)
            queue.append((successor, current_depth + 1))

# Apply corrected depths to graph
for node in G.nodes():
    if node in new_depth:
        G.nodes[node]['depth'] = new_depth[node]
    else:
        # Orphan nodes (not reachable from seed topics) get depth = max + 1
        G.nodes[node]['depth'] = 3

print("\nNew depth distribution:")
new_depths = {}
for node in G.nodes():
    d = G.nodes[node].get('depth', -1)
    new_depths[d] = new_depths.get(d, 0) + 1
for d in sorted(new_depths.keys()):
    print(f"  Depth {d}: {new_depths[d]} nodes")

# Save corrected graph
print("\nSaving corrected graph...")
pickle.dump(G, open('engineering_graph.gpickle', 'wb'))

# Save corrected JSON
data = {
    'nodes': [
        {
            'id': node,
            'depth': G.nodes[node].get('depth', 0),
            'summary': G.nodes[node].get('summary', ''),
            'short_summary': G.nodes[node].get('short_summary', ''),
            'url': G.nodes[node].get('url', ''),
            'content_preview': G.nodes[node].get('content_preview', ''),
            'categories': G.nodes[node].get('categories', []),
            'sections': G.nodes[node].get('sections', []),
            'images': G.nodes[node].get('images', []),
            'references': G.nodes[node].get('references', []),
            'content_length': G.nodes[node].get('content_length', 0),
            'word_count': G.nodes[node].get('word_count', 0),
            'degree_centrality': G.nodes[node].get('degree_centrality', 0),
            'in_degree': G.nodes[node].get('in_degree', 0),
            'out_degree': G.nodes[node].get('out_degree', 0),
            'pagerank': G.nodes[node].get('pagerank', 0)
        }
        for node in G.nodes()
    ],
    'edges': [
        {'source': u, 'target': v}
        for u, v in G.edges()
    ]
}

with open('engineering_graph.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done! Graph corrected and saved.")
