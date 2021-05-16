sudo apt-get update
sudo apt-get -y install python3 python3-pip git ffmpeg
git clone https://github.com/Defaultin/FourierTransformBot.git
cd FourierTransformBot/
sudo pip3 install -r requirements.txt
sudo pip3 install opencv-python Pillow
sudo pip3 uninstall pytelegrambotapi -y
sudo pip3 uninstall telebot -y
sudo pip3 install telebot==0.0.3
sudo pip3 install pytelegrambotapi==3.6.6
