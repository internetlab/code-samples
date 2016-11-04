from glob import glob
import os

apache_config_path = "/etc/apache2/sites-available/"
host_file_path = "/etc/hosts"

vhost_content = \
    """<VirtualHost *:80>
    ServerAdmin keerthi@kind.lk
    ServerName %s
    DocumentRoot %s

    Header set Access-Control-Allow-Origin "*"
    Header set Access-Control-Allow-Methods "POST, GET, OPTIONS, PUT, DELETE"
    Header set Access-Control-Allow-Headers "Content-Type, Accept, Authorization, X-Requested-With, Token, CompanyId"

    <Directory />
            Options +FollowSymLinks
            AllowOverride All
    </Directory>

    <Directory %s>
            Options +Indexes +FollowSymLinks
            AllowOverride All
            Require all granted
    </Directory>

    LogLevel warn

    ErrorLog /var/log/apache2/error.log
    CustomLog /var/log/apache2/access.log combined
</VirtualHost>
"""

# get vhost name
vhost_name = input("Enter Virtual Host Name (E.g. mydemo.dev) -> ")

# get doc root path
doc_root = input("Enter document root (E.g. /my/doc/root/path/) -> ")

# create new vhost file
vhost_content = vhost_content % (vhost_name, doc_root, doc_root)

names = [os.path.basename(x) for x in glob(apache_config_path + "[0-9][0-9]*.conf")]
conf_files = sorted(names)

print(conf_files)
last_file = conf_files[-1]

file_index = last_file[0:2]

try:
    file_index = int(file_index)
    file_index += 1
    file_index = "000" + str(file_index)
    file_index = file_index[-2:]
except ValueError:
    file_index = "01"

# save vhost file
new_conf_file_name = file_index + "-" + vhost_name + ".conf"
new_conf_file_path = apache_config_path + new_conf_file_name

new_conf_file = open(new_conf_file_path, 'w')
new_conf_file.write(vhost_content)
new_conf_file.close()

print("...config file saved\n")

# enable vhost apache
os.system("a2ensite %s" % new_conf_file_name)

# restart apache
os.system("service apache2 restart")

# append host record line and save
host_file = open(host_file_path, 'a')
host_file.write("127.0.0.1\t%s\n" % vhost_name)
host_file.close()

print("...host file updated\n")
print("...done, access your vhost at http://%s/\n" % vhost_name)
