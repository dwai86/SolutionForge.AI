from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os
from config import llm

load_dotenv()



business_analyst = Agent(
    role="Senior Business Analyst",
    goal="Perform Business analysis of the idea that the user has provided",
    backstory=(
        "You are an experienced Business Analyst.You are responsible for understanding the business idea and Extracting requirements, Identifying stakeholders, Functional requirements, Non-functional requirements, Assumptions, Identifying potential constraints, Highlighting missing information"
    ),
    llm = llm,
    verbose=True,
    max_iter=3,
    max_retry_limit=2,
)

def create_ba_task(
    ip_idea,
    ip_technology_preference,
    ip_cloud_preference,
    ip_daily_traffic,
    ip_delivery_timeline,
    ip_country_of_operation
):
    
    ba_task = Task(

        description= f"""Given the user inputs : 
        business idea - {ip_idea} 
        technology stack preference (enterprise / opensource) - {ip_technology_preference} 
        cloud preference (aws, azure, gcp, or no specific cloud preference) - {ip_cloud_preference}
        expected daily traffic - {ip_daily_traffic}
        expected delivery timeline (months) - {ip_delivery_timeline}
        country where data will be hosted - {ip_country_of_operation}
        YOUR RESPONSIBILITIES:

    1. Understand the core business problem.

    2. Identify the primary users and stakeholders.

    3. Extract requirements that are explicitly stated or strongly implied.

    4. Separate requirements into:

    a. Core MVP Requirements
    Features absolutely necessary for the first usable version.

    b. Important Requirements
    Features that are valuable but may be implemented after the MVP
    depending on timeline and budget.

    c. Future Enhancements
    Features that should not be included in the initial delivery scope.

    5. Identify relevant non-functional requirements based on the
    business domain and expected traffic.

    6. Identify assumptions.

    7. Identify constraints.

    8. Identify risks.

    9. Identify missing information and ask clarifying questions.


    IMPORTANT RULES:

    - Do not unnecessarily expand the project scope.

    - Do not automatically assume enterprise features.

    - Do not automatically include AI, analytics, payment systems,
    third-party integrations, mobile applications, or advanced
    features unless justified.

    - When information is missing, capture it as a clarification rather
    than inventing a requirement.

    - Consider the delivery timeline when defining MVP scope.

    - The output will be used by downstream Solution Architect and
    Technology Advisor agents, so recommendations must be realistic,
    prioritized, and internally consistent.

    - Do not repeat the same requirement across multiple categories unless there is
  a clear reason.
    
    OUTPUT CONSTRAINTS:

    - Keep the analysis concise, compact, structured, and focused on information required by
    downstream Solution Architect and Technology Advisor agents.
    - Target approximately 500-700 words.
    - Prioritize requirements and decisions that materially affect the solution.
    - Do not provide detailed solution designs, technology recommendations, or
    implementation plans.
    - Do not repeat the user's input unnecessarily.
    - Avoid generic business analysis explanations.
    - When information is unavailable, record it as an assumption or clarification
    rather than inventing details.
    - Do not make it too extensive. We need a quick response time.
    """,

        expected_output=""" 
A concise and structured business analysis in valid JSON format.

The JSON should contain the following fields:

{
    "business_problem": {
        "description": ""
    },

    "business_context": {
        "industry": "",
        "solution_type": ""
    },

    "business_objectives": [],

    "users": [],

    "requirements": {
        "confirmed": [],
        "inferred": [],
        "mvp": [],
        "future": []
    },

    "non_functional_requirements": {
        "user_specified": [],
        "recommended": []
    },

    "constraints": {
        "technology_preference": "",
        "traffic": "",
        "timeline": ""
    },

    "assumptions": [],

    "risks": [],

    "clarifications_required": []
}
""",

        agent=business_analyst
    )

    return ba_task





