# Umbrella
API calls to Cisco Umbrella

## Restrictions
  Only supports calls to the reporting API at this time

## Authentication
  Authentication is handled by the Auth class in core.py

### API Keys
  This requires an API key and an API secret, which can be generated from the Umbrella portal  
  https://docs.umbrella.com/umbrella-user-guide/docs/add-umbrella-api-keys

  The Auth class expects the API key and API secret to be stored in the DNS_API_KEY and DNS_API_SECRET environment variables  

### Generating a Token
  1. Instantiate the Auth class
  2. Call the GetToken() method

```
import core
auth_api = core.Auth()
auth_api.GetToken()
```

### Token Refresh
  Tokens expire after 60 minutes  
  The CheckExpiry() method is used to see if the token needs to be refreshed, or has already expired  
  This could be scheduled through a thread, or it could be run on demand.  

## API Calls
  The ApiCall class in core.py provides the template class to make API calls  
  Other classes can inherit this to customise these calls  
  The CheckExpiry() method of the Auth class is called for each API call, to check if the token is valid  

### Default Parameters
  There are three values that have defaults set. These are:
* 'from'
* 'to'
* 'offset'

  The offset will always default to zero. This is used for pagination.  
  'from' and 'to' are date/time ranges. These will default to the last 24 hours.  
  When instantiating the API class, these defaults can be overridden with other defaults that are used for the lifetime of the class.  
  These can also be overridden per method call, for example, for pagination.  
  

## Reporting
### Structure
  The Reports class in reports.py collects reporting information  
  This class inherits the ApiCall class from core.py  

### Usage
  This class has several methods to collect basic information:
  
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

### Filtering
  Optional parameters can be passed to each method to filter the results.  
  If ommitted, default values are used.  
* 'timefrom' - The starting time of the query  
* 'timeto' - The ending time of the query  
* 'size' - The number of results to return  
* 'page' - The result number to start with  

Formats for time filtering are:
* Unix epoch as a string
* Custom relative strings, referencing minutes, hours, and days. Notice, these strings need to start with the minus character:  
  - '-5minutes'
  - '-1hour'
  - '-30days'
  - '-2weeks'
* The string 'now' for the current time  
  https://developer.cisco.com/docs/cloud-security/#!api-reference-reports-reporting-overview/request-query-parameters
  
