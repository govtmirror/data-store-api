from sqlalchemy import *
import yaml
import flask

# This code needs some heavy refactoring

_EXCLUDED_COLUMNS = ("create date",
                     "update date",
                     "username",
                     "awards_data_id",
                     "financial_accounts_id")

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
        print "Done"

    @staticmethod
    def get_instance():
        if DatastoreDB._dbinstance == None:
            DatastoreDB._dbinstance = DatastoreDB()
        return DatastoreDB._dbinstance

    # Parameters is an array of n [[FIELD, OPERATOR, VALUE]]
    # Operators are guaranteed to go through the global array
    def query_awards(self, parameters):
        query = parameters
        sql = "SELECT * FROM awards_data"
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

    # Parameters is an array of n [[FIELD, OPERATOR, VALUE]]
    # Operators are guaranteed to go through the global array
    def query_financials(self, parameters):
        query = parameters
        sql = "SELECT * FROM financial_accounts"
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

def award_fain_fain_get(FAIN):
    parameters = {
        "columns": "*",
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
        "columns": "*",
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
        "columns": "*",
        "filters": [["URI", "=", str(URI)]]
    }
    results = DatastoreDB.get_instance().query_awards(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def awards_post(body):
    filters = []
    for clause in body:
        if not clause['operation'] in _OPERATORS.keys():
            raise Exception("Operation " + clause['operation'] + " not recognized")
        filters.append([clause['fieldname'], _OPERATORS[clause['operation']], clause['value']])
    parameters = {
        "columns": "*",
        "filters": filters
    }
    results = DatastoreDB.get_instance().query_awards(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def financial_account_mac_get(MAC):
    parameters = {
        "columns": "*",
        "filters": [["MainAccountCode", "=", str(MAC)]]
    }
    results = DatastoreDB.get_instance().query_financials(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def financial_accounts_post(body):
    filters = []
    for clause in body:
        if not clause['operation'] in _OPERATORS.keys():
            raise Exception("Operation " + clause['operation'] + " not recognized")
        filters.append([clause['fieldname'], _OPERATORS[clause['operation']], clause['value']])
    parameters = {
        "columns": "*",
        "filters": filters
    }
    results = DatastoreDB.get_instance().query_financials(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def financial_activities_post(body):
    filters = []
    for clause in body:
        if not clause['operation'] in _OPERATORS.keys():
            raise Exception("Operation " + clause['operation'] + " not recognized")
        filters.append([clause['fieldname'], _OPERATORS[clause['operation']], clause['value']])
    parameters = {
        "columns": "*",
        "filters": filters
    }
    results = DatastoreDB.get_instance().query_financials(parameters)
    query = results[0]
    results = results[1]
    return flask.jsonify({  "query": query,
                            "count": len(results),
                            "results": results})

def financial_activity_pac_get(PAC):
    raise Exception('PAC not currently available')
