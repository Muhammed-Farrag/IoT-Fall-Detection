"""
Input Handler Interface - Open/Closed Principle
Allows new input types to be added without modifying existing code
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models import InputMode


class IInputHandler(ABC):
    """
    Abstract interface for handling multimodal input.
    New input types (e.g., Brain Interface) can be added by implementing this interface.
    """
    
    @abstractmethod
    def set_active_mode(self, mode: InputMode) -> Dict[str, Any]:
        """
        Set the active input mode.
        
        Args:
            mode: The input mode to activate
            
        Returns:
            Dictionary with status and details
        """
        pass
    
    @abstractmethod
    def get_active_mode(self) -> InputMode:
        """
        Get the currently active input mode.
        
        Returns:
            Current InputMode
        """
        pass
    
    @abstractmethod
    def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input based on the active mode.
        
        Args:
            input_data: Raw input data to process
            
        Returns:
            Processed input result
        """
        pass
    
    @abstractmethod
    def validate_mode_availability(self, mode: InputMode) -> bool:
        """
        Check if a specific input mode is available.
        
        Args:
            mode: The input mode to check
            
        Returns:
            True if available, False otherwise
        """
        pass

