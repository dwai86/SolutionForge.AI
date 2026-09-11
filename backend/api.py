from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from crew import generate_solution


app = FastAPI(
    title="AI Solution Consultant API",
    description="API for generating AI-powered solution blueprints",
    version="1.0.0"
)


class SolutionRequest(BaseModel):

    business_idea: str = Field(
        "Your business idea",
        min_length=10,
        description="Business idea or problem statement"
    )

    technology_preference: str = Field(
        "opensource",
        description="Technology preference: enterprise or opensource"
    )

    cloud_preference: str = Field(
            "Azure",
            description="Cloud preference: AWS, Azure, GCP, or no specific preference"
        )

    daily_traffic: int = Field(
        5000,
        gt=0,
        description="Expected daily traffic"
    )

    delivery_timeline_months: int = Field(
        5,
        gt=0,
        description="Expected delivery timeline in months"
    )

    country: str = Field(
        "USA",
        min_length=2,
        description="Country where data will be hosted"
    )


class SolutionResponse(BaseModel):
    status: str
    report: str
    html: str


@app.get("/")
def root():
    return {
        "message": "AI Solution Consultant API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/api/v1/solution",
    response_model=SolutionResponse
)
def generate_solution_api(request: SolutionRequest):

    try:

        result = generate_solution(
            business_idea=request.business_idea,
            technology_preference=request.technology_preference,
            cloud_preference=request.cloud_preference,
            daily_traffic=request.daily_traffic,
            delivery_timeline_months=request.delivery_timeline_months,
            country=request.country
        )

        return SolutionResponse(
            status="success",
            report=result["result"],
            html=result["html"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Solution generation failed: {str(e)}"
        )