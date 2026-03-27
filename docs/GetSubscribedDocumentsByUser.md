# GetSubscribedDocumentsByUser API

Returns a paginated list of documents that the specified user is subscribed to. This API is similar to `GetSubscriptions` but targets a specific user and supports pagination.

## Endpoint

```
/srv.asmx/GetSubscribedDocumentsByUser
```

## Methods

- **GET** `/srv.asmx/GetSubscribedDocumentsByUser?authenticationTicket=...&userName=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetSubscribedDocumentsByUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetSubscribedDocumentsByUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `userName` | string | Yes | Username of the user whose subscribed documents to retrieve |
| `startingRow` | integer | Yes | Zero-based index of the first row to return |
| `rowCount` | integer | Yes | Maximum number of documents to return in this page |

## Response Structure

### Success Response

```xml
<response success="true" recordCount="42" startingRow="0" rowCount="10">
  <document id="123" name="report.docx" path="/Documents/report.docx"
            size="52480" extension="docx" ... />
  <document id="456" name="policy.pdf" path="/Policies/policy.pdf"
            size="128000" extension="pdf" ... />
</response>
```

### Empty Result Response

```xml
<response success="true" recordCount="0" startingRow="0" rowCount="0" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Response Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `recordCount` | integer | Total number of subscribed documents for the user |
| `startingRow` | integer | The starting row index used in the request |
| `rowCount` | integer | Number of document records returned in this response |

## Document Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | integer | Unique document identifier |
| `name` | string | Document file name |
| `path` | string | Full path to the document |
| `size` | long | File size in bytes |
| `extension` | string | File extension without the dot |
| `description` | string | Document description |
| `version` | integer | Current version number |
| `created` | datetime | Document creation date |
| `modified` | datetime | Last modification date |

## Required Permissions

- User must be authenticated
- **Same user query**: If `userName` matches the current authenticated user, no additional permissions required
- **Different user query**: Requires administrative permissions to view another user's subscriptions

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetSubscribedDocumentsByUser?authenticationTicket=abc123-def456&userName=john.smith&startingRow=0&rowCount=25 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetSubscribedDocumentsByUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=john.smith&startingRow=0&rowCount=25
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetSubscribedDocumentsByUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetSubscribedDocumentsByUser xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>john.smith</userName>
      <startingRow>0</startingRow>
      <rowCount>25</rowCount>
    </GetSubscribedDocumentsByUser>
  </soap:Body>
</soap:Envelope>
```

## Use Cases

1. **User Reports**
   - Generate reports of documents a user is subscribed to
   - Audit subscription activity across teams

2. **Administrative Oversight**
   - Review document subscriptions for a given user
   - Manage notification workload for users

3. **Pagination**
   - Use `startingRow` and `rowCount` together to page through large subscription lists
   - Use `recordCount` from the response to determine total pages

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getSubscribedDocumentsByUser(userName, startingRow = 0, rowCount = 25) {
    const ticket = getUserAuthTicket();

    const params = new URLSearchParams({
        authenticationTicket: ticket,
        userName: userName,
        startingRow: startingRow,
        rowCount: rowCount
    });

    const response = await fetch(`/srv.asmx/GetSubscribedDocumentsByUser?${params}`);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const totalCount = parseInt(root.getAttribute("recordCount"));
        const documents = [];
        xmlDoc.querySelectorAll("document").forEach(doc => {
            documents.push({
                id: doc.getAttribute("id"),
                name: doc.getAttribute("name"),
                path: doc.getAttribute("path"),
                size: parseInt(doc.getAttribute("size"))
            });
        });
        return { totalCount, documents };
    } else {
        throw new Error(root.getAttribute("error"));
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    var response = await client.GetSubscribedDocumentsByUserAsync(
        authTicket,
        "john.smith",
        startingRow: 0,
        rowCount: 25);

    var root = XElement.Parse(response.ToString());
    if (root.Attribute("success")?.Value == "true")
    {
        int totalCount = int.Parse(root.Attribute("recordCount")?.Value ?? "0");
        var documents = root.Elements("document").Select(doc => new
        {
            Id = int.Parse(doc.Attribute("id")?.Value ?? "0"),
            Name = doc.Attribute("name")?.Value,
            Path = doc.Attribute("path")?.Value
        }).ToList();

        Console.WriteLine($"Total subscribed documents: {totalCount}");
        Console.WriteLine($"Returned in this page: {documents.Count}");
    }
    else
    {
        Console.WriteLine($"Error: {root.Attribute("error")?.Value}");
    }
}
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | User does not have permission to view another user's subscriptions |
| `User not found` | The specified username does not exist |

## Notes

- Documents are returned sorted by document name in ascending order
- Use `recordCount` from the response to implement pagination logic
- `rowCount` in the response reflects the actual number of records returned, which may be less than the requested `rowCount` on the last page

## Related APIs

- `GetSubscribedFoldersByUser` - Get subscribed folders for a specified user
- `GetSubscriptions` - Get subscribed documents and folders for the current user
- `AddUserToDocumentSubscribers` - Subscribe a user to a document
- `RemoveUserFromDocumentSubscribers` - Remove a user from a document subscription
- `RemoveAllSubscriptions` - Remove all subscriptions for a user
