"""File analysis deep dive prompt implementation for comprehensive code/document review."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mcp.server.fastmcp.prompts import base
from typing import List, Optional
from utils.perplexity_client import get_perplexity_api


async def file_analysis_deep_dive(file_type: str, analysis_depth: str = "comprehensive", focus_areas: str = "general") -> str:
    """Comprehensive file analysis session with structured review approach."""

    try:
        # Define analysis approaches for different file types
        file_type_approaches = {
            "python": {
                "focus": "Python code quality, architecture, and best practices",
                "key_areas": ["Code structure and organization", "Performance and optimization", "Security considerations", "Testing and maintainability", "Documentation and readability"]
            },
            "javascript": {
                "focus": "JavaScript/TypeScript code quality, patterns, and performance",
                "key_areas": ["Code structure and patterns", "Performance and memory management", "Security and XSS prevention", "Modern syntax and features", "Browser/Node.js best practices"]
            },
            "json": {
                "focus": "Data structure, schema validation, and organization",
                "key_areas": ["Schema consistency", "Data validation", "Structure optimization", "Naming conventions", "Documentation and metadata"]
            },
            "markdown": {
                "focus": "Content structure, clarity, and documentation quality",
                "key_areas": ["Content organization", "Clarity and readability", "Formatting consistency", "Information completeness", "Accessibility and usability"]
            },
            "yaml": {
                "focus": "Configuration structure, validation, and best practices",
                "key_areas": ["Structure and hierarchy", "Validation and error handling", "Security considerations", "Environment management", "Documentation and comments"]
            },
            "text": {
                "focus": "Content analysis, structure, and information extraction",
                "key_areas": ["Content organization", "Key information extraction", "Structure and formatting", "Clarity and completeness", "Actionable insights"]
            }
        }

        analysis_depths = {
            "quick": "High-level overview with key insights and immediate recommendations",
            "standard": "Detailed analysis covering major aspects and improvement areas",
            "comprehensive": "In-depth review covering all aspects with detailed recommendations",
            "expert": "Expert-level analysis with advanced insights and optimization strategies"
        }

        focus_areas_map = {
            "general": "Overall quality and best practices",
            "security": "Security vulnerabilities and protective measures",
            "performance": "Performance optimization and efficiency",
            "maintainability": "Code structure, documentation, and long-term maintenance",
            "architecture": "Design patterns, structure, and architectural considerations",
            "testing": "Test coverage, quality, and testing strategies",
            "documentation": "Documentation quality, clarity, and completeness"
        }

        approach_info = file_type_approaches.get(file_type, {
            "focus": f"General {file_type} file analysis and improvement",
            "key_areas": ["Structure and organization", "Quality assessment", "Best practices", "Improvement opportunities", "Documentation"]
        })

        depth_desc = analysis_depths.get(analysis_depth, analysis_depths["standard"])
        focus_desc = focus_areas_map.get(focus_areas, focus_areas_map["general"])

        prompt = f"""🔍 **File Analysis Deep Dive**

**File Type:** {file_type.title()}
**Analysis Depth:** {analysis_depth.title()}
**Focus Area:** {focus_areas.title()}

**📋 Analysis Scope:**
- **Primary Focus:** {approach_info['focus']}
- **Depth Level:** {depth_desc}
- **Special Attention:** {focus_desc}

**🎯 Analysis Framework:**
"""

        # Add structured analysis sections
        prompt += f"""
**1. 📊 Structural Analysis**
- File organization and layout review
- Logical flow and coherence assessment
- Consistency checks across sections
- Hierarchical structure evaluation

**2. 🏆 Quality Assessment**
- {file_type.title()}-specific quality metrics
- Best practices compliance
- Industry standards alignment
- Comparative analysis with similar files

**3. 🔧 Improvement Opportunities**
- Performance optimization suggestions
- Maintainability enhancements
- Security improvements (if applicable)
- Documentation and clarity improvements

**4. 📈 Advanced Insights**
- Pattern recognition and suggestions
- Optimization strategies
- Integration considerations
- Future-proofing recommendations
"""

        # Add file-type specific analysis criteria
        prompt += f"\n**🎯 {file_type.title()}-Specific Analysis Criteria:**\n"

        for i, area in enumerate(approach_info['key_areas'], 1):
            prompt += f"**{i}. {area}**\n"

            if file_type == "python":
                if "structure" in area.lower():
                    prompt += "   - Class and function organization\n   - Module structure and imports\n   - Code reusability and DRY principles\n   - Design pattern implementation\n"
                elif "performance" in area.lower():
                    prompt += "   - Algorithm efficiency analysis\n   - Memory usage optimization\n   - I/O operations review\n   - Concurrency and async patterns\n"
                elif "security" in area.lower():
                    prompt += "   - Input validation and sanitization\n   - Authentication and authorization\n   - Sensitive data handling\n   - Dependency security assessment\n"
                elif "testing" in area.lower():
                    prompt += "   - Test coverage analysis\n   - Test quality and effectiveness\n   - Mocking and isolation strategies\n   - Integration testing considerations\n"
                elif "documentation" in area.lower():
                    prompt += "   - Docstring completeness and quality\n   - README and API documentation\n   - Code comments effectiveness\n   - Type hints and annotations\n"

            elif file_type == "javascript":
                if "structure" in area.lower():
                    prompt += "   - Function and class organization\n   - Module system usage (ES6/CommonJS)\n   - Scope and closure management\n   - Code splitting and bundling considerations\n"
                elif "performance" in area.lower():
                    prompt += "   - DOM manipulation efficiency\n   - Event handling optimization\n   - Memory leak prevention\n   - Bundle size and loading performance\n"
                elif "security" in area.lower():
                    prompt += "   - XSS prevention strategies\n   - Content Security Policy implementation\n   - Secure data transmission\n   - Third-party dependency security\n"
                elif "syntax" in area.lower():
                    prompt += "   - Modern JavaScript features usage\n   - TypeScript adoption opportunities\n   - Code style consistency\n   - ESLint configuration effectiveness\n"

            elif file_type == "json":
                if "schema" in area.lower():
                    prompt += "   - JSON schema validation opportunities\n   - Data type consistency\n   - Structural hierarchy analysis\n   - Validation rule implementation\n"
                elif "validation" in area.lower():
                    prompt += "   - Required field completeness\n   - Data format validation\n   - Range and constraint checking\n   - Error handling strategies\n"
                elif "structure" in area.lower():
                    prompt += "   - Nesting optimization\n   - Key naming conventions\n   - Data normalization opportunities\n   - Redundancy elimination\n"

            elif file_type == "markdown":
                if "content" in area.lower():
                    prompt += "   - Information hierarchy assessment\n   - Content completeness evaluation\n   - Target audience appropriateness\n   - Actionable content identification\n"
                elif "formatting" in area.lower():
                    prompt += "   - Markdown syntax consistency\n   - Heading structure analysis\n   - List and table formatting\n   - Link and image embedding quality\n"
                elif "accessibility" in area.lower():
                    prompt += "   - Screen reader compatibility\n   - Alt text for images\n   - Link descriptive text\n   - Structure and navigation clarity\n"

            prompt += "\n"

        # Add depth-specific instructions
        prompt += f"**🔬 {analysis_depth.title()} Analysis Protocol:**\n"

        if analysis_depth == "quick":
            prompt += """- Focus on immediate, high-impact improvements
- Identify critical issues only
- Provide actionable quick wins
- Highlight major strengths and concerns
"""
        elif analysis_depth == "standard":
            prompt += """- Comprehensive coverage of major areas
- Detailed improvement recommendations
- Best practices evaluation
- Implementation priority suggestions
"""
        elif analysis_depth == "comprehensive":
            prompt += """- Exhaustive analysis of all aspects
- Detailed code examples and suggestions
- Advanced optimization strategies
- Long-term maintenance considerations
"""
        elif analysis_depth == "expert":
            prompt += """- Expert-level insights and patterns
- Advanced architectural recommendations
- Performance tuning at micro and macro levels
- Cutting-edge best practices and innovations
"""

        prompt += f"""
**🚀 Analysis Process:**
1. **Upload File**: Provide the {file_type} file for analysis
2. **Initial Scan**: Quick assessment of structure and content
3. **Deep Analysis**: Apply {analysis_depth} review methodology
4. **Recommendations**: Generate actionable improvement suggestions
5. **Implementation Guide**: Provide step-by-step improvement roadmap

**📊 Expected Deliverables:**
- Quality score and assessment report
- Detailed improvement recommendations
- Code examples and best practice suggestions
- Implementation priority matrix
- Follow-up monitoring suggestions

Ready to analyze your {file_type} file with {analysis_depth} depth focusing on {focus_areas}?
"""

        return prompt

    except Exception as e:
        return f"Error generating file analysis deep dive prompt: {str(e)}"