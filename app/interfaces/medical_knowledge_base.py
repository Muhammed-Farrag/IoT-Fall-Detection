"""
Medical Knowledge Base Interface - Dependency Inversion Principle
Allows swapping RAG implementations without affecting dependent code
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IMedicalKnowledgeBase(ABC):
    """
    Abstract interface for medical query RAG system.
    Implementations can use different RAG backends (OpenAI, local LLM, etc.)
    """
    
    @abstractmethod
    def query(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Query the medical knowledge base using RAG.
        
        Args:
            question: User's medical question
            context: Optional context (user health data, history, etc.)
            
        Returns:
            Dictionary with answer, sources, and confidence
        """
        pass
    
    @abstractmethod
    def verify_response(self, response: str) -> Dict[str, Any]:
        """
        Verify the medical accuracy of a response.
        
        Args:
            response: The response to verify
            
        Returns:
            Dictionary with verification status and reliability score
        """
        pass
    
    @abstractmethod
    def get_sources(self, query_id: str) -> List[Dict[str, Any]]:
        """
        Get source documents used for a specific query.
        
        Args:
            query_id: Identifier for the query
            
        Returns:
            List of source documents with citations
        """
        pass
    
    @abstractmethod
    def add_disclaimer(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add medical disclaimer to the response.
        
        Args:
            response: The response to augment
            
        Returns:
            Response with disclaimer added
        """
        pass

