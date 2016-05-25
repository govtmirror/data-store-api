import flask

def get_mock_program_activity():
    return {
        "ByDirectReimbursableFundingSource": "string",
        "AllocationTransferAgencyIdentifier": "string",
        "ProgramActivityCode": "string",
        "ProgramActivityName": "string",
        "ObligationsDeliveredOrdersUnpaidTotal_FYB": 0,
        "GrossOutlaysUndeliveredOrdersPrepaidTotal_CPE": 0,
        "GrossOutlaysDeliveredOrdersPaidTotal_FYB": 0,
        "GrossOutlaysDeliveredOrdersPaidTotal_CPE": 0,
        "AgencyIdentifier": "string",
        "ObligationsUndeliveredOrdersUnpaidTotal_FYB": 0,
        "GrossOutlayAmountByProgramObjectClass_CPE": 0,
        "ObligationsUndeliveredOrdersUnpaidTotal_CPE": 0,
        "DeobligationsRecoveriesRefundsdOfPriorYearByProgramObjectClass_CPE": 0,
        "EndingPeriodOfAvailability": "string",
        "ObjectClass": "string",
        "SubAccountCode": "string",
        "ObligationsDeliveredOrdersUnpaidTotal_CPE": 0,
        "AvailabilityTypeCode": "string",
        "BeginningPeriodOfAvailability": "string",
        "MainAccountCode": "string",
        "GrossOutlayAmountByProgramObjectClass_FYB": 0,
        "ObligationsIncurredByProgramObjectClass_CPE": 0,
        "GrossOutlaysUndeliveredOrdersPrepaidTotal_FYB": 0
    }

def get_mock_financial_account():
    return {
        "ObligationsIncurredTotalByTAS_CPE": 0,
        "ContractAuthorityAmountTotal_CPE": 0,
        "AllocationTransferAgencyIdentifier": "string",
        "BudgetAuthorityUnobligatedBalanceBroughtForward_FYB": 0,
        "GrossOutlayAmountByTAS_CPE": 0,
        "BudgetAuthorityAvailableAmountTotal_CPE": 0,
        "AvailabilityTypeCode": "string",
        "AgencyIdentifier": "string",
        "DeobligationsRecoveriesRefundsByTAS_CPE": 0,
        "BorrowingAuthorityAmountTotal_CPE": 0,
        "AdjustmentsToUnobligatedBalanceBroughtForward_CPE": 0,
        "SpendingAuthorityfromOffsettingCollectionsAmountTotal_CPE": 0,
        "EndingPeriodOfAvailability": "string",
        "SubAccountCode": "string",
        "StatusOfBudgetaryResourcesTotal_CPE": 0,
        "BudgetAuthorityAppropriatedAmount_CPE": 0,
        "OtherBudgetaryResourcesAmount_CPE": 0,
        "UnobligatedBalance_CPE": 0,
        "MainAccountCode": "string",
        "BeginningPeriodOfAvailability": "string"
    }

def get_mock_award():
    return {
        "VendorFaxNumber": "string",
        "LegalEntityCityName": "string",
        "LegalEntityZip4": "string",
        "ParentAwardId": "string",
        "AgencyIdentifier": "string",
        "LegalEntityStateCode": "string",
        "URI": "string",
        "CurrentTotalValueOfAward": "string",
        "IDV Type": "string",
        "PIID": "string",
        "ObjectClass": "string",
        "NorthAmericanIndustrialClassificationSystemCode": "string",
        "SubAccountCode": "string",
        "TransactionObligatedAmount": "string",
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
        "AllocationTransferAgencyIdentifier": "string",
        "AwardType": "string",
        "ProgramActivityCode": "string",
        "PrimaryPlaceofPerformanceCongressionalDistrict": "string",
        "PeriodOfPerformanceCurrentEndDate": "string",
        "ProgramActivityName": "string",
        "AvailabilityTypeCode": "string",
        "MainAccountCode": "string",
        "LegalEntityCongressionalDistrict": "string",
        "AwardeeOrRecipientUniqueIdentifier": "string",
        "FAIN": "string",
        "AwardeeOrRecipientLegalEntityName": "string",
        "FundingOfficeCode": "string",
        "VendorPhoneNumber": "string",
        "FederalActionObligation": "string",
        "PeriodOfPerformancePotentialEndDate": "string",
        "FundingSubTierAgencyCode": "string",
        "EndingPeriodOfAvailability": "string",
        "VendorDoingAsBusinessName": "string",
        "BeginningPeriodOfAvailability": "string",
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
