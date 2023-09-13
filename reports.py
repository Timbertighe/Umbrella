"""
Umbrella reports

Usage:
    Import this file into your project
    Instantiate the Reports class
    Call the method you want to use

Authentication:
    Need to instantiate the auth class first

Restrictions:
    Package list in requirements.txt

To Do:
    Update anything category related to not show deprecated categories

Author:
    Luke Robertson - September 2023
"""


# import requests
import core


class Reports(core.ApiCall):
    """
    Get security information from Umbrella

    This class inherits the ApiCall class
    Methods will send a request to the Umbrella API

    Attributes
    ----------
    None

    Methods
    -------
    Summaries:
        summary()
        summary_by_category()
        summary_by_destination()
        summary_by_rule()

    Top:
        top_identities()
        top_destinations()
        top_categories()
        top_event_types()
        top_dns_query_types()
        top_files()
        top_threats()
        top_threat_types()
        top_ips()
        top_urls()

    Other:
        activity()
        identity_distribution()
        total_requests()
    """

    def __init__(self, auth, **kwargs):
        """
        Constructs the class

        Optionally set default parameters such as time range and limit

        Parameters
        ----------
        auth : class
            The auth class, which contains the bearer token

        limit : int
            Set the default limit for the number of results returned

        from : int or string
            Set the default 'from' time for the query

        to : int or string
            Set the default 'to' time for the query

        Raises
        ------
        None
        """

        # Inherit the API call class
        super().__init__(auth, **kwargs)

        # The base URI
        self.report_uri = 'api.umbrella.com/reports/v2'

    # Get a summary of activity
    def summary(self, **kwargs):
        return self.send_request('/summary', **kwargs)

    # Get a summary of activity by category
    def summary_by_category(self, **kwargs):
        return self.send_request('/summaries-by-category', **kwargs)

    # Get a summary of activity by destination
    def summary_by_destination(self, **kwargs):
        return self.send_request('/summaries-by-destination', **kwargs)

    # Get a summary of activity by intrusion rule
    def summary_by_rule(self, **kwargs):
        return self.send_request('/summaries-by-rule/intrusion', **kwargs)

    # Get a list of top identities
    def top_identities(self, **kwargs):
        return self.send_request('/top-identities', **kwargs)

    # Get top destinations
    def top_destinations(self, **kwargs):
        return self.send_request('/top-destinations', **kwargs)

    # Get top categories
    def top_categories(self, **kwargs):
        return self.send_request('/top-categories', **kwargs)

    # Get top event types
    def top_event_types(self, **kwargs):
        return self.send_request('/top-eventtypes', **kwargs)

    # Get top dns query types
    def top_dns_query_types(self, **kwargs):
        return self.send_request('/top-dns-query-types', **kwargs)

    # Get top files
    def top_files(self, **kwargs):
        return self.send_request('/top-files', **kwargs)

    # Get top threats
    def top_threats(self, **kwargs):
        return self.send_request('/top-threats', **kwargs)

    # Get top threat types
    def top_threat_types(self, **kwargs):
        return self.send_request('/top-threat-types', **kwargs)

    # Get top IPs
    def top_ips(self, **kwargs):
        return self.send_request('/top-ips', **kwargs)

    # Get top URLs
    def top_urls(self, **kwargs):
        return self.send_request('/top-urls', **kwargs)

    # Get a list of activity
    def activity(self, **kwargs):
        return self.send_request('/activity', **kwargs)

    # Get identity distribution
    def identity_distribution(self, **kwargs):
        return self.send_request('/identity-distribution', **kwargs)

    # Get total requests
    def total_requests(self, **kwargs):
        return self.send_request('/total-requests', **kwargs)
