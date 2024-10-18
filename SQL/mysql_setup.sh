sudo apt update
sudo apt upgrade
sudo apt install mysql-server -y
sudo mysql -u root -p
CREATE USER '<user>'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password>';
exit
sudo service mysql stop
sudo service mysql restart