
from pydantic import BaseModel, Field, field_validator


class BatchRequest(BaseModel):
    comments: list[str] = Field(min_length=1)

    @field_validator("comments")
    @classmethod
    def validate_comments(cls, comments):
        comments = [text.strip() for text in comments]

        if any(not text for text in comments):
            raise ValueError("Les commentaires ne doivent pas être vides")

        return comments
