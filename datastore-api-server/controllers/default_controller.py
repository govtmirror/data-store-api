import flask

def get_mock_program_activity():
    return {
        "ByDirectReimbursableFundingSource": "R",
        "AllocationTransferAgencyIdentifier": "020",
        "ProgramActivityCode": "0002",
        "ProgramActivityName": "Preschool Grants",
        "ObligationsDeliveredOrdersUnpaidTotal_FYB": -4500,
        "GrossOutlaysUndeliveredOrdersPrepaidTotal_CPE": -4500,
        "GrossOutlaysDeliveredOrdersPaidTotal_FYB": -4500,
        "GrossOutlaysDeliveredOrdersPaidTotal_CPE": -4500,
        "AgencyIdentifier": "097",
        "ObligationsUndeliveredOrdersUnpaidTotal_FYB": -4500,
        "GrossOutlayAmountByProgramObjectClass_CPE": -4500,
        "ObligationsUndeliveredOrdersUnpaidTotal_CPE": -4500,
        "DeobligationsRecoveriesRefundsdOfPriorYearByProgramObjectClass_CPE": 3500,
        "EndingPeriodOfAvailability": "2015",
        "ObjectClass": "254",
        "SubAccountCode": "000",
        "ObligationsDeliveredOrdersUnpaidTotal_CPE": -4500,
        "AvailabilityTypeCode": "X",
        "BeginningPeriodOfAvailability": "2014",
        "MainAccountCode": "1552",
        "GrossOutlayAmountByProgramObjectClass_FYB": -4500,
        "ObligationsIncurredByProgramObjectClass_CPE": -3500,
        "GrossOutlaysUndeliveredOrdersPrepaidTotal_FYB": -4500
    }

def get_mock_financial_account():
    return {
        "ObligationsIncurredTotalByTAS_CPE": 3500,
        "ContractAuthorityAmountTotal_CPE": 3500,
        "AllocationTransferAgencyIdentifier": "020",
        "BudgetAuthorityUnobligatedBalanceBroughtForward_FYB": 3500,
        "GrossOutlayAmountByTAS_CPE": -3500,
        "BudgetAuthorityAvailableAmountTotal_CPE": 3500,
        "AvailabilityTypeCode": "X",
        "AgencyIdentifier": "097",
        "DeobligationsRecoveriesRefundsByTAS_CPE": 3500,
        "BorrowingAuthorityAmountTotal_CPE": 3500,
        "AdjustmentsToUnobligatedBalanceBroughtForward_CPE": -3500,
        "SpendingAuthorityfromOffsettingCollectionsAmountTotal_CPE": 3500,
        "EndingPeriodOfAvailability": "2015",
        "SubAccountCode": "000",
        "StatusOfBudgetaryResourcesTotal_CPE": 3500,
        "BudgetAuthorityAppropriatedAmount_CPE": 3500,
        "OtherBudgetaryResourcesAmount_CPE": 3500,
        "UnobligatedBalance_CPE": 3500,
        "MainAccountCode": "5531",
        "BeginningPeriodOfAvailability": "2014"
    }

def get_mock_award():
    return {
        "VendorFaxNumber": "string",
        "LegalEntityCityName": "string",
        "LegalEntityZip4": "string",
        "ParentAwardId": "string",
        "AgencyIdentifier": "097",
        "LegalEntityStateCode": "string",
        "URI": "12-34-56-78-90-AS-DF-AB-XZ-YW",
        "CurrentTotalValueOfAward": "string",
        "IDV Type": "string",
        "PIID": "string",
        "ObjectClass": 254,
        "NorthAmericanIndustrialClassificationSystemCode": "string",
        "SubAccountCode": "000",
        "TransactionObligatedAmount": 3500,
        "LegalEntityCountryCode": "string",
        "PrimaryPlaceOfPerformanceZip4": "string",
        "PeriodOfPerformanceStartDate": "string",
        "AwardDescription": "string",
        "ReferencedIDVAgencyIdentifier": "string",
        "AwardingOfficeCode": "string",
        "ActionDate": "string",
        "AwardingSubTierAgencyCode": "string",
        "AwardModificationAmendmentNumber": "string",
        "PotentialTotalValueOfAward": "string",
        "AllocationTransferAgencyIdentifier": "020",
        "AwardType": "string",
        "ProgramActivityCode": "0002",
        "PrimaryPlaceofPerformanceCongressionalDistrict": "string",
        "PeriodOfPerformanceCurrentEndDate": "string",
        "ProgramActivityName": "Preschool Grants",
        "AvailabilityTypeCode": "X",
        "MainAccountCode": "1552",
        "LegalEntityCongressionalDistrict": "string",
        "AwardeeOrRecipientUniqueIdentifier": "string",
        "FAIN": "123456798",
        "AwardeeOrRecipientLegalEntityName": "string",
        "FundingOfficeCode": "string",
        "VendorPhoneNumber": "string",
        "FederalActionObligation": "string",
        "PeriodOfPerformancePotentialEndDate": "string",
        "FundingSubTierAgencyCode": "string",
        "EndingPeriodOfAvailability": "2015",
        "VendorDoingAsBusinessName": "string",
        "BeginningPeriodOfAvailability": "2014",
        "LegalEntityAddressLine2": "string",
        "LegalEntityAddressLine1": "string",
        "VendorAddressLine3": "string",
        "TypeofIDC": "string",
        "MultipleorSingleAwardIDV": "string"
    }

def award_fain_fain_get(FAIN):
    return flask.jsonify({ "results": get_mock_award()})

def award_piid_piid_get(PIID):
    return flask.jsonify({ "results": get_mock_award()})

def award_uri_uri_get(URI):
    return flask.jsonify({ "results": get_mock_award() })

def awards_post(body):
    return flask.jsonify({ "results": [get_mock_award(), get_mock_award()]})

def financial_account_mac_get(MAC):
    return flask.jsonify({ "results": get_mock_financial_account()})

def financial_accounts_post(body):
    return flask.jsonify({ "results": [get_mock_financial_account(), get_mock_financial_account()]})

def financial_activities_post(body):
    return flask.jsonify({ "results": [get_mock_program_activity(), get_mock_program_activity()]})

def financial_activity_pac_get(PAC):
    return flask.jsonify({ "results": get_mock_program_activity()})
