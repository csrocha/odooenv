#!/bin/bash
#
# Instala OpenERP en un servidor remoto
# ESTADO BETA.
#

REMOTEHOST=$1

if [ "x$REMOTEHOST" == 'x' ]; then
	echo "Error: No se indicó en que servidor hay que instalar OpenERP."
	exit -1;
fi

LOGFILE=~/$REMOTEHOST.oerpenv.install.log
touch $LOGFILE
echo "Log in: $LOGFILE"

#
# Crea tu usuario para no ejecutar todo en root.
#
grep "DONE:add-user:$USER" $LOGFILE
if [ "$?" == 1 ]; then
	echo "Crea el usuario de conexión. Necesita password de root."
	echo "RUN:add-user:$USER" > $LOGFILE
	ssh -l root $REMOTEHOST "adduser $USER; usermod -G sudo $USER"
	ssh $REMOTEHOST mkdir ~/.ssh
	cat ~/.ssh/id_rsa.pub | ssh $REMOTEHOST tee -a ~/.ssh/authorized_keys
	echo "DONE:add-user:$USER" > $LOGFILE
fi

SHROOT="ssh -tq $REMOTEHOST sudo"
OERPHOME=/opt/openerp
REPOSITORY=$OERPHOME/v7.0
PACKAGES="sudo postgresql python-pip python-dev \
	libpq-dev python-svn libldap2-dev libsasl2-dev libxml2-dev libxslt1-dev\
       	mercurial swig nginx \
	texlive-latex-extra texlive-fonts-extra texlive-fonts-recommended \
	python-psycopg2 cython"
BUILDPACKAGES=python-imaging

SCRIPTFILENAME=/tmp/$$.script
VERSION=trunk
declare -A ENVIRONMENT_LINK
ENVIRONMENT_LINK[7.0]='https://gist.github.com/csrocha/7203820/raw/cb01fa5e67d29867c20285b7ea56f58dbbac6c28/environment_v7.conf'
ENVIRONMENT_LINK[trunk]='https://gist.githubusercontent.com/csrocha/7203820/raw/9336bcae3ff2e0eb5f1783d0a8a0a01cf2c6262d/environment_v8.conf'
ENVIRONMENT_LINK=${ENVIRONMENT_LINK[$VERSION]}
ENVIRONMENT_ORIG=$(basename $ENVIRONMENT_LINK)

echo "Copia el script de instalacion."
grep "DONE:create-script" $LOGFILE
if [ "$?" == 1 ]; then
	echo "RUN:create-script" > $LOGFILE
	cat > $SCRIPTFILENAME << EOC
#BEGIN# REMOTE SCRIPT ####
apt-get update
apt-get install aptitude
aptitude -y safe-upgrade
aptitude -y install $PACKAGES
aptitude -y build-dep $BUILDPACKAGES

pip install oerpenv

# Crea todo los usuarios necesarios
adduser --system --group --home $OERPHOME openerp
sudo -s -u postgres createuser -d -r -S openerp

# Crea el lugar de trabajo
cd /opt/openerp/

# Crea el espacio de deployment si no existe.
if [ ! -d v$VERSION ]; then
  sudo -u openerp oerpenv init -v $VERSION v$VERSION
fi

cd v$VERSION
sudo -u openerp wget $ENVIRONMENT_LINK
sudo -u openerp mv $ENVIRONMENT_ORIG v$VERSION/environment.conf
sudo -u openerp oerpenv update
sudo -u openerp oerpenv install
sudo -u openerp oerpenv enable all
sudo -u openerp oerpenv server-start --debug -- --save --stop-after-init
sudo -u openerp sed -i 's/debug_mode = True/debug_mode = False/g' default/etc/openerp-server.conf
sudo -u openerp sed -i 's/_interface =.*/_interface = 127.0.0.1/g' default/etc/openerp-server.conf

# Startup script
cd /etc/init.d/
wget https://gist.github.com/csrocha/8983013/raw/3caf863a7f7d5a1c9e2c6e1784b9b97e94e97327/openerp-server
chmod +x openerp-server
update-rc.d openerp-server defaults

service openerp-server start

# Generate certificates
cd /etc/ssl
openssl genrsa -out host.key 1024
openssl req -new -key host.key -out host.csr
openssl x509 -req -days 365 -in host.csr -signkey host.key -out host.crt

# Setup ngnix
cd /etc/nginx/sites-enabled
rm -f default
cd /etc/nginx/sites-available
wget https://gist.github.com/csrocha/8983347/raw/1837a8d3c193e74fdb3a07429a89ab0f5c664c3e/ngnix-openerp
ln -s /etc/nginx/sites-available/ngnix-openerp /etc/nginx/sites-enabled
service nginx start
service nginx reload

#END### REMOTE SCRIPT ####
EOC
	chmod +x $SCRIPTFILENAME

	scp $SCRIPTFILENAME $REMOTEHOST:$SCRIPTFILENAME
	$SHROOT sudo $SCRIPTFILENAME

	echo "DONE:create-script" > $LOGFILE
fi

exit

