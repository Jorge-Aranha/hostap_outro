import hdbcli.dbapi as dbapi

def con():
    try:
        conn = dbapi.connect(
            address='brneo695',
            port=30013,
            user='U620433',
            password='Aj_Tonny@2006',
            databaseName = "BNP"
        )
        return conn

    except Exception as e:
        print('Erro', e)
        return None