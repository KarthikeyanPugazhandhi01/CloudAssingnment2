from google.cloud import storage
import requests
import gzip
import json


# Set the GCS bucket and local JSON key file location
bucket_name = 'mycloudassingnment2dcu1'
json_key_file_path = '/home/princekarthi/Assingnment2JsonKey.json'

# Authenticate with GCS using the downloaded JSON key file
storage_client = storage.Client.from_service_account_json(json_key_file_path)

# Set the GCS bucket
bucket = storage_client.get_bucket(bucket_name)

# Set the URL for the files
base_url = 'https://datasets.imdbws.com/'  # Replace with your actual URL
file_names = [
    'name.basics.tsv.gz',
    'title.akas.tsv.gz',
    'title.basics.tsv.gz',
    'title.episode.tsv.gz',
    'title.principals.tsv.gz',
    'title.ratings.tsv.gz',
    'title.crew.tsv.gz',
]

# Download, unzip, and upload each file
for file_name in file_names:
    file_url = base_url + file_name

    # Download the gzipped file
    response = requests.get(file_url)
    gzipped_data = response.content

    # Unzip the file
    unzipped_data = gzip.decompress(gzipped_data)

    # Upload the unzipped file to GCS
    blob = bucket.blob(file_name[:-3])  # Remove the '.gz' extension for the destination file
    blob.upload_from_string(unzipped_data)

    print(f'File {file_name[:-3]} uploaded to GCS bucket {bucket_name}.')

print('All files uploaded successfully.')
