import time
import boto3
import json
import os
import uuid
from urllib.request import urlopen

LOCALSTACK_ENDPOINT = 'http://localhost.localstack.cloud:4566'
AWS_REGION = "us-east-1"

transcribe_client = boto3.client("transcribe", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)
s3_client = boto3.client("s3", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)


def transcribe_file(job_name, file_uri):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat="wav",
        LanguageCode="en-US",
    )

    job = ''
    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]
        if job_status in ["COMPLETED", "FAILED"]:
            print(f"Job {job_name} is {job_status}.")
            if job_status == "COMPLETED":
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}."
                )
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)
    return job.get('TranscriptionJob').get('Transcript').get('TranscriptFileUri')


def lambda_handler(event, context):
    bucket_name = 'inputtranscribebucket'
    s3_client.upload_file('./audio_files/example-call.wav', bucket_name, 'example-call.wav')

    file_uri = f"s3://{bucket_name}/example-call.wav"

    transcribe_file_uri = transcribe_file(f'transcribeJob-{uuid.uuid4()}', file_uri)

    json_response = json.loads(urlopen(transcribe_file_uri).read().decode())
    print(json_response)

    transcript = json_response.get('results').get('transcripts')[0].get('transcript')

    return {
        'statusCode': 200,
        'body': json.dumps(transcript)
    }

