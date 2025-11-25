# Engineering Knowledge Graph Project Report

## Introduction

This project focuses on the acquisition and interactive visualization of knowledge relationships among engineering domains using Wikipedia data. By scraping Wikipedia, we constructed a graph of interconnected topics in various engineering fields and visualized them through an interactive Streamlit dashboard for exploration and analysis. The project closely aligns with course goals in data acquisition, real-time visual analytics, and decision-making.

## Methodology

- **Data Source**: Off-the-shelf Wikipedia articles related to major engineering domains (e.g., mechanical, electrical, civil, chemical, industrial engineering, etc.).
- **Acquisition Steps**: Starting from selected seed topics, we performed breadth-first scraping to capture related topics through Wikipedia's internal links, limiting the depth and number of nodes for manageability and relevance.
- **Graph Construction**: We built a directed knowledge graph using NetworkX, where nodes represent engineering topics and edges indicate direct conceptual relationships extracted from Wikipedia link structures. Node and edge attributes include summary, depth, and centrality metrics.
- **Metrics Calculated**: Degree centrality, in-degree, out-degree, betweenness centrality, and PageRank, using standard graph analytics.
- **Visualization**: The final dashboard leverages Pyvis and Plotly for node-link diagrams, bar charts, histograms, and summary views; hosted interactively on Streamlit.

## Exploratory Data Analysis & Visualization

- Distribution of topics by domain and connectivity
- Identification and exploration of high-centrality concepts ("hub" topics)
- Visualization of conceptual bridges and clusters in engineering knowledge structure
- Interactive features: search/filter by topic, connectivity, and scraping depth

## Results and Insights

- The engineering knowledge graph contains hundreds of richly interconnected topics, identified using off-the-shelf Wikipedia content and efficient scraping methods.
- Central hub topics (e.g., "Engineering", "Mechanics", etc.) show high connectivity and reveal foundational domains.
- The interactive dashboard enables rapid exploration, supporting knowledge discovery and curriculum design in engineering education or analysis.

## Technical Summary

- **Programming Language**: Python (requirements.txt provided)
- **Libraries Used**: wikipedia, networkx, pandas, plotly, pyvis, streamlit
- **Hosting**: Streamlit for real-time web-based visualization

## References

1. Wikipedia. "Engineering." https://en.wikipedia.org/wiki/Engineering
2. Wikipedia. "List of engineering branches." https://en.wikipedia.org/wiki/List_of_engineering_branches
3. Python Software Foundation. NetworkX documentation. https://networkx.org/
4. Streamlit. Documentation. https://streamlit.io/

---

### Appendix: Instructions

1. Run `wikipedia_scraper.py` to generate the engineering_graph files.
2. Start the dashboard: `streamlit run dashboard.py`
3. Explore the interactive network; try searching for core topics and viewing metrics tabs.
