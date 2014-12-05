#!/usr/bin/python2
import os,sys,traceback
print "Create Vhost v1.1"

# Parse the site name from the command line or just promt for it
site_name = ""
if len(sys.argv) > 1:
    site_name = sys.argv[1]
else:
    site_name = raw_input("Site Name: ")
if site_name[0:2] == "www":
    site_name = site_name[2:]


DocumentRoot = "/var/www/" + site_name + "/"
vhost = "/etc/nginx/sites-available/" + site_name
#git = "/home/ubuntu/" + site_name.replace(".","") + ".git/"
print """Will Create the following folders: 
 - Document Root: %s
 - nginx vhost:   %s""" % (DocumentRoot,vhost)

print "Continue? [Y/n]",
c = sys.stdin.read(1)
print
if c not in ("\n", "y", "Y"):
    print "Aborted by user"
    exit()

# Create http root

print "Creating DocumentRoot... ",
try:
    try:
        os.stat(DocumentRoot)
    except:
        os.mkdir(DocumentRoot)
except:
    print "[Fail]\n\n"
    traceback.print_exc()
    exit()
else:
    print "[OK]"


# Create nginx vhost


nginxfile = """server {
        listen 80;
        server_name %s www.%s; 
        root   /var/www/%s/current/public/;

        location / {
                index index.php index.html index.htm;
                try_files $uri $uri/ /index.php$is_args$args;
        }
 
        # serve static files directly
        location ~* ^.+.(jpg|jpeg|gif|css|png|js|ico|html|xml|txt)$ {
            access_log        off;
            expires           30d;
        }
 
        location ~ \.php$ {
                fastcgi_pass unix:/var/run/php5-fpm.sock;
                fastcgi_index index.php;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                fastcgi_param PATH_INFO $fastcgi_script_name;
                include /etc/nginx/fastcgi_params;
        }
        error_page 404 500 502 503 504 /error.html;
        location = /error.html {
            root /var/www/globalerror;
        }
}
""" % (server_name, server_name, DocumentRoot)
print "Creating nginx config... ",
try:
    open(vhost,"w").write(nginxfile)

    os.system("ln -s " + vhost + " " + vhost.replace("available", "enabled", 1))
except:
    print "[fail]\n\n"
    traceback.print_exc()
    exit()
else:
    print "[ok]"

# Create repository in home folder

# print "Creating git repository... ",

# try:
#     try:
#         os.stat(git)
#     except:
#         os.mkdir(git)   

#     os.chdir(git)

#     os.system("git init --bare")
#     os.system("rm hooks/*.sample")

#     githook = """#!/bin/sh
# GIT_WORK_TREE=%s git checkout -f
# echo "Pushed %s to web server""" % (DocumentRoot, site_name)

# 	open(git+"hooks/post-recieve", w).write(githook)

	
# except:
#     print "[Fail]\n\n"
#     traceback.print_exc()
#     exit()
# else:
#     print "[OK]"
