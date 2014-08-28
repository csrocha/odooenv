#!/bin/bash

timestamp=$(date +%Y-%m-%d.%H:%M:%S)
logfile=updates/update.${timestamp}.log

exec 1>> ${logfile} 2>&1

echo -#- Start Update.
cd /opt/openerp/homo

echo -#- Backup de la base de datos.
sudo -u openerp oerpenv snapshot elote_homo

echo -#- Detenemos el servidor de homologación.
sudo -s service openerp-homo-server stop

echo -#- Hacemos un update de los modulos.
sudo -u openerp oerpenv update

echo -#- Habilitamos todos los modulos.
sudo -u openerp oerpenv enable all

echo -#- Damos todos los permisos al usuario.
sudo -u postgres psql elote_homo -c 'GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO openerp;'
sudo -u postgres psql elote_homo -c 'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO openerp;'
for tbl in `psql -qAt -c "select tablename from pg_tables where schemaname = 'public';" elote_homo` ; do
        sudo -u postgres psql -c "alter table $tbl owner to openerp" elote_homo ;
done
for tbl in `psql -qAt -c "select sequence_name from information_schema.sequences where sequence_schema = 'public';" elote_homo` ; do
        sudo -u postgres psql -c "alter sequence $tbl owner to openerp" elote_homo ;
done
for tbl in `psql -qAt -c "select table_name from information_schema.views where table_schema = 'public';" elote_homo` ; do
        sudo -u postgres psql -c "alter table $tbl owner to openerp" elote_homo ;
done

echo -#- Reiniciamos el servidor.
sudo -s service openerp-homo-server start

echo -#- Update terminado.
