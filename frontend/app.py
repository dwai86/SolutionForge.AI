import streamlit as st
import requests
import streamlit.components.v1 as components
import threading
import time


API_URL = "http://127.0.0.1:8000/api/v1/solution"


# --------------------------------------------------
# Backend Call
# --------------------------------------------------

def call_backend(payload, result_container):

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=600
        )

        result_container["response"] = response

    except Exception as e:

        result_container["error"] = e


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Solution Consultant",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 AI Solution Consultant")

st.markdown(
    """
    ### Transform your business idea into a solution blueprint

    Provide your business requirements and constraints.  
    Our AI consulting team will analyze the problem, design the architecture,
    recommend technologies, and create a practical delivery plan.
    """
)

st.divider()


# --------------------------------------------------
# Input Section
# --------------------------------------------------

st.subheader("Business Requirements")


business_idea = st.text_area(
    "Business Idea / Problem Statement",
    placeholder=(
        "Example: Build a volunteer management portal where volunteers "
        "can register, maintain their profiles, view events and receive notices."
    ),
    height=120
)


col1, col2 = st.columns(2)


with col1:

    technology_preference = st.selectbox(
        "Technology Preference",
        options=["opensource", "enterprise"],
        index=0,
        format_func=lambda x: x.capitalize()
    )

    daily_traffic = st.number_input(
        "Expected Daily Traffic",
        min_value=1,
        value=5000,
        step=1000
    )

    cloud_preference = st.selectbox(
            "Cloud Preference",
            options=["AWS", "AZURE","GCP", "No Specific Cloud Preference"],
            index=0,
            format_func=lambda x: x.capitalize()
        )


with col2:

    delivery_timeline_months = st.number_input(
        "Delivery Timeline (Months)",
        min_value=1,
        value=5,
        step=1
    )

    country = st.text_input(
        "Country Where Data Will Be Hosted",
        value="USA"
    )


st.divider()


# --------------------------------------------------
# Generate Solution
# --------------------------------------------------

generate_button = st.button(
    "🚀 Generate Solution Blueprint",
    type="primary",
    use_container_width=True
)


if generate_button:

    # --------------------------------------------------
    # Validate Input
    # --------------------------------------------------

    if not business_idea.strip():

        st.error(
            "Please provide a business idea or problem statement."
        )

    else:

        request_payload = {
            "business_idea": business_idea,
            "technology_preference": technology_preference,
            "cloud_preference" : cloud_preference,
            "daily_traffic": daily_traffic,
            "delivery_timeline_months": delivery_timeline_months,
            "country": country
        }


        # --------------------------------------------------
        # Start Backend Request
        # --------------------------------------------------

        result_container = {}

        thread = threading.Thread(
            target=call_backend,
            args=(request_payload, result_container)
        )

        thread.start()


        # --------------------------------------------------
        # AI Consulting Progress
        # --------------------------------------------------

        st.subheader("🤖 AI Consulting Team")

        progress_box = st.empty()


        stages = [

            (
                "🔍",
                "Business Analyst",
                "Understanding business requirements"
            ),

            (
                "📋",
                "Requirements Analysis",
                "Identifying functional and non-functional requirements"
            ),

            (
                "🏗️",
                "Solution Architect",
                "Designing the high-level solution architecture"
            ),

            (
                "💻",
                "Technology Advisor",
                "Evaluating technology options and trade-offs"
            ),

            (
                "📅",
                "Delivery Planner",
                "Preparing the implementation roadmap"
            ),

            (
                "📝",
                "Blueprint Generator",
                "Compiling the final solution blueprint"
            )
        ]


        start_time = time.time()


        # --------------------------------------------------
        # Update Progress While Backend Is Running
        # --------------------------------------------------

        while thread.is_alive():

            elapsed = time.time() - start_time


            # ----------------------------------------------
            # Determine Current Stage
            # ----------------------------------------------

            if elapsed < 35:

                current_stage = 0

            elif elapsed < 75:

                current_stage = 1

            elif elapsed < 140:

                current_stage = 2

            elif elapsed < 210:

                current_stage = 3

            elif elapsed < 270:

                current_stage = 4

            else:

                current_stage = 5


            # ----------------------------------------------
            # Build Progress Display
            # ----------------------------------------------

            progress_text = """
🤖 AI Consulting Team is working

Multiple AI specialists are collaborating to build your solution.

"""


            for i, (icon, title, description) in enumerate(stages):

                if i < current_stage:

                    symbol = "✅"

                elif i == current_stage:

                    symbol = "🔄"

                else:

                    symbol = "⏳"


                progress_text += f"""
**{symbol} {icon} {title}**

&nbsp;&nbsp;&nbsp;&nbsp;{description}

"""


            # ----------------------------------------------
            # Elapsed Time
            # ----------------------------------------------

            minutes = int(elapsed) // 60
            seconds = int(elapsed) % 60


            progress_text += f"""
---

⏱️ **Elapsed time: {minutes:02d}:{seconds:02d}**
"""


            # ----------------------------------------------
            # Render Progress
            # ----------------------------------------------

            progress_box.markdown(progress_text)


            time.sleep(1)


        # Wait for thread to finish completely

        thread.join()


        # --------------------------------------------------
        # Handle Backend Error
        # --------------------------------------------------

        if "error" in result_container:

            st.error(
                f"Could not connect to the FastAPI backend: "
                f"{result_container['error']}"
            )


        else:

            response = result_container["response"]


            # --------------------------------------------------
            # Successful Response
            # --------------------------------------------------

            if response.status_code == 200:

                result = response.json()


                st.success(
                    "🎉 Solution blueprint generated successfully!"
                )


                st.divider()


                st.subheader("📋 Solution Blueprint")


                html_report = result.get("html", "")


                if html_report:

                    # ------------------------------------------
                    # Render HTML Report
                    # ------------------------------------------

                    components.html(
                        html_report,
                        height=1500,
                        scrolling=True
                    )


                    # ------------------------------------------
                    # Download HTML
                    # ------------------------------------------

                    st.download_button(
                        label="⬇️ Download Solution Blueprint",
                        data=html_report,
                        file_name="solution_blueprint.html",
                        mime="text/html"
                    )


                else:

                    st.error(
                        "The backend returned an empty HTML report."
                    )


            # --------------------------------------------------
            # Backend Error
            # --------------------------------------------------

            else:

                st.error(
                    f"Backend returned HTTP "
                    f"{response.status_code}"
                )


                try:

                    st.json(response.json())

                except Exception:

                    st.code(response.text)