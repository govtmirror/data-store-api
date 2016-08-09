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
        sql = text('SELECT column_name FROM information_schema.columns WHERE table_name=\'awards_data\'')
        result = self.engine.execute(sql)
        self.award_columns = []
        for row in result:
            if row[0] not in dbvars._EXCLUDED_COLUMNS:
                self.award_columns.append(row[0])
        self.award_columns_lower = [item.lower() for item in self.award_columns]

        sql = text('SELECT column_name FROM information_schema.columns WHERE table_name=\'financial_accounts\'')
        result = self.engine.execute(sql)
        self.financial_columns = []
        for row in result:
            if row[0] not in dbvars._EXCLUDED_COLUMNS:
                self.financial_columns.append(row[0])
        self.financial_columns_lower = [item.lower() for item in self.financial_columns]

        print("Done")

    @staticmethod
    def get_instance():
        if DatastoreDB._dbinstance == None:
            DatastoreDB._dbinstance = DatastoreDB()
        return DatastoreDB._dbinstance

    def query_awards(self, parameters):
        return self.query(parameters,
                         DatastoreDB.get_instance().award_columns,
                         DatastoreDB.get_instance().award_columns_lower,
                         mappings._AWARD_RESPONSE_MAP,
                         "awards_data")

    def query_financials(self, parameters):
                return self.query(parameters,
                                 DatastoreDB.get_instance().financial_columns,
                                 DatastoreDB.get_instance().financial_columns_lower,
                                 mappings._FINANCIAL_RESPONSE_MAP,
                                 "financial_accounts")

    # Parameters is an array of n [[FIELD, OPERATOR, VALUE]]
    # Operators are guaranteed to go through the global array
    def query(self, parameters, column_array, column_array_lower, responseMap, table_name):
        query = parameters
        columns = []
        for col in parameters["columns"]:
            if col in dbvars._SHORTCUT_COLUMNS:
                if col == "complete":
                    columns = columns + dbvars._SHORTCUT_COLUMNS[col]
                else:
                    # If a field is in the shortcut, we must verify it exists
                    # in the requested table
                    intersection = list(set.intersection(set(dbvars._SHORTCUT_COLUMNS[col]), set(column_array)))
                    for column in intersection:
                        columns.append("\"" + column + "\"")
            else:
                try:
                    index = column_array_lower.index(col.lower())
                    columns.append("\"" + column_array[index] + "\"")
                except ValueError:
                    raise Exception(col + " was not found in the list of available fields\n" +
                                    "Current available fields are: " + "\n\t".join(column_array))
        sql = "SELECT " + ",".join(columns) + " FROM " + table_name
        sqlparams = []
        if len(parameters["filters"]) > 0:
            for parameter in parameters["filters"]:
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
        return (query, dictresponse)

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
        "filters": [["FAIN", "=", str(FAIN)]],
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
        "filters": [["PIID", "=", str(PIID)]],
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
        "filters": [["URI", "=", str(URI)]],
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
    results = DatastoreDB.get_instance().query_awards(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def financial_accounts_object_class_get(ObjectClass):
    parameters = {
        "columns": ["complete"],
        "filters": [["ObjectClass", "=", str(ObjectClass)]],
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
        "filters": [["MainAccountCode", "=", str(MainAccountCode)]],
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
    results = DatastoreDB.get_instance().query_financials(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def financial_activities_post(body):
    parameters = construct_parameter_object(body)
    results = DatastoreDB.get_instance().query_financials(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})
