Very preliminary Ansible playbook to install [Ozone](https://hadoop.apache.org/ozone/) on a cluster.

# Install Ozone

## Initialize the Inventory File
_Inventory_ is a fancy Ansible name for the `hosts.yaml` file which contains a list of hosts grouped by role. The format of the file is self-documenting, see the included sample file.

The hosts file also defines some key variables like `ozone_tarball` and `java_home`.

You don't have to define variables in the inventory file. They can also be passed on the command-line when invoking the playbook using the `ansible-playbook --extra-vars=` option. However it is generally more convenient to define them in the inventory file.

## Create ozone-site.xml and ozone-site.yaml
Create the ozone-site.xml and ozone-site.yaml files under `conf/`. The file contents must be in sync. This does require some manual duplication effort for the configuration settings and is a bit clunky. It will be fixed soon.

_TODO: Generate ozone-site.xml automatically from ozone-site.yaml_

## Run the playbook
```
ansible-playbook -i hosts install-ozone.yaml -v
```
The `-v` option enables verbose logging which is useful for debugging when things go wrong.

# Stop all Ozone services.
Ozone services can be stopped using the following ad-hoc command. This kills all processes running as the `hdfs` user.
```
ansible --inventory=hosts.yaml  all -m shell -a 'pkill -u hdfs'
```

