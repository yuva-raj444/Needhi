"""
NyayaSahaya — Complaint draft generation + PDF download endpoints.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import io

from app.models.schemas import ComplaintRequest, ComplaintResponse
from app.services.complaint_service import ComplaintService
from app.services.pdf_service import PDFService

router = APIRouter()


@router.post("/draft", response_model=ComplaintResponse)
async def generate_complaint_draft(request: ComplaintRequest):
    """
    Generate a formal legal complaint draft from user-provided details.
    Returns the draft text; use /complaint/pdf for downloadable PDF.
    """
    try:
        service = ComplaintService()
        result = await service.generate_complaint(
            complainant_name=request.complainant_name,
            complainant_address=request.complainant_address,
            opponent_name=request.opponent_name,
            issue_description=request.issue_description,
            location=request.location,
            date=request.date,
            language=request.language or "en",
        )
        return ComplaintResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Complaint generation error: {str(e)}")


@router.post("/pdf")
async def generate_complaint_pdf(request: ComplaintRequest):
    """
    Generate a formal legal complaint as a downloadable PDF.
    """
    try:
        # First generate the complaint text
        complaint_service = ComplaintService()
        result = await complaint_service.generate_complaint(
            complainant_name=request.complainant_name,
            complainant_address=request.complainant_address,
            opponent_name=request.opponent_name,
            issue_description=request.issue_description,
            location=request.location,
            date=request.date,
            language=request.language or "en",
        )

        # Then convert to PDF
        pdf_service = PDFService()
        pdf_bytes = pdf_service.generate_complaint_pdf(
            draft_text=result["draft_text"],
            language=result["language"],
        )

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=complaint_{request.complainant_name.replace(' ', '_')}.pdf"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {str(e)}")
