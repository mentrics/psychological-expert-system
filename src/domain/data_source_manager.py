from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime
import logging
from pathlib import Path

from ..config.data_sources import (
    DataSource,
    SourceType,
    ALL_SOURCES,
    SOURCES_BY_ID,
    SOURCES_BY_TYPE,
    SOURCES_BY_SPECIALIZATION,
    SOURCES_BY_APPROACH,
)


class DataSourceManager:
    """Manages data sources and RAG implementation for psychological experts."""

    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def get_sources_by_specialization(self, specialization: str) -> List[DataSource]:
        """Get all data sources for a specific specialization."""
        return SOURCES_BY_SPECIALIZATION.get(specialization, [])

    def get_sources_by_approach(self, approach: str) -> List[DataSource]:
        """Get all data sources for a specific therapeutic approach."""
        return SOURCES_BY_APPROACH.get(approach, [])

    def get_sources_by_type(self, source_type: SourceType) -> List[DataSource]:
        """Get all data sources of a specific type."""
        return SOURCES_BY_TYPE.get(source_type, [])

    def get_source_by_id(self, source_id: str) -> Optional[DataSource]:
        """Get a specific data source by ID."""
        return SOURCES_BY_ID.get(source_id)

    def get_relevant_sources(
        self,
        specializations: List[str],
        approaches: List[str],
        min_reliability: float = 0.8,
    ) -> List[DataSource]:
        """Get relevant data sources based on specializations and approaches."""
        relevant_sources = set()
        
        # Add sources for each specialization
        for spec in specializations:
            relevant_sources.update(self.get_sources_by_specialization(spec))
        
        # Add sources for each approach
        for approach in approaches:
            relevant_sources.update(self.get_sources_by_approach(approach))
        
        # Filter by reliability score
        return [
            source for source in relevant_sources
            if source.reliability_score >= min_reliability and source.is_active
        ]

    def get_source_content(
        self,
        source_id: str,
        query: Optional[str] = None,
        max_results: int = 10,
    ) -> List[Dict]:
        """Get content from a specific data source."""
        source = self.get_source_by_id(source_id)
        if not source:
            raise ValueError(f"Source {source_id} not found")
        
        # Check cache first
        cache_file = self.cache_dir / f"{source_id}.json"
        if cache_file.exists():
            with open(cache_file) as f:
                cached_data = json.load(f)
                if self._is_cache_valid(cached_data, source):
                    return self._filter_cached_content(cached_data, query, max_results)
        
        # TODO: Implement actual data source fetching
        # This would involve:
        # 1. Authenticating with the source if required
        # 2. Fetching the content
        # 3. Processing and storing in cache
        # 4. Returning filtered results
        
        return []

    def update_source_cache(self, source_id: str) -> bool:
        """Update the cache for a specific data source."""
        source = self.get_source_by_id(source_id)
        if not source:
            raise ValueError(f"Source {source_id} not found")
        
        # TODO: Implement cache update logic
        # This would involve:
        # 1. Fetching fresh data from the source
        # 2. Processing and storing in cache
        # 3. Updating metadata
        
        return True

    def _is_cache_valid(self, cached_data: Dict, source: DataSource) -> bool:
        """Check if cached data is still valid."""
        if not cached_data.get("metadata", {}).get("last_updated"):
            return False
        
        last_updated = datetime.fromisoformat(
            cached_data["metadata"]["last_updated"]
        )
        cache_duration = source.access.cache_duration or 86400  # Default 24 hours
        
        return (datetime.now() - last_updated).total_seconds() < cache_duration

    def _filter_cached_content(
        self,
        cached_data: Dict,
        query: Optional[str],
        max_results: int,
    ) -> List[Dict]:
        """Filter cached content based on query and max results."""
        content = cached_data.get("content", [])
        
        if query:
            # TODO: Implement semantic search filtering
            # This would involve:
            # 1. Converting query to embeddings
            # 2. Comparing with content embeddings
            # 3. Ranking results by relevance
            pass
        
        return content[:max_results]

    def get_source_statistics(self) -> Dict:
        """Get statistics about available data sources."""
        return {
            "total_sources": len(ALL_SOURCES),
            "sources_by_type": {
                source_type.value: len(sources)
                for source_type, sources in SOURCES_BY_TYPE.items()
            },
            "sources_by_specialization": {
                spec: len(sources)
                for spec, sources in SOURCES_BY_SPECIALIZATION.items()
            },
            "sources_by_approach": {
                approach: len(sources)
                for approach, sources in SOURCES_BY_APPROACH.items()
            },
            "reliability_distribution": self._get_reliability_distribution(),
        }

    def _get_reliability_distribution(self) -> Dict[str, int]:
        """Get distribution of reliability scores."""
        distribution = {
            "0.9-1.0": 0,
            "0.8-0.9": 0,
            "0.7-0.8": 0,
            "0.6-0.7": 0,
            "0.5-0.6": 0,
            "0.0-0.5": 0,
        }
        
        for source in ALL_SOURCES:
            score = source.reliability_score
            if score >= 0.9:
                distribution["0.9-1.0"] += 1
            elif score >= 0.8:
                distribution["0.8-0.9"] += 1
            elif score >= 0.7:
                distribution["0.7-0.8"] += 1
            elif score >= 0.6:
                distribution["0.6-0.7"] += 1
            elif score >= 0.5:
                distribution["0.5-0.6"] += 1
            else:
                distribution["0.0-0.5"] += 1
        
        return distribution 