
# Teradici Slider

  

## Important Info

When connecting to a Teradici session for the first time after a machine reboot, you must Connect, Disconnect, and then Connect again for Teradici Slider to work. This is **not** on us, this is a Teradici bug. After that, it will work normally until PCoIP Agent is restarted, or the machine is rebooted.

Teradici slider is made for Linux based OSes and only tested on RockyLinux 9.x.

## Install
run ./INSTALL.sh --install

The script will check if `crudini`is installed, and if not, will attempt to download and install it.  This requires internet access.

Once installed, all file will be in `/opt/instinctual/teradicislider`. 
A sudo rule is also created in `/etc/sudoers.d/teradicislider` which allows ANY user to modify the `pcoip.maximum_initial_image_quality` parameter in `/etc/pcoip-agent/pcoip-agent.conf` without a password prompt.  This actually is the most secure way.

That is it.

## Un-Install
./INSTALL.sh --uninstall