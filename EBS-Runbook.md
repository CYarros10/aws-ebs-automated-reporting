# EBS Runbook

Summarized instructions for various EBS tasks.

## Table of Contents

1. How to Replace an Entire EC2 Instance [Console]
2. How to Replace an EBS Volume on an EC2 Instance [Console]
3. Frequently Asked Questions
4. Additional Resources
5. AWS CLI Examples

## How to Replace an Entire EC2 Instance [Console]

### Stop the EC2 Instance

1. Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/
2. From the navigation bar, select the region that your EC2 instance is located  in
3. In the navigation pane, select Instances
4. Select the EC2 instance you want to replace
5. Select the Actions dropdown
6. Select Instance State -> Stop Instance
7. Wait for EC2 instance state to equal "stopped"

### Detach the existing EBS volume(s) and create snapshot

8. In the description tab, scroll down to see Block Devices
9. Click the Block devices link
10. Click the EBS ID (ex: vol-xxxxxxxxxxxxxxxxx)
11. In the EBS Volumes page, select Actions dropdown
12. Select Detach Volume and confirm.
13. Create snapshot by selecting Actions -> Create Snapshot


### Terminate existing EC2 instance

14. In the navigation pane, select instances.
15. select Actions dropdown -> Instance State -> Terminate

### Spin up new EC2 instance and stop it

16. Select Launch Instance and follow prompts to create new EC2 instance of the desired type (must be same architecture)
17. Wait until the new EC2 instance is successfully running

### Detach and delete the auto-generated ebs volume

18. Select the newly created EC2 Instance
19. Select Actions -> Instance State -> Stop
20. Follow steps 8-13 to detach the new EBS volume
21. Delete the new EBS volume

### Attach original EBS volume and restart instance

22. Select Volumes in navigation pane if not already there
23. Select Actions -> Attach Volume
24. Provide EC2 instance ID of the new EC2 instance created in step 15.

### Restart the new EC2 instance and re-assign elastic IP if appropriate

25. Select Instances in navigation pane
26. Select the stopped EC2 Instance
27. Select Actions -> Instance State -> Start

## How to Replace an EBS Volume on an EC2 Instance

### Stop the EC2 Instance

1. Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/
2. From the navigation bar, select the region that your EC2 instance is located  in
3. In the navigation pane, select Instances
4. Select the EC2 instance you want to replace
5. Select the Actions dropdown
6. Select Instance State -> Stop Instance
7. Wait for EC2 instance state to equal "stopped"

### Detach the existing EBS volume(s)

8. In the description tab, scroll down to see Block Devices
9. Click the Block devices link
10. Click the EBS ID (ex: vol-xxxxxxxxxxxxxxxxx)
11. In the EBS Volumes page, select Actions dropdown
12. Select Detach Volume and confirm.
13. Take a snapshot of the existing EBS volume (if desired)

### Attach new EBS Volume to EC2 instance

14. Select Volumes in navigation pane if not already there
15. Select Actions -> Attach Volume
16. Provide EC2 instance ID of the existing EC2 instance.

### Restart the new EC2 instance and re-assign elastic IP if appropriate

17. Select Instances in navigation pane
18. Select the stopped EC2 Instance
19. Select Actions -> Instance State -> Start

## Frequently Asked Questions

### How do I determine if an EBS Volume failed?  What errors/alerts are received

**To view status checks in the console:**

1. Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/.

2. In the navigation pane, choose Volumes. The Volume Status column displays the operational status of each volume.

3. To view the status details of a volume, select the volume and choose Status Checks.

[Reference: Monitoring the Status of Your Volumes](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-volume-status.html#monitoring-vol-events)

**Alerts after failed EBS Volume**

Cloudwatch Events can be utilized to keep track of EBS.

[Reference: EBS Volume Events](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-cloud-watch-events.html)


### How do I locate the volume or volumes that have failed and the associated instance

1. Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/.

2. In the navigation pane, choose Volumes. The Volume Status column displays the operational status of each volume.

3. To get a list of failed EBS Volumes filter by tags and attributes in search bar:

* Volume Status -> Impaired
* Volume Status -> Warning
* Volume Status -> Insufficient Data

### How do I locate the snapshot(s) for the failed volume(s)/instance

1. Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/
2. In the navigation pane, choose Snapshots. You can edit the table contents by clicking the gear in the top right
3. Add column Volume to see the Volume ID for each snapshot
4. Alternatively, use the search bar to search by Volume ID or Tag

## Additional Resources

[EBS Volumes Documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumes.html)

[EBS Snapshots Documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)

## AWS CLI Examples

### Create EC2 Instance example

```bash
aws ec2 run-instances --image-id ami-1a2b3c4d --count 1 --instance-type c3.large --key-name MyKeyPair --security-groups MySecurityGroup
```

[Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/run-instances.html)

### Stop Instance example

```bash
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
```

[Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/stop-instances.html)

### Delete EC2 Instance example

```bash
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

[Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/terminate-instances.html)

### Detach Volume example

```bash
aws ec2 detach-volume --volume-id vol-1234567890abcdef0
```

[Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/detach-volume.html)

### Create Snapshot example

```bash
aws ec2 create-snapshot --volume-id vol-1234567890abcdef0 --description "This is my root volume snapshot"
```

[Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/create-snapshot.html)

### Attach EBS Volume to EC2 Instance example

```bash
aws ec2 attach-volume --volume-id vol-1234567890abcdef0 --instance-id i-01474ef662b89480 --device /dev/sdf
```

[Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/attach-volume.html)
