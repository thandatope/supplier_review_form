"""
Settings for response scores/weightings
Probably move to json, ini or something
"""

# Quality Scores

quality_company_change = -5
quality_no_company_change = 0
quality_accreditation_change = -10
quality_no_accreditation_change = 0
quality_no_attachments = -10
quality_has_attachments = 5

# Business scores

business_company_change = -5
business_no_company_change = 0
business_no_attachments = -5
business_has_attachments = 5

# Other scores

other_company_change = -5
other_no_company_change = 0
other_no_attachments = 0
other_has_attachments = 0
