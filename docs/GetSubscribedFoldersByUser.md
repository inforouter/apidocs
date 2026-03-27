# GetSubscribedFoldersByUser API

Returns a paginated list of folders that the specified user is subscribed to. This API is similar to `GetSubscriptions` but targets a specific user, returns folders only, and supports pagination.

## Endpoint

```
/srv.asmx/GetSubscribedFoldersByUser
```

## Methods

- **GET** `/srv.asmx/GetSubscribedFoldersByUser?authenticationTicket=...&userName=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetSubscribedFoldersByUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetSubscribedFoldersByUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `userName` | string | Yes | Username of the user whose subscribed folders to retrieve |
| `startingRow` | integer | Yes | Zero-based index of the first row to return |
| `rowCount` | integer | Yes | Maximum number of folders to return in this page |

## Response Structure

### Success Response

```xml
<response success="true" recordCount="15" startingRow="0" rowCount="10">
  <folder id="10" name="HR Policies" path="/Departments/HR Policies" ... />
  <folder id="25" name="Engineering" path="/Departments/Engineering" ... />
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
| `recordCount` | integer | Total number of subscribed folders for the user |
| `startingRow` | integer | The starting row index used in the request |
| `rowCount` | integer | Number of folder records returned in this response |

## Folder Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | integer | Unique folder identifier |
| `name` | string | Folder name |
| `path` | string | Full path to the folder |
| `created` | datetime | Folder creation date |
| `modified` | datetime | Last modification date |
| `description` | string | Folder description |

## Required Permissions

- User must be authenticated (anonymous users cannot perform this action)
- The target `userName` must exist in the system
- **Same user query**: If `userName` matches the current authenticated user, no additional permissions required
- **Different user query**: Requires administrative permissions to view another user's subscriptions

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetSubscribedFoldersByUser?authenticationTicket=abc123-def456&userName=john.smith&startingRow=0&rowCount=25 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetSubscribedFoldersByUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=john.smith&startingRow=0&rowCount=25
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetSubscribedFoldersByUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetSubscribedFoldersByUser xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>john.smith</userName>
      <startingRow>0</startingRow>
      <rowCount>25</rowCount>
    </GetSubscribedFoldersByUser>
  </soap:Body>
</soap:Envelope>
```

## Use Cases

1. **User Reports**
   - Generate reports of folders a user is subscribed to
   - Audit folder subscription activity across teams

2. **Administrative Oversight**
   - Review folder subscriptions for a given user
   - Manage notification workload for users

3. **Pagination**
   - Use `startingRow` and `rowCount` together to page through large subscription lists
   - Use `recordCount` from the response to determine total pages

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getSubscribedFoldersByUser(userName, startingRow = 0, rowCount = 25) {
    const ticket = getUserAuthTicket();

    const params = new URLSearchParams({
        authenticationTicket: ticket,
        userName: userName,
        startingRow: startingRow,
        rowCount: rowCount
    });

    const response = await fetch(`/srv.asmx/GetSubscribedFoldersByUser?${params}`);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const totalCount = parseInt(root.getAttribute("recordCount"));
        const folders = [];
        xmlDoc.querySelectorAll("folder").forEach(folder => {
            folders.push({
                id: folder.getAttribute("id"),
                name: folder.getAttribute("name"),
                path: folder.getAttribute("path")
            });
        });
        return { totalCount, folders };
    } else {
        throw new Error(root.getAttribute("error"));
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    var response = await client.GetSubscribedFoldersByUserAsync(
        authTicket,
        "john.smith",
        startingRow: 0,
        rowCount: 25);

    var root = XElement.Parse(response.ToString());
    if (root.Attribute("success")?.Value == "true")
    {
        int totalCount = int.Parse(root.Attribute("recordCount")?.Value ?? "0");
        var folders = root.Elements("folder").Select(f => new
        {
            Id = int.Parse(f.Attribute("id")?.Value ?? "0"),
            Name = f.Attribute("name")?.Value,
            Path = f.Attribute("path")?.Value
        }).ToList();

        Console.WriteLine($"Total subscribed folders: {totalCount}");
        Console.WriteLine($"Returned in this page: {folders.Count}");
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
| `[921]Insufficient rights` | Anonymous users or users without permission cannot perform this action |
| `User not found` | The specified username does not exist |

## Notes

- Use `recordCount` from the response to implement pagination logic
- `rowCount` in the response reflects the actual number of records returned, which may be less than the requested `rowCount` on the last page
- Anonymous users cannot call this API

## Related APIs

- `GetSubscribedDocumentsByUser` - Get subscribed documents for a specified user
- `GetSubscriptions` - Get subscribed documents and folders for the current user
- `AddUserToFolderSubscribers` - Subscribe a user to a folder
- `RemoveUserFromFolderSubscribers` - Remove a user from a folder subscription
- `RemoveAllSubscriptions` - Remove all subscriptions for a user
