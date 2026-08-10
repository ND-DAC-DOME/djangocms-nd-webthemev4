"""Site chrome defaults until the Settings model lands in M3."""
from datetime import datetime


def site_defaults(request):
    return {
        "site_name": "ND Theme CMS",
        "site_description": "Notre Dame django CMS base template (NDT 4.0)",
        "site_tagline": "",
        "parent_unit": "University of Notre Dame",
        "parent_unit_url": "https://www.nd.edu/",
        "address": "",
        "phone": "",
        "fax": "",
        "email": "webhelp@nd.edu",
        "facebook_link": "",
        "twitter_link": "",
        "instagram_link": "",
        "youtube_link": "",
        "linkedin_link": "",
        "current_year": datetime.now().year,
        "site_search_domain": "siteurl.nd.edu",
    }
