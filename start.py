import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_instance_ids():
    try:
        ec2 = boto3.client('ec2')
        instances = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': [
                        'stopped',
                    ]
                },

                {
                    'Name': 'tag-key',
                    'Values': [
                        os.environ['tagKey'],
                    ]
                },

                {
                    'Name': 'tag-value',
                    'Values': [
                        'enable',
                    ]
                }
            ],
        )

        instance_ids = []
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])

        logger.info(instance_ids)
        return instance_ids
    except Exception as e:
        logger.error(e)
        raise e

def start_instances():
    try:
        ec2 = boto3.client('ec2')
        instances = get_instance_ids()
        response = ec2.start_instances(
            InstanceIds=instances
        )

        return response
    except Exception as e:
        logger.error(e)
        raise e

def handle(event, context):
    return start_instances()
