## E-Reader or Reading Mirror or Intelligent Textbooks

This project includes the changes discussed in the work 

Barria-Pineda, Jordan et al. “Reading Mirror: Social Navigation and Social Comparison for Electronic Textbooks.” iTextbooks@AIED (2019). http://ceur-ws.org/Vol-2384/paper03.pdf.

#### Project Pre-requisites

The project runs on python3. MySQL client and server will need to be installed locally. The project runs the best on a Linux or MacOS system.

To install mysql client and server 

```
sudo apt install mysql-client-core mysql-server-core mysql-server
```
To install python pre-requisites

```
python3 -m pip install -r requirements.txt
```
References:
(https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install-linux-quick.html)
(https://dev.mysql.com/doc/refman/8.0/en/linux-installation.html)

#### Running the Project

If on a Linux machine, [without or without virtualenv](https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment)

```
sudo service mysql start
sudo mysql
mysql> CREATE USER 'developer'@'localhost' IDENTIFIED WITH auth_socket BY '*******';
mysql> GRANT USAGE ON *.* to 'developer'@'127.0.0.1';
mysql> GRANT USAGE ON *.* to 'developer'@'localhost';
mysql> GRANT ALL PRIVILEGES on *.* to 'developer'@'localhost';
mysql> GRANT ALL PRIVILEGES on *.* to 'developer'@'127.0.0.1';
mysql> CREATE DATABASE ereader;
mysql> \q
python3 manage.py makemigrations
python3 manage.py migrate
mysql -u developer -p
mysql> source dump_ereader_structure_20220511.sql
mysql> source ereader_dataonly_20220511.sql
mysql> \q
python3 import_users_from_file_django.py
```

#### Citing the project

```
@inproceedings{BarriaPineda2019ReadingMS,
  title={Reading Mirror: Social Navigation and Social Comparison for Electronic Textbooks},
  author={Jordan Barria-Pineda and Peter Brusilovsky and Daqing He},
  booktitle={iTextbooks@AIED},
  year={2019}
}
```