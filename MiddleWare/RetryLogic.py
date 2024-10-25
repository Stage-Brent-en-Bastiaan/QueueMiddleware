import random
from Settings import Settings


class RetryLogic:
    def __init__(self, exponentiality: float) -> None:
        settingsfactory = Settings()
        self.baseDelay = settingsfactory.basicRetryDelay
        self.maxRetries = settingsfactory.maxRetries
        self.maxDelay = 8640000 * 2
        self.exponentiality = exponentiality

    def exponential_backoff(self, retries: int):
        delay = min(self.baseDelay * (self.exponentiality**retries), self.maxDelay)
        return delay
