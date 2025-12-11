# wikipedia_scraper.py
# Engineering Knowledge Graph - Data Acquisition Module (Enhanced Version)
# This script scrapes Wikipedia pages related to engineering topics and builds a knowledge graph
# with detailed node metadata

import wikipedia
import networkx as nx
import pickle
import json
from collections import deque
import time
import re

class EngineeringKnowledgeGraphScraper:
    """
    Scrapes Wikipedia for engineering topics and builds a knowledge graph.
    Enhanced version with detailed node metadata.
    """
    
    def __init__(self, seed_topics=None, max_depth=2, max_nodes=1000):
        """
        Initialize the scraper.
        
        Args:
            seed_topics: List of starting Wikipedia page titles
            max_depth: How many levels deep to scrape (2 recommended)
            max_nodes: Maximum number of nodes to collect (prevents explosion)
        """
        self.seed_topics = seed_topics or [
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
        self.max_depth = max_depth
        self.max_nodes = max_nodes
        self.graph = nx.DiGraph()
        self.visited = set()
        self.engineering_keywords = [
            'engineering', 'engineer', 'technology', 'design', 'system',
            'construction', 'manufacturing', 'circuit', 'structure', 'material',
            'process', 'mechanics', 'thermodynamics', 'automation', 'robotics',
            'artificial', 'intelligence', 'machine learning', 'algorithm',
            'neural', 'data', 'computer', 'software', 'control', 'optimization'
        ]
        
    def is_engineering_related(self, title, summary):
        """
        Check if a Wikipedia page is engineering-related.
        """
        text = (title + " " + summary).lower()
        return any(keyword in text for keyword in self.engineering_keywords)
    
    def get_page_details(self, page_title):
        """
        Get comprehensive details from a Wikipedia page.
        Enhanced version with rich metadata.
        """
        try:
            page = wikipedia.page(page_title, auto_suggest=False)
            
            # Extract detailed information
            details = {
                'links': page.links[:50],  # Limit to first 50 links
                'summary': page.summary,  # FULL summary (not truncated)
                'url': page.url,
                'content': page.content[:2000],  # First 2000 chars of full content
                'categories': page.categories[:10] if hasattr(page, 'categories') else [],
                'sections': page.sections[:15] if hasattr(page, 'sections') else [],
                'images': page.images[:3] if hasattr(page, 'images') else [],
                'references': page.references[:5] if hasattr(page, 'references') else [],
                'content_length': len(page.content),
                'word_count': len(page.content.split())
            }
            
            return details
            
        except (wikipedia.exceptions.DisambiguationError, 
                wikipedia.exceptions.PageError) as e:
            print(f"Error fetching {page_title}: {str(e)[:100]}")
            return None
        except Exception as e:
            print(f"Unexpected error for {page_title}: {str(e)[:100]}")
            return None
    
    def scrape(self):
        """
        Perform breadth-first scraping of Wikipedia with detailed metadata.
        """
        print(f"Starting scrape with {len(self.seed_topics)} seed topics...")
        print(f"Max depth: {self.max_depth}, Max nodes: {self.max_nodes}")
        print("Extracting detailed metadata for each node...")
        
        # Queue stores (page_title, depth)
        queue = deque([(topic, 0) for topic in self.seed_topics])
        
        while queue and len(self.graph.nodes) < self.max_nodes:
            current_title, current_depth = queue.popleft()
            
            # Skip if already visited or depth exceeded
            if current_title in self.visited or current_depth > self.max_depth:
                continue
            
            print(f"Processing: {current_title} (depth {current_depth}, nodes: {len(self.graph.nodes)})")
            
            # Get comprehensive page details
            details = self.get_page_details(current_title)
            
            if not details:
                continue
            
            # Add current node with metadata (reduce metadata extraction at deeper depths for speed)
            # At depth 2+, skip expensive metadata to speed up scraping
            if current_depth < 2:
                categories = details['categories']
                sections = details['sections']
                images = details['images']
            else:
                categories = []  # Skip expensive extraction at depth 2+
                sections = []
                images = []
            
            self.graph.add_node(
                current_title,
                depth=current_depth,
                summary=details['summary'],  # Full summary
                short_summary=details['summary'][:300] + "...",  # Short version for display
                url=details['url'],
                content_preview=details['content'][:500],  # Content preview
                categories=categories,
                sections=sections,
                images=images,
                references=details['references'][:5],
                content_length=details['content_length'],
                word_count=details['word_count']
            )
            self.visited.add(current_title)
            
            # Process links (only if we haven't reached max depth to avoid wasted work)
            if current_depth < self.max_depth:
                engineering_links = []
                for link in details['links'][:15]:  # Reduced from 50 to 15 links per page
                    # Skip if we've hit node limit
                    if len(self.graph.nodes) >= self.max_nodes:
                        break
                    
                    # Basic filtering
                    if any(skip in link.lower() for skip in ['list of', 'category:', 'file:', 'template:']):
                        continue
                    
                    # Check if engineering-related (quick check on title)
                    if self.is_engineering_related(link, ""):
                        engineering_links.append(link)
                
                # Queue new nodes for processing (don't add edges until target node is processed)
                for link in engineering_links[:10]:  # Limit to 10 new links per page (was 20)
                    # Only queue if not visited and within depth limit
                    if link not in self.visited and current_depth < self.max_depth:
                        queue.append((link, current_depth + 1))
                    
                    # Add edge only if the target node already exists with proper attributes
                    if link in self.graph.nodes():
                        self.graph.add_edge(current_title, link)
            else:
                # At max depth, still add edges to nodes we've already processed
                for link in details['links'][:10]:
                    if link in self.graph.nodes():
                        self.graph.add_edge(current_title, link)
            
            # Rate limiting (0.1s is conservative; Wikpedia allows ~1 req/sec)
            time.sleep(0.1)
        
        print(f"\nScraping complete!")
        print(f"Total nodes: {len(self.graph.nodes)}")
        print(f"Total edges: {len(self.graph.edges)}")
        
        return self.graph
    
    def calculate_metrics(self):
        """
        Calculate graph metrics for analysis.
        """
        print("\nCalculating graph metrics...")
        
        # Convert to undirected for some metrics
        G_undirected = self.graph.to_undirected()
        
        metrics = {}
        
        # Degree centrality
        degree_cent = nx.degree_centrality(self.graph)
        metrics['degree_centrality'] = degree_cent
        
        # In-degree (how many pages link TO this page)
        in_degree = dict(self.graph.in_degree())
        metrics['in_degree'] = in_degree
        
        # Out-degree (how many pages this page links TO)
        out_degree = dict(self.graph.out_degree())
        metrics['out_degree'] = out_degree
        
        # Betweenness centrality (bridge between topics)
        try:
            between_cent = nx.betweenness_centrality(G_undirected, k=min(100, len(G_undirected.nodes)))
            metrics['betweenness_centrality'] = between_cent
            print(f"  Betweenness centrality calculated for {len(between_cent)} nodes")
        except Exception as e:
            print(f"  Warning: Betweenness calculation failed: {e}")
            metrics['betweenness_centrality'] = {}

        
        # PageRank (importance based on link structure)
        # Use alpha=0.85 (standard damping factor) and higher iterations
        try:
            pagerank = nx.pagerank(self.graph, alpha=0.85, max_iter=200, tol=1e-06)
            metrics['pagerank'] = pagerank
            print(f"  PageRank calculated for {len(pagerank)} nodes")
        except Exception as e:
            print(f"  Warning: PageRank calculation failed: {e}")
            # Fallback: use in-degree as proxy for importance
            pagerank = {node: in_degree.get(node, 0) / max(in_degree.values(), default=1) 
                       for node in self.graph.nodes()}
            metrics['pagerank'] = pagerank
            print(f"  Using in-degree as PageRank fallback")

        
        # Add metrics as node attributes
        for node in self.graph.nodes():
            self.graph.nodes[node]['degree_centrality'] = degree_cent.get(node, 0)
            self.graph.nodes[node]['in_degree'] = in_degree.get(node, 0)
            self.graph.nodes[node]['out_degree'] = out_degree.get(node, 0)
            self.graph.nodes[node]['betweenness'] = metrics['betweenness_centrality'].get(node, 0)
            self.graph.nodes[node]['pagerank'] = metrics['pagerank'].get(node, 0)
        
        print("Metrics calculated!")
        return metrics
    
    def save_graph(self, filename='engineering_graph.gpickle'):
        """
        Save graph to file.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.graph, f)
        print(f"Graph saved to {filename}")
    
    def save_graph_json(self, filename='engineering_graph.json'):
        """
        Save graph as JSON for portability (with detailed metadata).
        """
        data = {
            'nodes': [
                {
                    'id': node,
                    'depth': self.graph.nodes[node].get('depth', 0),
                    'summary': self.graph.nodes[node].get('summary', ''),
                    'short_summary': self.graph.nodes[node].get('short_summary', ''),
                    'url': self.graph.nodes[node].get('url', ''),
                    'content_preview': self.graph.nodes[node].get('content_preview', ''),
                    'categories': self.graph.nodes[node].get('categories', []),
                    'sections': self.graph.nodes[node].get('sections', []),
                    'images': self.graph.nodes[node].get('images', []),
                    'references': self.graph.nodes[node].get('references', []),
                    'content_length': self.graph.nodes[node].get('content_length', 0),
                    'word_count': self.graph.nodes[node].get('word_count', 0),
                    'degree_centrality': self.graph.nodes[node].get('degree_centrality', 0),
                    'in_degree': self.graph.nodes[node].get('in_degree', 0),
                    'out_degree': self.graph.nodes[node].get('out_degree', 0),
                    'pagerank': self.graph.nodes[node].get('pagerank', 0)
                }
                for node in self.graph.nodes()
            ],
            'edges': [
                {'source': u, 'target': v}
                for u, v in self.graph.edges()
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Graph saved to {filename}")


def main():
    """
    Main execution function.
    """
    print("=" * 60)
    print("ENGINEERING KNOWLEDGE GRAPH BUILDER (Enhanced)")
    print("Including: Traditional Engineering + Systems + AI/ML")
    print("With detailed metadata for each topic")
    print("=" * 60)
    
    # Initialize scraper
    scraper = EngineeringKnowledgeGraphScraper(
        max_depth=3,
        max_nodes=1000
    )
    
    # Scrape Wikipedia
    graph = scraper.scrape()
    
    # Calculate metrics
    metrics = scraper.calculate_metrics()
    
    # Display top nodes by different metrics
    print("\n" + "=" * 60)
    print("TOP 10 MOST CONNECTED TOPICS (by in-degree):")
    print("=" * 60)
    top_nodes = sorted(metrics['in_degree'].items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (node, score) in enumerate(top_nodes, 1):
        word_count = graph.nodes[node].get('word_count', 0)
        print(f"{i}. {node}: {score} incoming links | {word_count:,} words")
    
    print("\n" + "=" * 60)
    print("TOP 10 MOST IMPORTANT TOPICS (by PageRank):")
    print("=" * 60)
    top_pagerank = sorted(metrics['pagerank'].items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (node, score) in enumerate(top_pagerank, 1):
        categories = len(graph.nodes[node].get('categories', []))
        print(f"{i}. {node}: {score:.6f} | {categories} categories")
    
    # Save graph
    scraper.save_graph('engineering_graph.gpickle')
    scraper.save_graph_json('engineering_graph.json')
    
    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE!")
    print("=" * 60)
    print(f"Enhanced metadata includes: full summaries, categories,")
    print(f"sections, images, references, word counts, and more!")
    print(f"Next step: Run 'streamlit run dashboard.py' to visualize")


if __name__ == "__main__":
    main()