import boto3
import os
import json
import datetime,dateutil
from dateutil.relativedelta import relativedelta


#environment variables
targetArn = str(os.environ['SNS_TARGETARN'])
tagKey = "tag:"+str(os.environ['TAG_KEY'])
tagValue = str(os.environ['TAG_VALUE'])
remoteRegion = str(os.environ['REMOTE_REGION'])

print("Arn:", targetArn)
print("TagKey:", tagKey)
print("TagValue:", tagValue)
print("Region:", remoteRegion)

#Describe your regions here
region_list = [remoteRegion]
ec2_client = boto3.client('ec2')
sns_client = boto3.client('sns')

# Send alert to sns topic
def send_sns_alert(message):

    curr_date = datetime.datetime.now().strftime("%m/%d/%Y")
    subject = "EBS Backup Report: "+ str(curr_date)

    # Publish a simple message to the specified SNS topic
    sns_client.publish(
        TargetArn=targetArn,
        Message=str(message),
        Subject=str(subject)
    )

def lambda_handler(event, context):
    total_instances = 0
    tagged_instances = 0
    tagged_instances_without_recent_backups = 0
    ec2_volumes_report = []
    response = ec2_client.describe_snapshots(OwnerIds=["self"])
    snapshot_list=response['Snapshots']

    #Iterate over regions
    for region in region_list:
        print("\n"+"#"*60+"  "+region+"  "+"#"*60+"\n")
        client = boto3.client('ec2', region_name=region)

        paginator = ec2.get_paginator('describe_instances')
        print(paginator)

        response_all_instances = client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running', 'stopped']
                }
            ])
        for r in response_all_instances['Reservations']:
            total_instances = len(r['Instances'])
            print("Total number of instances:", total_instances)

        # list of tagged instances
        response_tagged_instances = client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running', 'stopped']
                },
                {
                    'Name':tagKey, 'Values': [tagValue]
                }
            ])

	    # Iterate over instance(s)
        print("iterating over ec2 instances...")
        for r in response_tagged_instances['Reservations']:
            tagged_instances = len(r['Instances'])
            print("Number of Instances tagged for backup:", tagged_instances)

            print("-----------------------------------------")

            for inst in r['Instances']:

                inst_id=inst['InstanceId']
                inst_tags = inst['Tags']
                inst_name = ""
                for tag in inst_tags:
                    if tag['Key'] == "Name":
                        inst_name = tag['Value']


                print("#### Beginning report for instance:", inst_id)

                volumes=inst['BlockDeviceMappings']
                volume_temp=[]

                #Iterate over instance's volume(s)
                for volume in volumes:
                    volume=volume['Ebs']['VolumeId']
                    volume_temp.append(volume)

                    print("# Number of Volumes:", len(volume_temp))

                    print("# Instance's volumes: ",volume_temp)


                    #Find the volumes in snapshots
                    for volume in volume_temp:
                        found = False
                        snapshot_status = ""
                        snapshot_state = ""
                        snapshot_progress = ""
                        snapshot_starttime = ""

                        for snapshot in snapshot_list:
                            snapshot_volume=snapshot['VolumeId']

                            #Check if volume in snapshot, if so check the date
                            if volume == snapshot_volume:
                                found = True

                                print("# Found snapshot for volume.")

                                snapshot_date=snapshot['StartTime']
                                curr_time = dateutil.parser.parse(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                snapshot_starttime = dateutil.parser.parse(datetime.date.strftime(snapshot_date,'%Y-%m-%d %H:%M:%S'))
                                date_diff = relativedelta(curr_time, snapshot_starttime)

                                snapshot_state = snapshot['State']
                                snapshot_progress = snapshot['Progress']


                                if (date_diff.days < 0):
                                    print("# snapshot older than 24 hours.")

                                # Snapshot is recent.
                                if date_diff.hours > -3:
                                    print("# snapshot is recent.")
                                    snapshot_status = "recent"

                                else:
                                    print("# snapshot is not within last  3 hour.")
                                    snapshot_status = "expired"
                                    tagged_instances_without_recent_backups = tagged_instances_without_recent_backups + 1


                        if (not found):
                            print('# a snapshot was not found for volume')
                            snapshot_state = ""
                            snapshot_progress = ""
                            snapshot_starttime = ""
                            snapshot_status = "missing"
                            tagged_instances_without_recent_backups = tagged_instances_without_recent_backups + 1

                        # add to report.
                        ec2_volumes_report.append(
                            {
                                "EC2InstanceName": inst_name,
                                "EC2InstanceID": inst_id,
                                "SnapshotVolumeID" : snapshot_volume,
                                "Status": snapshot_status,
                                "State": snapshot_state,
                                "Progress": snapshot_progress,
                                "StartTime": str(snapshot_starttime),
                                "ReportTime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                        )


    formmatted_ec2_volumes_report = json.dumps(json.loads(str(ec2_volumes_report).replace("\'", "\"")), indent=4, sort_keys=False)

    report = (
             'Total Number of Instances: '+str(total_instances)+'\n'
             'Total Number of Tagged Instances: '+str(tagged_instances)+'\n'
             'Total Number of Tagged Instances Without Backups: '+str(tagged_instances_without_recent_backups)+'\n'
             '\n'
             'Data:'+str(formmatted_ec2_volumes_report))

    print('---------------------------------------------------- \n')
    print(report)
    send_sns_alert(report)

    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }
