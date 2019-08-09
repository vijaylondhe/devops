import boto3
import json
import pprint
def get_hosts(ec2,fv):
    f={'Name':'tag:Server','Values':[fv]}
    hosts=[]
    for each_in in ec2.instances.filter(Filters=[f]):
        #print each_in.private_ip_address
        hosts.append(each_in.private_ip_address)
    return hosts

def main():
    ec2=boto3.resource("ec2")
    db_group=get_hosts(ec2,"db")
    app_group=get_hosts(ec2,"app")
#    print "db: ",db_group
#    print "app: ",app_group

    all_groups={
        'db':{
            'hosts':db_group,
            'vars':{
                'group_name': 'Database_group'
            }
        },
        'app':{
            'hosts': app_group,
            'vars':{
                'group_name': 'application group'
            }
        }
    }
    print json.dumps(all_groups)

if __name__="__main__":
    main()

