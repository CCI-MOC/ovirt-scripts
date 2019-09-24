#!/usr/bin/python
"""
This script performs a couple of things.
1. Remove snapshot attribute from disk devices.
2. If the VM is in this weird list called `vm_list`, then set the cache
policy to writeback.

Put this file at /usr/libexec/vdsm/hooks/before_vm_start/ and make sure it's executable.
"""

import traceback
import hooking

vm_list = ["test", "WindowsRocks"]
black_list = ["hostedengine"]
ENABLE_ALL = False

try:
    domxml = hooking.read_domxml()
    name = domxml.getElementsByTagName("name")[0].firstChild.nodeValue
    disks = domxml.getElementsByTagName('disk')

    for disk in disks:
        if disk.getAttribute('device') == 'disk':
            disk.removeAttribute('snapshot')
            if name.lower() not in black_list and (ENABLE_ALL or name.lower() in [vm.lower() for vm in vm_list]):
                driver = disk.getElementsByTagName('driver')[0]
                driver.setAttribute('cache', 'writeback')
    hooking.write_domxml(domxml)
except:
    sys.stderr.write('NAVED-RADO: %s\n' % traceback.format_exc())
    sys.exit(0)
