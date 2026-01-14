# Resilio Tech Demo Script (2 minutes)

---

**[Start on System Detail page - Summary tab]**

"Let's look under the hood. When assessment data is uploaded, it lands in S3 and triggers our ingestion pipeline. Amazon Bedrock analyzes the transcripts, extracts actors and relationships, and loads everything into Amazon Neptune as a graph database. From Neptune, we generate a Domain Specific Language that powers everything you see here.

**[Scroll through Summary - show stats, components, risks]**

The system summary shows us actors, relationships, and components—all extracted automatically. Each component has a relevance score calculated from production output and replaceability. We can see risks identified in the system and vulnerability assessments for each actor.

**[Open AI Chat]**

Want to ask questions about the system? Our AI assistant is powered by a Strands Agent running on Amazon Bedrock AgentCore. It has access to the full graph data in Neptune—ask it anything about the system structure, vulnerabilities, or recommendations.

**[Close chat, switch to Visualization tab - Network Graph]**

Now the visualization. This is a force-directed network graph—actors are nodes, relationships are edges. Colors indicate health: green is good, yellow is stressed, red is broken. You can drag nodes, zoom in, and the physics simulation keeps everything readable. The pulsing connections draw your eye to problem areas.

**[Navigate to Risk Simulator, select a scenario]**

Now the fun part—the Risk Simulator. Select a scenario, hit play.

**[Play the Drought scenario]**

Watch the network respond. Day zero, drought is declared. Day fourteen, water scarcity hits health centers—see them turn yellow. Day thirty, supply chains break—those edges go red. Each event on the timeline shows cascading impacts, and the sidebar shows suggested remediations with responsible actors identified.

**[Open Ask AI on simulator]**

Want a custom scenario? Ask the AI. Our Strands Agent fetches the system data, analyzes vulnerabilities, and generates a complete simulation DSL—ready to run.

**[Pause on simulator]**

We completed a Well-Architected Review—eighty-eight percent overall. This is production-ready infrastructure, not a prototype."

---

**Timing: ~2 minutes**

**Flow:**
1. Summary & data pipeline explanation (~25s)
2. AI Chat demo (~15s)
3. Network Graph visualization (~25s)
4. Risk Simulator demo (~45s)
5. Closing (~10s)
