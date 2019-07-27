Very preliminary Ansible playbook to install [Apache Hadoop Ozone](https://hadoop.apache.org/ozone/) on a cluster.

## Install Ozone
Follow the steps below to deploy your Ozone cluster.

### Edit the hosts.yaml file
The `hosts.yaml` contains a list of hosts grouped by role. The format of the included template file is self-documenting.

### Edit conf/settings.yaml
Edit the `conf/cluster-settings.yaml` template file. At the very least, you will need to modify the OM and SCM hostnames, the Ozone tarball file name, and the java_home location.

For production clusters or anytime you care about data persistence or performance, you should also edit the storage and metadata directory locations.


### Run the playbook
```
ansible-playbook -i hosts.yaml install-ozone.yaml -v
```
The `-v` option enables verbose logging which is useful for debugging when things go wrong.

## Stop all Ozone services.
Ozone services can be stopped using the following ad-hoc command. This kills all processes running as the `hdfs` user.
```
ansible --inventory=hosts.yaml  all -m shell -a 'pkill -u hdfs'
```

