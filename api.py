import json
from fastapi import FastAPI, UploadFile, UploadFile
import boto3
from ocr import extract_text_from_pdf
import uuid
import os
from typing import Annotated

from openai import OpenAI
client = OpenAI()

app = FastAPI()

llm = OpenAI()

s3_client = boto3.client(
    's3'
)

@app.post("/upload")
async def upload_file(files: list[UploadFile], use_llm: bool = True):
    # Connect to your S3 bucket
    print("use llm: ", use_llm)

    result = []
    for file in files:
        pdf_uuid = f'{uuid.uuid4().__str__()}.pdf'
        # Save the file to S3 bucket
        s3_client.upload_fileobj(file.file, 'pdf-grupob', pdf_uuid)

        # Extract text from the uploaded PDF file
        extracted_text = extract_text_from_pdf(pdf_uuid)
        print("extracted_text: ", extracted_text)
        try:
            if use_llm:
                print("started llm")
                our_query = f"Clasifica los datos de acuerdo a los siguientes items Nombre, Contacto (Teléfono y Correo Electrónico), Perfil Profesional, Experiencia Laboral (Empresa, Cargo, Periodo de Trabajo, Descripción de Responsabilidades), Educación (Grado Académico, Institución, Periodo de Estudio), Habilidades Técnicas y Blandas, Certificaciones. Si no tiene alguno de los items mencionados indicar 'No aplica' {extracted_text}"
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                        {"role": "user", "content": our_query}
                    ]
                )
                print(type(response.choices[0].message.content))
                result.append(json.loads(response.choices[0].message.content))
            else:
                result.append(extracted_text)
        except Exception as e:
            print(e)
            result.append(extracted_text)
    return result
