from sqlalchemy import *
import yaml
import flask
import controllers.constants.mappings as mappings
import controllers.constants.database_vars as dbvars

class DatastoreDB:
    _dbinstance = None
    def __init__(self):
        DatastoreDB._dbinstance = self
        print("Creating datastore database connection...")
        with open('config.yml', 'r') as stream:
            try:
                config = yaml.load(stream)['api']
            except yaml.YAMLError as exc:
                print(exc)

        datastore_string =  ( 'postgresql://' + config['data_store']['user'] +
                              ':' + config['data_store']['password'] +
                              '@' + config['data_store']['url'] +
                              ':' + str(config['data_store']['port']) +
                              '/' + config['data_store']['database'])

        self.engine = create_engine(datastore_string, echo=True)

        print("Database connection established, acquiring available columns")
        self.table_columns = {}
        for table in dbvars._AVAILABLE_TABLES:
            self.table_columns[table] = []
            sql = text('SELECT column_name FROM information_schema.columns WHERE table_name=:table;')
            result = self.engine.execute(sql, {'table': table})
            for row in result:
                if row[0] not in dbvars._EXCLUDED_COLUMNS:
                    self.table_columns[table].append(row[0])

        print(self.table_columns)

        print("Done")

    @staticmethod
    def get_instance():
        if DatastoreDB._dbinstance == None:
            DatastoreDB._dbinstance = DatastoreDB()
        return DatastoreDB._dbinstance

    # A query on File A
    def query_financial_accounts(self, parameters):
        tables = [
                    "appropriation_account_balances",
                    "treasury_appropriation_account"
                 ]
        join_relations = [
                    "appropriation_account_balances.treasury_account_identifier = treasury_appropriation_account.treasury_account_identifier"
                         ]
        return self.query(parameters,
                          tables,
                          join_relations,
                          mappings._FINANCIAL_RESPONSE_MAP)

    # A query on File B
    def query_financial_activities(self, parameters):
        tables = [
                    "financial_accounts_by_program_activity_object_class",
                    "appropriation_account_balances",
                    "treasury_appropriation_account"
                 ]
        join_relations = [
                    "financial_accounts_by_program_activity_object_class.appropriation_account_balances_id = appropriation_account_balances.appropriation_account_balances_id",
                    "appropriation_account_balances.treasury_account_identifier = treasury_appropriation_account.treasury_account_identifier"
                         ]
        return self.query(parameters,
                          tables,
                          join_relations,
                          mappings._FINANCIAL_RESPONSE_MAP)

    def query_award_financials(self, parameters):
        tables = [
                    "financial_accounts_by_awards",
                    "financial_accounts_by_awards_transaction_obligations",
                    "appropriation_account_balances",
                    "treasury_appropriation_account"
                 ]
        join_relations = [
                    "financial_accounts_by_awards.financial_accounts_by_awards_id = financial_accounts_by_awards_transaction_obligations.financial_accounts_by_awards_id",
                    "financial_accounts_by_awards.appropriation_account_balances_id = appropriation_account_balances.appropriation_account_balances_id",
                    "appropriation_account_balances.treasury_account_identifier = treasury_appropriation_account.treasury_account_identifier"
                         ]
        return self.query(parameters,
                          tables,
                          join_relations,
                          mappings._AWARD_RESPONSE_MAP)


    # tables - Array of table names
    #          e.g. ["TABLE_A",
    #               "TABLE_B",
    #               "TABLE_C"]
    # table_join_relations - Array of how tables join to one another
    #          e.g. ["TABLE_A.id = TABLE_B.table_a_id",
    #               "TABLE_C.table_b_id = TABLE_B.id"]
    def query(self, parameters, tables, table_join_relations, responseMap):
        columns = []
        available_columns = []
        # Get list of available columns from all of tables that will be joined
        for table in tables:
            available_columns = available_columns + self.table_columns[table]
        # For every requested column, we need to check if it is a shortcut column
        # and whether it exists in available_columns
        for col in parameters["columns"]:
            # If the requested column is a shortcut column
            if col in dbvars._SHORTCUT_COLUMNS:
                if col == "complete":
                    # Complete is *, which is not an 'available column', so just append it
                    columns = columns + dbvars._SHORTCUT_COLUMNS[col]
                else:
                    # Find the intersection of the shortcuts and available columns
                    intersection = list(set.intersection(set(dbvars._SHORTCUT_COLUMNS[col]), set(available_columns)))
                    for column in intersection:
                        columns.append(column)
            # If the column is just a regular column
            else:
                if col in available_columns:
                    columns.append(col)
                else:
                    # The column isn't a shortcut, and isn't in the available columns
                    # Throw an error so we return 500. TODO: May want to change this to just
                    # return a json object with an error parameter
                    raise Exception(col + " was not found in the list of available fields\n" +
                                    "Current available fields for this endpoint are: " + "\n\t".join(available_columns))

        # First, we construct the join statement
        join_statement = ""
        numjoins = 0
        # This will create either a string with solely the single queried table,
        # or a join satement using the provided relations
        for table in tables:
            if len(join_statement) == 0:
                join_statement = join_statement + table
            else:
                join_statement = join_statement + " INNER JOIN " + table + " ON " + table_join_relations[numjoins]
                numjoins = numjoins + 1
        sql = "SELECT " + ",".join(columns) + " FROM " + join_statement
        sqlparams = []

        if len(parameters["filters"]) > 0:
            for parameter in parameters["filters"]:
                # List is [0] - fieldname, [1] - operator, [2] - value
                if parameter[0] not in available_columns:
                    raise Exception(parameter[0] + " was not found in the list of available fields\n" +
                                    "Current available fields for this endpoint are: \n\t" + "\n\t".join(available_columns))
                # Construct an array of parameters for tuple construction later
                operatorExpressions = []
                sqlparams.append(parameter[2])
                operatorExpressions.append("\"" + parameter[0] + "\" " + parameter[1] + " %s")
            # Create a where clause that we can fill with a tuple
            sql = sql + " WHERE " + " AND ".join(operatorExpressions)
        # Pagination
        limit = parameters["page_length"]
        offset = (parameters["page"] - 1) * limit
        sql = sql + " OFFSET %s LIMIT %s" % (offset, limit)

        # Query
        result = self.engine.execute(sql, tuple(sqlparams))
        dictresponse = [mapResponse(row2dict(row), responseMap) for row in result]
        print(dictresponse)
        return (parameters, dictresponse)

def row2dict(row):
    d = {}
    for item in row.items():
        if item[0] in dbvars._EXCLUDED_COLUMNS: continue
        d[item[0]] = item[1]
    return d

# Dict response should be what is returned as a list element from the query()
# function, a dictionar of attribute:values. responseMap should be a either
# mappings._AWARD_RESPONSE_MAP or mappings._FINANCIAL_RESPONSE_MAP
def mapResponse(dictresponse, responseMap):
    newResponse = {}
    for key in dictresponse:
        # If we have that key in our response map, place it in the corresponding
        # grouping
        if key in responseMap:
            if responseMap[key] not in newResponse:
                # If the grouping dict isn't in our response yet, put it there
                newResponse[responseMap[key]] = {}
            newResponse[responseMap[key]][key] = dictresponse[key]
        else:
            # Otherwise, just drop it straight back in the response
            newResponse[key] = dictresponse[key]
    return newResponse

def construct_parameter_object(body):
    filters = []
    columns = ["complete"]
    page = 1
    page_length = 1000

    if "columns" in body:
        columns = body["columns"]
    if "filters" in body:
        for clause in body["filters"]:
            if not clause['operation'] in dbvars._OPERATORS.keys():
                raise Exception("Operation " + clause['operation'] + " not recognized")
            filters.append([clause['fieldname'], dbvars._OPERATORS[clause['operation']], clause['value']])
    if "page" in body:
        page = max(1, int(body["page"]))
    if "page_length" in body:
        page_length = min(1000, int(body["page_length"]))
    parameters = {
        "columns": columns,
        "filters": filters,
        "page": page,
        "page_length": page_length
    }
    return parameters

def award_fain_fain_get(FAIN):
    parameters = {
        "columns": ["complete"],
        "filters": [["fain", "=", str(FAIN)]],
        "page": 1,
        "page_length": 1000
    }
    results = DatastoreDB.get_instance().query_awards(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def award_piid_piid_get(PIID):
    parameters = {
        "columns": ["complete"],
        "filters": [["piid", "=", str(PIID)]],
        "page": 1,
        "page_length": 1000
    }
    results = DatastoreDB.get_instance().query_awards(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def award_uri_uri_get(URI):
    parameters = {
        "columns": ["complete"],
        "filters": [["uri", "=", str(URI)]],
        "page": 1,
        "page_length": 1000
    }
    results = DatastoreDB.get_instance().query_awards(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def awards_post(body):
    parameters = construct_parameter_object(body)
    results = DatastoreDB.get_instance().query_award_financials(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def financial_accounts_object_class_get(ObjectClass):
    parameters = {
        "columns": ["complete"],
        "filters": [["object_class", "=", str(ObjectClass)]],
        "page": 1,
        "page_length": 1000
    }
    results = DatastoreDB.get_instance().query_financials(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def financial_activites_main_account_code_get(MainAccountCode):
    parameters = {
        "columns": ["complete"],
        "filters": [["main_account_code", "=", str(MainAccountCode)]],
        "page": 1,
        "page_length": 1000
    }
    results = DatastoreDB.get_instance().query_financials(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})


def financial_accounts_post(body):
    parameters = construct_parameter_object(body)
    results = DatastoreDB.get_instance().query_financial_accounts(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def financial_activities_post(body):
    parameters = construct_parameter_object(body)
    results = DatastoreDB.get_instance().query_financial_activities(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})
