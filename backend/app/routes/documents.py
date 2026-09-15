import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from app.config import (
    DOCUMENTS_PATH
)

from app.rag.ingest import (
    ingest_pdf
)


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


# Make sure documents folder exists
os.makedirs(
    DOCUMENTS_PATH,
    exist_ok=True
)


# =========================================================
# UPLOAD PDF
# =========================================================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )


    # Only PDF
    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )


    # Prevent path traversal
    safe_filename = os.path.basename(
        file.filename
    )


    file_path = os.path.join(
        DOCUMENTS_PATH,
        safe_filename
    )


    try:

        # Save PDF
        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        print(
            f"Saved PDF: {file_path}"
        )


        # Process PDF
        result = ingest_pdf(
            file_path
        )


        return {
            "success": True,
            "message": (
                "Document uploaded "
                "and indexed successfully."
            ),
            "data": result
        }


    except Exception as e:

        print(
            f"Document processing error: {e}"
        )


        raise HTTPException(
            status_code=500,
            detail=str(e)
        )