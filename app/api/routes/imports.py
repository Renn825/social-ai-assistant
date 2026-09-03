from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.imports import ImportRequest, ImportResult
from app.services.local_import import import_local_files

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("", response_model=ImportResult)
def import_data(
    request: ImportRequest,
    session: Session = Depends(get_session),
) -> ImportResult:
    inserted_posts, skipped_posts, imported_comments, skipped_comments = import_local_files(
        session, request.posts_file, request.comments_file
    )
    return ImportResult(
        imported_posts=inserted_posts,
        skipped_posts=skipped_posts,
        imported_comments=imported_comments,
        skipped_comments=skipped_comments,
    )
