# import virtualbox

# vbox = virtualbox.VirtualBox()

# names = [m.name for m in vbox.machines]
# print("entering...")
# print(names)

import vboxapi

print("reached")
vbox_mgr = vboxapi.VirtualBoxManager(None, None)
print("reached")
vbox = vbox_mgr.vbox
print([m.name for m in vbox.machines])
