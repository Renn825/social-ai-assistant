import json

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.report import AnalysisReport
from app.schemas.report import AnalysisReportRead, ReportRequest
from app.services.report import generate_report, generate_weekly_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=list[AnalysisReportRead])
def list_reports(
    limit: int = 20,
    session: Session = Depends(get_session),
) -> list[AnalysisReport]:
    return list(
        session.exec(
            select(AnalysisReport)
            .order_by(AnalysisReport.created_at.desc())
            .limit(limit)
        ).all()
    )


@router.post("", response_model=AnalysisReportRead)
def create_report(
    request: ReportRequest,
    session: Session = Depends(get_session),
) -> AnalysisReport:
    return generate_report(session, request)


@router.post("/weekly", response_model=AnalysisReportRead)
def create_weekly_report(
    platform: str = "xiaohongshu",
    session: Session = Depends(get_session),
) -> AnalysisReport:
    return generate_weekly_report(session, platform)


@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    format: str = Query(default="markdown", pattern="^(markdown|html|json)$"),
    session: Session = Depends(get_session),
) -> Response:
    report = session.get(AnalysisReport, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="report not found")

    if format == "json":
        return Response(
            content=json.dumps({"title": report.title, "content": report.content}, ensure_ascii=False),
            media_type="application/json",
        )
    if format == "html":
        content = report.content
        media_type = "text/html"
    else:
        content = report.content
        media_type = "text/markdown"
    return Response(content=content, media_type=media_type)


@router.get("/{report_id}", response_model=AnalysisReportRead)
def get_report(
    report_id: int,
    session: Session = Depends(get_session),
) -> AnalysisReport:
    report = session.get(AnalysisReport, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="report not found")
    return report
