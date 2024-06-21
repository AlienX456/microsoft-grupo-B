from fastapi import FastAPI, File, UploadFile
import boto3
from ocr import extract_text_from_pdf
import uuid

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Connect to your S3 bucket
    s3_client = boto3.client(
        's3',
        region_name='us-east-1',
    )
    pdf_uuid = f'{uuid.uuid4().__str__()}.pdf'
    # Save the file to S3 bucket
    s3_client.upload_fileobj(file.file, 'pdf-grupob', pdf_uuid)

    # Extract text from the uploaded PDF file
    extracted_text = extract_text_from_pdf(pdf_uuid)

    return {"message": extracted_text}
