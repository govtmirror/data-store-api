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

_AWARD_RESPONSE_MAP = {
    "VendorFaxNumber": "recipient_info",
    "LegalEntityCityName": "recipient_info",
    "LegalEntityZip4": "recipient_info",
    "ParentAwardId": "linking_procurement",
    "AgencyIdentifier": "tas",
    "LegalEntityStateCode": "recipient_info",
    "URI": "linking_financial_assistance",
    "CurrentTotalValueOfAward": "award_action",
    "IDV Type": "indirect_delivery_vehicle_specific_charactersitcs",
    "PIID": "linking_procurement",
    "NorthAmericanIndustrialClassificationSystemCode": "award_type",
    "SubAccountCode": "tas",
    "TransactionObligatedAmount": "transaction_obligated_amount",
    "LegalEntityCountryCode": "recipient_info",
    "PrimaryPlaceOfPerformanceZip4": "place_of_performance",
    "PeriodOfPerformanceStartDate": "award_dates",
    "AwardDescription": "award_info",
    "ReferencedIDVAgencyIdentifier": "indirect_delivery_vehicle_specific_charactersitcs",
    "AwardingOfficeCode": "awarding_agency",
    "ActionDate": "award_action",
    "AwardingSubTierAgencyCode": "awarding_agency",
    "AwardModificationAmendmentNumber": "award_modification",
    "PotentialTotalValueOfAward": "award_action",
    "AllocationTransferAgencyIdentifier": "tas",
    "AwardType": "award_action",
    "PrimaryPlaceofPerformanceCongressionalDistrict": "place_of_performance",
    "PeriodOfPerformanceCurrentEndDate": "award_dates",
    "AvailabilityTypeCode": "tas",
    "MainAccountCode": "tas",
    "LegalEntityCongressionalDistrict": "recipient_info",
    "AwardeeOrRecipientUniqueIdentifier": "award_recipient",
    "FAIN": "linking_financial_assistance",
    "AwardeeOrRecipientLegalEntityName": "award_recipient",
    "FundingOfficeCode": "funding_agency",
    "VendorPhoneNumber": "recipient_info",
    "FederalActionObligation": "award_action",
    "PeriodOfPerformancePotentialEndDate": "award_dates",
    "FundingSubTierAgencyCode": "funding_agency",
    "EndingPeriodOfAvailability": "tas",
    "VendorDoingAsBusinessName": "award_recipient",
    "BeginningPeriodOfAvailability": "tas",
    "LegalEntityAddressLine2": "recipient_info",
    "LegalEntityAddressLine1": "recipient_info",
    "VendorAddressLine3": "recipient_info",
    "TypeofIDC": "indirect_delivery_vehicle_specific_charactersitcs",
    "MultipleorSingleAwardIDV": "indirect_delivery_vehicle_specific_charactersitcs"
}

_FINANCIAL_RESPONSE_MAP = {
    "AgencyIdentifier": "SomeGroupA",
    "MainAccountCode": "SomeGroupB",
    "StatusOfBudgetaryResourcesTotal_CPE": "SomeGroupB"
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
                         _AWARD_RESPONSE_MAP,
                         "awards_data")

    def query_financials(self, parameters):
                return self.query(parameters,
                                 DatastoreDB.get_instance().financial_columns,
                                 DatastoreDB.get_instance().financial_columns_lower,
                                 _FINANCIAL_RESPONSE_MAP,
                                 "financial_accounts")

    # Parameters is an array of n [[FIELD, OPERATOR, VALUE]]
    # Operators are guaranteed to go through the global array
    def query(self, parameters, column_array, column_array_lower, responseMap, table_name):
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
        dictresponse = [mapResponse(row2dict(row), responseMap) for row in result]
        return (query, dictresponse)

def row2dict(row):
    d = {}
    for item in row.items():
        if item[0] in _EXCLUDED_COLUMNS: continue
        d[item[0]] = item[1]
    return d

# Dict response should be what is returned as a list element from the query()
# function, a dictionar of attribute:values. responseMap should be a either
# _AWARD_RESPONSE_MAP or _FINANCIAL_RESPONSE_MAP
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
        "columns": ["complete"],
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
        "columns": ["complete"],
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
        "columns": ["complete"],
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
