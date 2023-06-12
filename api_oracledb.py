import sqlalchemy
import oracledb

oracledb.defaults.config_dir = "./otc/wallet_oracle"
oracledb.init_oracle_client()
'''connection = oracledb.connect(user="hr", password=userpwd, dsn="orclpdb",
                              config_dir="/opt/oracle/config")'''