# AWS EBS Snapshot Cost Optimizer

An AWS cloud cost optimization project that automates the cleanup of
unnecessary Amazon EBS snapshots using AWS Lambda, Python, Boto3,
EC2, EBS, IAM, and CloudWatch/EventBridge.

## Project Overview

EBS snapshots are useful for backups, but unnecessary snapshots can
continue to consume storage and increase AWS costs.

This project implements automated snapshot cleanup using serverless
AWS Lambda functions.

The project contains two cleanup workflows:

1. Orphaned snapshot cleanup
2. 30-day snapshot retention cleanup

---

## Architecture

```text
                 CloudWatch / EventBridge
                         |
              +----------+----------+
              |                     |
              v                     v
      Lambda Function 1      Lambda Function 2
      Orphan Snapshot        30-Day Snapshot
         Cleanup                 Cleanup
              |                     |
              v                     v
        EC2 / EBS APIs        EBS Snapshots
              |                     |
              v                     v
       Identify orphaned      Check snapshot age
         snapshots                  |
              |                     |
              v                     v
       Delete snapshot        Delete if older
                              than 30 days
              |                     |
              +----------+----------+
                         |
                         v
                 Cost Optimization
