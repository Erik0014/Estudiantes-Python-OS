# import pymysql
# pymysql.install_as_MySQLdb()

from django.db.backends.mysql.base import DatabaseWrapper

# Forzar Django para aceptar MySQL 5.7
DatabaseWrapper.mysql_version = (8, 0, 11)
DatabaseWrapper.mariadb_version = (8, 0, 11)

# Desactivar la verificacion de version
original_check = DatabaseWrapper.check_database_version_supported

def patched_check_version(self):
    pass

DatabaseWrapper.check_database_version_supported = patched_check_version