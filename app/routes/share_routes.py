from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models import User, Note, SharedNote
from app.schemas import ShareRequest

router = APIRouter()


@router.post("/notes/{id}/share")
def share_note(
    id: int,
    data: ShareRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find note
    note = db.query(Note).filter(
        Note.id == id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to share this note"
        )

    # Find target user
    target_user = db.query(User).filter(
        User.email == data.share_with_email
    ).first()

    if not target_user:
        raise HTTPException(
            status_code=404,
            detail="User with this email does not exist"
        )

    # Prevent sharing with self
    if target_user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot share note with yourself"
        )

    # Check already shared
    existing_share = db.query(SharedNote).filter(
        SharedNote.note_id == note.id,
        SharedNote.shared_with_user_id == target_user.id
    ).first()

    if existing_share:
        raise HTTPException(
            status_code=400,
            detail="Note already shared with this user"
        )

    # Create share entry
    shared_note = SharedNote(
        note_id=note.id,
        shared_with_user_id=target_user.id
    )

    db.add(shared_note)
    db.commit()

    return {
        "message": f"Note shared with {target_user.email}"
    }