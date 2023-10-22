split_into_claims = {
    "name": "split_into_claims",
    "description": "Splits some text into individual claims",
    "parameters": {
        "type": "object",
        "properties": {
            "claims": {
                "type": "array",
                "description": "A list of individual claims (each claim should only be making a single claim)",
                "items": {
                    "type": "string",
                    "description": "A sentence/piece of a sentence making only a single claim",
                },
            },
        },
        "required": ["claims"],
    },
}

determine_search_term = {
    "name": "determine_search_term",
    "description": "Determines the search term / topic of a claim (that could be used to search for evidence)",
    "parameters": {
        "type": "object",
        "properties": {
            "claim": {
                "type": "string",
                "description": "A sentence/piece of a sentence making only a single claim",
            },
            "searchTerm": {
                "type": "string",
                "description": "The topic or search term associated with the claim",
            },
            "genre": {
                "type": "string",
                "description": "The genre of the claim (strictly history, science or politics)",
            },
        },
        "required": ["claim", "searchTerm", "genre"],
    },
}

evaluate_claim = {
    "name": "evaluate_claim",
    "description": "Evaluates the factual accuracy of a claim based on provided evidence.",
    "parameters": {
        "type": "object",
        "properties": {
            "claim": {
                "type": "string",
                "description": "The claim being evaluated",
            },
            "fixed_claim": {
                "type": "string",
                "description": "If the claim is not true, then provide a fixed claim correcting it",
            },
            "evaluation": {
                "type": "boolean",
                "description": "The evaluation of the claim (true = factual, false = not factual)",
            },
            "evidence": {
                "type": "array",
                "description": "The evidence used to support/oppose the claim (only evidence pertaining to the claim should be provided)",
                "items": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL of the evidence",
                        },
                        "source": {
                            "type": "string",
                            "description": "The source of the evidence",
                        },
                        "text": {
                            "type": "string",
                            "description": "The text of the evidence",
                        },
                    },
                    "required": ["url", "source", "text"],
                },
            }
        },
        "required": ["claim", "evaluation", "evidence"],
    },
}