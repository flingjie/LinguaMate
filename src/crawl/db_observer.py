from storage import save_news
from log import logger
from  typing import List
from .data_observer import DataObserver


class DBObserver(DataObserver):
    def update(self, data: List[dict]):
        for item in data:
            try:
                logger.debug(f"Observer received: {item.to_dict()}")
                # save_news(item)
            except Exception as e:
                logger.error(e)