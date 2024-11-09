from Helpers.configs import get_settings
from abc import ABC , abstractmethod


class BaseController(ABC):
    def __init__(self):
        self.app_settings = get_settings()
    
    @abstractmethod
    def run(self):
        pass    
    