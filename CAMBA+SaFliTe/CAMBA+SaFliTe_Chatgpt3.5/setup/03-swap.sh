# As ROOT
su -

# Create storage file
# 1024 * 1024 * 10GB = 10485760 block size
dd if=/dev/zero of=/swapfile bs=1024 count=10485760

# Secure swap file
chown root:root /swapfile
chmod 0600 /swapfile

# Set up a Linux swap area
mkswap /swapfile

# Enabling the swap file
swapon /swapfile

# Update /etc/fstab file
nano /etc/fstab
# Append the following line:
/swapfile none swap sw 0 0

# Reboot instance
reboot

# Verify Linux swap file
free -m
swapon -s
htop
