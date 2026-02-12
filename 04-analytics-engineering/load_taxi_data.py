import os
import sys
import urllib.request
import gzip
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
import time


# Change this to your bucket name
BUCKET_NAME = "de-zoomcamp-485516"
GCS_PREFIX = "taxi_rides_ny"

# If you authenticated through the GCP SDK you can comment out these two lines
CREDENTIALS_FILE = "gcs.json"
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
# If commented initialize client with the following
# client = storage.Client(project='zoomcamp-mod3-datawarehouse')

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
TAXI_TYPES = ["yellow", "green"]
YEARS = [2019, 2020]
MONTHS = [f"{i:02d}" for i in range(1, 13)]
DOWNLOAD_DIR = "data"

CHUNK_SIZE = 8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)


def get_files_to_download():
    """Generate list of (taxi_type, year, month) tuples to download."""
    files = []
    for taxi_type in TAXI_TYPES:
        for year in YEARS:
            for month in MONTHS:
                files.append((taxi_type, year, month))
    return files


def download_file(taxi_type, year, month):
    filename = f"{taxi_type}_tripdata_{year}-{month}.csv"
    csv_path = os.path.join(DOWNLOAD_DIR, filename)

    # Check if CSV already exists
    if os.path.exists(csv_path):
        print(f"File already exists, skipping download: {csv_path}")
        return csv_path

    gz_filename = f"{filename}.gz"
    url = f"{BASE_URL}/{taxi_type}/{gz_filename}"
    gz_path = os.path.join(DOWNLOAD_DIR, gz_filename)

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, gz_path)
        print(f"Downloaded: {gz_path}")

        # Extract the .gz file
        try:
            with gzip.open(gz_path, 'rb') as f_in:
                with open(csv_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"Extracted: {csv_path}")
            # Remove the .gz file after extraction
            os.remove(gz_path)
            return csv_path
        except Exception as e:
            print(f"Failed to extract {gz_path}: {e}")
            return None
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def create_bucket(bucket_name):
    try:
        # Get bucket details
        bucket = client.get_bucket(bucket_name)

        # Check if the bucket belongs to the current project
        project_bucket_ids = [bckt.id for bckt in client.list_buckets()]
        if bucket_name in project_bucket_ids:
            print(
                f"Bucket '{bucket_name}' exists and belongs to your project. Proceeding..."
            )
        else:
            print(
                f"A bucket with the name '{bucket_name}' already exists, but it does not belong to your project."
            )
            sys.exit(1)

    except NotFound:
        # If the bucket doesn't exist, create it
        bucket = client.create_bucket(bucket_name)
        print(f"Created bucket '{bucket_name}'")
    except Forbidden:
        # If the request is forbidden, it means the bucket exists but you don't have access to see details
        print(
            f"A bucket with the name '{bucket_name}' exists, but it is not accessible. Bucket name is taken. Please try a different bucket name."
        )
        sys.exit(1)


def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, max_retries=3):
    filename = os.path.basename(file_path)
    blob_name = f"{GCS_PREFIX}/{filename}"

    # Check if already uploaded
    if verify_gcs_upload(blob_name):
        print(f"File already in GCS, skipping upload: {filename}")
        return

    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to gs://{BUCKET_NAME}/{blob_name} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {filename}")
                return
            else:
                print(f"Verification failed for {filename}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)

    files_to_process = get_files_to_download()
    print(f"Total files to download and process: {len(files_to_process)}")

    # Download and extract files in parallel
    csv_files = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(download_file, taxi_type, year, month): (taxi_type, year, month)
            for taxi_type, year, month in files_to_process
        }
        for future in as_completed(futures):
            taxi_type, year, month = futures[future]
            try:
                result = future.result()
                if result:
                    csv_files.append(result)
            except Exception as e:
                print(f"Error processing {taxi_type} {year}-{month}: {e}")

    print(f"\nSuccessfully downloaded and extracted {len(csv_files)} files")

    # Upload CSV files to GCS in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(upload_to_gcs, file_path) for file_path in csv_files]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error during upload: {e}")

    print("\nAll files processed and uploaded to GCS.")
