import streamlit as st
import networkx as nx
import pickle
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# Page configuration
st.set_page_config(
    page_title="Engineering Knowledge Graph",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_graph():
    """Load the pre-built knowledge graph."""
    if not os.path.exists('engineering_graph.gpickle'):
        st.error("Graph file not found! Please run wikipedia_scraper.py first.")
        st.stop()
    
    with open('engineering_graph.gpickle', 'rb') as f:
        graph = pickle.load(f)
    return graph

def get_graph_statistics(G):
    """Calculate comprehensive graph statistics."""
    stats = {
        'Total Topics': len(G.nodes()),
        'Total Connections': len(G.edges()),
        'Avg Connections per Topic': round(sum(dict(G.degree()).values()) / len(G.nodes()), 2),
        'Most Connected Topic': max(dict(G.in_degree()).items(), key=lambda x: x[1])[0],
        'Graph Density': round(nx.density(G), 4)
    }
    return stats

def create_pyvis_network(G, node_filter=None, max_nodes=1000):
    """Create an interactive network visualization using PyVis."""
    
    # Filter nodes if specified
    if node_filter:
        nodes_to_include = [n for n in G.nodes() if node_filter.lower() in n.lower()]
        if nodes_to_include:
            # Get subgraph with neighbors
            neighbors = set()
            for node in nodes_to_include:
                neighbors.update(G.predecessors(node))
                neighbors.update(G.successors(node))
            nodes_to_include = list(set(nodes_to_include) | neighbors)
            G_filtered = G.subgraph(nodes_to_include[:max_nodes])
        else:
            st.warning(f"No topics found matching '{node_filter}'")
            return None
    else:
        # Limit to top nodes by degree
        top_nodes = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)[:max_nodes]
        G_filtered = G.subgraph(top_nodes)
    
    # Create PyVis network
    net = Network(height='600px', width='100%', bgcolor='#ffffff', font_color='#000000')
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=100, spring_strength=0.001)
    
    # Add nodes with attributes
    for node in G_filtered.nodes():
        degree = G_filtered.degree(node)
        pagerank = G.nodes[node].get('pagerank', 0)
        
        # Size based on degree
        size = 10 + (degree * 2)
        
        # Color based on depth
        depth = G.nodes[node].get('depth', 0)
        if depth == 0:
            color = '#ff6b6b'  # Red for seed topics
        elif depth == 1:
            color = '#4ecdc4'  # Teal for first level
        else:
            color = "#f004f0"  # Purple for deeper levels
        
        # Tooltip
        title = f"{node}<br>Connections: {degree}<br>PageRank: {pagerank:.4f}"
        
        net.add_node(node, label=node, size=size, color=color, title=title)
    
    # Add edges
    for edge in G_filtered.edges():
        net.add_edge(edge[0], edge[1], arrows='to')
    
    # Save and return
    net.save_graph('temp_graph.html')
    return 'temp_graph.html'

def plot_top_topics_bar(G, metric='in_degree', top_n=15):
    """Create bar chart of top topics by specified metric."""
    
    if metric == 'in_degree':
        data = dict(G.in_degree())
        title = f"Top {top_n} Most Referenced Topics (Incoming Links)"
        x_label = "Number of Incoming Links"
    elif metric == 'out_degree':
        data = dict(G.out_degree())
        title = f"Top {top_n} Topics with Most Outgoing Links"
        x_label = "Number of Outgoing Links"
    elif metric == 'pagerank':
        data = {n: G.nodes[n].get('pagerank', 0) for n in G.nodes()}
        title = f"Top {top_n} Topics by PageRank Score"
        x_label = "PageRank Score"
    else:
        data = dict(G.degree())
        title = f"Top {top_n} Most Connected Topics"
        x_label = "Total Connections"
    
    # Sort and get top N
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    df = pd.DataFrame(sorted_data, columns=['Topic', 'Value'])
    
    fig = px.bar(
        df,
        x='Value',
        y='Topic',
        orientation='h',
        title=title,
        labels={'Value': x_label, 'Topic': 'Engineering Topic'},
        color='Value',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def plot_degree_distribution(G):
    """Plot degree distribution histogram."""
    degrees = [G.degree(n) for n in G.nodes()]
    
    fig = px.histogram(
        x=degrees,
        nbins=30,
        title="Distribution of Topic Connectivity",
        labels={'x': 'Number of Connections', 'y': 'Number of Topics'},
        color_discrete_sequence=['#1f77b4']
    )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

def plot_depth_distribution(G):
    """Plot distribution of topics by depth."""
    depths = [G.nodes[n].get('depth', 0) for n in G.nodes()]
    
    depth_counts = pd.Series(depths).value_counts().sort_index()
    
    fig = px.bar(
        x=depth_counts.index,
        y=depth_counts.values,
        title="Topic Distribution by Scraping Depth",
        labels={'x': 'Depth Level', 'y': 'Number of Topics'},
        color=depth_counts.values,
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header"> Engineering Knowledge Graph Explorer</h1>', unsafe_allow_html=True)
    st.markdown("**Interactive visualization of engineering concepts from Wikipedia**")
    st.markdown("---")
    
    # Load graph
    with st.spinner("Loading knowledge graph..."):
        G = load_graph()
    
    # Sidebar
    st.sidebar.header(" Controls")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["-> Overview", "-> Network Graph", "-> Analytics", "-> Topic Explorer"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This dashboard visualizes the relationships between engineering concepts "
        "scraped from Wikipedia. Explore connections, identify central topics, "
        "and discover knowledge patterns."
    )
    
    # Page routing
    if page == " Overview":
        show_overview(G)
    elif page == " Network Graph":
        show_network_graph(G)
    elif page == " Analytics":
        show_analytics(G)
    else:
        show_topic_explorer(G)

def show_overview(G):
    """Display overview page with statistics."""
    st.header("Knowledge Graph Overview")
    
    # Statistics
    stats = get_graph_statistics(G)
    
    cols = st.columns(5)
    for i, (key, value) in enumerate(stats.items()):
        with cols[i]:
            st.metric(label=key, value=value)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = plot_top_topics_bar(G, metric='in_degree', top_n=15)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = plot_top_topics_bar(G, metric='pagerank', top_n=15)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        fig3 = plot_degree_distribution(G)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        fig4 = plot_depth_distribution(G)
        st.plotly_chart(fig4, use_container_width=True)

def show_network_graph(G):
    """Display interactive network graph."""
    st.header("Interactive Network Visualization")
    
    st.markdown("""
    **How to use:**
    - Search for specific topics using the filter below
    -  Click and drag nodes to explore connections
    -  Hover over nodes to see details
    -  Colors indicate depth: Red (seed) → Teal (level 1) → Purple (level 2+)
    """)
    
    # Controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Filter topics (leave empty to show most connected)",
            placeholder="e.g., Mechanical, Electrical, Civil"
        )
    
    with col2:
        max_nodes = st.slider("Max nodes to display", 50, 1000, 100, 10)
    
    # Create network
    with st.spinner("Generating network visualization..."):
        html_file = create_pyvis_network(G, search_term if search_term else None, max_nodes)
        
        if html_file:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            components.html(html_content, height=650)

def show_analytics(G):
    """Display detailed analytics."""
    st.header("Advanced Analytics")
    
    # Metric selector
    metric_type = st.selectbox(
        "Select metric to analyze",
        ["Degree Centrality", "PageRank", "In-Degree", "Out-Degree", "Betweenness Centrality"]
    )
    
    metric_map = {
        "Degree Centrality": 'degree',
        "PageRank": 'pagerank',
        "In-Degree": 'in_degree',
        "Out-Degree": 'out_degree',
        "Betweenness Centrality": 'betweenness'
    }
    
    selected_metric = metric_map[metric_type]
    
    # Display chart
    top_n = st.slider("Number of topics to show", 10, 30, 20)
    fig = plot_top_topics_bar(G, metric=selected_metric, top_n=top_n)
    st.plotly_chart(fig, use_container_width=True)
    
    # Explanation
    st.markdown("---")
    st.subheader("Understanding the Metrics")
    
    explanations = {
        "Degree Centrality": "Measures how connected a topic is. Higher values indicate topics that connect many concepts.",
        "PageRank": "Measures importance based on link structure. Topics linked by important topics score higher.",
        "In-Degree": "Number of topics that link TO this topic. Indicates foundational or frequently referenced concepts.",
        "Out-Degree": "Number of topics this topic links TO. Indicates broad or interdisciplinary topics.",
        "Betweenness Centrality": "Measures how often a topic appears on shortest paths between other topics. High values indicate 'bridge' concepts."
    }
    
    st.info(explanations[metric_type])
    
    # Additional statistics
    st.markdown("---")
    st.subheader("Detailed Statistics")
    
    # Create DataFrame with all metrics
    data = []
    for node in G.nodes():
        data.append({
            'Topic': node,
            'Degree': G.degree(node),
            'In-Degree': G.in_degree(node),
            'Out-Degree': G.out_degree(node),
            'PageRank': G.nodes[node].get('pagerank', 0),
            'Depth': G.nodes[node].get('depth', 0)
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('PageRank', ascending=False)
    
    st.dataframe(df, use_container_width=True, height=400)
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label=" Download Full Dataset (CSV)",
        data=csv,
        file_name="engineering_knowledge_graph_metrics.csv",
        mime="text/csv"
    )

def show_topic_explorer(G):
    """Display topic explorer with search."""
    st.header("Topic Explorer")
    
    # Search box
    search_query = st.text_input(
        " Search for a topic",
        placeholder="e.g., Thermodynamics, Robotics, Structural Engineering"
    )
    
    if search_query:
        # Find matching topics
        matching = [n for n in G.nodes() if search_query.lower() in n.lower()]
        
        if matching:
            st.success(f"Found {len(matching)} matching topics")
            
            selected_topic = st.selectbox("Select a topic to explore", matching)
            
            if selected_topic:
                st.markdown("---")
                
                # Topic details
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader(f" {selected_topic}")
                    
                    summary = G.nodes[selected_topic].get('summary', 'No summary available')
                    st.write(summary)
                    
                    url = G.nodes[selected_topic].get('url', '')
                    if url:
                        st.markdown(f"[ Read full article on Wikipedia]({url})")
                
                with col2:
                    st.metric("Total Connections", G.degree(selected_topic))
                    st.metric("Incoming Links", G.in_degree(selected_topic))
                    st.metric("Outgoing Links", G.out_degree(selected_topic))
                    st.metric("PageRank", f"{G.nodes[selected_topic].get('pagerank', 0):.6f}")
                
                st.markdown("---")
                
                # Connected topics
                col3, col4 = st.columns(2)
                
                with col3:
                    st.subheader(" Topics that link HERE")
                    predecessors = list(G.predecessors(selected_topic))
                    if predecessors:
                        for pred in predecessors[:10]:
                            st.write(f"• {pred}")
                        if len(predecessors) > 10:
                            st.write(f"... and {len(predecessors) - 10} more")
                    else:
                        st.write("No incoming links")
                
                with col4:
                    st.subheader(" Topics this links TO")
                    successors = list(G.successors(selected_topic))
                    if successors:
                        for succ in successors[:10]:
                            st.write(f"• {succ}")
                        if len(successors) > 10:
                            st.write(f"... and {len(successors) - 10} more")
                    else:
                        st.write("No outgoing links")
        else:
            st.warning(f"No topics found matching '{search_query}'")
    else:
        st.info(" Enter a search term above to explore specific topics")
        
        # Show random sample
        st.markdown("---")
        st.subheader(" Browse All Topics")
        
        all_topics = sorted(G.nodes())
        st.write(f"Total topics in graph: {len(all_topics)}")
        
        # Display in columns
        cols = st.columns(3)
        for i, topic in enumerate(all_topics[:30]):
            with cols[i % 3]:
                st.write(f"• {topic}")
        
        if len(all_topics) > 30:
            st.write(f"... and {len(all_topics) - 30} more topics")

if __name__ == "__main__":
    main()