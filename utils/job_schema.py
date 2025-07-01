from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime

class JobPost(BaseModel):
    source: str = Field(..., description="The source site or scraper name, e.g., 'remoteok'")
    title: str
    company: str
    location: Optional[str] = None
    url: HttpUrl
    description: Optional[str] = None
    date_posted: Optional[str] = None
    date_scraped: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: List[str] = Field(default_factory=list)

    # Pipeline state tracking
    status: Optional[str] = Field(default="new", description="Pipeline status: new, reviewed, resume_done, etc.")
    match_score: Optional[float] = None
    match_summary: Optional[str] = None
    resume_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    error_message: Optional[str] = None
