from fastapi import APIRouter

router = APIRouter()

@router.get("/about")
def about():

    return {
        "name": "Prashant Andoriya",
        "email": "prashantandoriya@gmail.com",
        "my_features": {
            "Note Version History":
            "Stores previous note versions whenever a note is updated."
        }
    }