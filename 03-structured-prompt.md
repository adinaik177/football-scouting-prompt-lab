You are a football performance analyst supporting a recruitment team.

Analyse this player using only the statistics provided. Do not invent any
information.

Player:
- Name: James Carter
- Age: 21
- Position: Central Midfielder
- Minutes played: 1,650
- Goals: 4
- Assists: 7
- Pass completion: 86%
- Chances created: 41
- Tackles won: 38
- Interceptions: 27
- Successful dribbles: 32

Identify:
1. Three strengths
2. Two development areas
3. One suitable tactical role
4. A recruitment recommendation
5. The limitations of the analysis

Every conclusion must reference the supplied statistics.

Return only valid JSON using this structure:

{
  "player_name": "",
  "position": "",
  "strengths": [
    {
      "strength": "",
      "evidence": ""
    }
  ],
  "development_areas": [
    {
      "area": "",
      "evidence": "",
      "suggested_action": ""
    }
  ],
  "recommended_role": {
    "role": "",
    "reason": ""
  },
  "recruitment_recommendation": "recommend, monitor, or insufficient evidence",
  "confidence": "high, medium, or low",
  "limitations": []
}