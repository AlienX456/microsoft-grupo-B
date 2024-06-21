import boto3
import time
from textract import run_get_kv_map

def extract_text_from_pdf(file_name):
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

    return run_get_kv_map(response['Blocks'])
