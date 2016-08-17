# This file includes constant dictionaries and lists

_EXCLUDED_COLUMNS = ("create_date",
                     "update_date",
                     "create_user_id",
                     "update_user_id"
                     )

_AVAILABLE_TABLES = ("treasury_appropriation_account",
                     "appropriation_account_balances",
                     "financial_accounts_by_program_activity_object_class",
                     "financial_accounts_by_awards",
                     "financial_accounts_by_awards_transaction_obligations")

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
