import boto3
import os
import time
from textract import run_get_kv_map

def extract_text_from_pdf(file_path):
    # Create a Textract client
    textract_client = boto3.client('textract',
            region_name='us-east-1',
    )


    # Call Textract to extract text from the PDF
    response = textract_client.start_document_analysis(
        DocumentLocation={'S3Object': {'Bucket': 'pdf-grupob', 'Name': file_name}},
        FeatureTypes=['FORMS']
    )

    # Get the JobId from the response
    job_id = response['JobId']
    print(f'Started Textract job with JobId: {job_id}')

    # Get the results of the Textract job
    response = textract_client.get_document_analysis(JobId=job_id)
    status = response['JobStatus']
    print(f'Pending Textract job with JobId: {response}')

    while status == 'IN_PROGRESS':
        response = textract_client.get_document_analysis(JobId=job_id)
        status = response['JobStatus']
        time.sleep(1)

    print(f'Finished Textract job with JobId: {response}')
    # Extract the text from the response
    extracted_text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text += item['Text'] + '\n'

    run_get_kv_map(response['Blocks'])

    

# Path to the folder containing the PDFs
folder_path = '/Users/erome12/Documents/GitHub/grupo-b-ocr/pdfs'

# Create an S3 client
s3_client = boto3.client(
    's3',
    region_name='us-east-1'
)

# Iterate over the PDF files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.pdf'):
        file_path = os.path.join(folder_path, file_name)

        # Upload the PDF file to the S3 bucket
        s3_client.upload_file(file_path, 'pdf-grupob', file_name)

        # Generate the S3 URL for the uploaded file
        s3_url = f'https://s3.amazonaws.com/pdf-grupob/{file_name}'

        # Extract text from the uploaded PDF file
        extracted_text = extract_text_from_pdf(s3_url)
        print(f'Text extracted from {file_name}:\n{extracted_text}\n')