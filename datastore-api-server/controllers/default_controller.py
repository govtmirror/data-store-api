from sqlalchemy import *
import yaml
import flask

# This code needs some heavy refactoring

_EXCLUDED_COLUMNS = ("create date",
                     "update date",
                     "username",
                     "awards_data_id",
                     "financial_accounts_id")

_SHORTCUT_COLUMNS = {
    "complete": ["*"],
    "basic": []
}

_OPERATORS = {
    "equals": "=",
    "greater than": ">",
    "less than": "<",
}

class DatastoreDB:
    _dbinstance = None
    def __init__(self):
        DatastoreDB._dbinstance = self
        print "Creating datastore database connection..."
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

        print "Database connection established, acquiring available columns"
        sql = text('SELECT column_name FROM information_schema.columns WHERE table_name=\'awards_data\'')
        result = self.engine.execute(sql)
        self.award_columns = []
        for row in result:
            if row[0] not in _EXCLUDED_COLUMNS:
                self.award_columns.append(row[0])
        self.award_columns_lower = [item.lower() for item in self.award_columns]

        sql = text('SELECT column_name FROM information_schema.columns WHERE table_name=\'financial_accounts\'')
        result = self.engine.execute(sql)
        self.financial_columns = []
        for row in result:
            if row[0] not in _EXCLUDED_COLUMNS:
                self.financial_columns.append(row[0])
        self.financial_columns_lower = [item.lower() for item in self.financial_columns]

        print "Done"

    @staticmethod
    def get_instance():
        if DatastoreDB._dbinstance == None:
            DatastoreDB._dbinstance = DatastoreDB()
        return DatastoreDB._dbinstance

    def query_awards(self, parameters):
        return self.query(parameters,
                         DatastoreDB.get_instance().award_columns,
                         DatastoreDB.get_instance().award_columns_lower,
                         "awards_data")

    def query_financials(self, parameters):
                return self.query(parameters,
                                 DatastoreDB.get_instance().financial_columns,
                                 DatastoreDB.get_instance().financial_columns_lower,
                                 "financial_accounts")

    # Parameters is an array of n [[FIELD, OPERATOR, VALUE]]
    # Operators are guaranteed to go through the global array
    def query(self, parameters, column_array, column_array_lower, table_name):
        query = parameters
        columns = []
        for col in parameters["columns"]:
            if col in _SHORTCUT_COLUMNS:
                columns = columns + _SHORTCUT_COLUMNS[col]
            else:
                try:
                    index = column_array_lower.index(col.lower())
                    columns.append("\"" + column_array[index] + "\"")
                except ValueError:
                    raise Exception(col + " was not found in the list of available fields\n" +
                                    "Current available fields are: " + "\n\t".join(column_array))
        sql = "SELECT " + ",".join(columns) + " FROM " + table_name
        sqlparams = []
        if len(parameters["filters"]) == 0:
            sql = sql + " LIMIT 1000" # Maybe change this later
        else:
            for parameter in parameters["filters"]:
                # Construct an array of parameters for tuple construction later
                operatorExpressions = []
                sqlparams.append(parameter[2])
                operatorExpressions.append("\"" + parameter[0] + "\" " + parameter[1] + " %s")
            # Create a where clause that we can fill with a tuple
            sql = sql + " WHERE " + " AND ".join(operatorExpressions)
        result = self.engine.execute(sql, tuple(sqlparams))
        return (query, [row2dict(row) for row in result])

def row2dict(row):
    d = {}
    for item in row.items():
        if item[0] in _EXCLUDED_COLUMNS: continue
        d[item[0]] = item[1]
    return d

def construct_parameter_object(body):
    filters = []
    columns = ["*"]
    if "columns" in body:
        columns = body["columns"]
    if "filters" in body:
        for clause in body["filters"]:
            if not clause['operation'] in _OPERATORS.keys():
                raise Exception("Operation " + clause['operation'] + " not recognized")
            filters.append([clause['fieldname'], _OPERATORS[clause['operation']], clause['value']])
    parameters = {
        "columns": columns,
        "filters": filters
    }
    return parameters

def award_fain_fain_get(FAIN):
    parameters = {
        "columns": ["*"],
        "filters": [["FAIN", "=", str(FAIN)]]
    }
    results = DatastoreDB.get_instance().query_awards(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def award_piid_piid_get(PIID):
    parameters = {
        "columns": ["*"],
        "filters": [["PIID", "=", str(PIID)]]
    }
    results = DatastoreDB.get_instance().query_awards(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def award_uri_uri_get(URI):
    parameters = {
        "columns": ["*"],
        "filters": [["URI", "=", str(URI)]]
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
