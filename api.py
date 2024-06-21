import json
from fastapi import FastAPI, File, UploadFile
import boto3
from ocr import extract_text_from_pdf
import uuid
import os

from openai import OpenAI
client = OpenAI()


app = FastAPI()

llm = OpenAI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Connect to your S3 bucket
    s3_client = boto3.client(
        's3',
        region_name='us-east-1'
    )
    pdf_uuid = f'{uuid.uuid4().__str__()}.pdf'
    # Save the file to S3 bucket
    s3_client.upload_fileobj(file.file, 'pdf-grupob', pdf_uuid)

    # Extract text from the uploaded PDF file
    extracted_text = extract_text_from_pdf(pdf_uuid)
    result = ""
    try:
        our_query = f"Clasifica los datos de acuerdo a los siguientes items Nombre, Contacto (Teléfono y Correo Electrónico), Perfil Profesional, Experiencia Laboral, Educación, Habilidades Técnicas y Blandas, Certificaciones. Si no tiene alguno de los items mencionados indicar 'No aplica' {extracted_text}"
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": our_query}
            ]
        )
        print(type(response.choices[0].message.content))
        result = json.loads(response.choices[0].message.content)
    except Exception as e:
        print(e)
        result = extracted_text

    return result
