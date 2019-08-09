####Chapter 1: Introduction to Ansible

#Connection Plugin:
-	Native SSH		--> default connection for ansible
-	local	--> for localhost without SSH connection
-	Paramiko SSH	--> for older versions of redhat RHEL5
-	Winrm 	--> for windows hosts
-	Docker Connection		--> for docker installed hosts

#Group hosts:
/etc/ansible/hosts file 

[datacenter1]
web1.example.com
web2.example.com

[datacenter2]
web3.example.com
web4.example.com

[datacenter3:children]
datacenter1
datacenter2


#Host patterns:

ansible web1.example.com -i /etc/ansible/hosts --list-hosts
ansible datacenter1 -i /etc/ansible/hosts --list-hosts
ansible web1.example.com, datacenter2 -i /etc/ansible/hosts --list-hosts
ansible all -i /etc/ansible/hosts --list-hosts
ansible '*' -i /etc/ansible/hosts --list-hosts

#Advanced host patterns
ansible 'datacenter1:datacenter2' -i etc/ansible/hosts -list-hosts			--> removed duplicate hosts from groups
ansible 'datacenter1:&datacenter2' -i /etc/ansible/hosts --list-hosts	-->  shows only duplicate hosts
ansible 'datacenter1:!web1.example.com' -i /etc/ansible/hosts --list-hosts	--> exclude web1 from list 
ansible 'all:!web2.example.com' -i /etc/ansible/hosts --list-hosts	--> all excluding web2 host

**************************************************************************************


###Chapter 2: Deploying Ansible 

#Install Ansible on control node 
sudo yum installed python
sudo yum install ansible -y
ssh servera.lab.example.com
exit

mkdir /home/student/dep-install/
vi /home/student/dep-install/inventory
[dev]
servera.lab.example.com

ansible dev -i /home/student/dep-install/inventory --list-hosts

#Configuration file and Precedence

/etc/ansible/ansible.cfg		--> default file when installed ansible   *3 

~/.ansible.cfg	-->	inside users home directory         *2 

./ansible.cfg	--> in existing directory from where ansible command executes   *1 

enviroment variable:
$ansible_config 

To identify which config file used 
ansible -version
ansible datacenter1 --list-hosts -v 

grep "^\[" /etc/ansible/ansible.cfg
[defaults]
[priviledge_escalation]
[paramiko_connection]
[ssh_connection]
[accelerate]
[selinux]
[galaxy]


#some common settings in ansible configuration file 

[defaults]
inventory = /etc/ansible/hosts
remote_user = root

[priviledge_escalation]
become = True 
become_method = sudo
become_user = root
become_ask_pass = False

export ANSIBLE_CONFIG=/home/student/dep-config/inventory
ansible datacenter1 --list-hosts

#Running Ad-Hoc Commands:
Format:

ansible host-pattern -m module_name [-a arguments] -i inventory_path 

ansible datacenter1 -m command -a /usr/bin/hostname -o 

-o: display output in single line

#command and shell module 

ansible -m command -a set		--> commands are not executed from shell enviroment
ansible -m shell -a set					--> use shell module to invoke commands from shell enviroment

#remote_user = root 
by default from the user ad hoc command executed same user will connect to managed hosts if not defined in config file

Previledge escation is not enabled by default
become = True 						-->	--become, -b 
become_method = sudo	-->	--become-method
become_user = root				-->	--become-user
become_ask_pass = False	-->	--ask-become-pass, -K 

remote_user	--> -u
inventory  		--> -i 

ansible localhost -m command -a 'id' 
ansible localhost -m command -a 'id' -u devops 


local user: student 
remote user: devops 

ansible localhost -m command -a 'cat /etc/motd' -u devops 
ansible localhost -m command -a 'content="Managed by Ansible\n" dest=/etc/motd' -u devops 

it will be failed due to insufficient priviledge
ansible localhost -m command -a 'content="Managed by Ansible\n" dest=/etc/motd' -u devops --become --become_user root

In this ansible make SSH connection with "devops" user but performs operation using "root" user

**Copy Module
ansible web1.example.com -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd' -u devops --become --become-user root

#Dynamic Inventory:
If inventory file is executable it is treated as dynamic inventory

./inventoryscript --list
./inventoryscript --host demoserver

Can write in any programming language but must return JSON syntax 
If multiple inventory file exists, they are examined with alphabetical orders.

#YAML Basics:
-	Identations using space
-	YAML forbids tab 
-	Start with --- end with ...
-	For multi line strings use | or  >

	include_newlines:	|
		Example Company
		123 Main street
		Atlanta, GA 30333
		
	fold_newlines:	>
		This is 
		a very long,
		long, long, long
		sentence.
		
-	Dictionary
	---	
		{name: autmation using ansible, code: do407}
-	Lists
	---
		-	red
		-	green
		-	blue
	
	---
	fruits:
		[red, green, blue]

#Verifying YAML syntax: 
1) Read the playbook using python to check syntax errors 

python -c 'import yaml, sys; print yaml.load(sys.stdin)' < main.yml 

2) Online YAML syntax varification: http://yamllint.com/

3) use ansible-playbook playbook_name.yml --syntax-check 

#Implementing Modules
Core: by Ansible 
Extras:	by community
Custom:	by end user

Core and extras modules are always available but for custom module ansible looks into 

$ANSIBLE_LIBRARY enviroment  or library = /usr/share/my_modules parameter in ansible configuration file 

or ./library directory relative to the location of playbook being used

Module location on RHEL7 systems:
/usr/lib/python2.7/site-packages/ansible/modules

core and extras modules stored under separate directory

Module documentation available at doc.ansible.com or see using command line on control node 

$ansible-doc -l		--> list all modules
$ansible-doc yum		--> see documentation for yum module
$ansible-doc service 	--> see documentation for service module 
$ansible-doc -s yum 	--> -s or snippest for how to use module 

---
-	hosts:	all	
	tasks:
		-	name: install http packages
			yum:
				name:	httpd
				state:		latest
				
Using command line 

ansible localhost -m yum -a "name=tree state=present"
ansible localhost -m service -a "name=httpd state=restarted"
ansible localhost -m uri -a "url=http://materials.example.com/"

******************************************************************************************

###Chapter 3: Implementing Playbooks

#Implement Playbooks 
-	Sequantial order execution
-	Idempotent:		can run multiple times
-	Name Attribute:
	-	name:  description for play
-	Host Attribute:
	hosts:  web1.example.com
- 	User Attribute:
	remote_user:	devops
	become: 	yes
	become_method:	sudo
	become_user: root
-	Task Attribute:
	tasks:
		-	name: install httpd
			yum:
				name:	httpd
				state:	latest

-	avoid using modules like shell, command, raw as they are not idempotent

#Block

---
-	hosts:	all
	name:	block example
	tasks:
	-	block:
		-	name: install httpd
			yum:
				name:	httpd
				state: latest
	-	block:
		-	name: start service
			service:
				name:	httpd
				state:	started

To check syntax of playbook
#ansible-playbook example.yml --syntax-check

To execute as a Dry Run (it does not do actaul changes)
#ansible-playbook -C example.yml 

Step by Step execution of playbook:
#ansible-playbook --step example.yml

it asks for each steps (y/n)

#Module: firewalld
- name: install firewalld 
  yum: 
   name: firewalld
   state: latest
- name: all rule for ftp service
  firewalld:
    service: ftp
    permenant: true
    state: enabled 
    immediate: yes

#Module uri
- name: test webpage of http
  uri:
   url: http://web1.example.com/index.html
   status_code: 200

#mariadb-server using yum
- name: install mariadb package
  yum:
   name: mariadb-server
   state: latest
- name: start mariadb service
  service:
   name: mariadb
   state: started 

#Module get_url
Downloads files from HTTP, HTTPS, or FTP to the remote server

- name: download file from remote server
  get_url:
   url: http://workstation.example.com/resources/index.html
   dest: /var/www/html/index.html
   mode: 0644


***********************************************************************************************
####Chapter 4: Managing variables, facts and Inclusions 

#Variable Scope:
Global Scope: from command line or from configuration file 
Play Scope: inside playbook
Host Scope: inside inventory file 

Scope       Priority
inventory   3
playbook    2
commandline 1

e.g
#variables in playbook

---
- hosts: all
  name: install apache webserver and start service
  vars:
    web_pkg: httpd
    firewall_pkg: firewalld
    web_service: httpd
    firewall_service: firewalld
    python_pkg: python-httplib2
    rule: http
  tasks:
    - name: install "{{ web_pkg }}" package
      yum:
       name: {{ web_pkg }}
       state: latest 
    - name: start "{{ web_service }}" service
      service:
       name: {{ web_service }}
       state: started  
    - name: install other packages
      yum:
       name:
        - "{{ python_pkg }}"
        - "{{ firewalld_pkg }}"
       state: latest


#it is also possible to define var_files and include in playbooks

- name: include variables using files
  var_files:
    - vars/users.yml

users.yml file look like 

user: vijay
location: mumbai
hometown: baramati

#host and group variables in inventory files

[servers]
web1.example.com ansible_user=vijay
web2.example.com 

[servers:vars]
ansible_user=londhe

#note: host varibale takes precedence over group varibale but playbook variables takes
# precednce over both

#using group_vars and host_vars directories: this is prefered approach 
#create directories  in same place where inventory file exists

group_vars/datacenter
host_vars/web1.example.com

#variables and arrays
users:
  bjones:
    first_name: vijay
    last_name: londhe
    location: mumbai
  cjones:
    first_name: xyz
    last_name: abc
    location: 123

access varibles:
 users.bjones.first_name
 users.cjones.location

 users['bjones']['first_name']
 users['cjones']['location']


#Register variables: to capture output and store inside variable than can used later
---
- hosts: all
  name: use case of register varibale
  tasks:
   - name: install package
     yum:
      name: httpd
      state: installed
     register: install_result
   - debug: var=install_result


#e.g
inventory file 
[datacenter]
web1.example.com

[datcenter:vars]
package=httpd

[dbservers]
web1.example.com

group_vars/dbservers
package=mariadb-server

Playbook file:
---
- hosts: all
  tasks:
   - name: install the "{{ package }}" package
     yum:
      name: {{ package }}
      state: latest 

host_vars/web1.example.com
package=screen

ansible-playbook example.yml
ansible-playbook -e 'package=elinks' example.yml

#result: host variable takes precedence over group varibles defined inside group_vars directory
#variables passing from command line has highest precedence using -e option for ansible command


#Managing Facts:
#setup module
This are variables automcatically discovred by ansible from managed host
facts are pulled using setup module
facts can be used in playbooks to accomplish tasks based on certain conditions 

#ansible web1.example.com -m setup 

e.g
{{ ansible_hostname }}
{{ ansible_default_ipv4.address }}
{{ ansible_kernel }}
{{ ansible_os_family }}

---
- hosts: all
  tasks:
   - name: Print variable ansible fact
     debug:
      msg: >
        The default ipv4 address of server is {{ ansible_default_ipv4.address }}
        and hostname of server is {{ ansible_hostname }}


#Facts using filter

#ansible web1.example.com -m setup -a 'filter=ansible_eth0'

#Custom Facts:
administrator can create custom facts and push to managed hosts
once created they can read by setup module 

used for:
- defining perticular value for system based on custom script
- defining value based on program execution

#custom fact found by ansible if fact file saved inside /etc/ansible/facts.d directory
#and files must be .fact extension and must be created on managed host
#custom fact file can be in INI or JSON format

[packages]
web_package=httpd
db_package=mariadb-server

[users]
user1=vijay
user2=londhe

#result is returned in ansible_local variable

#ansible web1.example.com -m setup -a 'filter=ansible_local'

use and acess custom facts in playbook

---
- hosts: all
  tasks:
   - name: install packages
     yum:
      name: 
       - "{{ ansible_local.custom.packages.web_package }}"
       - "{{ ansible_local.custom.packages.db_package }}"

#Managing Inclusions (tasks and variables)
#include variables and tasks from different file in playbooks

tasks:
 - name: include task to install db-server
   include: tasks/db_server.yml

tasks:
 - name: include variable files
   include_vars: vars/variable.yml

#Note: prior to ansible version 2.4 only "include" are available for both playbook and tasks
#changes from version 2.4 are "import_playbook" and "include_tasks"

#Difference between import and include

#import: statements are pre processed at the time of playbook parsed
#include: statements are processed as they encountered during execution of playbook

- import_playbook: webservers.yml
- import_playbook: databases.yml

tasks:
- import_tasks: common_tasks.yml
# or
- include_tasks: common_tasks.yml

#include_vars
e.g
variables.yml file 

---
packages:
    web_package: httpd
    db_package: mariadb-server

main.yml file 

---
- hosts: all
  tasks:
   - name: include variables for tasks
     include_vars: variables.yml
   - name: install web package 
     yum:
      name: "{{ packages.web_package }}"
      state: latest


#access variables from file
packages['web_package']
packages['db_package']

#Priority of variables:
#1.command line variables using -e argument
#2.variables defined in playbook using vars, include_vars 
#3.variables defined in inventory file --> host varibles, group varibales or host_vars
#   group_vars directory 

*********************************************************************************************

#### Chapter 5: Implementing Task Control 

#Implement loops in playbook
#Construct Conditionals in playbooks
#Combine loops and Conditionals

#Implement loops in playbook
1. Simple loops

- name: install packges
  yum:
   name: "{{ item }}"
   state: latest
  with_items:
    - httpd
    - mariadb-server

#or 

---
- hosts: all
  vars:
   mail_services:
   - postfix
   - dovecot
  tasks:
  - name: install packages
    yum: 
     name: "{{ item }}"
     state: latest
    with_items: "{{ mail_Services }}"

2. Nested loops
#with_nested

#ansible loops
with_files
with_fileglob
with_sequence
with_random_choices


#Construct Conditionals in playbooks:

Conditional operators: <, >, =, !=, ==, <=, >=
    
#ansible "when" statement
e.g. 

---
- hosts: all
  tasks:
  - name: install package
    apt:
     name: mariadb-server
     state: installed 
    when: ansible_facts['ansible_os_family'] == "Debian"


#multiple conditions inside when statement

---
- hosts: all
  tasks:
  - name: install package
    package:
     name: mariadb-server
     state: installed 
    when: ansible_facts['ansible_os_family'] == "Debian" or  ansible_facts['ansible_os_family'] == "Redhat" 

#Implementing Handlers:
#handlers are tasks that respond to a notification triggered by other tasks
#each handler name must be unique and defined at end of block
#handler tasks are inactive only executed when invoked using "notify" statement
#ansible notifies handlers only if the task acquires the changed status 
#Handlers always run in the order in which defined in handlers section not in order of notify
e.g

---
- hosts: all
  tasks:
  - name: install package
    yum:
     name: httpd
     state: latest
    notify:
     - start apache
  handlers:
  - name: start apache
    service:
     name: httpd
     state: started

#As of Ansible 2.2, handlers can also “listen” to generic topics, and tasks can notify those topics as follows:

handlers:
    - name: restart memcached
      service:
        name: memcached
        state: restarted
      listen: "restart web services"
    - name: restart apache
      service:
        name: apache
        state: restarted
      listen: "restart web services"

tasks:
    - name: restart everything
      command: echo "this task will restart the web services"
      notify: "restart web services"


# Implementing Tags:
#tags are used to run subset of tasks from playbook  using --tag option in command
#we can use --skip-tag option to skip specific tasks from playbook

e.g
---
- hosts: all
  tasks:
  - name: install packages
    yum:
     name: httpd
     state: latest
    tags: production
  - name: install maria-db 
    yum:
     name: mariadb-server
     state: latest

or 

tasks:
- yum:
    name: "{{ item }}"
    state: present
  loop:
  - httpd
  - memcached
  tags:
  - packages

- template:
    src: templates/src.j2
    dest: /etc/foo.conf
  tags:
  - configuration

#ansible-playbook main.yml --tags 'production'
#ansible-playbook main.yml --skip-tags 'production'

#Special tags:
#:always : This tag causes the task to always be executed even if --skip-tags option used 

#Three special tags that can be used from command line with --tags option 
#tagged: run only tagged tasks from playbook 
#untagged: run only untagged tasks from playbook
#all: defalt option which runs all tasks from playbook


# Handling Errors:
#normally when task failed ansible stops execution of further tasks 
#sometime admin requires to countinue tasks even if some tasks are failed 


#use "ignore_errors" statement to exclude failure and countinue play execution

e.g.
---
- hosts: all
  tasks:
  - name: install package
    yum:
     name: nopkg
     state: latest
    ignore_errors: yes 

#use "force_handlers" this forces the handlers to be called even if tasks fails 

e.g.
---
- hosts: all
  force_handlers: yes 
  tasks:
  - name: install package
    yum:
     name: no_pkg
     state: latest
    notify:
    - restart_database
  handlers:
    - name: restart_database
      service:
       name: mariadb
       state: restarted 


#override the failed state:
#if task is executed successful yet adminstrator want to mark task as failed based on specific criteria using "failed_when" condition at end of task

tasks:
 - shell:
    cmd: /usr/local/bin/create_users.sh
   register: command_result
   failed_when: "'Password missing' in command_result.stdout"

#override the changed state:
#if task does not perform any change, handlers are skipped, administrator can override this default behaviour using "changed_when" statement

tasks:
 - shell:
    cmd: /usr/local/bin/upgrade_database.sh
   register: command_result
   changed_when: "'Sucess' in command_result.stdout"
   notify:
    - restart_database


# ansible blocks and error handling 

# block: Defines the main tasks to run
# rescue: Define the task that will run if task defined in "block" is failed 
# always: Define the task that will always run even if success and failure of block and rescue

- name: Attempt and graceful roll back demo
  block:
    - debug:
        msg: 'I execute normally'
    - name: i force a failure
      command: /bin/false
    - debug:
        msg: 'I never execute, due to the above task failing, :-('
  rescue:
    - debug:
        msg: 'I caught an error'
    - name: i force a failure in middle of recovery! >:-)
      command: /bin/false
    - debug:
        msg: 'I also never execute :-('
  always:
    - debug:
        msg: "This always executes"

********************************************************************************************

#### Chapter 6: Implementing Jinja2 templates

#Modify files before they are distributed to managed hosts
#Three feature of Jinja2 templates: Varible filters/Loops/Conditionals
#Two delimeters allowed in jinja2: {{..}} for variables and  {%..%} for expressions

#Using template module to place jinja2 templates to managed hosts

vi /tmp/j2-template.j2

Welcome to {{ ansible_hostname }}
Today's date is: {{ ansible_date_time.date }}

vi /tmp/main.yml
---
- hosts: all
  tasks:
  - name: place on remote machine using jinja2 template
    template:
     src: /tmp/j2-template.j2
     dest: /tmp/dest-config-file.txt

**********************************************************************************************

#### Chapter 7: Implementing Roles

#Used to organise playbook into separate, smaller playbooks and files 
#Roles provides ansible with a way to load tasks, handlers, and variables from external files
#Top level directory defines name of roles itself

#user.example
#   defaults                            --> default values of roles variables
#       -   main.yml
#   files                               --> directory contains static files used by role
#       -   my_config.cfg
#       -   my_work.txt
#   handlers                            --> handlers to be invoked by tasks
#       -   main.yml
#   meta                                --> information about role,author,license,dependency
#       -   main.yml
#   README.md                           
#   tasks                               --> contains roles tasks defination
#       -   main.yml
#   templates                           --> contains jinja2 templates
#       -   motd.j2
#   tests                               --> inventory file and playbook used to test role
#       -   inventory
#       -   test.yml
#   vars                                --> contains roles variable values 
#       -   main.yml

default variables are defind in defauls/main.yml
they have low precendece over any other variables including inventory variables
we can use vars/main.yml to define other variables

Using roles inside the playbook
---
- hosts: all
  roles:
    -   role1
    -   role2


#Role Dependencies:
allow to include other roles as dependencies in playbook
dependencies are defined in meta/main.yml

---
dependencies:
  - { role: apache, port:8080 }
  - { role: postgres, dbname:serverlist, admin_user: felix }

#allow_duplicates=yes role can add dependeny to other roles

#Creating directory structure for roles
#ansible will look roles directory to find out roles in project directory
#roles can also kept in other path by using roles_path varibale in ansible config file 

e.g.

#roles
#   motd
#       -   defaults
#           -   main.yml
#       -   files
#       -   handlers
#       -   tasks
#           -   main.yml
#       -   templates
#           -   motd.j2

#vi /home/ansible/roles/motd/tasks/main.yml
---
- name: deliver motd file
  template:
   src: templates/motd.j2
   dest: /etc/motd
   owner: root
   group: root
   mode: 0644

#vi /home/ansible/roles/motd/templates/motd.j2
This is the system {{ ansible_hostname }}.
Today's date is: {{ ansible_date_time.date }}.
Only use this system with permission prior to {{ system_onwer }}


#vi /home/ansible/roles/motd/defaults/main.yml
---
system_onwer: user@web1.example.com

#Using role in playbook

#vi /home/ansible/use-motd-role.yml
---
- hosts: all
  name: use motd role in playbook
  user: devops 
  become: yes
  roles:
    - motd 

#run playbook to execute motd role 
#ansible-playbook -i inventory use-motd-role.yml

e.g.
#mkdir -p roles/myvhost/{files,handlers}
#mkdir -p roles/myvhost/{meta,tasks,templates,defaults}


#Ansible Galaxy:

#Public library for ansible roles
#ansible-galaxy command line tool can be used to search for display information about role to install,list,remove, or initialize roles 

#ansible-galaxy search 'install git' --platforms el
#ansible-galaxy info davidkarban.git
#ansible-galaxy install davidkarban.git -p roles/

The default location for installed role is in /etc/ansible/roles/
This location can be overriden by role_path in configuration file

#Install multiple roles with ansible-galaxy command using -r option

#vi roles2install.yml

#from galaxy
- src: davidkarban.git

#from webserver
- src: https://web1.example.com/roles/roleinstall.tgz
  name: ftpserver-role

#ansible-galaxy init -r role2install.yml

#ansible-galaxy list

#ansible-galaxy remove student.bash_env

#Using ansible-galaxy to create roles

#ansible-galaxy init --offline student.example


#Use pre_tasks and post_tasks statement to executes tasks before of after role is executed 

e.g.
---
- hosts: all
  tasks:
  pre_tasks:
   - debug:
      msg: 'begining of webserver configuration'
  roles:
   - myvhost
  post_tasks:
   - debug:
      msg: 'webserver configuration is completed'


*********************************************************************************************

#### Chapter 8: Optimizing Ansible

#configure connection type and enviroment in playbook
#configure delegation in playbook
#configure parallellism in ansible 


#SSH Pipelining: Enabling pipelining in Ansible reduces the number of SSH operations required to execute a module on the remote server, by executing many ansible modules without actual file transfer. This can result in a very significant performance improvement when enabled.


#To support SSH pipelining the requiretty feature must be disabled in sudoers file on managed hosts
#Pipelining is enabled by setting pipelining to true in ansible configuration file in [ssh_connection] section

#Control Persist feature of SSH 
#ControlPersist set, the master connection will remain open for the specified number of seconds after your last SSH session on that connection has exited.
#They do not have to repeatedly go through the initial SSH handshake until Control Persist timeout is reached.

#Connection Types:
# 1. Smart: this connection types check locally installed open ssh supports control persist or not, if support it uses local openssh else they use paramiko connection type. control persist default value is 60 seconds and configured in ansible configuration file 

# 2. paramiko: this is python implementation of ssh v2 protocol, this supports rhel versinos 6 or prior they do not have support for control persist feature

# 3. local: local connection runs command locally, instead of running over SSH

# 4. ssh: the ssh connection uses open ssh based connection which supports control persist feature

# 5. docker: this connection used for docker host to run commands on container using docker exec command 

# other connection types such as- chroot, libvirt_lxc, jail for free BSD, winrm and pywinrm for windows remote hosts


#Configuring connection types
in ansible configuration file "transport" key in [default] section 

#transport=smart

transport global value can be overriden by -c TRANSPORTNAME option in ad-hoc command 

[ssh_connection]
#pipelining=False
#control_path

additionallly inside inventory file we can also set the connection parameters
e.g.
[datacenter]
web1.example.com ansible_connection=local
web2.example.com ansible_connection=smart

or using command line 
#ansible-playbook main.yml --connection=local


#Setting enviroment variable in playbooks
e.g. set http_proxy for managed hosts

use enviroment: parameter 

---
- hosts: all
  tasks:
   - name: install package from internet
     get_url:
      url: http://webserver.example.com/package
      dest: /tmp/packages/
     enviroment:
      http_proxy: http://demo.lab.example.com:8080


# Configuration Delegation 
# Delegation can help by performing necessary actions for tasks on hosts other than the managed host being targeted by play in the inventory.

#some scenarios for delegation
#1. delegating task to local machine 
#2. delegating task to host outside play
#3. delegating task to host that exist in inventory
#4. delegating task to host does not exist in inventory 

#1. delegating task to local machine

delegate_to: localhost

#2. delegating task to host outside play

delegate_to: loadbalancer_host

#4. delegating task to host that does not exist in inventory

use add_host statement to add ephemeral host inside playbook

---
- hosts: localhost
  tasks:
   - name: add delegation host
     add_host: name=demo ansible_host=172.25.250.10 ansible_user=devops

   - name: echo hello
     command: echo "Hello from {{ inventory_hostname }}"
     delegate_to: demo
     register: output
    
   - debug:
      msg: "{{ output.stdout }}"

#ssh servers has "MaxStartups" option from which we can control number of concurrent ssh connection


#Configuring Parallelism

#By default ansible only fork upto 5 times, so it will run perticular task on 5 different machines at once.

#grep forks /etc/ansible/ansible.cfg

#vaules can be overriden by --forks option in command 

#Use "serial" option to reduce number of machines running in parallel
#serial value can also be specified in percentage

---
- hosts: all
  serial: 2
  tasks:
   - name: limit the number of hosts
     yum:
      name: httpd
      state: latest


#Asyncronous Tasks:

#There are some tasks which takes longer time to complete, in this case we instruct tasks to run in backgroung and can be checked later, it express using "async" option in playbook 
#"Poll" option: indicates to ansible how often to poll to check command has been completed

e.g.
---
- hosts: web1.example.com
  tasks:
   - name: download big file from web server
     get_url:
      url: http://demo.example.com/file1
      async: 3600
      poll: 10 

********************************************************************************************

#### Chapter 9: Implementing Ansible Vault

#Create, edit,rekey,encrypt,and decrypt files
#Run playbook with ansible vault

two ways to store data securely
1. use ansible vault to enrypt decrypt files
2. use thord party service like aws kms, vault by hashicorp, azure key vault 

#ansible vault uses python toolkit that uses symmetric encryption with aes256 
#default editor for vault is vim 

#ansible-vault create secret.yml
#ansible-vault create --vault-password-file=vault-pass secret.yml
#ansible-vault edit secret.yml

#ansible-vault rekey secret.yml
#ansible-vault --new-vault-password-file=test2 secret.yml

#To encrypt existing file 
#ansible-vault encrypt secret1 secret2
#ansible-vault vew secret.yml

#ansible-vault decrypt secret.yml --output=secret-decrypted.yml


***********************************************************************************************************

#AWS Provisioning with ansible 


requirement: pip, boto3, aws-cli 
module: 
#ec2
options:


instance_type: --> type of ec2 instance
wait: yes --> playbook wait until instance is provisioned 
group: --> security group name
group_id: --> security group id, for multiple group use ['','']
count: -->no.of instance required 
image: --> ami id of image 
key_name: --> key required for instance
region: --> region name in which ec2 instance to be launched



