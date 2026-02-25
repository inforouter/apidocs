# GetCheckedoutDocumentsByUser API

Returns a list of checked out documents by the specified user. This API is similar to `GetCheckedoutDocuments` but allows querying documents for any user (with appropriate permissions).

## Endpoint

```
/srv.asmx/GetCheckedoutDocumentsByUser
```

## Methods

- **GET** `/srv.asmx/GetCheckedoutDocumentsByUser?authenticationTicket=...&userName=...&withpropertysets=...&withsecurity=...&withOwner=...&withVersions=...`
- **POST** `/srv.asmx/GetCheckedoutDocumentsByUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetCheckedoutDocumentsByUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `userName` | string | Yes | Username of the user whose checked out documents to retrieve |
| `withpropertysets` | boolean | No | Include custom property sets in the response |
| `withsecurity` | boolean | No | Include security/permission information |
| `withOwner` | boolean | No | Include document owner information |
| `withVersions` | boolean | No | Include version history information |

## Response Structure

### Success Response

```xml
<response success="true">
  <document id="123" name="report.docx" path="/Documents/report.docx"
            checkedOutBy="john.smith" checkedOutDate="2024-01-15T10:30:00"
            size="52480" extension="docx" ... />
  <document id="456" name="contract.pdf" path="/Legal/contract.pdf"
            checkedOutBy="john.smith" checkedOutDate="2024-01-14T14:20:00"
            size="128000" extension="pdf" ... />
</response>
```

### Empty Result Response

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Document Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | integer | Unique document identifier |
| `name` | string | Document file name |
| `path` | string | Full path to the document |
| `checkedOutBy` | string | Username who checked out the document |
| `checkedOutDate` | datetime | When the document was checked out |
| `size` | long | File size in bytes |
| `extension` | string | File extension without the dot |
| `description` | string | Document description |
| `version` | integer | Current version number |
| `created` | datetime | Document creation date |
| `modified` | datetime | Last modification date |

## Required Permissions

- User must be authenticated
- **Same user query**: If `userName` matches the current authenticated user, no additional permissions required
- **Different user query**: Requires `ListingAuditLogOfUser` permission on the target user

### Permission Matrix

| Scenario | Permission Required |
|----------|---------------------|
| Viewing own checked out documents | None (authenticated user) |
| Viewing another user's checked out documents | `ListingAuditLogOfUser` |

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetCheckedoutDocumentsByUser?authenticationTicket=abc123-def456&userName=john.smith&withpropertysets=false&withsecurity=false&withOwner=true&withVersions=false HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetCheckedoutDocumentsByUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=john.smith&withpropertysets=false&withsecurity=false&withOwner=true&withVersions=false
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetCheckedoutDocumentsByUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetCheckedoutDocumentsByUser xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>john.smith</userName>
      <withpropertysets>false</withpropertysets>
      <withsecurity>false</withsecurity>
      <withOwner>true</withOwner>
      <withVersions>false</withVersions>
    </GetCheckedoutDocumentsByUser>
  </soap:Body>
</soap:Envelope>
```

## Use Cases

1. **User Reports**
   - Generate reports of documents checked out by a specific user
   - Monitor document checkout activity across teams
   - Identify documents that may need to be checked in

2. **Administrative Oversight**
   - View checked out documents for users who are on leave
   - Audit document access patterns
   - Manage document locks across the organization

3. **Support Operations**
   - Help users identify their checked out documents
   - Troubleshoot document access issues
   - Assist with checkout/checkin workflows

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getCheckedoutDocumentsByUser(userName) {
    const ticket = getUserAuthTicket();

    const params = new URLSearchParams({
        authenticationTicket: ticket,
        userName: userName,
        withpropertysets: 'false',
        withsecurity: 'false',
        withOwner: 'true',
        withVersions: 'false'
    });

    const url = `/srv.asmx/GetCheckedoutDocumentsByUser?${params}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const documents = [];
        xmlDoc.querySelectorAll("document").forEach(doc => {
            documents.push({
                id: doc.getAttribute("id"),
                name: doc.getAttribute("name"),
                path: doc.getAttribute("path"),
                checkedOutBy: doc.getAttribute("checkedOutBy"),
                checkedOutDate: doc.getAttribute("checkedOutDate"),
                size: parseInt(doc.getAttribute("size"))
            });
        });
        return documents;
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage
const userDocs = await getCheckedoutDocumentsByUser("john.smith");
console.log(`User has ${userDocs.length} checked out documents`);
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetCheckedoutDocumentsByUserAsync(
            authTicket,
            "john.smith",
            withpropertysets: false,
            withsecurity: false,
            withOwner: true,
            withVersions: false);

        var root = XElement.Parse(response.ToString());
        if (root.Attribute("success")?.Value == "true")
        {
            var documents = root.Elements("document").Select(doc => new
            {
                Id = int.Parse(doc.Attribute("id")?.Value ?? "0"),
                Name = doc.Attribute("name")?.Value,
                Path = doc.Attribute("path")?.Value,
                CheckedOutBy = doc.Attribute("checkedOutBy")?.Value,
                CheckedOutDate = DateTime.Parse(doc.Attribute("checkedOutDate")?.Value ?? DateTime.MinValue.ToString())
            }).ToList();

            Console.WriteLine($"Found {documents.Count} checked out documents");
            foreach (var doc in documents)
            {
                Console.WriteLine($"  - {doc.Name} (checked out: {doc.CheckedOutDate:g})");
            }
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

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[921]Insufficient rights` | User does not have permission to view another user's documents |
| `User not found` | The specified username does not exist |

## Notes

- Documents are returned sorted by document name in ascending order
- Only documents that the target user has explicitly checked out are returned
- System checkout locks (automatic locks) are not included in the results
- The response includes full document metadata including path, size, and modification dates

## Related APIs

- `GetCheckedoutDocuments` - Get checked out documents for the current user
- `GetMyLockedDocuments` - Get documents locked by the current user
- `CheckoutDocument` - Check out a document for editing
- `CheckinDocument` - Check in a previously checked out document
- `UndoCheckoutDocument` - Cancel a document checkout

## Version History

- **New in current version**: Initial release of `GetCheckedoutDocumentsByUser` API
- Supports permission-based access control for viewing other users' documents

## See Also

- Control Panel UI: `UserReportDocuments.aspx` - User document report page
