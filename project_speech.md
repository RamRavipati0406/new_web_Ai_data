# Engineering Knowledge Graph Explorer: Complete Project Explanation

## Opening

Good [morning/afternoon]. Today I'm going to walk you through a project called the **Engineering Knowledge Graph Explorer**—a tool that maps out and visualizes how different engineering concepts relate to and influence each other. Even if you've never worked with software or data visualization before, by the end of this explanation, you'll understand exactly what this project does, where the information comes from, and what each visualization tells us.

---

## Part 1: What is the Problem We're Solving?

Imagine you're a student learning engineering. You know "Machine Learning" is important, and you've heard of "Robotics," "Systems Engineering," and "Artificial Intelligence." But here's the question: **How do all these topics connect? Which ones are foundational? Which ones are more specialized? Which concepts does everything else build upon?**

This project answers those questions by creating a **visual map** of engineering knowledge—showing which topics are the big hubs that everything else connects to, and which ones are more niche or specialized.

---

## Part 2: Where Does the Data Come From?

The data comes from **Wikipedia**. Here's how:

### **Step 1: Choose Starting Topics**

We begin with a carefully selected list of 30 seed topics—major areas in engineering:
- Traditional fields like Mechanical Engineering, Electrical Engineering, Civil Engineering
- Modern areas like Systems Engineering, Robotics, and Automation
- Cutting-edge fields like Artificial Intelligence, Machine Learning, Deep Learning, and Neural Networks

### **Step 2: Extract Wikipedia Links**

For each starting topic, we go to its Wikipedia page and extract every hyperlink (clickable link) found in the article. These hyperlinks point to related topics.

**Example:** The Wikipedia page for "Artificial Intelligence" contains links to topics like "Machine Learning," "Deep Learning," "Neural Networks," "Computer Vision," and many others. Each of these links represents a connection—a relationship between concepts.

### **Step 3: Filter for Relevance**

Not every link is relevant to engineering. The program automatically filters out irrelevant links and keeps only those related to engineering, technology, systems, design, and similar domains.

### **Step 4: Expand Outward (Depth)**

The process repeats recursively. Once we've captured links from the seed topics, we then look at the Wikipedia pages for those newly discovered topics and extract *their* links. We typically go 2 levels deep to balance comprehensiveness with avoiding information overload.

### **Step 5: Collect Rich Information**

For each topic, we don't just record a link—we also capture:
- The **full Wikipedia summary** (the introductory paragraph)
- **Categories** the topic belongs to (e.g., "Engineering," "Artificial Intelligence")
- **Article sections** (the table of contents—what aspects the topic covers)
- **Images** from the Wikipedia page [TBD]
- **Reference links** (academic citations within Wikipedia)
- **Word count** (how detailed the article is..)

**Result:** A dataset of approximately 1000 engineering-related topics with their connections and rich metadata.

---

## Part 3: How Are the Connections (Links) Formed?

Think of the connections like a **conversation map**:

When Wikipedia page A mentions and links to page B, it means "This concept is related to and references that concept." By collecting all these mentions across hundreds of Wikipedia pages, we create a network that shows which ideas talk about each other—which ideas reference which other ideas.

These connections form a **directed graph**:
- Each circle (node) is a topic
- Each arrow (edge) is a link from one topic to another
- The arrow points in the direction of the reference

**In simple terms:** If the "Robotics" page links to "Artificial Intelligence," there's an arrow from Robotics → AI. This tells us that Robotics pages reference and depend on AI concepts.

---

## Part 4: Understanding the Visualizations and Graphs

Now, let's walk through every graph and visualization in the dashboard, explaining what each one tells us.

### **Graph 1: The Network Graph (The Visual Map)**

**What you see:** A beautiful, interactive map with colored circles (nodes) connected by arrows (edges). Nodes are color-coded by depth:
- **Red nodes:** The original seed topics (our starting points)
- **Teal nodes:** Topics discovered in the first level of links
- **Green nodes:** Topics discovered in the second level

**What it means:** This is the actual knowledge network. You can see the "shape" of how engineering knowledge is organized. Some topics have many connections (hubs), while others are more isolated (specialized).

**Why it matters:** This visual immediately shows you which topics are central versus peripheral, and how different fields cluster together.

---

### **Graph 2: Top 10 Most Referenced Topics (Bar Chart)**

**What you see:** A horizontal bar chart showing the 10 topics that are most frequently referenced by other pages. The longer the bar, the more pages link to that topic.

**What it means:** These are the **foundational concepts**—the topics that many other concepts depend on or build from. If a topic has many incoming links, it means many other pages cite it as important.

**Key insight:** "Artificial Intelligence" consistently appears at the top. This tells us that AI is a foundational concept that nearly every other engineering field references. This makes sense in today's world—AI touches everything from robotics to systems engineering to data science.

**Why it matters:** If you're learning engineering, these top topics are probably the first things you should understand because everything else builds on them.

---

### **Graph 3: Top 10 Most Important Topics by PageRank (Bar Chart)**

**What you see:** Another bar chart, but this one uses a different ranking system called "PageRank."

**What is PageRank?** Imagine you're at a cocktail party, and you want to know who the most influential people are. You can't just count how many people mention their names—you also have to consider who's doing the mentioning. If important people mention your name, you become more important.

PageRank works the same way:
- A topic gets a high score if many other topics link to it
- AND those topics that link to it also have high PageRank scores themselves
- It's recursive—importance is based on being connected to other important things

**What it means:** PageRank shows you the **truly foundational, widely-trusted concepts** in the knowledge network. Not just frequently mentioned—but mentioned by other highly-regarded concepts.

**Key insight:** Again, "Artificial Intelligence" ranks at the top. This means not only do many topics reference AI, but those topics themselves are central and important. AI is fundamental.

**Why it matters:** PageRank gives you a global view of the importance hierarchy in the field.

---

### **Graph 4: Distribution of Topic Connectivity (Histogram)**

**What you see:** A histogram (bar chart) showing how many topics have 0 connections, how many have 1, how many have 2, etc.

**What it means:** This shows the "shape" of the network. Are topics evenly connected, or are there a few hubs with many connections and most topics with few?

**Real-world interpretation:** If you see most bars on the left (low connectivity) and a few tall bars on the right (high connectivity), you've discovered a "hub-and-spoke" network—typical of real knowledge systems. A few core concepts connect to everything; most specific topics are more isolated.

**Key insight:** In your graph, you'll see this pattern. "Artificial Intelligence," "Engineering," and "Machine Learning" are major hubs. Topics like "Stepper motor" or "Crystallography" might have fewer connections—they're more specialized.

**Why it matters:** This tells you the structure of knowledge. It shows that engineering isn't a flat, uniform landscape. It has hubs (foundational concepts everyone knows) and spokes (specialized subfields).

---

### **Graph 5: Topic Distribution by Scraping Depth (Bar Chart)**

**What you see:** A bar chart with typically 3 bars (or however many depths you scraped to), showing how many topics were discovered at each depth level.

**Depth explanation:**
- **Depth 0:** Your original 30 seed topics (e.g., AI, Mechanical Engineering)
- **Depth 1:** Topics that were linked from the seed topics (~150-200 topics)
- **Depth 2:** Topics linked from those topics (~200-300 more topics)

**What it means:** This shows how the discovery process expanded. Most topics are at depth 1 or 2—they're one or two links away from the core concepts.

**Key insight:** Very few topics end up at depth 2, meaning most of engineering knowledge is directly connected to or one step away from the major hubs. This reflects how well-organized and interconnected engineering knowledge is.

**Why it matters:** This metric helps you understand the "shape" of your data collection—how much you've explored, and that you haven't gone too far "off track" into irrelevant topics.

---

### **Graph 6: Detailed Statistics Table (Data Table)**

**What you see:** A spreadsheet-style table listing every single topic with metrics including:
- **Degree:** Total number of connections
- **In-Degree:** How many topics link TO this topic
- **Out-Degree:** How many topics this topic links to
- **PageRank:** Its importance score
- **Depth:** How many hops from the seed topics

**What it means:** This is the "raw data" view. For researchers or analysts, it provides precise numbers for every topic.

**Key insight:** You can sort this table, export it to CSV, and perform deeper analysis—answering questions like "Which topics are the broadest (highest out-degree)?" or "Which topics are most foundational (highest in-degree)?"

**Why it matters:** Reproducibility and transparency. Anyone can see exactly what data you collected and verify your findings.

---

## Part 5: Why is Artificial Intelligence Always at the Top?

This is the most important finding of the project.

**The Short Answer:** In modern engineering, AI is the central hub. Nearly every engineering discipline now references, uses, or builds upon AI concepts.

**The Detailed Explanation:**

1. **Modern Relevance:** Over the past 10 years, AI and machine learning have become foundational to engineering. Robotics, automation, control systems, data science, computer vision—all of these now depend on AI concepts.

2. **Wikipedia's Structure:** Wikipedia reflects this reality. The AI page is extensively linked from hundreds of other pages because the Wikipedia community itself recognizes AI's centrality.

3. **Breadth of Application:** Unlike traditional engineering disciplines (which focus on specific domains like bridges or motors), AI is applicable across *all* engineering domains. This universal applicability causes it to become a hub.

4. **What This Tells Us:** Your visualization isn't just a technical diagram—it's a snapshot of how knowledge is organized in 2024. It shows that if you want to be a modern engineer, understanding AI is no longer optional; it's foundational.

---

## Part 6: The Interactive Dashboard

The project includes a **Streamlit dashboard**—a web-based application where users can:

1. **Explore the Network:** Interact with the graph, click on nodes, drag them around, and see connections.
2. **Search for Topics:** Type in a topic name, and the app shows you that topic, its incoming links (what references it), and its outgoing links (what it references).
3. **View Detailed Information:** Click on any topic to see its full Wikipedia summary, categories, sections, images, and metrics.
4. **Download Data:** Export all metrics and tables for further analysis.

**Purpose:** The dashboard makes the data explorable and actionable—not just a static report, but an interactive tool for learning and discovery.

---

## Part 7: Why This Project Matters

This project demonstrates several important principles:

1. **Data Acquisition:** We collected real-world data from a reputable source (Wikipedia) and cleaned/organized it meaningfully.

2. **Visualization for Decision-Making:** We didn't just create pretty pictures—each visualization tells a specific story and helps you understand the structure of knowledge.

3. **Graph Analysis:** By applying network science (centrality metrics, PageRank), we revealed hidden patterns—like that AI is the modern hub of engineering.

4. **Reproducibility:** The code is transparent, the data is saved, and the dashboard is publicly hosted. Anyone can verify these findings.

5. **Practical Application:** This type of analysis can be used for:
   - Curriculum design (what should students learn first?)
   - Research planning (what are emerging subfields?)
   - Knowledge management (how should organizations structure documentation?)

---

## Conclusion

This **Engineering Knowledge Graph Explorer** is more than a visualization project. It's a data-driven investigation into how modern engineering knowledge is organized. By scraping Wikipedia, building a network, and analyzing it with graph theory, we've revealed that:

- Engineering knowledge is **hub-centric**—a few core concepts (especially AI) support everything else
- Modern engineering is **highly interconnected**—concepts rarely stand alone
- Knowledge follows a **hierarchical structure**—from foundational (AI, Engineering) to specialized (specific technologies and subfields)

The interactive dashboard lets anyone explore these patterns, and the open-source code allows others to build on this work.

**Thank you.**

---

## Q&A Preparation

**Common questions you might get:**

**Q: Why Wikipedia?**  
A: Wikipedia is a crowdsourced, public knowledge base that reflects how the broad community organizes concepts. It's also free and accessible for academic projects.

**Q: Why is the graph directed?**  
A: Because direction matters. A page linking to another shows influence or dependency. "A links to B" doesn't mean "B links to A."

**Q: Could you have used other data sources?**  
A: Yes—academic papers, textbooks, course syllabi. But Wikipedia's link structure is already rich and well-maintained.

**Q: What are the limitations?**  
A: Wikipedia reflects volunteer curation, not peer-reviewed research. It represents public knowledge, not cutting-edge research. Some topics may be over or underrepresented.

**Q: What insights could you act on?**  
A: Course designers could use this to structure curriculum. Researchers could identify emerging fields (topics at periphery with growing links). Companies could use it for knowledge management.

