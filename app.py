import json
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Football Scouting Prompt Lab",
    page_icon="⚽",
    layout="wide",
)

BASE_FOLDER = Path(__file__).parent
RESULTS_FOLDER = BASE_FOLDER / "results"
PROMPTS_FOLDER = BASE_FOLDER / "prompts"
EVALUATION_FILE = BASE_FOLDER / "evaluation" / "evaluation-results.csv"


def load_json(file_path):
    """Load a JSON response and remove accidental Markdown fences."""
    text = file_path.read_text(encoding="utf-8").strip()

    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return json.loads(text.strip())


st.title("⚽ Football Scouting Prompt Evaluation Lab")

st.write(
    """
    This project examines how prompt structure affects the quality,
    consistency and factual grounding of AI-generated football scouting reports.
    """
)

st.info(
    "The players and statistics used in this project are fictional. "
    "The reports are pre-generated evaluation results, not live scouting advice."
)

report_tab, comparison_tab, prompts_tab, methodology_tab = st.tabs(
    [
        "Player Reports",
        "Prompt Comparison",
        "Prompt Versions",
        "Methodology",
    ]
)


with report_tab:
    st.header("Structured scouting reports")

    json_files = sorted(RESULTS_FOLDER.glob("*.json"))

    if not json_files:
        st.error(
            "No JSON reports were found. Check that your files are "
            "inside the results folder."
        )
    else:
        player_options = {
            file_path.stem.replace("-", " ").title(): file_path
            for file_path in json_files
        }

        selected_player = st.selectbox(
            "Select a player",
            list(player_options.keys()),
        )

        try:
            report = load_json(player_options[selected_player])

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Player",
                report.get("player_name", "Not provided"),
            )

            col2.metric(
                "Position",
                report.get("position", "Not provided"),
            )

            col3.metric(
                "Recommendation",
                report.get(
                    "recruitment_recommendation",
                    "Not provided",
                ).title(),
            )

            st.subheader("Strengths")

            for strength in report.get("strengths", []):
                with st.container(border=True):
                    st.markdown(
                        f"**{strength.get('strength', 'Strength')}**"
                    )
                    st.write(
                        strength.get(
                            "evidence",
                            "No evidence provided.",
                        )
                    )

            st.subheader("Development areas")

            for area in report.get("development_areas", []):
                with st.container(border=True):
                    st.markdown(
                        f"**{area.get('area', 'Development area')}**"
                    )
                    st.write(
                        f"Evidence: {area.get('evidence', 'Not provided')}"
                    )
                    st.write(
                        "Suggested action: "
                        + area.get(
                            "suggested_action",
                            "Not provided",
                        )
                    )

            st.subheader("Recommended tactical role")

            role = report.get("recommended_role", {})

            st.markdown(
                f"**{role.get('role', 'Not provided')}**"
            )
            st.write(role.get("reason", "No reason provided."))

            st.subheader("Confidence")

            st.write(
                report.get("confidence", "Not provided").title()
            )

            st.subheader("Limitations")

            limitations = report.get("limitations", [])

            if limitations:
                for limitation in limitations:
                    st.write(f"- {limitation}")
            else:
                st.write("No limitations were recorded.")

            st.download_button(
                label="Download this report",
                data=json.dumps(report, indent=2),
                file_name=player_options[selected_player].name,
                mime="application/json",
            )

            with st.expander("View the complete JSON"):
                st.json(report)

        except json.JSONDecodeError:
            st.error(
                "This player file does not contain valid JSON. "
                "Check for missing brackets, incomplete text or code fences."
            )


with comparison_tab:
    st.header("Prompt comparison")

    comparison_data = pd.DataFrame(
        {
            "Evaluation criterion": [
                "Used numerical evidence",
                "Avoided invented information",
                "Followed requested format",
                "Gave relevant tactical analysis",
                "Explained limitations",
                "Total score",
            ],
            "Basic prompt": [2, 0, 2, 2, 2, 8],
            "Role prompt": [2, 1, 2, 2, 2, 9],
            "Structured prompt": [2, 1, 2, 2, 2, 9],
        }
    )

    st.dataframe(
        comparison_data,
        use_container_width=True,
        hide_index=True,
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Basic prompt", "8/10")
    col2.metric("Role prompt", "9/10")
    col3.metric("Structured prompt", "9/10")

    st.metric("Structured-output reliability", "96.7%")

    st.caption(
        "Scoring: 0 = failed, 1 = partly passed, 2 = fully passed."
    )

    st.subheader("Main finding")

    st.write(
        """
        The structured prompt produced the most consistent format across
        the five player profiles. It passed 29 of 30 reliability checks.
        The remaining failure came from Markdown code fences around one
        JSON response.
        """
    )

    if EVALUATION_FILE.exists():
        with st.expander("View uploaded evaluation file"):
            evaluation_data = pd.read_csv(EVALUATION_FILE)
            st.dataframe(
                evaluation_data,
                use_container_width=True,
                hide_index=True,
            )


with prompts_tab:
    st.header("Prompt versions")

    prompt_files = sorted(PROMPTS_FOLDER.glob("*.md"))

    if not prompt_files:
        st.warning(
            "No prompt files were found inside the prompts folder."
        )
    else:
        for prompt_file in prompt_files:
            prompt_name = (
                prompt_file.stem
                .replace("-", " ")
                .replace("01 ", "")
                .replace("02 ", "")
                .replace("03 ", "")
                .title()
            )

            with st.expander(prompt_name):
                st.code(
                    prompt_file.read_text(encoding="utf-8"),
                    language="text",
                )


with methodology_tab:
    st.header("Evaluation methodology")

    st.write(
        """
        Three prompt versions were tested:

        1. A basic zero-shot prompt
        2. A role-based prompt
        3. A structured production prompt

        The structured prompt was then tested across five fictional
        player profiles.
        """
    )

    st.subheader("Evaluation criteria")

    st.write(
        """
        Each response was assessed for:

        - Numerical evidence
        - Unsupported or invented claims
        - Format compliance
        - Tactical relevance
        - Explanation of limitations
        - Valid JSON structure
        """
    )

    st.subheader("Important limitations")

    st.write(
        """
        This is an educational prompt-engineering project. It does not
        replace professional scouting, video analysis, medical evaluation
        or contextual performance data. No real players or confidential
        club information were used.
        """
    )

st.divider()

st.caption(
    "Created by Aditya Naik as a prompt-engineering and "
    "football-analytics portfolio project."
)
