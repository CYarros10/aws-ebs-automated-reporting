
# EBS Daily Report

Simplified Cloudformation templates to deploy an EBS reporting solution.

## Goal

Build infrastucture as code to perform the following tasks:

* Run report daily and confirm all instances with given tag/value <key>: <value> have snapshots in the last 24 hours.  The lifecycle policy will be configured to set tag <key>:<value> on all snapshots it creates.
* Make sure all snapshots are in a status of complete.
* Also make sure the number of snapshots for a given day match the number of ebs volumes attached to a given instance.
* Send report to SNS topic for automated emailing.
* Take IAM role for Lambda as a parameter. (IAM role must be created before deploying template)

## Set up / Getting Started

The Cloudformation Template utilizes the Serverless Application Model.

1. Download ebs-report.yml
2. Download ebs-report-lambda.py
3. Edit ebs-report.yml to specify local path of ebs-report-lambda.py (line 62)
4. Create S3 Bucket for Cloudformation staging. (or specify existing bucket in next step.)
5. Run the following command (make sure to replace s3 bucket name):

```bash
aws cloudformation package --template ebs-report.yml --s3-bucket <insert s3 bucket name here> --output-template-file packaged-template.yml
```

6. Go to [AWS Cloudformation Console](https://console.aws.amazon.com/cloudformation) and click Create Stack.
7. Select template file option
8. Upload packaged-template.yml
9. Enter parameters with desired values:

* Stack Name
* pEmailSubscriber : the email address that will receive the EBS report
* pLambdaRate : Frequency at which the Lambda function will run and generate the EBS Report (default: 1 day)
* pRemoteRegion : The region that contains the EC2 instances
* pRoleArn : The Lambda Role with permissions required to access EC2 information and push to SNS topic
* pTagKey : Tag Key that specifies EC2 instance whether to be included in the EBS report
* pTagValue : Tag Value that specifies EC2 instance whether to be included in the EBS report

10. Click Next
11. Optionally, specify tags for all resources created by this cloudformation stack.
12. Optionally, specify cloudformation IAM role. If empty, it will use permissions based on your user credentials.
13. Click Next
14. Scroll down and check the boxes for Capabilities and transforms.
15. Click Create Stack
16. View progress in Events tab.

## References / Resources

[Cloudformation Tutorial](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/GettingStarted.Walkthrough.html)

[Uploading Local Artifacts to an S3 Bucket](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-cli-package.html)

[AWS::Serverless Transform](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-aws-serverless.html)
