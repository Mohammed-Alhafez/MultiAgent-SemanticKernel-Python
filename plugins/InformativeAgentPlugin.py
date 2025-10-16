"""
Informative Agent Plugin

This plugin provides access to company knowledge base through Azure Cognitive Search.
It performs hybrid semantic search combining keyword search, vector search, and
semantic answers to provide relevant company information, policies, and guidelines.

Author: MultiAgent-SemanticKernel-Python
"""

import os
from semantic_kernel.functions import kernel_function
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding
from azure.search.documents.models import VectorizableTextQuery, QueryType


class InformativeAgentPlugin:
    """
    Plugin for searching company knowledge base using Azure Cognitive Search.
    
    This plugin provides hybrid semantic search capabilities that combine
    keyword search, vector search, and semantic answers to find relevant
    company information, policies, and guidelines.
    """
    
    def __init__(self):
        """
        Initialize the Azure Search client and embedding service.
        
        Loads configuration from environment variables and sets up
        connections to Azure Cognitive Search and OpenAI embedding service.
        """
        # Load Azure Search configuration
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX")
        self.api_key = os.getenv("AZURE_SEARCH_API_KEY")
        
        try:
            # Initialize Azure Search client
            self.search_client = SearchClient(
                endpoint=self.endpoint,
                index_name=self.index_name,
                credential=AzureKeyCredential(self.api_key)
            )
            self.initialized = True
        except Exception as e:
            print(f"Warning: Failed to initialize Azure Search client: {e}")
            self.initialized = False

    async def _get_embedding(self, text: str) -> list[float]:
        """
        Generate text embedding using Azure OpenAI.
        
        Args:
            text: Input text to generate embedding for
            
        Returns:
            list[float]: Vector embedding of the input text
        """
        embedding_service = AzureTextEmbedding(
            deployment_name="text-embedding-3-small",
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-12-01-preview"
        )
        response = await embedding_service.generate_embeddings([text])
        return response[0]

    @kernel_function(
        name="hybrid_search_knowledge_base",
        description="Performs hybrid semantic search (keyword + vector + captions + answers) on company knowledge base"
    )
    async def hybrid_search_knowledge_base(self, query: str) -> str:
        """
        Perform hybrid semantic search on the company knowledge base.
        
        This function combines keyword search, vector search, and semantic answers
        to find the most relevant information from the company knowledge base.
        
        Args:
            query: Search query string
            
        Returns:
            str: Relevant information from the knowledge base or error message
        """
        # Check if Azure Search is properly initialized
        if not self.initialized:
            return "Azure Search client not initialized. Please check your configuration."

        try:
            # Generate embedding for vector search
            query_vector = await self._get_embedding(query)
            vector_query = VectorizableTextQuery(
                text=query,
                fields="text_vector",
                k_nearest_neighbors=3,
                exhaustive=True
            )
            
            # Perform hybrid search with semantic configuration
            results = self.search_client.search(
                search_text=query,
                vector_queries=[vector_query],
                query_type=QueryType.SEMANTIC,
                semantic_configuration_name="rag-1756823952605-semantic-configuration",
                query_caption="extractive",
                query_answer="extractive",
                query_answer_count=3,
                top=3,
                include_total_count=True,
                select=["parent_id", "chunk_id", "chunk"]
            )

            # Try to use semantic answers first (most relevant)
            semantic_answers = results.get_answers() if hasattr(results, "get_answers") else []
            if semantic_answers:
                for answer in semantic_answers:
                    if answer.highlights:
                        return answer.highlights
                    elif answer.text:
                        return answer.text

            # Fallback to captions or chunks from search results
            for result in results:
                captions = result.get("@search.captions", [])
                if captions and isinstance(captions, list) and len(captions) > 0:
                    caption = captions[0]
                    if hasattr(caption, "highlights") and caption.highlights:
                        return caption.highlights
                    elif hasattr(caption, "text"):
                        return caption.text
                        
                # Final fallback to chunk field
                if result.get("chunk"):
                    return result["chunk"]

            return "No relevant information found in the knowledge base."

        except Exception as e:
            return f"Error during hybrid search: {str(e)}"


