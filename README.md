## Introduction
[Ansible](https://www.ansible.com/resources/videos/quick-start-video) is an agent-less provisioning and deployment tool. We provide an Ansible playbook, custom module and config file templates to deploy [Apache Hadoop Ozone](https://hadoop.apache.org/ozone/) to an arbitrarily large cluster.

All you need is ssh access to the cluster for the `root` user, and Ansible installed on a control node. The control node may be one of the nodes in your cluster or an external node.

## Steps to deploy Ozone

#### 1. Edit the hosts.yaml file
A template `hosts.yaml` file is provided. It contains a list of hosts grouped by role. The format of the included template file is (hopefully) self-documenting.

#### 2. Edit conf/settings.yaml
Edit the `conf/settings.yaml` template file. At the very least, you will need to specify the Ozone tarball file name and the `JAVA_HOME` location.

For production clusters or anytime you care about data persistence or performance, you should also edit the storage and metadata directory locations.

#### 3. Run the playbook
```
ansible-playbook -i hosts.yaml install-ozone.yaml -v
```
The `-v` option enables verbose logging which is useful for debugging when things go wrong.

## Useful ad-hoc commands

Ansible allows running ad-hoc commands on cluster hosts. A few useful examples:

#### Generate the ozone-site.xml
It is useful to verify the generated `ozone-site.xml` before doing a full installation. The file can be generated with the following command:
```
ansible-playbook -i hosts.yaml install-ozone.yaml -v --tags "generate"
```
The output file will be available as `conf/auto_generated/ozone-site.xml`.

#### Stop all Ozone services.
Ozone services can be stopped with the following command that simply kills all processes running as the `hdfs` user.
```
ansible --inventory=hosts.yaml all -m shell -a 'pkill -u hdfs'
```

#### List Ozone services running on each host
The following works by listing the java process names on each host.
```
ansible --inventory=hosts.yaml all -m shell -a 'jps | grep -ivw [j]ps'
```

_Apache®, Apache Hadoop, Hadoop®, and the yellow elephant logo are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries._
