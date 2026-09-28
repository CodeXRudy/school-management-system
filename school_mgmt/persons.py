"""Abstract base class shared by every kind of person in the system."""
from abc import ABC, abstractmethod


class persons(ABC):
    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass
    
    @staticmethod
    def validate_email(email):
        if "@" in email and "." in email:
            return True
        return False
