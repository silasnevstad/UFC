split_into_claims = {
    "name": "split_into_claims",
    "description": "Verifies a list of individual claims",
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

determine_factualness_or_credibility = {
    "name": "determine_factualness_or_credibility",
    "description": "Determines the factualness or credibility of a claim",
    "parameters": {
        "type": "object",
        "properties": {
            "claim": {
                "type": "string",
                "description": "A sentence/piece of a sentence making only a single claim",
            },
            "topic": {
                "type": "string",
                "description": "The topic or search term associated with the claim",
            },
            "genre": {
                "type": "string",
                "description": "The genre of the claim (strictly history, science or politics)",
            },
        },
        "required": ["claim", "topic"],
    },
}

evaluate_claim = {
    "name": "give_claim_evaluation",
    "description": "Returns a claim evaluation given claim evaluation information",
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