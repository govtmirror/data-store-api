from sqlalchemy import *
import yaml
import flask

# This code needs some heavy refactoring

_EXCLUDED_COLUMNS = ("create date",
                     "update date",
                     "username",
                     "awards_data_id",
                     "financial_accounts_id")

_AGENCY_TO_TERSE_LABELS = {
    "PIID": "piid",
    "AwardingSubTierAgencyCode": "awarding_sub_tier_agency_c",
    "AwardingSubTierAgencyName": "awarding_sub_tier_agency_n",
    "AwardingAgencyCode": "awarding_agency_code",
    "AwardingAgencyName": "awarding_agency_name",
    "ParentAwardId": "parent_award_id",
    "AwardModificationAmendmentNumber": "award_modification_amendme",
    "TypeOfContractPricing": "type_of_contract_pricing",
    "ContractAwardType": "contract_award_type",
    "NAICS": "naics",
    "NAICS_Description": "naics_description",
    "AwardeeOrRecipientUniqueIdentifier": "awardee_or_recipient_uniqu",
    "UltimateParentLegalEntityName": "ultimate_parent_legal_enti",
    "UltimateParentUniqueIdentifier": "ultimate_parent_unique_ide",
    "AwardDescription": "award_description",
    "PrimaryPlaceOfPerformanceZIP+4": "place_of_performance_zip4a",
    "PrimaryPlaceOfPerformanceCongressionalDistrict": "place_of_performance_congr",
    "AwardeeOrRecipientLegalEntityName": "awardee_or_recipient_legal",
    "LegalEntityCityName": "legal_entity_city_name",
    "LegalEntityStateCode": "legal_entity_state_code",
    "LegalEntityZIP+4": "legal_entity_zip4",
    "LegalEntityCongressionalDistrict": "legal_entity_congressional",
    "LegalEntityAddressLine1": "legal_entity_address_line1",
    "LegalEntityAddressLine2": "legal_entity_address_line2",
    "LegalEntityAddressLine3": "legal_entity_address_line3",
    "LegalEntityCountryCode": "legal_entity_country_code",
    "LegalEntityCountryName": "legal_entity_country_name",
    "PeriodOfPerformanceStartDate": "period_of_performance_star",
    "PeriodOfPerformanceCurrentEndDate": "period_of_performance_curr",
    "PeriodOfPerfPotentialEndDate": "period_of_perf_potential_e",
    "OrderingPeriodEndDate": "ordering_period_end_date",
    "ActionDate": "action_date",
    "ActionType": "action_type",
    "FederalActionObligation": "federal_action_obligation",
    "CurrentTotalValueAwardAmount": "current_total_value_award",
    "PotentialTotalValueAwardAmount": "potential_total_value_awar",
    "FundingSubTierAgencyCode": "funding_sub_tier_agency_co",
    "FundingSubTierAgencyName": "funding_sub_tier_agency_na",
    "FundingOfficeCode": "funding_office_code",
    "FundingOfficeName": "funding_office_name",
    "AwardingOfficeCode": "awarding_office_code",
    "AwardingOfficeName": "awarding_office_name",
    "Referenced IDV Agency Identifier": "referenced_idv_agency_iden",
    "FundingAgencyCode": "funding_agency_code",
    "FundingAgencyName": "funding_agency_name",
    "PrimaryPlaceOfPerformanceLocationCode": "place_of_performance_locat",
    "PrimaryPlaceOfPerformanceStateCode": "place_of_performance_state",
    "PrimaryPlaceOfPerformanceCountryCode": "place_of_perform_country_c",
    "IDV_Type": "idv_type",
    "Vendor Doing As Business Name": "vendor_doing_as_business_n",
    "Vendor Phone Number": "vendor_phone_number",
    "Vendor Fax Number": "vendor_fax_number",
    "Multiple or Single Award IDV": "multiple_or_single_award_i",
    "Type of IDC": "type_of_idc",
    "A-76 FAIR Act Action": "a_76_fair_act_action",
    "DoD Claimant Program Code": "dod_claimant_program_code",
    "Clinger-Cohen Act Planning Compliance": "clinger_cohen_act_planning",
    "Commercial Item Acquisition Procedures": "commercial_item_acquisitio",
    "Commercial Item Test Program": "commercial_item_test_progr",
    "Consolidated Contract": "consolidated_contract",
    "Contingency Humanitarian or Peacekeeping Operation": "contingency_humanitarian_o",
    "Contract Bundling": "contract_bundling",
    "Contract Financing": "contract_financing",
    "Contracting Officer's Determination of Business Size": "contracting_officers_deter",
    "Cost Accounting Standards Clause": "cost_accounting_standards",
    "Cost or Pricing Data": "cost_or_pricing_data",
    "Country of Product or Service Origin": "country_of_product_or_serv",
    "Davis Bacon Act": "davis_bacon_act",
    "Evaluated Preference": "evaluated_preference",
    "Extent Competed": "extent_competed",
    "FedBizOpps": "fed_biz_opps",
    "Foreign Funding": "foreign_funding",
    "Government Furnished Equipment GFE and Government Furnished Property GFP": "government_furnished_equip",
    "Information Technology Commercial Item Category": "information_technology_com",
    "Interagency Contracting Authority": "interagency_contracting_au",
    "Local Area Set Aside": "local_area_set_aside",
    "Major program": "major_program",
    "Purchase Card as Payment Method": "purchase_card_as_payment_m",
    "Multi Year Contract": "multi_year_contract",
    "National Interest Action": "national_interest_action",
    "Number of Actions": "number_of_actions",
    "Number of Offers Received": "number_of_offers_received",
    "Other Statutory Authority": "other_statutory_authority",
    "Performance-Based Service Acquisition": "performance_based_service",
    "Place of Manufacture": "place_of_manufacture",
    "Price Evaluation Adjustment Preference Percent Difference": "price_evaluation_adjustmen",
    "Product or Service Code": "product_or_service_code",
    "Program Acronym": "program_acronym",
    "Other than Full and Open Competition": "other_than_full_and_open_c",
    "Recovered Materials/Sustainability": "recovered_materials_sustai",
    "Research": "research",
    "Sea Transportation": "sea_transportation",
    "Service Contract Act": "service_contract_act",
    "Small Business Competitiveness Demonstration Program": "small_business_competitive",
    "Solicitation Identifier": "solicitation_identifier",
    "Solicitation Procedures": "solicitation_procedures",
    "Fair Opportunity Limited Sources": "fair_opportunity_limited_s",
    "Subcontracting Plan": "subcontracting_plan",
    "Program, System, or Equipment Code": "program_system_or_equipmen",
    "Type Set Aside": "type_set_aside",
    "EPA-Designated Product": "epa_designated_product",
    "Walsh Healey Act": "walsh_healey_act",
    "Transaction Number": "transaction_number",
    "SAM Exception": "sam_exception",
    "City Local Government": "city_local_government",
    "County Local Government": "county_local_government",
    "Inter-Municipal Local Government": "inter_municipal_local_gove",
    "Local Government Owned": "local_government_owned",
    "Municipality Local Government": "municipality_local_governm",
    "School District Local Government": "school_district_local_gove",
    "Township Local Government": "township_local_government",
    "U.S. State Government": "us_state_government",
    "U.S. Federal Government": "us_federal_government",
    "Federal Agency": "federal_agency",
    "Federally Funded Research and Development Corp": "federally_funded_research",
    "U.S. Tribal Government": "us_tribal_government",
    "Foreign Government": "foreign_government",
    "Community Developed Corporation Owned Firm": "community_developed_corpor",
    "Labor Surplus Area Firm": "labor_surplus_area_firm",
    "Corporate Entity Not Tax Exempt": "corporate_entity_not_tax_e",
    "Corporate Entity Tax Exempt": "corporate_entity_tax_exemp",
    "Partnership or Limited Liability Partnership": "partnership_or_limited_lia",
    "Sole Proprietorship": "sole_proprietorship",
    "Small Agricultural Cooperative": "small_agricultural_coopera",
    "International Organization": "international_organization",
    "U.S. Government Entity": "us_government_entity",
    "Emerging Small business": "emerging_small_business",
    "8a Program Participant": "8a_program_participant",
    "SBA Certified 8 a Joint Venture": "sba_certified_8_a_joint_ve",
    "DoT Certified Disadvantaged Business Enterprise": "dot_certified_disadvantage",
    "Self-Certified Small Disadvantaged Business": "self_certified_small_disad",
    "Historically Underutilized Business Zone HUBZone Firm": "historically_underutilized",
    "Small Disadvantaged Business": "small_disadvantaged_busine",
    "The AbilityOne Program": "the_ability_one_program",
    "Historically Black College or University": "historically_black_college",
    "1862 Land grant College": "1862_land_grant_college",
    "1890 land grant College": "1890_land_grant_college",
    "1994 Land Grant College": "1994_land_grant_college",
    "Minority Institution": "minority_institution",
    "Private University or College ": "private_university_or_coll",
    "School of Forestry": "school_of_forestry",
    "State Controlled Institution of Higher Learning": "state_controlled_instituti",
    "Tribal College": "tribal_college",
    "Veterinary College": "veterinary_college",
    "Educational Institution": "educational_institution",
    "Alaskan Native Servicing Institution": "alaskan_native_servicing_i",
    "Community Development Corporation": "community_development_corp",
    "Native Hawaiian Servicing Institution": "native_hawaiian_servicing",
    "Domestic Shelter": "domestic_shelter",
    "Manufacturer of Goods": "manufacturer_of_goods",
    "Hospital Flag": "hospital_flag",
    "Veterinary Hospital": "veterinary_hospital",
    "Hispanic Servicing Institution": "hispanic_servicing_institu",
    "Foundation": "foundation",
    "Woman Owned business": "woman_owned_business",
    "Minority Owned Business": "minority_owned_business",
    "Women Owned Small Business": "women_owned_small_business",
    "Economically Disadvantaged Women Owned Small Business": "economically_disadvantaged",
    "Joint Venture Women Owned Small Business": "joint_venture_women_owned",
    "Joint Venture Economically Disadvantaged Women Owned Small Business": "joint_venture_economically",
    "Veteran Owned Business": "veteran_owned_business",
    "Service Disabled Veteran Owned Business": "service_disabled_veteran_o",
    "Contracts": "contracts",
    "Grants": "grants",
    "Receives Contracts and Grants": "receives_contracts_and_gra",
    "Airport Authority": "airport_authority",
    "Council of Governments": "council_of_governments",
    "Housing Authorities Public/Tribal": "housing_authorities_public",
    "Interstate Entity": "interstate_entity",
    "Planning Commission": "planning_commission",
    "Port Authority": "port_authority",
    "Transit Authority": "transit_authority",
    "Subchapter S Corporation": "subchapter_s_corporation",
    "Limited Liability Corporation": "limited_liability_corporat",
    "Foreign Owned and Located": "foreign_owned_and_located",
    "American Indian Owned Business": "american_indian_owned_busi",
    "Alaskan Native Owned Corporation or Firm": "alaskan_native_owned_corpo",
    "Indian Tribe Federally Recognized": "indian_tribe_federally_rec",
    "Native Hawaiian Owned Business": "native_hawaiian_owned_busi",
    "Tribally Owned Business": "tribally_owned_business",
    "Asian Pacific American Owned business": "asian_pacific_american_own",
    "Black American Owned Business": "black_american_owned_busin",
    "Hispanic American Owned Business": "hispanic_american_owned_bu",
    "Native American Owned Business": "native_american_owned_busi",
    "Subcontinent Asian Asian - Indian American Owned Business": "subcontinent_asian_asian_i",
    "Other Minority Owned Business": "other_minority_owned_busin",
    "For Profit Organization": "for_profit_organization",
    "Nonprofit Organization": "nonprofit_organization",
    "Other Not For Profit Organization": "other_not_for_profit_organ",
    "U.S. Local Government": "us_local_government",
    "Referenced IDV Modification Number": "referenced_idv_modificatio",
    "Undefinitized Action": "undefinitized_action",
    "Domestic or Foreign Entity": "domestic_or_foreign_entity",
    "ActionType": "action_type",
    "AdjustmentsToUnobligatedBalanceBroughtForward": "adjustments_to_unobligated",
    "AgencyIdentifier": "agency_identifier",
    "AllocationTransferAgencyIdentifier": "allocation_transfer_agency",
    "AssistanceType": "assistance_type",
    "AvailabilityTypeCode": "availability_type_code",
    "AwardReportMonth": "award_report_month",
    "AwardReportYear": "award_report_year",
    "BeginningPeriodOfAvailability": "beginning_period_of_availa",
    "BorrowingAuthorityAmountTotal": "borrowing_authority_amount",
    "BudgetAuthorityAppropriatedAmount": "budget_authority_appropria",
    "BudgetAuthorityAvailableAmountTotal": "budget_authority_available",
    "BudgetAuthorityUnobligatedBalanceBroughtForward": "budget_authority_unobligat",
    "BusinessFundsIndicator": "business_funds_indicator",
    "BusinessTypes": "business_types",
    "ByDirectReimbursableFundingSource": "by_direct_reimbursable_fun",
    "CFDA_Number": "cfda_number",
    "CFDA_NumberAndTitle": "cfda_number_and_title",
    "CFDA_Title": "cfda_title",
    "ContractAuthorityAmountTotal": "contract_authority_amount",
    "CorrectionLateDeleteIndicator": "correction_late_delete_ind",
    "DeobligationsRecoveriesRefundsByTAS": "deobligations_recoveries_r",
    "DeobligationsRecoveriesRefundsOfPriorYearByAward": "deobligations_recov_by_awa",
    "DeobligationsRecoveriesRefundsOfPriorYearByProgramObjectClass": "deobligations_recov_by_pro",
    "EndingPeriodOfAvailability": "ending_period_of_availabil",
    "FaceValueLoanGuarantee": "face_value_loan_guarantee",
    "FAIN": "fain",
    "FiscalYearAndQuarterCorrection": "fiscal_year_and_quarter_co",
    "GrossOutlayAmountByAward": "gross_outlay_amount_by_awa",
    "GrossOutlayAmountByProgramObjectClass": "gross_outlay_amount_by_pro",
    "GrossOutlayAmountByTAS": "gross_outlay_amount_by_tas",
    "GrossOutlaysDeliveredOrdersPaidTotal": "gross_outlays_delivered_or",
    "GrossOutlaysUndeliveredOrdersPrepaidTotal": "gross_outlays_undelivered",
    "HighCompOfficerAmount": "high_comp_officer_amount",
    "HighCompOfficerFirstName": "high_comp_officer_first_na",
    "HighCompOfficerFullName": "high_comp_officer_full_nam",
    "HighCompOfficerLastName": "high_comp_officer_last_nam",
    "HighCompOfficerMiddleInitial": "high_comp_officer_middle_i",
    "LegalEntityCityCode": "legal_entity_city_code",
    "LegalEntityCountyCode": "legal_entity_county_code",
    "LegalEntityCountyName": "legal_entity_county_name",
    "LegalEntityForeignCityName": "legal_entity_foreign_city",
    "LegalEntityForeignPostalCode": "legal_entity_foreign_posta",
    "LegalEntityForeignProvinceName": "legal_entity_foreign_provi",
    "LegalEntityStateName": "legal_entity_state_name",
    "LegalEntityZIP5": "legal_entity_zip5",
    "LegalEntityZIPLast4": "legal_entity_zip_last4",
    "MainAccountCode": "main_account_code",
    "NonFederalFundingAmount": "non_federal_funding_amount",
    "ObjectClass": "object_class",
    "ObligationsDeliveredOrdersUnpaidTotal": "obligations_delivered_orde",
    "ObligationsIncurredByProgramObjectClass": "obligations_incurred_by_pr",
    "ObligationsIncurredTotalByAward": "obligations_incurred_byawa",
    "ObligationsIncurredTotalByTAS": "obligations_incurred_total",
    "ObligationsUndeliveredOrdersUnpaidTotal": "obligations_undelivered_or",
    "OriginalLoanSubsidyCost": "original_loan_subsidy_cost",
    "OtherBudgetaryResourcesAmount": "other_budgetary_resources",
    "PrimaryPlaceOfPerformanceAddressLine1": "place_of_performance_addre",
    "PrimaryPlaceOfPerformanceCityName": "place_of_performance_city",
    "PrimaryPlaceOfPerformanceCode": "place_of_performance_code",
    "PrimaryPlaceOfPerformanceCountryName": "place_of_perform_country_n",
    "PrimaryPlaceOfPerformanceCountyName": "place_of_perform_county_na",
    "PrimaryPlaceOfPerformanceForeignLocationDescription": "place_of_performance_forei",
    "PrimaryPlaceOfPerformanceStateName": "place_of_perform_state_nam",
    "PrimaryPlaceOfPerformanceZIP+4": "place_of_performance_zip4",
    "PrimeAwardReportId": "prime_award_report_id",
    "ProgramActivityCode": "program_activity_code",
    "ProgramActivityName": "program_activity_name",
    "RecModelQuestion1": "rec_model_question1",
    "RecModelQuestion2": "rec_model_question2",
    "RecordType": "record_type",
    "SAI_Number": "sai_number",
    "SpendingAuthorityFromOffsettingCollectionsAmountTotal": "spending_authority_from_of",
    "StatusOfBudgetaryResourcesTotal": "status_of_budgetary_resour",
    "SubAccountCode": "sub_account_code",
    "SubawardeeBusinessType": "subawardee_business_type",
    "SubAwardeeOrRecipientLegalEntityName": "sub_awardee_or_recipient_l",
    "SubAwardeeOrRecipientUniqueIdentifier": "sub_awardee_or_recipient_u",
    "SubAwardeeUltimateParentLegalEntityName": "sub_awardee_ultimate_paren",
    "SubAwardeeUltimateParentUniqueIdentifier": "sub_awardee_ultimate_pa_id",
    "SubawardNumber": "subaward_number",
    "SubcontractAwardAmount": "subcontract_award_amount",
    "TotalFundingAmount": "total_funding_amount",
    "TransactionObligatedAmount": "transaction_obligated_amou",
    "UnobligatedBalance": "unobligated_balance",
    "URI": "uri",
    "USSGL480100_UndeliveredOrdersObligationsUnpaid": "ussgl480100_undelivered_or",
    "USSGL480200_UndeliveredOrdersObligationsPrepaidAdvanced": "ussgl480200_undelivered_or",
    "USSGL483100_UndeliveredOrdersObligationsTransferredUnpaid": "ussgl483100_undelivered_or",
    "USSGL483200_UndeliveredOrdersObligationsTransferredPrepaidAdvanced": "ussgl483200_undelivered_or",
    "USSGL487100_DownwardAdjustmentsOfPriorYearUnpaidUndeliveredOrdersObligationsRecoveries": "ussgl487100_downward_adjus",
    "USSGL487200_DownwardAdjustmentsOfPriorYearPrepaidAdvancedUndeliveredOrdersObligationsRefundsCollected": "ussgl487200_downward_adjus",
    "USSGL488100_UpwardAdjustmentsOfPriorYearUndeliveredOrdersObligationsUnpaid": "ussgl488100_upward_adjustm",
    "USSGL488200_UpwardAdjustmentsOfPriorYearUndeliveredOrdersObligationsPrepaidAdvanced": "ussgl488200_upward_adjustm",
    "USSGL490100_DeliveredOrdersObligationsUnpaid": "ussgl490100_delivered_orde",
    "USSGL490200_DeliveredOrdersObligationsPaid ": "ussgl490200_delivered_orde",
    "USSGL490800_AuthorityOutlayedNotYetDisbursed": "ussgl490800_authority_outl",
    "USSGL493100_DeliveredOrdersObligationsTransferredUnpaid": "ussgl493100_delivered_orde",
    "USSGL497100_DownwardAdjustmentsOfPriorYearUnpaidDeliveredOrdersObligationsRecoveries": "ussgl497100_downward_adjus",
    "USSGL497200_DownwardAdjustmentsOfPriorYearPaidDeliveredOrdersObligationsRefundsCollected": "ussgl497200_downward_adjus",
    "USSGL498100_Upward AdjustmentsOfPriorYearDeliveredOrdersObligationsUnpaid  ": "ussgl498100_upward_adjustm",
    "USSGL498200_UpwardAdjustmentsOfPriorYearDeliveredOrdersObligationsPaid ": "ussgl498200_upward_adjustm",
}

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
    "BudgetAuthorityUnobligatedBalanceBroughtForward_FYB": "budget_authority",
    "AdjustmentsToUnobligatedBalanceBroughtForward_CPE": "budget_authority",
    "BudgetAuthorityAppropriatedAmount_CPE": "budget_authority",
    "OtherBudgetaryResourcesAmount_CPE": "budget_authority",
    "BudgetAuthorityAvailableAmountTotal_CPE": "budget_authority",
    "ObligationsIncurredTotalByTAS_CPE": "budgetary_resources",
    "GrossOutlayAmountByTAS_CPE": "budgetary_resources",
    "ContractAuthorityAmountTotal_CPE": "budget_authority",
    "BorrowingAuthorityAmountTotal_CPE": "budget_authority",
    "SpendingAuthorityfromOffsettingCollectionsAmountTotal_CPE": "budget_authority",
    "StatusOfBudgetaryResourcesTotal_CPE": "budgetary_resources",
    "AllocationTransferAgencyIdentifier": "tas",
    "AvailabilityTypeCode": "tas",
    "EndingPeriodOfAvailability": "tas",
    "BeginningPeriodOfAvailability": "tas",
    "AgencyIdentifier": "tas",
    "SubAccountCode": "tas",
    "MainAccountCode": "tas",
    "DeobligationsRecoveriesRefundsByTAS_CPE": "budgetary_resources",
    "UnobligatedBalance_CPE": "budgetary_resources",
    "DeobligationsRecoveriesRefundsdOfPriorYearByProgramObjectClass_CPE": "obligations_incurred",
    "GrossOutlayAmountByProgramObjectClass_CPE": "gross_outlays",
    "GrossOutlayAmountByProgramObjectClass_FYB": "gross_outlays",
    "GrossOutlaysDeliveredOrdersPaidTotal_FYB": "gross_outlays",
    "GrossOutlaysDeliveredOrdersPaidTotal_CPE": "gross_outlays",
    "GrossOutlaysUndeliveredOrdersPrepaidTotal_CPE": "gross_outlays",
    "GrossOutlaysUndeliveredOrdersPrepaidTotal_FYB": "gross_outlays",
    "ObligationsDeliveredOrdersUnpaidTotal_FYB": "obligations_incurred",
    "ObligationsDeliveredOrdersUnpaidTotal_CPE": "obligations_incurred",
    "ObligationsIncurredByProgramObjectClass_CPE": "obligations_incurred",
    "ObligationsUndeliveredOrdersUnpaidTotal_FYB": "obligations_incurred",
    "ObligationsUndeliveredOrdersUnpaidTotal_CPE": "obligations_incurred"
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
                if col == "complete":
                    columns = columns + _SHORTCUT_COLUMNS[col]
                else:
                    # If a field is in the shortcut, we must verify it exists
                    # in the requested table
                    intersection = list(set.intersection(set(_SHORTCUT_COLUMNS[col]), set(column_array)))
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
    page = 1
    page_length = 1000

    if "columns" in body:
        columns = body["columns"]
    if "filters" in body:
        for clause in body["filters"]:
            if not clause['operation'] in _OPERATORS.keys():
                raise Exception("Operation " + clause['operation'] + " not recognized")
            filters.append([clause['fieldname'], _OPERATORS[clause['operation']], clause['value']])
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
