"""
Additional API endpoints for the RAG chatbot backend.
These endpoints provide advanced querying capabilities for the Physical AI & Humanoid Robotics book.
"""
from fastapi import HTTPException, Query, APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import openai
import logging
import os
from dotenv import load_dotenv
import asyncio

# Import the qdrant_client from the main module
from main import qdrant_client, logger

# Create a router for advanced endpoints
router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    filters: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    execution_time: float

class SearchRequest(BaseModel):
    text: str
    page_filter: Optional[str] = None
    top_k: Optional[int] = 5

class SearchResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]

# Advanced search endpoint
@router.post("/api/search", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest):
    """
    Search for content in the book using semantic similarity.
    This endpoint allows more specific searches with optional page filtering.
    """
    start_time = asyncio.get_event_loop().time()

    try:
        # Generate embedding for the search query using the main module function
        from main import create_embedding
        query_embedding = await create_embedding(request.text)

        # Prepare filters if provided
        from qdrant_client.http import models
        filters = None
        if request.page_filter:
            filters = models.Filter(
                must=[
                    models.FieldCondition(
                        key="page",
                        match=models.MatchValue(value=request.page_filter)
                    )
                ]
            )

        # Search in Qdrant with filters
        search_results = qdrant_client.search(
            collection_name="book_content",
            query_vector=query_embedding,
            query_filter=filters,
            limit=request.top_k
        )

        # Format results
        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "content": result.payload["content"],
                "title": result.payload.get("title", ""),
                "url": result.payload.get("url", ""),
                "page": result.payload.get("page", ""),
                "relevance_score": result.score
            })

        execution_time = asyncio.get_event_loop().time() - start_time

        logger.info(f"Search for '{request.text}' returned {len(results)} results in {execution_time:.3f}s")

        return SearchResponse(
            query=request.text,
            results=results
        )

    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.post("/api/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Advanced query endpoint with filtering capabilities.
    Allows for more complex queries with metadata filtering.
    """
    start_time = asyncio.get_event_loop().time()

    try:
        # Generate embedding for the query using the main module function
        from main import create_embedding
        query_embedding = await create_embedding(request.query)

        # Prepare filters if provided
        from qdrant_client.http import models
        qdrant_filters = None
        if request.filters:
            must_conditions = []

            for key, value in request.filters.items():
                if isinstance(value, str):
                    must_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    )
                elif isinstance(value, list):
                    # Handle "in" queries
                    must_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchAny(any=value)
                        )
                    )

            if must_conditions:
                qdrant_filters = models.Filter(must=must_conditions)

        # Search in Qdrant with filters
        search_results = qdrant_client.search(
            collection_name="book_content",
            query_vector=query_embedding,
            query_filter=qdrant_filters,
            limit=request.top_k
        )

        # Format results
        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "content": result.payload["content"],
                "title": result.payload.get("title", ""),
                "url": result.payload.get("url", ""),
                "page": result.payload.get("page", ""),
                "relevance_score": result.score
            })

        execution_time = asyncio.get_event_loop().time() - start_time

        logger.info(f"Advanced query for '{request.query}' returned {len(results)} results in {execution_time:.3f}s")

        return QueryResponse(
            query=request.query,
            results=results,
            execution_time=execution_time
        )

    except Exception as e:
        logger.error(f"Error in advanced query endpoint: {e}")
        raise HTTPException(status_code=500, detail="Query failed")


@router.get("/api/pages")
async def list_pages():
    """
    Get a list of all pages/sections in the book that have been indexed.
    """
    try:
        from qdrant_client.http import models
        # Use scroll to get all points and extract unique pages
        offset = None
        all_pages = set()

        while True:
            records, next_offset = qdrant_client.scroll(
                collection_name="book_content",
                limit=1000,
                offset=offset,
                with_payload=True
            )

            for record in records:
                page = record.payload.get("page")
                if page:
                    all_pages.add(page)

            if next_offset is None:
                break
            offset = next_offset

        return {"pages": sorted(list(all_pages))}

    except Exception as e:
        logger.error(f"Error listing pages: {e}")
        raise HTTPException(status_code=500, detail="Failed to list pages")


@router.get("/api/stats")
async def get_stats():
    """
    Get statistics about the indexed content.
    """
    try:
        collection_info = qdrant_client.get_collection("book_content")

        # Additional stats could be gathered from metadata in Neon DB if used
        stats = {
            "total_documents": collection_info.points_count,
            "vector_size": collection_info.config.params.vectors.size,
            "collection_name": "book_content"
        }

        return stats

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get stats")