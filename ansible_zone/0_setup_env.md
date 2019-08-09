sudo yum update -y 
sudo yum install wget 
sudo vi /etc/ssh/sshd_config

PasswordAuthentication yes

sudo systemctl restart sshd.service
ssh-keygen
ssh-copy-id -i ~/.ssh/id_rsa.pub localhost
sudo wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo rpm -Uvh epel-release-latest-7.noarch.rpm
sudo yum groupinstall -y 'development tools'
sudo yum -y install python-pip python-devel
sudo pip install setuptools --upgrade
pip install --upgrade pip       -->19.2.1 pip version 
sudo pip install ansible 
sudo ansible --version
sudo pip install boto
sudo pip install boto3
sudo pip install awscli --upgrade --user

aws configure



#python version upgradation:
https://linuxhint.com/install_python3_centos7/


vi ~/.boto

aws_access_key_id = 
aws_secret_access_key = 

mkdir -p /opt/aws
cd /opt/aws

vi hosts
[local]
localhost

