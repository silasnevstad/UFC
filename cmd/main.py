import json
from gpt.gpt_client import GPTClient
from constants.functions import split_into_claims, determine_search_term, evaluate_claim
from constants.prompts import INITIAL_PROMPT
from .claim_processing import process_claim, get_topic_and_genre
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('app.log'),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)

def run_conversation(user_input):
    logger.info('Starting a new conversation.')

    gpt_client = GPTClient()
    messages = [
        {"role": "system", "content": INITIAL_PROMPT},
        {"role": "user", "content": user_input}
    ]
    functions = [split_into_claims, determine_search_term, evaluate_claim]

    evaluation_results = []

    # Initial interaction to determine if input has single or multiple claims
    function_call = gpt_client.get_function_call(messages, functions)

    if function_call:
        function_name = function_call.get('name')
        logger.info(f'Found function call: {function_name}, arguments: {function_call.get("arguments")}')
        if function_name == 'split_into_claims':
            # Multiple claims scenario
            claims = json.loads(function_call.get('arguments', {})).get('claims', [])
            logger.info(f'Found {len(claims)} claims: {claims}')
            for claim in claims:
                topic, genre = get_topic_and_genre(logger, gpt_client, claim)
                result = process_claim(logger, gpt_client, claim, topic, genre)
                evaluation_results.append(result)
        elif function_name == 'determine_search_term':
            # Single claim scenario
            arguments = json.loads(function_call.get('arguments', {}))
            claim = arguments.get('claim')
            topic = arguments.get('searchTerm')
            genre = arguments.get('genre')
            logger.info(f'Found single claim: {claim}')
            result = process_claim(logger, gpt_client, claim, topic, genre)
            evaluation_results.append(result)
        else:
            print("Unexpected function call:", function_name)
    else:
        logger.error("No function call found in response")

    # logger.info(f"Evaluation results: {evaluation_results}")
    return evaluation_results

if __name__ == "__main__":
    user_input = "The Nazis killed 6 million jews."
    evaluation_results = run_conversation(user_input)