sudo apt-get update
sudo apt-get -y install python3 python3-pip git
git clone https://github.com/Defaultin/FourierTransformBot.git
cd FourierTransformBot/
sudo pip3 install -r requirements.txt
sudo pip3 install opencv-python Pillow
sudo python3 main.py
