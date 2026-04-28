import sqlite3
import os
from datetime import datetime
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/workspaces/capstone-project/keys/healthcareapi-492922-629ebacee4bb.json"

def backup_to_gcs(
    db_path:    str = "education.db",
    bucket_name: str = "education-capstone-db",
    backup_dir: str = "backup1"  # folder inside the bucket
):
    #Create a safe local backup 
    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_path  = f"/tmp/database_{timestamp}.db"

    src = sqlite3.connect(db_path)
    dst = sqlite3.connect(local_path)
    src.backup(dst)
    dst.close()
    src.close()

    #Upload to GCS
    client     = storage.Client()
    bucket     = client.bucket(bucket_name)
    blob_name  = f"{backup_dir}/database_{timestamp}.db"
    blob       = bucket.blob(blob_name)

    blob.upload_from_filename(local_path)
    os.remove(local_path)  # clean up the temp file

    print(f"Backup uploaded to gs://{bucket_name}/{blob_name}")


if __name__ == "__main__":
    backup_to_gcs()