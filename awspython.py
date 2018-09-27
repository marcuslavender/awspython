import boto3
import sys
from botocore.exceptions import ClientError




def help():

    print(" Run with a aws profile specified, along with resource, action, a d  instance id. \n"
          "'default profile is assumed if no profile specified'\n "
          "example: if my AWS credentials file contains test-environment run like: \n"
          "'python3 awspython.py (test-environment), (resource), (action), (instance id)' ")


def check_arguments():

    arguments = (len(sys.argv))
    if arguments != 5:
        help()
        sys.exit(1)

check_arguments()



boto3.setup_default_session(profile_name=sys.argv[1])






class AwsEnvironment:
    profile_name = None
    client = None


    def __init__(self, profile_name=sys.argv[1], resource=sys.argv[2] ):
        self.profile_name = profile_name
        self.client = None


    def set_profile_name(self, aws_profile):
        self.profile_name = aws_profile

    def get_profile_name(self):
        return self.profile_name

    def change_environment_session(self):
         boto3.setup_default_session(
             profile_name=input("Enter a profile name: "))

    def print_instances_in_environment(self, resource ):
            print(
                boto3.session.Session().get_available_regions(resource))

    def get_boto_client(self):
        return self.client

    def set_boto_client(self, resource):
        self.client =  boto3.client(resource)

    def get_boto_state(self):
        return self.ec2_state

    def set_boto_state(self, resource):
        self.ec2_state = boto3.client(resource)

    def check_running_instances(self):
        instances = self.get_boto_client().instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            print(instance.id, instance.instance_type)







class AwsInstance:
    action = None
    instance_id = None

    def __init__(self, Ainstance_id=sys.argv[4], Aaction=sys.argv[3]):
        self.action = Aaction
        self.instance_id = Ainstance_id

    def get_action(self):
        return self.action

    def set_action(self, action):
        self.action =  action.upper()

    def set_intance_id(self, instance_id ):
        self.instance_id = instance_id.upper()

    def get_instance_id(self):
        return self.instance_id



awsenv = AwsEnvironment()
awsenv.set_boto_client(sys.argv[2])
#awsenv.set_boto_state('ec2')


instance = AwsInstance()

#instance.set_action('on')
#instance.set_intance_id('i-0fdbebb6809409c7f')






## Connect to ec2 and test if permissions are ok

def stop_start_instance(env,ainstance):


    if instance.get_action() == 'on':
        try:
            env.get_boto_client().start_instances(InstanceIds=[ainstance.get_instance_id()], DryRun=True)

        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise



        try:
            response = env.get_boto_client().start_instances(InstanceIds=[ainstance.get_instance_id()])
            print(response)
        except ClientError as e:
            print(e)


    if instance.get_action() == 'off':
        try:
            env.get_boto_client().stop_instances(InstanceIds=[ainstance.get_instance_id()], DryRun=True)

        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        try:
            response = env.get_boto_client().stop_instances(InstanceIds=[ainstance.get_instance_id()])
            print(response)
        except ClientError as e:
            print(e)

stop_start_instance(awsenv, instance)













