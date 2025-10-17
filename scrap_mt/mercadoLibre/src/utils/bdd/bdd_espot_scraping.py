import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError
from src.utils.wait import *



class BddEspotScraping:
    """
    Class to automate web scraping related database operations.
    """

    def __init__(self, database, host='127.0.0.1', user='root', password='', instance_id=''):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.instance_id = instance_id

    def _make_conexion_sqlalchemy(self, p=True):
        """Creates a connection using SQLAlchemy."""
        try:
            db_connection_values = f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}'
            sqlalchemy_engine = create_engine(db_connection_values, pool_size=10, max_overflow=20)
            with sqlalchemy_engine.connect() as connection:
                if(p):
                    print("Successful connection with SQLAlchemy")
            return sqlalchemy_engine
        except SQLAlchemyError as e:
            print("Error creating the connection with SQLAlchemy:")
            print("\t", e)
            print(type(e))
            print("\t", getattr(e, "orig", e))
            return None

    def getLinks(self, n):
        """
        Retrieves n records from the database and marks them as processed.

        :param n: Number of records to retrieve.
        :return: List of retrieved records.
        """
        attempts = 0
        max_attempts = 5
        success = False
        links = []

        while attempts < max_attempts and not success:
            sqlalchemy_engine = self._make_conexion_sqlalchemy(p=False)
            if sqlalchemy_engine:
                try:
                    with sqlalchemy_engine.connect() as connection:
                        # Select records and mark them with the unique identifier
                        select_query = text(f"SELECT id, link FROM links WHERE processed = 0 LIMIT {n} FOR UPDATE")
                        result = connection.execute(select_query)
                        links = result.fetchall()
                        if links:
                            ids_to_update = [link[0] for link in links]
                            update_query = text(f"UPDATE links SET processed = -1, instance_id = :instance_id WHERE id IN :ids")
                            connection.execute(update_query, {'instance_id': self.instance_id, 'ids': tuple(ids_to_update)})
                            connection.commit()
                            # print("Links retrieved and marked successfully with SQLAlchemy")
                            success = True
                except SQLAlchemyError as e:
                    print("Error executing the query with SQLAlchemy:")
                    print("\t", e)
                    sqlalchemy_engine.dispose()
                    sqlalchemy_engine = None
            if not success:
                attempts += 1
                if attempts < max_attempts:
                    print(f"Reattempting to connect ({attempts}/{max_attempts})...")
                    wait(30, mensaje_espera='Waiting to try reconnection')  # 5 minutos
        if not success:
            print("Failed to retrieve and mark the links after multiple attempts.")
        return ids_to_update,links


    def confirmLinks(self, ids_to_update):
        """
        Retrieves n records from the database and marks them as processed.

        :ids_to_update: Ids to update to 1 in processed field
        """
        attempts = 0
        max_attempts = 5
        success = False

        while attempts < max_attempts and not success:
            sqlalchemy_engine = self._make_conexion_sqlalchemy(p=False)
            if sqlalchemy_engine:
                try:
                    with sqlalchemy_engine.connect() as connection:
                        # Select records and mark them with the unique identifier
                        update_query = text(f"UPDATE links SET processed = 1, instance_id = :instance_id WHERE id IN :ids")
                        connection.execute(update_query, {'instance_id': self.instance_id, 'ids': tuple(ids_to_update)})
                        connection.commit()
                        # print("Links retrieved and marked successfully with SQLAlchemy")
                        success = True
                except SQLAlchemyError as e:
                    print("Error executing the query with SQLAlchemy:")
                    print("\t", e)
                    sqlalchemy_engine.dispose()
                    sqlalchemy_engine = None
            if not success:
                attempts += 1
                if attempts < max_attempts:
                    print(f"Reattempting to connect ({attempts}/{max_attempts})...")
                    wait(30, mensaje_espera='Waiting to try reconnection')  # 5 minutos
        if not success:
            print("Failed to retrieve and mark the links after multiple attempts.")
        return success



    def getRemainingLinks(self):
        """
        Retrieves the count of records from the database where `processed = 0`.

        :return: Integer count of remaining records or None if failed.
        """
        attempts = 0
        max_attempts = 5
        success = False
        remaining_count = None  # Inicializa fuera del bucle

        while attempts < max_attempts and not success:
            sqlalchemy_engine = self._make_conexion_sqlalchemy(p=False)
            if sqlalchemy_engine:
                try:
                    with sqlalchemy_engine.connect() as connection:
                        # Select count of records where processed = 0
                        select_query = text("SELECT COUNT(*) as remaining FROM links WHERE processed = 0")
                        result = connection.execute(select_query)
                        remaining_count = result.scalar()  # Retorna el primer valor de la primera fila
                        success = True  # Marca como exitoso si se obtuvo el resultado
                except SQLAlchemyError as e:
                    print("Error executing the query with SQLAlchemy:")
                    print("\t", e)
                    sqlalchemy_engine.dispose()
                    sqlalchemy_engine = None

            if not success:
                attempts += 1
                if attempts < max_attempts:
                    print(f"Reattempting to connect ({attempts}/{max_attempts})...")
                    wait(30, mensaje_espera='Waiting to try reconnection')  # 5 minutos

        if not success:
            print("Failed to retrieve the count of remaining links after multiple attempts.")
        return remaining_count
    

    def makeInserts(self, inserts_list):
        """
        Executes a list of insert statements.

        :param inserts_list: List of SQL insert statements.
        """
        attempts = 0
        max_attempts = 5
        success = False
        while attempts < max_attempts and not success:
            sqlalchemy_engine = self._make_conexion_sqlalchemy()
            if sqlalchemy_engine:
                try:
                    with sqlalchemy_engine.connect() as connection:
                        ok_count = 0
                        error_count = 0
                        for insert_query in inserts_list:
                            try:
                                connection.execute(text(insert_query))
                                ok_count += 1
                            except ProgrammingError as e:
                                error_count += 1
                                print("SQL syntax error:", e)
                                print("Query:", insert_query[:300], "...")
                                continue
                            #Insertamos este log para ver si que errores de insercion a la BD hay
                            except SQLAlchemyError as e:
                                error_count += 1
                                print("SQLAlchemy error:", e)
                                print("Query:", insert_query[:300], "...")
                                continue
                        connection.commit()
                        print(f"Inserts executed successfully with SQLAlchemy (ok={ok_count}, error={error_count})")
                        success = True
                except SQLAlchemyError as e:
                    print("Error executing the inserts with SQLAlchemy:")
                    print("\t", e)
                    sqlalchemy_engine.dispose()
                    sqlalchemy_engine = None
                    
            if not success:
                attempts += 1
                if attempts < max_attempts:
                    print(f"Reattempting to connect ({attempts}/{max_attempts})...")
                    wait(30, mensaje_espera='Waiting to try reconnection')  # 5 minutos

        if not success:
            print("Failed to execute the inserts after multiple attempts.")
        
    def makeInsert(self, insert_query):
        """
        Executes a single insert query.

        :param insert_query: SQL insert statement.
        """
        attempts = 0
        max_attempts = 5
        success = False

        while attempts < max_attempts and not success:
            sqlalchemy_engine = self._make_conexion_sqlalchemy(p=False)
            if sqlalchemy_engine:
                try:
                    with sqlalchemy_engine.connect() as connection:
                        connection.execute(text(insert_query))
                        connection.commit()
                        success = True
                except SQLAlchemyError as e:
                    print("Error executing the insert with SQLAlchemy:")
                    print("\t", e)
                    sqlalchemy_engine.dispose()
                    sqlalchemy_engine = None
            if not success:
                attempts += 1
                if attempts < max_attempts:
                    print(f"Reattempting to connect ({attempts}/{max_attempts})...")
                    wait(30, mensaje_espera='Waiting to try reconnection')  # 5 minutos
            return success 

        if not success:
            print("Failed to execute the insert after multiple attempts.")
            
    def make_bulk_insert(self, query ,insert_queries):
        """
        Ejecuta múltiples inserciones usando el método executemany de SQLAlchemy.

        :param insert_queries: Lista de diccionarios con los datos para insertar.
        """
        sqlalchemy_engine = self._make_conexion_sqlalchemy(p=False)
        if sqlalchemy_engine:
            try:
                with sqlalchemy_engine.connect() as connection:
                    # Consulta SQL usando placeholders
                    insert_sql = text(query)
                    # Ejecutar todas las filas en un solo `executemany`
                    connection.execute(insert_sql, insert_queries)
                    connection.commit()
                return True
            except SQLAlchemyError as e:
                print("Error executing the bulk insert with SQLAlchemy:")
                print("\t", e)
                sqlalchemy_engine.dispose()
                return False
