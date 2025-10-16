"""Research assistant prompt implementation for comprehensive research guidance."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mcp.server.fastmcp.prompts import base
from typing import List, Optional
from utils.perplexity_client import get_perplexity_api


async def research_assistant(research_topic: str, research_type: str = "comprehensive", output_format: str = "structured") -> str:
    """AI research assistant that guides systematic information gathering and analysis."""

    try:
        # Define research types and their methodologies
        research_types = {
            "comprehensive": "Thorough, multi-source research covering all aspects of the topic",
            "comparative": "Side-by-side analysis of multiple options, approaches, or solutions",
            "historical": "Evolution and development of the topic over time",
            "technical": "In-depth technical analysis with implementation details",
            "market": "Market analysis, trends, and competitive landscape",
            "academic": "Scholarly research with academic rigor and citations",
            "practical": "Applied research focusing on real-world implementation and use cases"
        }

        output_formats = {
            "structured": "Organized sections with clear hierarchy and actionable insights",
            "executive": "Concise summary for decision-makers with key takeaways",
            "detailed": "Comprehensive report with in-depth analysis and extensive details",
            "interactive": "Q&A format with interactive exploration of findings"
        }

        research_desc = research_types.get(research_type, research_types["comprehensive"])
        format_desc = output_formats.get(output_format, output_formats["structured"])

        prompt = f"""🎓 **AI Research Assistant Session**

**Research Topic:** {research_topic}
**Research Type:** {research_type.title()}
**Output Format:** {output_format.title()}

**📋 Research Scope:**
- **Methodology:** {research_desc}
- **Output Style:** {format_desc}

**🔍 Research Framework:**
"""

        # Add research methodology based on type
        if research_type == "comprehensive":
            prompt += """**1. 🔎 Topic Scoping & Definition**
- Define key concepts and terminology
- Establish research boundaries and scope
- Identify primary and secondary research questions
- Map knowledge domains and intersections

**2. 📚 Multi-Source Discovery**
- Academic sources and scholarly publications
- Industry reports and white papers
- Expert opinions and thought leadership
- Current news and recent developments
- Documentation and technical resources

**3. 🔬 Critical Analysis**
- Source credibility and bias assessment
- Information triangulation and validation
- Contrasting viewpoints and debates
- Gap identification in current knowledge

**4. 📊 Synthesis & Integration**
- Pattern recognition across sources
- Theme and trend identification
- Cause-and-effect relationships
- Contextual relevance assessment

"""
        elif research_type == "comparative":
            prompt += """**1. ⚖️ Comparison Framework**
- Define comparison criteria and metrics
- Identify key alternatives or options
- Establish evaluation methodology
- Set success criteria and priorities

**2. 🔍 Deep Dive Analysis**
- Individual option analysis and profiling
- Strength and weakness assessment
- Feature comparison matrix
- Performance benchmarking

**3. 📈 Comparative Evaluation**
- Side-by-side feature analysis
- Cost-benefit analysis
- Risk assessment and mitigation
- Suitability for different use cases

**4. 🎯 Recommendation Matrix**
- Scoring and ranking methodology
- Context-specific recommendations
- Implementation considerations
- Decision-making framework

"""
        elif research_type == "technical":
            prompt += """**1. 🔧 Technical Foundation**
- Core concepts and principles
- Architecture and design patterns
- Technical specifications and standards
- Implementation requirements

**2. 💻 Implementation Analysis**
- Code examples and patterns
- Performance characteristics
- Integration possibilities
- Development tools and resources

**3. 🔬 Technical Deep Dive**
- Advanced features and capabilities
- Optimization techniques
- Troubleshooting and debugging
- Scalability and maintenance

**4. 🚀 Practical Applications**
- Real-world use cases and examples
- Best practices and guidelines
- Common pitfalls and solutions
- Future development trends

"""
        elif research_type == "market":
            prompt += """**1. 📊 Market Landscape**
- Market size and growth trends
- Key players and competitors
- Market segmentation and niches
- Industry dynamics and forces

**2. 🔍 Competitive Analysis**
- Competitor strengths and weaknesses
- Market positioning strategies
- Pricing and business models
- Differentiation factors

**3. 📈 Trend Analysis**
- Current market trends and drivers
- Emerging opportunities and threats
- Technology adoption curves
- Future market predictions

**4. 🎯 Strategic Insights**
- Market entry strategies
- Competitive positioning recommendations
- Risk assessment and mitigation
- Growth opportunity identification

"""
        elif research_type == "academic":
            prompt += """**1. 🎓 Literature Review**
- Scholarly articles and peer-reviewed papers
- Academic journals and publications
- Citation analysis and impact
- Theoretical frameworks and models

**2. 🔬 Research Methodology**
- Research methods and approaches
- Data collection and analysis techniques
- Statistical significance and validation
- Research limitations and biases

**3. 📊 Evidence Synthesis**
- Meta-analysis and systematic review
- Evidence grading and quality assessment
- Consensus and controversy identification
- Research gaps and future directions

**4. 📝 Academic Standards**
- Proper citation and referencing
- Academic integrity and ethics
- Peer review and validation processes
- Contribution to field advancement

"""

        # Add output format specifications
        prompt += f"**📋 {output_format.title()} Output Structure:**\n"

        if output_format == "structured":
            prompt += """**Executive Summary** (2-3 sentences)
- Key findings and main takeaways

**Introduction & Background**
- Topic context and importance
- Research questions and objectives

**Main Findings** (organized by theme)
- Detailed analysis with supporting evidence
- Data and examples where applicable
- Source attribution and credibility assessment

**Analysis & Insights**
- Pattern identification and interpretation
- Implications and significance
- Contrasting viewpoints and debates

**Conclusions & Recommendations**
- Summary of key findings
- Actionable recommendations
- Areas for further research

**References & Sources**
- Comprehensive source list with links
- Source credibility assessment
"""
        elif output_format == "executive":
            prompt += """**Key Findings** (bullet points)
- 3-5 most important discoveries
- Direct impact on decisions

**Strategic Implications**
- What this means for your objectives
- Risk and opportunity assessment

**Recommended Actions**
- Immediate next steps
- Priority ranking and timeline

**Resource Summary**
- Key sources for deeper dive
- Quick reference links
"""
        elif output_format == "detailed":
            prompt += """**Comprehensive Analysis** (full detail)
- Exhaustive coverage of all findings
- Complete data sets and statistics
- Full source attribution
- Methodology explanation
- Limitations and caveats
- Extensive appendix and references
"""
        elif output_format == "interactive":
            prompt += """**Q&A Research Format**
- Questions driving the research
- Answers with supporting evidence
- Follow-up questions and exploration
- Interactive discovery process
- Customize research depth based on interest
"""

        prompt += f"""
**🔍 Research Tools & Resources:**
- **Primary Search**: Use `search_perplexity` with profile="research"
- **Follow-up Exploration**: Use `chat_with_perplexity` for deeper dives
- **Source Verification**: Cross-reference multiple sources
- **Document Analysis**: Analyze specific documents with `analyze_file_with_perplexity`

**🎯 Research Best Practices:**
1. **Start Broad, Then Focus**: Begin with general understanding, then narrow to specific aspects
2. **Source Diversity**: Use multiple types of sources (academic, industry, practical)
3. **Critical Evaluation**: Assess source credibility and potential biases
4. **Information Triangulation**: Verify findings across multiple sources
5. **Contextual Relevance**: Consider your specific use case and context

**📊 Quality Assurance Checklist:**
- [ ] Research questions clearly defined
- [ ] Multiple credible sources consulted
- [ ] Information cross-validated
- [ ] Contrasting viewpoints considered
- [ ] Conclusions supported by evidence
- [ ] Sources properly attributed
- [ ] Relevance to your objectives confirmed

**🚀 Ready to Begin Research!**

I'm prepared to conduct a thorough {research_type} analysis of **{research_topic}** and deliver results in {output_format} format.

**To start the research:**
1. Provide any specific focus areas or questions
2. Indicate if you have any particular source preferences
3. Share any constraints (time, scope, specific aspects to include/exclude)
4. Specify the intended use or audience for this research

Let's begin our research journey!
"""

        return prompt

    except Exception as e:
        return f"Error generating research assistant prompt: {str(e)}"