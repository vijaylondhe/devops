Chef is designed in ruby launguage

chef infra server
chef infra client 

Requirement:
1) Chefdk (Development Kit) on workstation
2) Chef starting kit (zip file) on workstation at any location
    - starter kit helps workstation to connect chef server by using private key file located inside starter kit (chef-starter\chef-repo\.chef\xxx.pem)
    - knife.rb file for chef server address

bootstrap: A bootstrap installs Chef Infra Client on a target system so that it can run as a client and communicate with Chef Infra Server.
(only while bootstraping chef server initiate connection with nodes)

Unattended bootstrap:

Tools:

knife: command line tool, using knife command to bootstrap the node, required credentials of node to bootstrap

#knife subcommand options 
#knife node list 
#knife bootstrap 
chef generate: creating cookbooks

after installing chefdk and downloading starter kit run this command in powershell

#knife --version
Chef Infra Client: 15.1.36

Use > RefreshEnv.cmd to refresh shell in windows 

#knife node list 

go to path where starter kit is located 
> cd D:\QT_Devops\ChefZone\chef-starter\chef-repo

#knife node list

#knife bootstrap "public_ip_or_hostname" --sudo -i "key_file.pem" -x 'ubuntu' -N 'private_dns_of_instance'

#knife node list

Check chef webconsole to see nodes added to chef server

#Delete nodes using knife

#knife delete --help
#knife node delete 'private_dns_name_of_instance'

when next time you bootstrap same node, it will just match the keys because agent is already installed






