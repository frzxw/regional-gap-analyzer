"""
Pagination utilities for list endpoints.
"""

from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters for list queries."""

    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(
        default=20, ge=1, le=100, description="Items per page (max 100)"
    )

    @property
    def skip(self) -> int:
        """Calculate number of documents to skip."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Alias for page_size."""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""

    items: List[T]
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse[T]":
        """
        Create a paginated response.

        Args:
            items: List of items for current page
            total: Total count of all items
            page: Current page number
            page_size: Items per page

        Returns:
            PaginatedResponse instance
        """
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )


class CursorPaginationParams(BaseModel):
    """Cursor-based pagination for large datasets."""

    cursor: Optional[str] = Field(
        default=None, description="Cursor for next page"
    )
    limit: int = Field(
        default=20, ge=1, le=100, description="Items to fetch"
    )


class CursorPaginatedResponse(BaseModel, Generic[T]):
    """Cursor-based paginated response."""

    items: List[T]
    next_cursor: Optional[str] = Field(
        None, description="Cursor for next page"
    )
    has_more: bool = Field(..., description="Whether there are more items")
