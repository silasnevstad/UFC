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
    "description": "Extracts specific seacrh term (that can be used to query evidence) and genre from a claim. For instance, claim: 'The Amazon rainforest is the lungs of the Earth', search term: 'Amazon rainforest 'lungs of the Earth''; claim: 'In 1920, US women secured voting rights', search term: 'US women voting rights 1920'; claim: 'Mount Everest stands at 8,848 meters tall', search term: 'Mount Everest height'",
    "parameters": {
        "type": "object",
        "properties": {
            "claim": {
                "type": "string",
                "description": "Single claim sentence.",
            },
            "searchTerm": {
                "type": "string",
                "description": "Really specific search term to be used for evidence search.",
            },
            "genre": {
                "type": "string",
                "description": "Claim genre (strictly either history, science, politics, finance or current events).",
            },
        },
        "required": ["claim", "searchTerm", "genre"],
    },
}

evaluate_claim = {
    "name": "evaluate_claim",
    "description": "Evaluate claim's truth based on evidence.",
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