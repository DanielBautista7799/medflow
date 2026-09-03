import asyncio
import boto3
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import ServiceReport

BUCKET_NAME = "medflow-service-reports-2478"
SERVICE_REPORTS_PREFIX = "service-reports/"

#partition splits into 
#bucket name
#/
#service-reports/work-order-001.txt (which is key)
#exxtracts the file in s3 bucket
def extract_s3_key(file_url: str) -> str:
    without_scheme = file_url.removeprefix("s3://")
    _, _, key = without_scheme.partition("/")
    return key




# connection to the bucket, go into service-reports, loop through the files, and save their paths in keys
def list_s3_keys(bucket_name: str, prefix: str) -> set[str]:
    s3_client = boto3.client("s3")
    paginator = s3_client.get_paginator("list_objects_v2")

    keys: set[str] = set()

    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.add(obj["Key"])

    return keys

#fetch all service reports from db return them
async def fetch_service_reports() -> list[ServiceReport]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ServiceReport))
        return list(result.scalars().all())
    


    
# Get all S3 files and service reports (bucket vs db), then compare them both ways to find
#  healthy(in db and s3), broken (in db not s3), and orphaned files(in s3 not db)
async def main() -> None:
    s3_keys = list_s3_keys(BUCKET_NAME, SERVICE_REPORTS_PREFIX)
    reports = await fetch_service_reports()

    healthy: list[ServiceReport] = []
    broken: list[ServiceReport] = []
    referenced_keys: set[str] = set()

    for report in reports:
        key = extract_s3_key(report.file_url)
        referenced_keys.add(key)

        if key in s3_keys:
            healthy.append(report)
        else:
            broken.append(report)
    orphaned_keys = s3_keys - referenced_keys
    print("== Healthy (database row + matching S3 file) ==")
    if not healthy:
        print("None found")
    for report in healthy:
        print(f"ServiceReport {report.id}: {report.file_url}")

    print("== Broken (database row, no matching S3 file) ==")
    if not broken:
        print("None found")
    for report in broken:
        print(f"ServiceReport {report.id}: {report.file_url}")

    print("== Orphaned (file in S3, but no matching database row) ==")
    if not orphaned_keys:
        print("None found")
    for key in orphaned_keys:
        print(f"s3://{BUCKET_NAME}/{key}")


if __name__ == "__main__":
    asyncio.run(main())