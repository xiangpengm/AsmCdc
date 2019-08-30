# 安装gui基础依赖
sudo apt install gir1.2-gtk-3.0 gir1.2-webkit2-4.0
sudo apt install libgirepository1.0-dev

# 解压缩conda
tar zxf soft/miniconda3.tar.gz

# 移动conda安装包到系统目录下
sudo mv miniconda3 /usr/local
sudo ln -s /usr/local/miniconda3/bin/python3.7 /usr/local/bin/
sudo ln -s /usr/local/miniconda3/bin/spades.py /usr/local/bin/
sudo ln -s /usr/local/miniconda3/bin/trimmomatic /usr/local/bin/

# 安装主程序到/usr/local/pipe中
sudo mkdir /usr/local/cdcAsm/
sudo cp *.py /usr/local/cdcAsm/
sudo cp -a templates /usr/local/cdcAsm/
sudo cp main.sh /usr/local/cdcAsm/

# 安装主程序到桌面
cp "CDC Asm Client.desktop" ${HOME}/Desktop/