"""Consultation session prompt implementation for interactive expert guidance."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mcp.server.fastmcp.prompts import base
from typing import List, Optional
from utils.perplexity_client import get_perplexity_api


async def consultation_session(topic: str, expertise_area: str = "general", session_type: str = "exploration") -> str:
    """Expert consultation session that provides structured guidance."""

    try:
        # Define expertise areas and their focus
        expertise_areas = {
            "technical": "Technical implementation, architecture, and development best practices",
            "research": "Information gathering, analysis, and comprehensive research methods",
            "troubleshooting": "Problem diagnosis, resolution strategies, and prevention",
            "optimization": "Performance improvement, efficiency gains, and resource optimization",
            "security": "Security assessment, vulnerability analysis, and protective measures",
            "strategy": "Planning, decision-making, and strategic approaches",
            "learning": "Educational guidance, skill development, and knowledge acquisition"
        }

        session_types = {
            "exploration": "Open-ended discovery and learning about your topic",
            "problem_solving": "Focused issue resolution with actionable solutions",
            "planning": "Strategic planning and implementation roadmap development",
            "review": "Critical analysis and improvement recommendations",
            "brainstorming": "Creative ideation and possibility exploration"
        }

        expertise_desc = expertise_areas.get(expertise_area, expertise_areas["general"] if "general" in expertise_areas else "General consultation and advisory services")
        session_desc = session_types.get(session_type, session_types["exploration"])

        prompt = f"""🎯 **Expert Consultation Session**

**Topic:** {topic}
**Expertise Area:** {expertise_area.title()}
**Session Type:** {session_type.replace('_', ' ').title()}

**📋 Session Overview:**
This consultation focuses on: {expertise_desc}
Session approach: {session_desc}

"""

        # Add session-specific structure
        if session_type == "exploration":
            prompt += """**🔍 Exploration Framework:**
1. **Current Understanding**: What do you already know about this topic?
2. **Knowledge Gaps**: What areas need clarification or deeper insight?
3. **Application Context**: How do you plan to use this information?
4. **Success Criteria**: What would make this consultation successful for you?

**💭 Exploration Questions to Consider:**
- What sparked your interest in this topic?
- Are there specific aspects you'd like to dive deeper into?
- Do you have any constraints or requirements we should consider?
- What level of detail would be most helpful?

"""
        elif session_type == "problem_solving":
            prompt += """**🔧 Problem-Solving Framework:**
1. **Issue Definition**: Clearly articulate the challenge you're facing
2. **Impact Assessment**: Understand the scope and consequences
3. **Solution Space**: Explore potential approaches and alternatives
4. **Implementation Plan**: Develop actionable next steps

**🎯 Problem-Solving Questions:**
- What specific problem are you trying to solve?
- What have you tried so far, and what were the results?
- What are the constraints or limitations you're working with?
- What does success look like for this situation?

"""
        elif session_type == "planning":
            prompt += """**📅 Strategic Planning Framework:**
1. **Goal Definition**: Establish clear, measurable objectives
2. **Current State Analysis**: Assess your starting point and resources
3. **Gap Analysis**: Identify what needs to be developed or acquired
4. **Roadmap Development**: Create a structured implementation plan

**📋 Planning Considerations:**
- What are your short-term and long-term goals?
- What resources (time, budget, skills) are available?
- What are the key milestones or checkpoints?
- How will you measure progress and success?

"""
        elif session_type == "review":
            prompt += """**🔍 Critical Review Framework:**
1. **Current State Assessment**: Evaluate existing approaches or solutions
2. **Strengths Analysis**: Identify what's working well
3. **Improvement Opportunities**: Find areas for enhancement
4. **Recommendations**: Develop specific, actionable suggestions

**📊 Review Focus Areas:**
- What specific item or approach would you like me to review?
- What aspects are most important to evaluate (quality, efficiency, security, etc.)?
- Are there particular concerns or issues you've noticed?
- What standards or criteria should I use for evaluation?

"""
        elif session_type == "brainstorming":
            prompt += """**💡 Creative Brainstorming Framework:**
1. **Idea Generation**: Explore diverse possibilities and approaches
2. **Feasibility Assessment**: Evaluate practicality and constraints
3. **Innovation Potential**: Identify novel or creative solutions
4. **Synthesis**: Combine ideas into actionable concepts

**🎨 Brainstorming Prompts:**
- What if there were no constraints? What would you explore?
- How might others approach this challenge differently?
- What analogies or parallels exist in other domains?
- What are the most unconventional ideas we can consider?

"""

        # Add expertise-specific guidance
        prompt += f"**🎓 {expertise_area.title()} Expertise Focus:**\n"

        if expertise_area == "technical":
            prompt += """- Technical architecture and design patterns
- Implementation best practices and code quality
- Performance optimization and scalability
- Integration strategies and compatibility
- Technology selection and evaluation
"""
        elif expertise_area == "research":
            prompt += """- Information gathering and source evaluation
- Research methodology and analysis techniques
- Comprehensive coverage and validation
- Recent developments and trends
- Cross-referencing and verification
"""
        elif expertise_area == "troubleshooting":
            prompt += """- Systematic problem diagnosis
- Root cause analysis techniques
- Solution testing and validation
- Prevention and monitoring strategies
- Documentation and knowledge transfer
"""
        elif expertise_area == "optimization":
            prompt += """- Performance bottleneck identification
- Resource utilization analysis
- Efficiency improvement strategies
- Measurement and benchmarking
- Continuous optimization approaches
"""
        elif expertise_area == "security":
            prompt += """- Threat assessment and vulnerability analysis
- Security best practices and standards
- Protective measures and controls
- Compliance and regulatory considerations
- Security monitoring and incident response
"""
        elif expertise_area == "strategy":
            prompt += """- Strategic planning and goal alignment
- Risk assessment and mitigation
- Resource optimization and allocation
- Decision-making frameworks
- Long-term vision and sustainability
"""
        elif expertise_area == "learning":
            prompt += """- Learning path development
- Knowledge structuring and retention
- Practical application and skill building
- Resource recommendations and curation
- Progress tracking and assessment
"""

        prompt += f"""
**🚀 Ready to Begin!**

I'm ready to provide expert guidance on **{topic}**.

**To get started, please share:**
1. Your current context or situation
2. Specific questions or areas of focus
3. Any constraints or requirements
4. What you hope to achieve from this session

Let's work together to achieve your goals!
"""

        return prompt

    except Exception as e:
        return f"Error generating consultation session prompt: {str(e)}"