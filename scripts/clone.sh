#!/bin/bash

timestamp=$(date +%Y-%m-%d.%H:%M:%S)
logfile=updates/clone.${timestamp}.log

exec 1>> ${logfile} 2>&1

echo -#- Backup de la base de datos.
sudo -u openerp oerpenv snapshot elote_prod

echo -#- Detenemos los servidores.
sudo -s service openerp-server stop
sudo -s service openerp-homo-server stop

echo -#- Clonamos la base de datos.
sudo -u postgres dropdb elote_prod
sudo -u postgres createdb -O openerp -T elote_homo elote_prod "Base de datos de producción del ELOTE"

echo -#- Clonamos los archivos en el fs
sudo -u openerp tar -cPzf filesystem_prod.${timestamp}.tar.gz /opt/openerp/.local/share/OpenERP/filestore/elote_prod
sudo -u openerp rm -rf /opt/openerp/.local/share/OpenERP/filestore/elote_prod
sudo -u openerp cp -r /opt/openerp/.local/share/OpenERP_Homo/filestore/elote_homo /opt/openerp/.local/share/OpenERP/filestore/elote_prod

echo -#- Reiniciamos los servicios
sudo -s service openerp-server start
sudo -s service openerp-homo-server start

echo -#- Update terminado.
