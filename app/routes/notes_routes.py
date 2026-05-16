from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from app.schemas import (
    NoteCreate,
    NoteUpdate,
    NoteResponse
)

from app.models import (
    Note,
    SharedNote,
    NoteHistory,
    User
)

from app.dependencies import (
    get_db,
    get_current_user
)

router = APIRouter()

@router.get(
    "/notes",
    response_model=list[NoteResponse]
)
def get_notes(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    shared_note_ids = db.query(
        SharedNote.note_id
    ).filter(
        SharedNote.shared_with_user_id == current_user.id
    )

    notes = db.query(Note).filter(
        or_(
            Note.owner_id == current_user.id,
            Note.id.in_(shared_note_ids)
        )
    ).offset(offset).limit(limit).all()

    return notes


@router.get(
    "/search",
    response_model=list[NoteResponse]
)
def search_notes(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    shared_note_ids = db.query(
        SharedNote.note_id
    ).filter(
        SharedNote.shared_with_user_id == current_user.id
    )

    notes = db.query(Note).filter(
        or_(
            Note.owner_id == current_user.id,
            Note.id.in_(shared_note_ids)
        ),
        or_(
            Note.title.ilike(f"%{q}%"),
            Note.content.ilike(f"%{q}%")
        )
    ).all()

    return notes


# GET SINGLE NOTE
@router.get(
    "/notes/{id}",
    response_model=NoteResponse
)
def get_note(
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

    return note


# CREATE NOTE
@router.post(
    "/notes",
    status_code=201,
    response_model=NoteResponse
)
def create_note(
    data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Validation
    if not data.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    if not data.content.strip():
        raise HTTPException(
            status_code=400,
            detail="Content cannot be empty"
        )

    note = Note(
        title=data.title,
        content=data.content,
        owner_id=current_user.id
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


# UPDATE NOTE
@router.put(
    "/notes/{id}",
    response_model=NoteResponse
)
def update_note(
    id: int,
    data: NoteUpdate,
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

    # Only owner can update
    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    # Save previous version
    history = NoteHistory(
        note_id=note.id,
        old_title=note.title,
        old_content=note.content
    )

    db.add(history)

    # Partial updates
    if data.title is not None:

        if not data.title.strip():
            raise HTTPException(
                status_code=400,
                detail="Title cannot be empty"
            )

        note.title = data.title

    if data.content is not None:

        if not data.content.strip():
            raise HTTPException(
                status_code=400,
                detail="Content cannot be empty"
            )

        note.content = data.content

    note.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(note)

    return note


# DELETE NOTE
@router.delete(
    "/notes/{id}",
    status_code=204
)
def delete_note(
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

    # Only owner can delete
    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    # Delete related shared notes
    db.query(SharedNote).filter(
        SharedNote.note_id == id
    ).delete()

    # Delete note history
    db.query(NoteHistory).filter(
        NoteHistory.note_id == id
    ).delete()

    # Delete actual note
    db.delete(note)

    db.commit()

    return Response(status_code=204)