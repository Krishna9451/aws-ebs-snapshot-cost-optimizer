import boto3


def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all EBS snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Get all active EC2 instance IDs
    instances_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    active_instance_ids = set()

    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    # Check each snapshot
    for snapshot in response['Snapshots']:

        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        if not volume_id:
            ec2.delete_snapshot(
                SnapshotId=snapshot_id
            )

            print(
                f"Deleted EBS snapshot {snapshot_id} "
                f"as it was not attached to any volume."
            )

        else:
            try:
                volume_response = ec2.describe_volumes(
                    VolumeIds=[volume_id]
                )

                if not volume_response['Volumes'][0]['Attachments']:

                    ec2.delete_snapshot(
                        SnapshotId=snapshot_id
                    )

                    print(
                        f"Deleted EBS snapshot {snapshot_id} "
                        f"as its volume was not attached."
                    )

            except ec2.exceptions.ClientError as e:

                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':

                    ec2.delete_snapshot(
                        SnapshotId=snapshot_id
                    )

                    print(
                        f"Deleted EBS snapshot {snapshot_id} "
                        f"as its associated volume was not found."
                    )
