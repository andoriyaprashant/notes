from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models import User, Note, NoteHistory, SharedNote

router = APIRouter()


@router.get("/notes/{id}/history")
def get_note_history(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    shared_access = db.query(SharedNote).filter(
        SharedNote.note_id == id,
        SharedNote.shared_with_user_id == current_user.id
    ).first()

    if (
        note.owner_id != current_user.id
        and not shared_access
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    history = db.query(NoteHistory).filter(
        NoteHistory.note_id == id
    ).all()

    return history