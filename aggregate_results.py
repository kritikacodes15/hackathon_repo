import csv
import json


with open("claim_results.json", "r", encoding="utf-8") as f:
    claim_results = json.load(f)


# ===============================
# INPUT (dummy for now)
# ===============================

claim_results = {
    "story_001": {
        "claims": [
            {"claim_id": "C1", "score": 1, "core": True},
            {"claim_id": "C2", "score": 0, "core": True},
            {"claim_id": "C3", "score": 1, "core": False}
        ]
    }
}

# ===============================
# AGGREGATION LOGIC
# ===============================

def aggregate_claims(claims):
    """
    Rule:
    - If ANY core claim has score 0 → final prediction = 0
    - Else → final prediction = 1
    """
    for claim in claims:
        if claim["core"] and claim["score"] == 0:
            return 0, "A core backstory claim is contradicted by the narrative."
    return 1, "All core backstory claims are consistent with the narrative."

# ===============================
# WRITE CSV
# ===============================

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["story_id", "prediction", "rationale"])

    for story_id, data in claim_results.items():
        prediction, rationale = aggregate_claims(data["claims"])
        writer.writerow([story_id, prediction, rationale])

print("✅ results.csv created successfully")
