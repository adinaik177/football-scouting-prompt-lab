import json

import streamlit as st
from anthropic import Anthropic


st.set_page_config(
    page_title="AI Football Scout",
    page_icon="⚽",
    layout="centered"
)

st.title("AI Football Scouting Assistant")
st.write(
    "Enter a player's statistics to generate a structured "
    "AI-assisted scouting report."
)

with st.form("player_form"):
    player_name = st.text_input("Player name", "James Carter")
    age = st.number_input("Age", min_value=16, max_value=45, value=21)
    position = st.selectbox(
        "Position",
        [
            "Goalkeeper",
            "Centre-Back",
            "Right-Back",
            "Left-Back",
            "Defensive Midfielder",
            "Central Midfielder",
            "Attacking Midfielder",
            "Right Winger",
            "Left Winger",
            "Striker"
        ]
    )

    minutes = st.number_input(
        "Minutes played",
        min_value=1,
        value=1650
    )

    goals = st.number_input("Goals", min_value=0, value=4)
    assists = st.number_input("Assists", min_value=0, value=7)

    pass_completion = st.number_input(
        "Pass completion (%)",
        min_value=0.0,
        max_value=100.0,
        value=86.0
    )

    chances_created = st.number_input(
        "Chances created",
        min_value=0,
        value=41
    )

    tackles_won = st.number_input(
        "Tackles won",
        min_value=0,
        value=38
    )

    interceptions = st.number_input(
        "Interceptions",
        min_value=0,
        value=27
    )

    successful_dribbles = st.number_input(
        "Successful dribbles",
        min_value=0,
        value=32
    )

    submitted = st.form_submit_button("Generate scouting report")


if submitted:
    prompt = f"""
You are a football performance analyst supporting a recruitment team.

Analyse this player using only the supplied statistics.

Player:
- Name: {player_name}
- Age: {age}
- Position: {position}
- Minutes played: {minutes}
- Goals: {goals}
- Assists: {assists}
- Pass completion: {pass_completion}%
- Chances created: {chances_created}
- Tackles won: {tackles_won}
- Interceptions: {interceptions}
- Successful dribbles: {successful_dribbles}

Identify:
1. Three strengths
2. Two development areas
3. One suitable tactical role
4. A recruitment recommendation
5. Limitations of the analysis

Rules:
- Use only the supplied statistics.
- Every conclusion must include numerical evidence.
- Do not invent information.
- Do not describe a metric as strong, weak, high or low unless a
  suitable benchmark has been supplied.
- Treat successful dribbles as volume, not efficiency, because
  attempted dribbles have not been supplied.
- Do not infer finishing ability from chances created.
- Clearly identify information that is missing.
- Return only valid JSON.
- Do not place the JSON inside Markdown code fences.

Use this exact structure:

{{
  "player_name": "",
  "position": "",
  "strengths": [
    {{
      "strength": "",
      "evidence": ""
    }}
  ],
  "development_areas": [
    {{
      "area": "",
      "evidence": "",
      "suggested_action": ""
    }}
  ],
  "recommended_role": {{
    "role": "",
    "reason": ""
  }},
  "recruitment_recommendation": "recommend, monitor, or insufficient evidence",
  "confidence": "high, medium, or low",
  "limitations": []
}}
"""

    try:
        client = Anthropic(
            api_key=st.secrets["ANTHROPIC_API_KEY"]
        )

        with st.spinner("Analysing the player..."):
            message = client.messages.create(
                model=st.secrets["ANTHROPIC_MODEL"],
                max_tokens=1500,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

        response_text = message.content[0].text.strip()

        # Remove Markdown fences if the model adds them.
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        try:
            report = json.loads(response_text)

            st.success("Scouting report generated")
            st.subheader("Player assessment")
            st.json(report)

            st.download_button(
                label="Download report as JSON",
                data=json.dumps(report, indent=2),
                file_name=f"{player_name.lower().replace(' ', '-')}.json",
                mime="application/json"
            )

        except json.JSONDecodeError:
            st.warning(
                "The model returned a response that was not valid JSON."
            )
            st.text(response_text)

    except Exception as error:
        st.error(f"Unable to generate report: {error}")

st.divider()
st.caption(
    "Educational portfolio project. AI output should be supported "
    "by video scouting, contextual data and human evaluation."
)
