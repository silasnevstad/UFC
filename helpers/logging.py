import logging

def log_function_call(logger, function_name, arguments):
    log_header = f'{logger.name} - {logging.getLevelName(logging.INFO)}'
    args_pretty = "\n".join([f"{k}: {v}" for k, v in arguments.items()]) if isinstance(arguments, dict) else arguments
    
    log_msg = f"""
-------------------------------------------
Function Call: {function_name}
Arguments:
{args_pretty}
-------------------------------------------
"""
    
    logger.log(logging.INFO, log_msg.strip())