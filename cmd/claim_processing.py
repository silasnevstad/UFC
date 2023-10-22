import json
from constants.functions import determine_search_term, evaluate_claim
from helpers.tokens import count_tokens
from sources.api.dpla import DPLAClient
from sources.api.arxiv import ArxivClient
from sources.api.pubmed import PubMedClient
from sources.web.national_archives import NationalArchivesScraper
from sources.web.history_net import HistoryNetScraper
from sources.web.bbc import BBCScraper
from sources.web.google_scholar import GoogleScholarScraper
import logging

GENRES = {
    'history': [
        DPLAClient(),
        NationalArchivesScraper(),
        HistoryNetScraper(),
        BBCScraper(),
    ],
    'science': [
        ArxivClient(),
        PubMedClient(),
        GoogleScholarScraper(),
        BBCScraper(),
    ],
    'politics': [
        BBCScraper(),
    ],
}

def process_claim(logger, gpt_client, claim, topic=None, genre=None):
    logger.info(f'Processing claim: {claim}.')

    while topic is None or genre is None:
        # If topic or genre is not provided, then we need to determine it
        function_call = gpt_client.get_function_call(
            [{"role": "user", "content": f"Identify topic for the claim : {claim}"}],
            [determine_search_term]
        )
        
        if function_call:
            logger.info(f'Found function call: {function_call.get("name")}, arguments: {function_call.get("arguments")}')
            arguments = function_call.get('arguments')
            topic = json.loads(arguments).get('searchTerm')
            genre = json.loads(arguments).get('genre')
        else:
            logger.error("No function call found in response")
            return
    
    limited_source_results = limit_sources(logger, query_sources(logger, genre, topic))
    source_results_str = json.dumps(limited_source_results, indent=2)

    messages = [
        {"role": "system", "content": "Reputable evidence for evaluation."},
        {"role": "system", "content": source_results_str},
        {"role": "user", "content": f"Evaluate the claim (making sure to provide evidence): {claim}"}
    ]

    evaluation_response = gpt_client.chat_completion(messages, [evaluate_claim])
    arguments = evaluation_response["choices"][0]["message"]["function_call"]["arguments"]
    arguments_json = json.loads(arguments)

    claim = arguments_json["claim"]
    evaluation = arguments_json["evaluation"]
    evidence = arguments_json["evidence"]

    result = {
        'claim': claim,
        'topic': topic,
        'genre': genre,
        'evaluation': evaluation,
        'evidence': evidence
    }

    return result

def query_sources(logger, genre, topic):
    logger.info(f'Querying sources for genre: {genre} and topic: {topic}.')

    sources = GENRES.get(genre, [])
    results = []

    for source in sources:
        results.extend(source.search(topic))

    logger.info(f'Found {len(results)} results.')

    return results

def limit_sources(logger, results):
    max_tokens = 3800
    current_tokens = count_tokens(json.dumps(results))

    while current_tokens > max_tokens:
        results.pop()
        current_tokens = count_tokens(json.dumps(results))

    logger.info(f'Limited results to {len(results)}.')

    return results