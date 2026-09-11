from crewai import Agent, Task
from config import llm


delivery_planner = Agent(
    role="Senior Delivery Planner",
    goal=(
        "Create a practical and realistic delivery plan for the proposed solution "
        "based on the business requirements, solution architecture, and technology "
        "recommendations provided by the previous agents."
    ),
    backstory=(
        "You are an experienced Senior Delivery Planner with expertise in planning "
        "software and AI-enabled solution delivery. You translate business and "
        "technical recommendations into an executable delivery plan. "
        
        "You assess the scope, technical complexity, dependencies, team requirements, "
        "implementation sequence, milestones, risks, and delivery timeline. "
        
        "You ensure that the delivery plan is realistic for the stated delivery "
        "timeline and expected scale. You prioritize the MVP and avoid unnecessary "
        "scope expansion or over-engineering. "
        
        "You do not redesign the solution architecture or replace technology "
        "recommendations made by the Solution Architect or Technology Advisor unless "
        "a clear delivery constraint makes a recommendation impractical. In such "
        "cases, explicitly explain the reason for the change. "
        
        "You clearly distinguish confirmed requirements, assumptions, dependencies, "
        "and items requiring stakeholder clarification."
    ),
    llm=llm,
    max_iter=3,
    max_retry_limit=2,
    verbose=True
)


def create_dp_task(ba_task, sa_task, ta_task):

    dp_task = Task(
        description="""
        Based on the Business Analysis, Solution Architecture, and Technology
        Advisor outputs from the previous tasks, create a practical delivery plan
        for the proposed solution.

        Your responsibility is to determine how the recommended solution can be
        delivered within the stated constraints and timeline.

        Cover the following:

        1. Delivery approach
           - Recommended implementation approach
           - MVP-first strategy
           - Major delivery phases

        2. Scope and priorities
           - MVP scope
           - Important features
           - Future enhancements
           - Clearly identify anything that should be deferred
        
        3. Recommended Technology Stack
            - Capture the final recommended technology stack from the Technology Advisor.
            - Organize it by major solution layer/component.
            - For each technology, include its primary purpose.
            - Do not independently redesign or replace the Technology Advisor's
                recommendations unless a delivery constraint requires it.

        4. Implementation workstreams
           - Frontend
           - Backend
           - Database / data
           - AI / agentic components, if applicable
           - Infrastructure / cloud / deployment
           - Security
           - Testing
           - CI/CD and operations
           Include only the workstreams relevant to the proposed solution.

        5. Team composition and roles
           - Recommended team roles
           - Key responsibilities of each role
           - Identify where one person could reasonably cover multiple roles
             for an MVP or small team.

        6. Delivery timeline
           - Break the delivery into realistic phases or milestones.
           - Map major activities to the stated delivery timeline.
           - Identify critical-path activities and dependencies.

        7. Effort and complexity assessment
           - Overall implementation complexity on a scale of 1-10.
           - Main factors contributing to complexity.
           - Identify areas requiring the most engineering effort.

        8. Dependencies and prerequisites
           - Technical dependencies
           - External integrations
           - Infrastructure requirements
           - Security / compliance prerequisites
           - Business decisions that must be resolved before implementation.
         
         9. High-Level Solution Architecture
            - Provide a simple, readable text-based architecture diagram.
            - Show the major system components and their relationships.
            - Show the primary request/data flow.
            - Reflect the architecture and technology stack recommended by the
            Solution Architect and Technology Advisor.
            - Keep the diagram high-level, compact, and easy to understand.
            - Do not include implementation-level details.
            - Do not use Mermaid, PlantUML, or other diagramming languages.
            - Do not provide a long textual explanation in place of the diagram.

        10. Testing and quality strategy
           - Functional testing
           - Integration testing
           - Security testing
           - Performance testing
           - User acceptance testing
           Include only the testing activities appropriate for the proposed solution.

        11. Deployment and release strategy
           - Environment strategy
           - CI/CD approach
           - Release approach
           - Rollback considerations
           - Production readiness considerations

        12. Delivery risks and mitigation
            - Identify the most significant delivery risks.
            - Provide a practical mitigation for each.

        13. Future evolution
            - Identify major capabilities or architectural changes that can be
              considered after the MVP.
            - Do not unnecessarily expand the MVP scope.

        IMPORTANT GUIDELINES:

        - Base the delivery plan on the outputs of the previous agents.
        - Do not redesign the architecture unless a delivery constraint clearly
          requires it.
        - Respect the stated delivery timeline.
        - The delivery plan MUST fit within the stated delivery timeline.
        - Ensure that all phases, milestones, testing, UAT, go-live, and buffer fit within the stated timeline. Do not produce a schedule that exceeds the user's timeline.
        - Treat the user's stated delivery timeline as a hard constraint.
        - The final milestone must occur within the stated timeline.
        - Any contingency or buffer must be included within the stated timeline,
          not added after it.
        - Use one consistent interpretation of months and weeks throughout the plan.
        - Validate the timeline before producing the final output.
        - Validate the consistency of all week/month references before producing the final output.
        - Prioritize the MVP and defer non-essential functionality.
        - Do not introduce unnecessary technologies, frameworks, or infrastructure.
        - Clearly distinguish confirmed requirements from assumptions and items
          requiring clarification.
        - Do not assume regulatory or compliance requirements that have not been
          confirmed. Identify them as validation items where appropriate.
        - Do not include cost estimates, cost assumptions, pricing, or budget-related questions anywhere in the delivery plan.
        - Keep the recommendations practical and suitable for the expected scale
          of the solution.
        - Do not introduce new technology choices or detailed infrastructure specifications unless they are necessary for delivery planning. Use the Technology Advisor's recommendations as the source of truth for the technology stack.
        - Do not make it too extensive. We need a quick response time.
        """,

        expected_output="""
        A structured Delivery Plan in Markdown containing:

        1. Delivery Overview
        2. MVP Scope and Priorities
        3. Recommended Technology Stack (as captured by technology advisor agent)
        4. Implementation Workstreams
        5. Recommended Team and Roles
        6. Delivery Timeline and Milestones
        7. Effort and Complexity Assessment
        8. Dependencies and Prerequisites
        9. High-Level Solution Architecture
        10. Testing and Quality Strategy
        11. Deployment and Release Strategy
        12. Delivery Risks and Mitigations
        13. Future Evolution
        14. Key Delivery Assumptions and Open Questions

        The plan should be concise, actionable, and directly traceable to the
        Business Analyst, Solution Architect, and Technology Advisor outputs.
        """,

        agent=delivery_planner,
        context=[ba_task, sa_task, ta_task]
    )

    return dp_task