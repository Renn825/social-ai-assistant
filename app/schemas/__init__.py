from app.schemas.assistant import AssistantRequest, AssistantResponse
from app.schemas.comment import PostCommentRead
from app.schemas.post import CrawlPostRead, CollectRequest
from app.schemas.report import AnalysisReportRead, ReportRequest
from app.schemas.task import CrawlTaskCreate, CrawlTaskRead

__all__ = [
    "AssistantRequest",
    "AssistantResponse",
    "PostCommentRead",
    "CrawlPostRead",
    "CollectRequest",
    "AnalysisReportRead",
    "ReportRequest",
    "CrawlTaskCreate",
    "CrawlTaskRead",
]
