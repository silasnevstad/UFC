split_into_claims = {
    "name": "split_into_claims",
    "description": "Breaks text into individual, standalone claims.",
    "parameters": {
        "type": "object",
        "properties": {
            "claims": {
                "type": "array",
                "description": "List of distinct claims.",
                "items": {
                    "type": "string",
                    "description": "Single, standalone claim.",
                },
            },
        },
        "required": ["claims"],
    },
}

determine_search_term = {
    "name": "determine_search_term",
    "description": "Extracts specific seacrh term and genre from a claim.",
    "parameters": {
        "type": "object",
        "properties": {
            "claim": {
                "type": "string",
                "description": "Single claim sentence.",
            },
            "searchTerm": {
                "type": "string",
                "description": "Specific search term to be used for evidence search.",
            },
            "genre": {
                "type": "string",
                "description": "Claim genre (strictly either history, science, politics).",
            },
        },
        "required": ["claim", "searchTerm", "genre"],
    },
}

evaluate_claim = {
    "name": "evaluate_claim",
    "description": "Assesses claim's truth based on evidence.",
    "parameters": {
        "type": "object",
        "properties": {
            "claim": {
                "type": "string",
                "description": "Statement being assessed.",
            },
            "fixedClaim": {
                "type": "string",
                "description": "Accurate version if claim is false.",
            },
            "evaluation": {
                "type": "boolean",
                "description": "Truth assessment (true/false).",
            },
            "evidence": {
                "type": "array",
                "description": "Evidence supporting/opposing claim (!!!MAX 3!!!).",
                "items": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "Evidence URL.",
                        },
                        "source": {
                            "type": "string",
                            "description": "Evidence source.",
                        },
                        "text": {
                            "type": "string",
                            "description": "Excerpt from evidence supporting/oppsing claim.",
                        },
                    },
                    "required": ["url", "source", "text"],
                },
            }
        },
        "required": ["claim", "evaluation", "evidence", "fixedClaim"],
    },
}