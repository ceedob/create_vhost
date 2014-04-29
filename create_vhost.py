#!/usr/bin/python2
import os,sys,traceback
print "Create Vhost v1.0"
site_name = raw_input("Site Name: ")
if site_name[0:2] == "www":
    site_name = site_name[2:]
DocumentRoot = "/var/www/" + site_name + "/"
vhost = "/etc/nginx/sites-available/" + site_name
git = "/home/ubuntu/" + site_name.replace(".","") + ".git/"
print """Will Create the following folders: 
 - Document Root: %s
 - nginx vhost:   %s
 - Git repository %s""" % (DocumentRoot,vhost,git)

print "Continue? [Y/n]",
c = sys.stdin.read(1)
print
if c != "\n" and c != "y" and c != "Y":
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
 
        location / {
                root   %s;
                index index.php;
 
        }
 
        # serve static files directly
        location ~* ^.+.(jpg|jpeg|gif|css|png|js|ico|html|xml|txt)$ {
            access_log        off;
            expires           30d;
        }
 
        location ~ \.php$ {
                fastcgi_pass 127.0.0.1:9000;
                fastcgi_index index.php;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                fastcgi_param PATH_INFO $fastcgi_script_name;
                include /usr/local/nginx/conf/fastcgi_params;
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

print "Creating git repository... ",

try:
    try:
        os.stat(git)
    except:
        os.mkdir(git)   

    os.chdir(git)

    os.system("git init --bare")
    os.system("rm hooks/*.sample")

    githook = """#!/bin/sh
GIT_WORK_TREE=%s git checkout -f
echo "Pushed %s to web server""" % (DocumentRoot, site_name)

	open(git+"hooks/post-recieve", w).write(githook)

	
except:
    print "[Fail]\n\n"
    traceback.print_exc()
    exit()
else:
    print "[OK]"
