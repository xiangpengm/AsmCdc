# 组装流程依赖
sudo apt install pigz -y 
sudo apt install openjdk-8-jdk -y 
# install conda
conda install pigz -c bioconda -y
conda install trimmomatic -c bioconda -y 
conda install spades -c bioconda -y
python -m pip install pywebview[qt]==3.0.1
pip3 install psutil