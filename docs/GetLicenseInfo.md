# GetLicenseInfo API

Retrieves the application license information including company details, licensed user counts, subscription dates, and feature flags. This API is restricted to system administrators with the `ViewLicenseInformation` permission.

## Endpoint

```
/srv.asmx/GetLicenseInfo
```

## Methods

- **GET** `/srv.asmx/GetLicenseInfo?authenticationTicket=...`
- **POST** `/srv.asmx/GetLicenseInfo` (form data)
- **SOAP** Action: `http://tempuri.org/GetLicenseInfo`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true">
  <LicenseInfo>
    <CompanyName>Acme Corporation</CompanyName>
    <Address>123 Main Street, Suite 100</Address>
    <Country>United States</Country>
    <ContactName>John Smith</ContactName>
    <PhoneNumber>555-0100</PhoneNumber>
    <EmailAddress>admin@acme.com</EmailAddress>
    <IsConcurrent>false</IsConcurrent>
    <UserCount>50</UserCount>
    <ActiveUserCount>35</ActiveUserCount>
    <DisabledUserCount>5</DisabledUserCount>
    <DatabaseType>SQLServer</DatabaseType>
    <AuthenticationType>INFOROUTER</AuthenticationType>
    <MaxDocumentCount>0</MaxDocumentCount>
    <MaxLibraryCount>0</MaxLibraryCount>
    <AnonymousAccess>true</AnonymousAccess>
    <Workflow>true</Workflow>
    <TrialCopy>false</TrialCopy>
    <ExpirationDate>2027-12-31T00:00:00</ExpirationDate>
    <SubscriptionStartDate>2025-01-01T00:00:00</SubscriptionStartDate>
    <SubscriptionEndDate>2027-12-31T00:00:00</SubscriptionEndDate>
  </LicenseInfo>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## LicenseInfo Properties

| Property | Type | Description |
|----------|------|-------------|
| `CompanyName` | string | Licensed company name |
| `Address` | string | Company address |
| `Country` | string | Company country |
| `ContactName` | string | Primary contact name |
| `PhoneNumber` | string | Contact phone number |
| `EmailAddress` | string | Contact email address |
| `IsConcurrent` | boolean | Whether the license is concurrent (shared seats) or named-user |
| `UserCount` | integer | Total number of licensed user seats |
| `ActiveUserCount` | integer | Number of currently active users (authors + readonly) |
| `DisabledUserCount` | integer | Number of disabled user accounts |
| `DatabaseType` | string | Licensed database type (e.g., SQLServer, MySQL, Oracle) |
| `AuthenticationType` | string | Authentication type (e.g., INFOROUTER, NATIVE) |
| `MaxDocumentCount` | integer | Maximum number of documents allowed (0 = unlimited) |
| `MaxLibraryCount` | integer | Maximum number of libraries allowed (0 = unlimited) |
| `AnonymousAccess` | boolean | Whether anonymous (guest) access is licensed |
| `Workflow` | boolean | Whether workflow features are licensed |
| `TrialCopy` | boolean | Whether this is a trial license |
| `ExpirationDate` | DateTime | License expiration date (ISO 8601) |
| `SubscriptionStartDate` | DateTime | Subscription start date (ISO 8601) |
| `SubscriptionEndDate` | DateTime | Subscription end date (ISO 8601) |

## Required Permissions

- Administrators only: User must have `ViewLicenseInformation` admin permission
- Non-admin users will receive an insufficient rights error

## Use Cases

1. **License Monitoring**
   - Check remaining user seat capacity
   - Monitor subscription expiration dates
   - Verify licensed features

2. **Administration Dashboard**
   - Display license status on admin control panel
   - Show active vs. licensed user counts
   - Alert on approaching subscription expiration

3. **Compliance Reporting**
   - Document license entitlements
   - Audit user seat usage

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetLicenseInfo?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetLicenseInfo HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetLicenseInfo"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetLicenseInfo xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetLicenseInfo>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getLicenseInfo() {
    const ticket = getUserAuthTicket();
    const url = `/srv.asmx/GetLicenseInfo?authenticationTicket=${encodeURIComponent(ticket)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const info = xmlDoc.querySelector("LicenseInfo");
        return {
            companyName: info.querySelector("CompanyName").textContent,
            userCount: parseInt(info.querySelector("UserCount").textContent),
            activeUserCount: parseInt(info.querySelector("ActiveUserCount").textContent),
            disabledUserCount: parseInt(info.querySelector("DisabledUserCount").textContent),
            isConcurrent: info.querySelector("IsConcurrent").textContent === "true",
            workflow: info.querySelector("Workflow").textContent === "true",
            trialCopy: info.querySelector("TrialCopy").textContent === "true",
            expirationDate: info.querySelector("ExpirationDate").textContent,
            subscriptionEndDate: info.querySelector("SubscriptionEndDate").textContent
        };
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function displayLicenseStatus() {
    try {
        const license = await getLicenseInfo();
        const availableSeats = license.userCount - license.activeUserCount;

        console.log(`Company: ${license.companyName}`);
        console.log(`Licensed seats: ${license.userCount} (${availableSeats} available)`);
        console.log(`Active users: ${license.activeUserCount}`);
        console.log(`Subscription ends: ${license.subscriptionEndDate}`);
        console.log(`Workflow enabled: ${license.workflow}`);
    } catch (error) {
        console.error("Failed to get license info:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetLicenseInfoAsync(authTicket);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            var info = root.Element("LicenseInfo");
            var license = new
            {
                CompanyName = info.Element("CompanyName")?.Value ?? "",
                UserCount = int.Parse(info.Element("UserCount")?.Value ?? "0"),
                ActiveUserCount = int.Parse(info.Element("ActiveUserCount")?.Value ?? "0"),
                DisabledUserCount = int.Parse(info.Element("DisabledUserCount")?.Value ?? "0"),
                IsConcurrent = info.Element("IsConcurrent")?.Value == "true",
                Workflow = info.Element("Workflow")?.Value == "true",
                TrialCopy = info.Element("TrialCopy")?.Value == "true",
                SubscriptionEndDate = info.Element("SubscriptionEndDate")?.Value ?? ""
            };

            Console.WriteLine($"Company: {license.CompanyName}");
            Console.WriteLine($"Licensed seats: {license.UserCount}");
            Console.WriteLine($"Active users: {license.ActiveUserCount}");
            Console.WriteLine($"Subscription ends: {license.SubscriptionEndDate}");
        }
        else
        {
            var error = root.Attribute("error")?.Value;
            Console.WriteLine($"Error: {error}");
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Exception: {ex.Message}");
    }
}
```

## Notes

- **ActiveUserCount** is the sum of author users and readonly users.
- **MaxDocumentCount** and **MaxLibraryCount** of 0 means unlimited.
- **ExpirationDate**, **SubscriptionStartDate**, and **SubscriptionEndDate** are returned in ISO 8601 format.
- Boolean values (`IsConcurrent`, `AnonymousAccess`, `Workflow`, `TrialCopy`) are returned as lowercase strings ("true"/"false").
- License data is read from a `license.lic` file in the application configuration path.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | User does not have `ViewLicenseInformation` admin permission |

## Related APIs

- `UpdateApplicationLicense` - Update the application license
- `ServerInfo` - Get basic server information (no authentication required)
- `getApplicationParameters` - Get application parameters (role-based response)
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New in current version**: Provides programmatic access to license details for administration dashboards
- Admin-only for security reasons
