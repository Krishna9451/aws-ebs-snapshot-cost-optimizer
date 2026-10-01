import boto3
import os
from datetime import datetime, timezone, timedelta


ec2 = boto3.client("ec2")

RETENTION_DAYS = int(os.environ.get("RETENTION_DAYS", "30"))
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() == "true"


def lambda_handler(event, context):

    cutoff_date = (
        datetime.now(timezone.utc)
        - timedelta(days=RETENTION_DAYS)
    )

    print(f"Retention period: {RETENTION_DAYS} days")
    print(f"Cutoff date: {cutoff_date}")
    print(f"Dry run: {DRY_RUN}")

    deleted_count = 0
    skipped_count = 0

    paginator = ec2.get_paginator("describe_snapshots")

    for page in paginator.paginate(OwnerIds=["self"]):

        for snapshot in page["Snapshots"]:

            snapshot_id = snapshot["SnapshotId"]
            start_time = snapshot["StartTime"]

            if start_time < cutoff_date:

                if DRY_RUN:

                    print(
                        f"[DRY RUN] Snapshot {snapshot_id} "
                        f"is older than {RETENTION_DAYS} days."
                    )

                else:

                    try:
                        ec2.delete_snapshot(
                            SnapshotId=snapshot_id
                        )

                        deleted_count += 1

                        print(
                            f"Deleted snapshot {snapshot_id} "
                            f"because it is older than "
                            f"{RETENTION_DAYS} days."
                        )

                    except Exception as error:

                        print(
                            f"Failed to delete {snapshot_id}: "
                            f"{error}"
                        )

            else:

                skipped_count += 1

                print(
                    f"Keeping snapshot {snapshot_id}; "
                    f"it is within the retention period."
                )

    print(f"Deleted snapshots: {deleted_count}")
    print(f"Snapshots kept: {skipped_count}")

    return {
        "statusCode": 200,
        "retention_days": RETENTION_DAYS,
        "deleted_snapshots": deleted_count,
        "snapshots_kept": skipped_count
    }
