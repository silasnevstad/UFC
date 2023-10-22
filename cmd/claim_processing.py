import json
from constants.functions import determine_search_term, evaluate_claim
from helpers.tokens import count_tokens
from helpers.logging import log_function_call
from sources.api.dpla import DPLAClient
from sources.api.arxiv import ArxivClient
from sources.api.pubmed import PubMedClient
from sources.web.national_archives import NationalArchivesScraper
from sources.web.history_net import HistoryNetScraper
from sources.web.bbc import BBCScraper
from sources.web.google_scholar import GoogleScholarScraper
from sources.web.nature import NatureScraper
from rich.progress import track
from rich import print

# genres are ordered by priority (lower number = higher priority)
GENRES = {
    'history': {
        BBCScraper(): 1,
        NationalArchivesScraper(): 2,
        HistoryNetScraper(): 3,
        DPLAClient(): 4,
    },
    'science': {
        ArxivClient(): 1,
        NatureScraper(): 2,
        GoogleScholarScraper(): 3,
        PubMedClient(): 4,
    },
    'politics': {
        BBCScraper(): 1,
    },
}

def get_topic_and_genre(logger, gpt_client, claim):
    function_call = gpt_client.get_function_call(
        [{"role": "user", "content": f"Identify the seacrh term and topic for the claim: {claim}"}],
        [determine_search_term]
    )
    
    if function_call:
        arguments = json.loads(function_call.get('arguments', '{}'))
        # log_function_call(logger, function_call.get('name'), arguments)
        topic = arguments.get('searchTerm')
        genre = arguments.get('genre')
        print(f"Found topic: [bold cyan]{topic}[/] and genre: [bold cyan]{genre}[/] for the claim: [green]{claim}[/]")
    else:
        logger.error("No function call found in response")
        return
    
    return topic, genre

def process_claim(logger, gpt_client, claim, topic, genre):
    if not topic or not genre:
        logger.warning(f'No topic or genre found for claim: {claim}.')
        topic, genre = get_topic_and_genre(logger, gpt_client, claim)
    
    limited_source_results = limit_sources(logger, query_sources(logger, genre, topic))
    source_results_str = json.dumps(limited_source_results, indent=2)

    messages = [
        {"role": "system", "content": "Reputable evidence for evaluation."},
        {"role": "system", "content": source_results_str},
        {"role": "user", "content": f"Evaluate the claim (making sure to provide evidence): {claim}"}
    ]

    evaluation_call = gpt_client.get_function_call(messages, [evaluate_claim])

    if evaluation_call:
        # log_function_call(logger, evaluation_call.get('name'), evaluation_call.get("arguments"))
        json_string = evaluation_call.get('arguments', '{}')
        try:
            arguments = json.loads(json_string)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            logger.error(f"JSON content: {json_string}")
            return
        evaluation = arguments.get('evaluation')
        evidence = arguments.get('evidence')
        fixed_claim = arguments.get('fixedClaim')
    else:
        logger.error("No function call found in response")
        return

    if evaluation == True:
        print(f"[bold green]{claim}[/] has been [bold green]verified[/]!")
    else:
        print(f"[bold red]{claim}[/] has been [bold red]debunked[/]!")
    

    result = {
        'claim': claim,
        'topic': topic,
        'genre': genre,
        'evaluation': evaluation,
        'evidence': evidence,
        'fixedClaim': fixed_claim if fixed_claim else None,
    }

    return result

def query_sources(logger, genre, topic):
    sources = GENRES.get(genre, {})
    sorted_sources = sorted(sources, key=sources.get)  # Sort sources by priority

    results = []

    for source in track(sorted_sources, description=f"Querying {genre} sources for {topic}...", transient=True):
        source_results = source.search(topic)
        
        if source_results:
            results.extend(source_results)

            # if we have enough results, stop querying sources
            if len(results) >= 10:
                logger.info(f'Quitting early after querying {sorted_sources.index(source) + 1} sources. Found {len(results)} results.')
                break

    else:
        logger.info(f'Finished querying all sources. Found {len(results)} results.')

    return results

def limit_sources(logger, results):
    max_tokens = 3700
    current_tokens = count_tokens(json.dumps(results))

    while current_tokens > max_tokens:
        results.pop()
        current_tokens = count_tokens(json.dumps(results))

    logger.info(f'Limited results to {len(results)} (tokens: {current_tokens}).')

    return results