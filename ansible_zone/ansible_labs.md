# Chapter 1: Introduction to Ansible 

#1. Ansible architecture, pre-requisite, inventory files, connection plugins
#2. ansible command line tool and host patterns

# Chapter 2: Deploying Ansible

#1. Install ansible on control node and connect with managed hosts
#2. Create configuration files and check precedence of configuration file
#3. Configuration file sections and default enviroment varibales
#4. Runnung ad-hoc commands on managed hosts and see different command line arguments 
#5. Dynamic Inventory
#6. YAML basics and way to check yaml syntax using python command and yamllint website and using --syntax-check option
#7. Implementing modules and  ansible-doc module_name command


# Chapter 3: Implementing Playbooks

#1. Properties of plabooks and notations 
#2. how to execute playbooks 
#3. how to use block in playbooks
#4. how to use modules in playbooks 

# Chapter 4: Managing Variables and Inlcusions:

#1. Define varibales in playbook using "vars", "var_files", host and group varibales in inventory file, create host_vars and group_vars directories 
#2. Create custom facts and use these fact in playbook to manage hosts
#3. Create separate playbook for tasks and include playbook in main.yml using include_tasks
#4. Define variable in separate files and include in playbook using include_vars

# Chapter 5: Implementing Task Controls:

#1. Implement ansible loops (simple loops with "with_items", nested loops)
#2. Construct conditionals using "when" statement in tasks with operators (<,>,=,!=,&&,or,||)
#3. Implement handlers in playbook using notify and listen statement
#4. Implement tags for playbooks with option --tags, --skip-tags, special tags (tagged/untagged/all)
#5. Implement Error handlings: using ignore_errors, force_handlers, failed_when, changed_when and using block of error handling (block/rescue/always)


# Chapter 6: Implementing Jinja2 templates:

#1. Using template module to place jinja2 templates to managed hosts


# Chapter 7: Implementing Roles:

#1. Create role directory structure inside roles directory 
#2. Use pre_tasks and post_tasks to accomplish task before and after role execution
#3. Install role from ansible galaxy using ansible-galaxy install -p roles command
#4. Create role using ansible-galaxy command ansible-galaxy init --offline -p roles empty.example


# Chapter 8: Optimizing Ansible

#1. Configuring connection types for ansible (smart,paramiko,ssh,local,docker,winrm,pywinrm)
#2. Set connection types in ansible configuration file and in inventory file or pass from command line option --connecton=ssh or --connection=smart
#3. Use enviroment variable in playbook to specify http_proxy values 
#4. Configure delegation of tasks to localhost, host other than mentioned in playbook or host not available in inventory using add_host statement in playbook
#5. Configuring Parallelism specifying --fork option or fork parameter in configuration file
#6. Limiting number of host for execution using "limit" option in configuration file 
#7. Use "async" and "poll" options in playbook for asyncronous tasks on managed hosts





# labs:

#create dynamic inventory for ec2
#create custom module using python
#launch ec2 instance using ansible 
#start stop ec2 instance using ansible 
#launch windows ec2 using ansible
#s3 basics operation using ansible
#launch auto scaling group using ansible 
#linux patch update using ansible 

