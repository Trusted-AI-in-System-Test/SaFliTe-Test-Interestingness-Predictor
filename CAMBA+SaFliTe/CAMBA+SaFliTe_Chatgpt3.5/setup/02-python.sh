# As ROOT
su -
apt -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
cd ~
wget https://www.python.org/ftp/python/3.8.18/Python-3.8.18.tgz
tar -xf Python-3.8.18.tgz
cd Python-3.8.18
./configure --enable-optimizations && make -j$(nproc) && make altinstall
cd ~
rm -rf Python-3.8.18
rm -rf Python-3.8.18.tgz
