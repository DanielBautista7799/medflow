import asyncio
import boto3

from app.database import AsyncSessionLocal
from app.models import ServiceReport

BUCKET_NAME = "medflow-service-reports-2478"
LOCAL_FILE_PATH = "scripts/sample_service_report.txt"
S3_KEY = "service-reports/work-order-001.txt"

def upload_to_s3() -> str:
    s3_client = boto3.client("s3")
    s3_client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, S3_KEY)
    return f"s3://{BUCKET_NAME}/{S3_KEY}"

async def record_service_report(file_url: str) -> None:
    async with AsyncSessionLocal() as session:
        report = ServiceReport(
            work_order_id=1,
            file_url=file_url,
            notes="Uploaded via the Day 8 boto3 demo script.",
        )

        session.add(report)
        await session.commit()
        await session.refresh(report)
        print(
            f"Created ServiceReport id={report.id}, "
            f"file_url={report.file_url}"
        )



async def main() -> None:
    file_url = upload_to_s3()
    print(f"Uploaded to {file_url}")
    await record_service_report(file_url)


if __name__ == "__main__":
    asyncio.run(main())