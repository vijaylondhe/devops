Track 1:    Getting Started
    Module 1:   Getting started with Learn Chef Rally
    Chef Automate: It integrates three open source projects 
    -   Chef:   for infra automation
    -   InSpec: for compliance automation
    -   Habitat: for application automation

Track 2:    Infrastructure Automation
    Module 1:   Learn the Chef basics
    -   install chefdk on ubuntu 18.04

        ChefDK version: 4.2.0
        Chef Infra Client version: 15.1.36
        Chef InSpec version: 4.7.3
        Test Kitchen version: 2.2.5
        Foodcritic version: 16.1.1
        Cookstyle version: 5.0.0

    -   check how to use chef-client --local-mode on workstation locally 
        chef-client --local-mode webserver.rb
    -   See how to use resouces like file, package, service, apt_update   
    -   generate cookbook using chef generate cookbook command 
    -   generate template using chef genarate cookbooks/learn_ubuntu_apache2 index.html
    -   see .erb extention on template file means for placeholder
    -   see how to write recipe using apt_update, package,service, template resources
    -   see how to run cookbook using chef command in --local-mode 
        chef-client --local-mode --runlist 'recipe[learn_chef_apache2]'

    
    Module 2:   Manage the node with chef server

    -   Setup the workstation
        -   Chefk includes chef infra client, ruby, rubygems, and other tools such as testkitchen, cookstyle, foodcritic, and chefspec
        -   workstaion can be linux, windows, macos 
        -   chefdk installer directory
            windows c:\opscode\chefdk
            linux: /opt/chefdk
        -   on windows, powershell is required 
        -   setup git account
            git config --global user.name "vijaylondhe"
            git config --global user.email vijay.londhe815@gmail.com
    
    -   Get setup with hosted chef
        -   There are 3 ways to setup chef server
            -   using hosted chef server (https://manage.chef.io/signup/)
            -   install chef server on your own instance
            -   use chef automate that have chef server
        -   configure workstation to interact with chefserver
        -   knife is used to upload cookbooks to chef server and using knife command we can bootstrap the nodes
        -   knife requires two things: RSA Private Key File and knife.rb configuration file (url of chef server, location of key file and default loction of cookbooks)
        -   both of the files are typically located in .chef folder

        -   Generate knife configuration file from hosted chef
        -   reset key for user and download .pem file
        -   create new directory ~/learn_chef and copy these two files in it
        -   run knife ssl check command to test connectivity with chef server

    -   Upload Cookbook to chef server
        -   mkdir cookbooks
        -   cd cookbooks
        -   git clone https://github.com/learn-chef/learn_chef_httpd.git
        -   knife cookbook upload learn_chef_httpd
        -   knife cookbook list 

    -   Get node bootstrapped
        -   see how to use knife bootstrap command
        
        -   note: if you bootstrapping azure instance then we need to create metadata for public ip and hostname for instance manually using JSON attriutes for aws ec2 it is available
        -   $public_ip = '{"cloud": {"public_ip": "13.82.139.157"}}' | ConvertTo-Json
        -   then with bootstrap command pass the --json-attributes $public_ip

        -   bootstrap types
            -   using key based authnetication
            -   using password authentication
            -   using forward port forlocal virtual machine
        
        -   Command:
        knife bootstrap ADDRESS --connection-user USER --sudo --ssh-identity-file IDENTITY_FILE --node-name node1-centos --run-list 'recipe[learn_chef_httpd]'

        knife bootstrap 13.232.198.180 --connection-user centos --sudo --ssh-identity-file .chef/control_key.pem --node-name 'ip-172-31-17-7.ap-south-1.compute.internal' --run-list 'recipe[learn_chef_httpd]'

        or 

        knife bootstrap 13.232.198.180 --sudo -i .\.chef\control_key.pem -x 'ubuntu' -N 'ip-172-31-17-7.ap-south-1.compute.internal' --run-list 'recipe[learn_chef_httpd]'
  
        -   list the node using knife node list command 
        -   see details of node using knife node show 'ip-172-31-17-7.ap-south-1.compute.internal'


    -   Update nodes configration

        -   Add template to our code and use node attributes inside it 
        -   Update index.html template in cookbook
            <html>
                <body>
                    <h1>hello from <%= node['fqdn'] %></h1>
                </body>
            </html>
        -   see how to use placeholder for node attribute <%= %>

        -   Update cookbook version metadata in metadata.rb file in cookook
        -   chef generate cookbook command to create your cookbook, the initial version is set to 0.1.0. 
        
        -   See what is semantic versioning "Major.Minor.Patch"
        -   Upload cookbook to chef server
            knife cookbook upload learn_chef_httpd

        -   see how to use knife ssh to run chef-client command on node or multiple nodes 

        knife ssh 'name:ip-172-31-17-7.ap-south-1.compute.internal' 'sudo chef-client' -x centos --ssh-identity-file .chef/control_key.pem --attribute 13.232.198.180


    -   Resolve a failed chef-client run

        -   edit default.rb file to update template resource
        -   add mode '0644' owner 'web_admin' and group 'web_admin' 
        -   update metadata.rb to version 0.3.0
        -   upload cookbook to chef sever using knife cookbook upload learn_chef_httpd
        -   run knife ssh command on node to run chef-client
            knife ssh 'name:ip-172-31-17-7.ap-south-1.compute.internal' 'sudo chef-client' -x centos --ssh-identity-file .centos/control_key.pem --attribute 13.232.198.180

        -   you will get an error that UserID Not found

        -   Resolve the failure 
            -   in default.rb recipe add the web_admin group and user before  template resource
            -   change patch version in metadata.rb file and upload cookbook to chef server
            -   run knife ssh command to run chef-client on node server
                knife ssh 'name:ip-172-31-17-7.ap-south-1.compute.internal' 'sudo chef-client' -x centos --ssh-identity-file .centos/control_key.pem --attribute 13.232.198.180

            
    -   Run chef-client periodically
        -   see what is configuration drift
        -   see why need to run chef-client on node periodically to remove any dirft
        -   check how to get chef-client cookbook from chef supermarket
        -   chef-client cookbook runs on multiple platfomrs
        -   see how to use Berkshelf to resolve cookbook dependencies
        -   see how to use a role to define your node's attributes and its run-list
        -   chef-client cookbook from chef supermarket has some dependencies on other cookbooks
        -   Berkshelf is tool that help you to resolve these dependencies, it retrives the cookbook and upload to the chef server

        -   create Berksfile in direcory
            souce 'https://supermarket.chef.io'
            cookbook 'chef-client'
        -   run berks install to install chef-cliet cookbook with its dependencies
        -   run berks upload to upload all cookbooks to chef server

        -   Create a Role for chef-client cookbook using two node attributes
            
            node['chef-client']['interval'] number of seconds after chef-client is run (default is 1800 second/30 mins)
            
            node['chef-client']['splay']    maximum random number of seconds that is added to the interval, to avoid many chef-client runs at same time (default is 300 second/5 mins)
        
        -   see why to use roles and how to create using knife role create command 
        -   A role enables you define your node's behavior and attributes based on its function
        -   roles can defined in json fomrat and pass to command such as knife role from file 
        -   create web role in learn_chef directory

            {
                "name": "web",
                "description": "Web server role.",
                "json_class": "Chef::Role",
                "default_attributes": {
                    "chef_client": {
                    "interval": 300,
                    "splay": 60
                    }
            },
            "override_attributes": {
            },
            "chef_type": "role",
            "run_list": ["recipe[chef-client::default]",
                        "recipe[chef-client::delete_validation]",
                        "recipe[learn_chef_httpd::default]"
                        ],
            "env_run_lists": {
                }
            }

        -   knife role from file roles/web.json
        -   knife role list
        -   knife role show web
        -   set run_list for node
        -   knife node run_list set ip-172-31-17-7.ap-south-1.compute.internal "role[web]"
        -   knife node show ip-172-31-17-7.ap-south-1.compute.internal --run-list

        -   Run chef-client using web role
            knife ssh 'role:web' 'sudo chef-client' --ss-identity-file .chef/control_key.pem -x centos --attribute 13.232.198.180

        -   knife status 'role:web' --run-list

        -   Clean up enviroment if required
        -   Delete the node from chef server
            knife node delete ip-172-31-17-7.ap-south-1.compute.internal --yes
            knife client delete ip-172-31-17-7.ap-south-1.compute.internal --yes
        
        -   Delete the cookbook from chef server 
            knife cookbook delete learn_chef_httpd --all --yes
                --all : to delete all verisons of cookbook
        
        -   Delete the web role
            knife role delete web --yes
        
        -   Delete rsa private key file
            rm -rf vijaylondhe.pem

        




