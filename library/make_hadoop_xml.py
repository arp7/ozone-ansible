#!/usr/bin/python

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License. See accompanying LICENSE file.

from ansible.module_utils.basic import *
import yaml

"""
Ansible module to convert a YAML file into a Hadoop XML configuration
file.

This allows us to generate Hadoop/Ozone configuration files as YAML
which can be consumed easily by Ansible playbooks.
"""

# This header is common to all Hadoop/Ozone XML config files.
#
xml_header="""<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->

<configuration>
"""

xml_footer="""
</configuration>
"""

property_tag_template="""
  <property>
    <name>{}</name>
    <value>{}</value>
  </property>
"""

def main():
    fields = {
            "source_yaml": {"required": True, "type": "str"},
            "dest_xml": {"required": True, "type": "str"},
            "site_name": {"required": True, "type": "str"},
            "om_hosts": {"required": True, "type": "list"},
            "scm_hosts": {"required": True, "type": "list"}
    }

    module = AnsibleModule(argument_spec=fields)
    make_xml(source=module.params["source_yaml"],
            dest=module.params["dest_xml"],
            site_name=module.params["site_name"],
            om_hosts=module.params["om_hosts"],
            scm_hosts=module.params["scm_hosts"])
    module.exit_json(changed=True,
            msg="Generated XML file {}".format(module.params["dest_xml"]))

def make_xml(source=None, dest=None, site_name=None,
        om_hosts=None, scm_hosts=None):
    with open(dest, "w") as f:
        f.write(xml_header)
        write_yaml_fields(source, f, site_name, om_hosts, scm_hosts)
        f.write(xml_footer)


def write_yaml_fields(source=None, f=None, site_name=None,
        om_hosts=None, scm_hosts=None):
    with open(source, "r") as y:
        content = yaml.safe_load(y)
    settings = content[site_name]

    # If OM host was not defined in ozone_site, then pick the hostnames
    # from the inventory
    if "ozone.om.address" not in settings:
        f.write(property_tag_template.format("ozone.om.address",
            ",".join(om_hosts)))

    # If SCM host was not defined in ozone_site, then pick the hostnames
    # from the inventory
    if "ozone.scm.names" not in settings:
        f.write(property_tag_template.format("ozone.scm.names",
            ",".join(scm_hosts)))

    # Write everything else
    #
    for name, value in settings.items():
        f.write(property_tag_template.format(name, value))

if __name__ == '__main__':
    main()

