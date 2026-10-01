# AWS EBS Snapshot Cost Optimizer Architecture

```mermaid
flowchart TD
    A[CloudWatch / EventBridge] --> B[Orphan Snapshot Cleanup Lambda]
    A --> C[30-Day Snapshot Cleanup Lambda]

    B --> D[Amazon EC2 / EBS]
    D --> E[EC2 Instances]
    D --> F[EBS Volumes]
    D --> G[EBS Snapshots]

    E --> H{Source Volume Exists?}
    F --> H

    H -->|No| I[Delete Orphaned Snapshot]
    H -->|Yes| J[Keep / Evaluate]

    C --> G
    G --> K{Snapshot Age >= 30 Days?}

    K -->|No| L[Keep Snapshot]
    K -->|Yes| M[Delete Snapshot]

    I --> N[Reduce Unnecessary Storage Cost]
    M --> N

    P[IAM Execution Role] --> B
    P --> C
