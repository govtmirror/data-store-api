# This file includes constant dictionaries and lists

_EXCLUDED_COLUMNS = ("create date",
                     "update date",
                     "username",
                     "awards_data_id",
                     "financial_accounts_id")

_SHORTCUT_COLUMNS = {
    "complete": ["*"],
    "basic": [  "AwardeeOrRecipientUniqueIdentifier",
                "AwardeeOrRecipientLegalEntityName",
                "LegalEntityAddressLine1",
                "LegalEntityAddressLine2",
                "LegalEntityStateCode",
                "LegalEntityCountryCode",
                "FAIN",
                "URI",
                "PIID",
                "AwardModificationAmendmentNumber",
                "ParentAwardId",
                "AwardDescription",
                "ActionDate",
                "AgencyIdentifier",
                "AwardingSubTierAgencyCode",
                "FundingSubTierAgencyCode",
                "PeriodOfPerformanceStartDate",
                "PeriodOfPerformanceCurrentEndDate",
                "PeriodOfPerformancePotentialEndDate",
                "AwardType",
                "PrimaryPlaceofPerformanceCongressionalDistrict",
                "FederalActionObligation",
                "CurrentTotalValueOfAward",
                "TransactionObligatedAmount"
            ]
}

_OPERATORS = {
    "equals": "=",
    "greater than": ">",
    "less than": "<",
}
