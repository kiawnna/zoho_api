# Zoho Desk API Integration
## TEST CODEPIPELINE

This integration uses the Serverless Framework to deploy functions that interact with Zoho Desk's RESTful API.
An authentication layer is set up so that a all a user needs to pass in is the route in Zoho Desk they want to hit,
and the secret_id containing their OAuth2 information. All authentication is done using the OAuth2 flow, and is 
completely automated after an initial request with minimal user interaction.

## Instructions for Setup:

* Gather the below information from the Zoho Desk Developer portal and input into Secrets Manager as `json plaintext`, so that it is ready after you
generate an authorization code in step 2 (the code is only good for 10 minutes). Name your secret `zoho_auth`.
```
{
    "client_id": "From self-client",
    "client_secret": "From self-client,
    "redirect_uri": "from web client",
    "code": "Authorization code/grant token that is generated from self-client (scope to use is below)",
    "org_id": "from Zoho Desk API settings page"
}
```
* Initially, a self-client and web client will need to be created, even if the web client has a dummy redirect_uri
value. This is done from the Zoho Desk API's Developer platform. Use the self-client to generate an authorization code (named code in Secrets Manager) using the correct scope.
The below scope gives all access. If you only need some access, choose the correct scopes from below.
All scopes should be separated by commas, no spaces.
> Please note that `AAAServer.profile.ALL` **must** be included in
**all scopes**.

* You will also need to edit the `serverless.yaml` file.
    * Under `resources`, update the line `BucketName: InsertABucketNameHere` by choosing a bucket name to store the Zoho reports in. Bucket names must be unique globally.
    * Optionally: you can remove the schedule from each function and instead rely on manual execution of the lambdas. Currently, the non-Pro APIs are set to run every 4 hours.

```
Desk.tickets.ALL,Desk.activities.calls.READ,Desk.tasks.ALL,Desk.settings.ALL,Desk.search.READ,Desk.events.ALL,
Desk.articles.READ,Desk.articles.CREATE,Desk.articles.UPDATE,Desk.articles.DELETE,Desk.contacts.READ,Desk.contacts.WRITE,
Desk.contacts.UPDATE,Desk.contacts.CREATE,Desk.basic.READ,Desk.basic.CREATE,AAAServer.profile.ALL, Desk.activities.READ
```
* Enter the authorization code into the secret, saved with the key `code`.

## Instructions for calling Zoho Desk's API directly (in AWS Lambda, not in Postman)

* To call a route manually, you may or may not need to pass in a payload. The result will be stored in the S3 Bucket you chose in a previous step.

The following functions require a payload:
- `agent_time_entry`, : needs a valid department_id
    ```
    {
        "agent_id": "value for valid agent id"
    }
    ```
- `queue_by_status`: needs a ticket status to queue for
    ```
    {
        "status": "value for valid ticket status"
    }
    ```
- `threads` and `ticket_time_entry`: need a valid ticket_id
    ```
    {
        "ticket_id": "value for valid ticket id"
    }
    ```
- `customer_happiness`, `ticket_tags`, `notification-email_delivery_failures`, and `notification-pending_approvals`: need a valid department_id
    ```
    {
        "department_id": "value for valid department id"
    }
    ```
    > Pass in `allDepartment` instead to return the report for all departments. Check Zoho documentation to ensure this is available for each endpoint.

Some functions are not available unless an active Zoho Desk Pro plan is in place. These functions are:
- `queue_by_status`
- `ticket_time_entry`
- `customer_happiness`
- `agent_time_entry`

## Scheduled Events
This integration with Zoho's Desk API has scheduled events that call the following routes every 4 hours. Each time the
route is called, the resulting data is saved into a json file and stored in an S3 bucket with the API and timestamp as file prefixes.

Routes called once a day:
- Accounts (lists all accounts)
- Agents (lists all agents)
- Agent Time Entry (lists all time entries for a particular agent--Zoho Pro only)
- Calls (lists all calls)
- Contacts (lists all contacts)
- Customer Happiness (lists the customer happiness for all departments--Zoho Pro only)
- Departments (lists all departments)
- Notification (email delivery failures- lists all failures to deliver via email)
- Notification (pending approval- lists all pending approval notifications)
- Queue (lists all tickets of a certain status in queue--Zoho Pro only)
- Threads (lists all threads for a particular ticket)
- Ticket Tags (lists all available tags for tickets)
- Ticket Time Entry (lists all time entries for a particular ticket--Zoho Pro only)
- Ticket (lists all tickets)
