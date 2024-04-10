from loggers.log_manager import get_logger
import logging
from polygon import RESTClient
from polygon.rest.models import PreviousCloseAgg


def get_previous_close(symbol) -> float:
    client = RESTClient()
    responses = client.get_previous_close_agg(symbol)
    logging.info(f"The response for {symbol} is \n{responses}")
    price = 0.00
    for response in responses:
        if isinstance(response, PreviousCloseAgg):
            price = response.close
            break
    return price
