#yum update
#yum install vim wget 
#vim /etc/ssh/sshd_config
#set PasswordAuthentication yes
#systemctl restart sshd.service
#ssh-keygen
#ssh-copy-id -i /home/ansible/.ssh/id_rsa.pub localhost
#ssh localhost
#sudo wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
#sudo rpm -Uvh epel-release-latest-7.noarch.rpm
#sudo yum groupinstall -y 'development tools'
#sudo yum install python-pip python-devel -y 
#sudo pip install setuptools --upgrade
#sudo pip install --upgrade pip
#sudo pip install ansible
#ansible --version
#sudo pip install boto
#sudo pip install boto3

#set access key id and secret access 

#export AWS_ACCESS_KEY_ID=''
#export AWS_SECRET_ACCESS_KEY=''
#export ANSIBLE_HOST_KEY_CHECKING=False


or 

#sudo pip install awscli 
#aws configure
provide access key id and secret access key

#cd /home/ansible/.aws
#ls -la 
#cat configure
#cat credentials


#mkdir -p /opt/aws
#cp /etc/ansible/ansible.cfg /opt/aws/
#vi /home/ansible/ansible.cfg
inventory = hosts

#vi /home/ansible/hosts
[local]
localhost

#create playbook to launch ec2 instance 
#vi /home/ansible/ec2.yml
---
- hosts: localhost
  name: Launching aws ec2 instance
  gather_facts: false
  tasks:
  - name: Launching ec2 instance with ec2 module
    ec2:
      instance_type: t2.micro
      image: ami-009110a2bf8d7dd0a
      key_name: control_key
      region: ap-south-1
    
#ansible-playbook -i hosts ec2.yml

#Download ec2.py and ec2.ini file for dynamic inventory

#cd /etc/ansible

#wget https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/ec2.py

#wget https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/ec2.ini

#export ANSIBLE_HOSTS=/etc/ansible/ec2.py
#export EC2_INI_PATH=/etc/ansible/ec2.ini


#copy key file .pem to ~/.ssh
#cd ~/.ssh
#eval 'ssh-agent -s'
or
#eval "$(ssh-agent)"
#ssh-add ~/.ssh/control_key.pem
#ssh-add -l

#./ec2.py --list 

#ansible -i ec2.py -u ubuntu tag_prod_web -m ping 
#ansible -i ec2.py -u ubuntu tag_prod_web -m command -a 'hostname' 


#Reference video
https://www.youtube.com/watch?v=9z67s1t8UgM