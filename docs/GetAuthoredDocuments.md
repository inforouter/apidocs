# GetAuthoredDocuments API

Returns the list of documents authored (created) by the specified user across all libraries visible to the caller. The results are sorted alphabetically by document name.

## Endpoint

```
/srv.asmx/GetAuthoredDocuments
```

## Methods

- **GET** `/srv.asmx/GetAuthoredDocuments?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/GetAuthoredDocuments` (form data)
- **SOAP** Action: `http://tempuri.org/GetAuthoredDocuments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `userName` | string | Yes | The user name to retrieve authored documents for |

## Response Structure

### Success Response

```xml
<response success="true">
  <document id="1234" name="Q1_Report.docx" size="245760" modificationDate="2026-02-01T14:30:00" publishedVersionAuthorName="John Smith" ... />
  <document id="1235" name="Invoice_001.pdf" size="102400" modificationDate="2026-01-15T09:00:00" publishedVersionAuthorName="John Smith" ... />
  <!-- ... additional documents ... -->
</response>
```

### Empty Result

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Document Attributes

Each `<document>` element contains the standard document properties including:

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | integer | Unique document identifier |
| `name` | string | Document file name |
| `size` | long | Document size in bytes |
| `modificationDate` | DateTime | Last modification date |
| `publishedVersionAuthorName` | string | Name of the published version author |

Additional standard document attributes may be included depending on the document type and system configuration.

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- If the caller is querying their own documents, no additional permissions are required
- If the caller is querying another user's documents, the caller must have `ListingAuditLogOfUser` admin permission for the target user

## Use Cases

1. **User Administration**
   - View all documents created by a user before account changes or deactivation
   - Audit document creation activity for a specific user

2. **Content Ownership**
   - Identify all content authored by a user for ownership transfer
   - Review document authorship for compliance purposes

3. **User Reports**
   - Generate reports of document creation by user
   - Analyze content contribution across the organization

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetAuthoredDocuments?authenticationTicket=abc123-def456&userName=jsmith HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetAuthoredDocuments HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetAuthoredDocuments"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetAuthoredDocuments xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
    </GetAuthoredDocuments>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getAuthoredDocuments(userName) {
    const ticket = getUserAuthTicket();
    const url = `/srv.asmx/GetAuthoredDocuments?authenticationTicket=${encodeURIComponent(ticket)}&userName=${encodeURIComponent(userName)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const documents = [];
        xmlDoc.querySelectorAll("document").forEach(doc => {
            documents.push({
                id: parseInt(doc.getAttribute("id")),
                name: doc.getAttribute("name"),
                size: parseInt(doc.getAttribute("size")),
                modificationDate: doc.getAttribute("modificationDate"),
                publishedVersionAuthorName: doc.getAttribute("publishedVersionAuthorName")
            });
        });
        return documents;
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function displayAuthoredDocuments(userName) {
    try {
        const documents = await getAuthoredDocuments(userName);

        console.log(`Authored documents: ${documents.length}`);
        documents.forEach(doc => {
            const sizeKB = (doc.size / 1024).toFixed(1);
            console.log(`[${doc.id}] ${doc.name} (${sizeKB} KB) - Modified: ${doc.modificationDate}`);
        });
    } catch (error) {
        console.error("Failed to get authored documents:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetAuthoredDocumentsAsync(authTicket, userName);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            var documents = root.Elements("document")
                .Select(doc => new
                {
                    Id = int.Parse(doc.Attribute("id")?.Value ?? "0"),
                    Name = doc.Attribute("name")?.Value ?? "",
                    Size = long.Parse(doc.Attribute("size")?.Value ?? "0"),
                    ModificationDate = doc.Attribute("modificationDate")?.Value ?? "",
                    Author = doc.Attribute("publishedVersionAuthorName")?.Value ?? ""
                })
                .ToList();

            Console.WriteLine($"Found {documents.Count} authored documents");
            foreach (var doc in documents)
            {
                Console.WriteLine($"[{doc.Id}] {doc.Name} ({doc.Size / 1024} KB) - {doc.ModificationDate}");
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

## Notes

- Results include documents from all libraries visible to the caller.
- Documents are sorted alphabetically by document name in ascending order.
- The response uses the standard document serialization format, consistent with other document-listing APIs like `GetCheckedoutDocumentsByUser`.
- If the user has no authored documents, the response will be a success with no `<document>` child elements.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | Caller does not have `ListingAuditLogOfUser` admin permission for the target user |
| User not found error | The specified `userName` does not exist in the system |

## Related APIs

- `GetCheckedoutDocumentsByUser` - Get checked out documents for a specified user
- `GetSubscriptionsByUser` - Get folder and document subscriptions for a user
- `GetUsersTaskPerformance` - Get user task performance statistics
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New**: Added to provide programmatic access to user-authored document listings previously only available through the Control Panel UI
