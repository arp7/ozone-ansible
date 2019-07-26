Very preliminary Ansible playbook for install Ozone to a cluster of hosts.

Create the ozone-site.xml file under conf/ozone-site.xml.

Execute the playbook with:
    ```
    ansible-playbook -i hosts playbook.yaml --extra-vars=ozone_tarball=ozone-0.5.0-SNAPSHOT.tar.gz -v
    ```
