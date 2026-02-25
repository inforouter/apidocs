# GetSubscriptionsByUser API

Retrieves folder and document subscriptions for a specific user. This API returns both subscribed folders and subscribed documents with optional metadata.

## Endpoint

```
/srv.asmx/GetSubscriptionsByUser
```

## Methods

- **GET** `/srv.asmx/GetSubscriptionsByUser?authenticationTicket=...&userName=...&withrules=...&withpropertysets=...&withsecurity=...&withOwner=...&withVersions=...`
- **POST** `/srv.asmx/GetSubscriptionsByUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetSubscriptionsByUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `userName` | string | Yes | User name to retrieve subscriptions for |
| `withrules` | boolean | Yes | Include folder rules in response |
| `withpropertysets` | boolean | Yes | Include property sets in response |
| `withsecurity` | boolean | Yes | Include security/permissions information |
| `withOwner` | boolean | Yes | Include owner information |
| `withVersions` | boolean | Yes | Include version information for documents |

## Response

### Success Response

```xml
<root success="true">
  <folders>
    <folder id="123" name="Project Documents" path="/Library/Projects" ...>
      <!-- Folder details based on optional parameters -->
    </folder>
    <!-- More folders -->
  </folders>
  <documents>
    <document id="456" name="Report.pdf" ...>
      <!-- Document details based on optional parameters -->
    </document>
    <!-- More documents -->
  </documents>
</root>
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

- **Authenticated User**: Must be logged in
- **Self Access**: Users can view their own subscriptions
- **Admin Access**: To view another user's subscriptions, requires `ListingAuditLogOfUser` permission
- **User Must Exist**: The specified user must exist in the system

## Permission Checks

The API performs the following permission checks:

1. **Authentication**: Valid authentication ticket required
2. **User Exists**: Target user must exist
3. **Access Rights**: 
   - If viewing own subscriptions: No additional permission needed
   - If viewing another user's subscriptions: Requires `ListingAuditLogOfUser` admin permission

## Example (REST GET)

```
GET /srv.asmx/GetSubscriptionsByUser?authenticationTicket=abc123-def456&userName=jsmith&withrules=true&withpropertysets=false&withsecurity=false&withOwner=true&withVersions=false HTTP/1.1
Host: your-inforouter-server.com
```

### Example (REST POST)

```
POST /srv.asmx/GetSubscriptionsByUser HTTP/1.1
Host: your-inforouter-server.com
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith&withrules=true&withpropertysets=false&withsecurity=false&withOwner=true&withVersions=false
```

### SOAP Request

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetSubscriptionsByUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetSubscriptionsByUser xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
      <withrules>true</withrules>
      <withpropertysets>false</withpropertysets>
      <withsecurity>false</withsecurity>
      <withOwner>true</withOwner>
      <withVersions>false</withVersions>
    </GetSubscriptionsByUser>
  </soap:Body>
</soap:Envelope>
```

## Use Cases

### 1. View User's Subscriptions for Audit
Administrators can view what folders and documents a user is subscribed to:

```csharp
var result = await client.GetSubscriptionsByUserAsync(
    ticket, 
    "jsmith", 
    withrules: false, 
    withpropertysets: false, 
    withsecurity: false, 
    withOwner: true, 
    withVersions: false
);
```

### 2. User Subscription Report
Generate a detailed report of all user subscriptions:

```csharp
var result = await client.GetSubscriptionsByUserAsync(
    ticket, 
    "jsmith", 
    withrules: true, 
    withpropertysets: true, 
    withsecurity: true, 
    withOwner: true, 
    withVersions: true
);
```

### 3. Subscription Transfer Analysis
Before transferring subscriptions from one user to another, analyze what they're subscribed to:

```csharp
// Get subscriptions from departing user
var subscriptions = await client.GetSubscriptionsByUserAsync(
    ticket, 
    "departing.user", 
    withrules: false, 
    withpropertysets: false, 
    withsecurity: false, 
    withOwner: false, 
    withVersions: false
);

// Process and transfer to new user
```

### 4. Subscription Cleanup
Identify and clean up old or unnecessary subscriptions:

```csharp
var subscriptions = await client.GetSubscriptionsByUserAsync(
    ticket, 
    "inactive.user", 
    withrules: false, 
    withpropertysets: false, 
    withsecurity: false, 
    withOwner: true, 
    withVersions: false
);

// Remove subscriptions for inactive user
```

## Integration Example (C#)

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Xml.Linq;

public class SubscriptionClient
{
    private readonly string _baseUrl;
    private readonly HttpClient _httpClient;

    public SubscriptionClient(string baseUrl)
    {
        _baseUrl = baseUrl;
        _httpClient = new HttpClient();
    }

    public async Task<UserSubscriptions> GetSubscriptionsByUserAsync(
        string ticket, 
        string userName,
        bool withRules = false,
        bool withPropertySets = false,
        bool withSecurity = false,
        bool withOwner = true,
        bool withVersions = false)
    {
        var url = $"{_baseUrl}/srv.asmx/GetSubscriptionsByUser" +
                  $"?authenticationTicket={Uri.EscapeDataString(ticket)}" +
                  $"&userName={Uri.EscapeDataString(userName)}" +
                  $"&withrules={withRules}" +
                  $"&withpropertysets={withPropertySets}" +
                  $"&withsecurity={withSecurity}" +
                  $"&withOwner={withOwner}" +
                  $"&withVersions={withVersions}";

        var response = await _httpClient.GetAsync(url);
        response.EnsureSuccessStatusCode();

        var xmlContent = await response.Content.ReadAsStringAsync();
        var xml = XElement.Parse(xmlContent);

        if (xml.Attribute("success")?.Value != "true")
        {
            throw new Exception($"API Error: {xml.Attribute("error")?.Value}");
        }

        return new UserSubscriptions
        {
            Folders = ParseFolders(xml.Element("folders")),
            Documents = ParseDocuments(xml.Element("documents"))
        };
    }

    private List<FolderInfo> ParseFolders(XElement? foldersElement)
    {
        var folders = new List<FolderInfo>();
        if (foldersElement == null) return folders;

        foreach (var folder in foldersElement.Elements("folder"))
        {
            folders.Add(new FolderInfo
            {
                Id = int.Parse(folder.Attribute("id")?.Value ?? "0"),
                Name = folder.Attribute("name")?.Value ?? "",
                Path = folder.Attribute("path")?.Value ?? ""
            });
        }

        return folders;
    }

    private List<DocumentInfo> ParseDocuments(XElement? documentsElement)
    {
        var documents = new List<DocumentInfo>();
        if (documentsElement == null) return documents;

        foreach (var doc in documentsElement.Elements("document"))
        {
            documents.Add(new DocumentInfo
            {
                Id = int.Parse(doc.Attribute("id")?.Value ?? "0"),
                Name = doc.Attribute("name")?.Value ?? ""
            });
        }

        return documents;
    }
}

public class UserSubscriptions
{
    public List<FolderInfo> Folders { get; set; } = new();
    public List<DocumentInfo> Documents { get; set; } = new();
}

public class FolderInfo
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string Path { get; set; } = "";
}

public class DocumentInfo
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
}

// Usage
var client = new SubscriptionClient("https://your-inforouter-server.com");
var subscriptions = await client.GetSubscriptionsByUserAsync(
    "your-auth-ticket",
    "jsmith",
    withOwner: true
);

Console.WriteLine($"User has {subscriptions.Folders.Count} folder subscriptions");
Console.WriteLine($"User has {subscriptions.Documents.Count} document subscriptions");

foreach (var folder in subscriptions.Folders)
{
    Console.WriteLine($"Folder: {folder.Path}");
}

foreach (var doc in subscriptions.Documents)
{
    Console.WriteLine($"Document: {doc.Name}");
}
```

## Integration Example (JavaScript/TypeScript)

```javascript
async function getSubscriptionsByUser(ticket, userName, options = {}) {
    const {
        withrules = false,
        withpropertysets = false,
        withsecurity = false,
        withOwner = true,
        withVersions = false
    } = options;

    const params = new URLSearchParams({
        authenticationTicket: ticket,
        userName: userName,
        withrules: withrules.toString(),
        withpropertysets: withpropertysets.toString(),
        withsecurity: withsecurity.toString(),
        withOwner: withOwner.toString(),
        withVersions: withVersions.toString()
    });

    const response = await fetch(`/srv.asmx/GetSubscriptionsByUser?${params}`);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xml = parser.parseFromString(xmlText, 'text/xml');
    const root = xml.documentElement;

    if (root.getAttribute('success') !== 'true') {
        throw new Error(root.getAttribute('error') || 'Unknown error');
    }

    const folders = [];
    const foldersElement = root.querySelector('folders');
    if (foldersElement) {
        foldersElement.querySelectorAll('folder').forEach(folder => {
            folders.push({
                id: parseInt(folder.getAttribute('id') || '0'),
                name: folder.getAttribute('name') || '',
                path: folder.getAttribute('path') || ''
            });
        });
    }

    const documents = [];
    const documentsElement = root.querySelector('documents');
    if (documentsElement) {
        documentsElement.querySelectorAll('document').forEach(doc => {
            documents.push({
                id: parseInt(doc.getAttribute('id') || '0'),
                name: doc.getAttribute('name') || ''
            });
        });
    }

    return { folders, documents };
}

// Usage
const subscriptions = await getSubscriptionsByUser('auth-ticket', 'jsmith', {
    withOwner: true
});

console.log(`Folder subscriptions: ${subscriptions.folders.length}`);
console.log(`Document subscriptions: ${subscriptions.documents.length}`);

subscriptions.folders.forEach(folder => {
    console.log(`Subscribed to folder: ${folder.path}`);
});

subscriptions.documents.forEach(doc => {
    console.log(`Subscribed to document: ${doc.name}`);
});
```

## Integration Example (Python)

```python
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

def get_subscriptions_by_user(
    base_url: str,
    ticket: str,
    user_name: str,
    withrules: bool = False,
    withpropertysets: bool = False,
    withsecurity: bool = False,
    with_owner: bool = True,
    with_versions: bool = False
) -> Dict[str, List[Dict]]:
    """Get subscriptions for a specific user"""
    
    url = f"{base_url}/srv.asmx/GetSubscriptionsByUser"
    params = {
        'authenticationTicket': ticket,
        'userName': user_name,
        'withrules': str(withrules).lower(),
        'withpropertysets': str(withpropertysets).lower(),
        'withsecurity': str(withsecurity).lower(),
        'withOwner': str(with_owner).lower(),
        'withVersions': str(with_versions).lower()
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    root = ET.fromstring(response.text)
    
    if root.get('success') != 'true':
        raise Exception(f"API Error: {root.get('error')}")
    
    # Parse folders
    folders = []
    folders_element = root.find('folders')
    if folders_element is not None:
        for folder in folders_element.findall('folder'):
            folders.append({
                'id': int(folder.get('id', 0)),
                'name': folder.get('name', ''),
                'path': folder.get('path', '')
            })
    
    # Parse documents
    documents = []
    documents_element = root.find('documents')
    if documents_element is not None:
        for doc in documents_element.findall('document'):
            documents.append({
                'id': int(doc.get('id', 0)),
                'name': doc.get('name', '')
            })
    
    return {
        'folders': folders,
        'documents': documents
    }

# Usage
subscriptions = get_subscriptions_by_user(
    'https://your-inforouter-server.com',
    'auth-ticket',
    'jsmith',
    with_owner=True
)

print(f"Folder subscriptions: {len(subscriptions['folders'])}")
print(f"Document subscriptions: {len(subscriptions['documents'])}")

for folder in subscriptions['folders']:
    print(f"Subscribed to folder: {folder['path']}")

for doc in subscriptions['documents']:
    print(f"Subscribed to document: {doc['name']}")
```

## Response Fields

### Folder Fields (when included)

- `id` - Folder ID
- `name` - Folder name
- `path` - Full folder path
- Additional fields based on parameters:
  - When `withrules=true`: Folder rule information
  - When `withpropertysets=true`: Property set values
  - When `withsecurity=true`: Permission/security information
  - When `withOwner=true`: Owner information

### Document Fields (when included)

- `id` - Document ID
- `name` - Document name
- Additional fields based on parameters:
  - When `withpropertysets=true`: Property set values
  - When `withsecurity=true`: Permission/security information
  - When `withOwner=true`: Owner information
  - When `withVersions=true`: Version history

## Notes

- **Performance**: Setting all boolean parameters to `true` may result in slower responses for users with many subscriptions
- **Minimal Data**: For best performance when you only need basic subscription lists, set all optional parameters to `false`
- **Permission Required**: Viewing another user's subscriptions requires administrative permissions
- **Empty Results**: If user has no subscriptions, empty `<folders>` and `<documents>` elements are returned
- **Deleted Items**: Subscriptions to deleted folders/documents are automatically cleaned up and won't appear

## Common Error Messages

| Error Code | Message | Solution |
|------------|---------|----------|
| 114 | User not found | Verify the userName parameter is correct |
| Invalid Ticket | Authentication failed | Obtain a new authentication ticket |
| Insufficient rights | Permission denied | Ensure user has appropriate permissions |

## Related APIs

- `GetMyStuff` - Get subscriptions for current authenticated user
- `AddUserToFolderSubscribers` - Subscribe user to a folder
- `AddUserToDocumentSubscribers` - Subscribe user to a document
- `RemoveUserFromFolderSubscribers` - Remove folder subscription
- `RemoveUserFromDocumentSubscribers` - Remove document subscription
- `GetUserStatistics` - Get comprehensive user statistics including subscription counts
- `TransferUserDocumentSubscriptions` - Transfer subscriptions from one user to another
- `TransferUserFolderSubscriptions` - Transfer folder subscriptions from one user to another

## Version History

- Available since infoRouter 8.7
- Async support added for better performance with large subscription lists
- Compatible with infoRouter 8.7 and later

## Support

For additional information, see:
- [API Documentation](https://support.inforouter.com/api-docs/GetSubscriptionsByUser)
- [User Management Guide](https://support.inforouter.com/user-management)
- [Subscription Management](https://support.inforouter.com/subscriptions)
