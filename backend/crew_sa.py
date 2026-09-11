from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os
from config import llm

load_dotenv()

solution_architect = Agent(
    role="Senior Technical Solution architect",
    goal=(
        "Design a practical, scalable, secure, and cost-effective "
        "high-level solution architecture based on the business requirements "
        "and constraints provided."
    ),
    backstory=(
        "You are an experienced Senior Solution Architect with expertise in "
        "designing software and AI-enabled solutions. You translate business "
        "requirements into practical technical architectures. "
        
        "You are responsible for determining how a solution should be built, "
        "including the overall solution approach, architecture style, major "
        "system components, component interactions, data flow, integration "
        "requirements, data storage needs, security considerations, scalability "
        "strategy, and deployment approach. "
        
        "You always balance scalability, maintainability, security, cost, "
        "development complexity, expected traffic, and delivery timeline. "
        
        "You avoid unnecessary over-engineering and prefer simple, pragmatic "
        "architectures for MVP solutions. You do not recommend microservices, "
        "complex distributed systems, or enterprise-grade infrastructure unless "
        "they are genuinely justified by the requirements. "
        
        "You also distinguish between the recommended MVP architecture and "
        "possible future architectural evolution as the solution scales."
    ),
    llm = llm,
    max_iter=3,
    max_retry_limit=2,
    verbose=True
)


def create_sa_task(ba_task):
    sa_task = Task(

        description="""
    Based on the Business Analysis generated in the previous task,
    design a high-level technical solution architecture.

    Your responsibility is to determine HOW the proposed solution
    should be implemented.

    Analyse the business requirements, constraints, expected traffic,
    technology preferences, and delivery timeline.

    Provide recommendations for:

    1. Recommended solution approach
    2. Architecture style
    3. Major components 
    4. Responsibility of each technology component in the overall system
    5. High-level data flow
    6. Integration requirements
    7. Data storage architecture
    8. Authentication and authorization approach
    9. Security considerations
    10. Scalability strategy
    11. Deployment approach
    12. MVP architecture
    13. Future architecture evolution
    14. Architecture complexity assessment
    15. Key architecture decisions and their rationale

    IMPORTANT GUIDELINES:

    - Do not repeat the business requirements unless necessary.
    - Focus on translating requirements into a technical architecture.
    - Avoid unnecessary over-engineering.
    - Do not recommend microservices unless justified.
    - Consider the expected traffic and delivery timeline.
    - Respect the user's technology preference where practical.
    - Clearly differentiate between what is required for the MVP and
    what can be introduced in future versions.
    - Do not select very specific technologies unless required for the
    architectural decision. Detailed technology selection will be
    handled by a Technology Advisor agent.
    - Respect the user's stated cloud preference when designing the architecture.
    - If a specific cloud platform is selected (AWS, Azure, or GCP), prefer that
    platform's services where they provide a suitable architectural fit.
    - If "No Specific Cloud Preference" is selected, remain cloud-neutral and
    evaluate cloud options based on technical fit, scalability, security,
    operational simplicity, and delivery timeline.
    - Do not introduce a different cloud platform unless there is a strong
    architectural justification.

    The architecture should be practical and implementable by a
    development team.

    OUTPUT CONSTRAINTS:
    - Keep the output concise and decision-oriented.
    - Target approximately 800-1000 words.
    - Do not provide exhaustive technology comparisons or implementation details.
    - Focus only on architecture decisions that are necessary to satisfy the requirements.
    - For each major architectural decision, provide a brief rationale.
    - Clearly separate MVP architecture from future evolution.
    - Do not make it too extensive. We need a quick response time.
    """,

        expected_output="""
    A concise Solution Architecture Document in Markdown containing:
1. Solution Overview
2. Recommended Architecture
3. Major Components and Responsibilities
4. High-Level Data Flow
5. Data Architecture
6. Security and Authentication
7. Scalability
8. Deployment Approach
9. MVP vs Future Architecture
10. Key Architecture Decisions and Risks
    """,

        agent=solution_architect,

        context=[ba_task]
    )

    return sa_task