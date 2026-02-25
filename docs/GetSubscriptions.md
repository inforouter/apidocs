# GetSubscriptions API

Returns the list of documents and folders that the current authenticated user is subscribed to. Subscriptions are created via the `AddUserToDocumentSubscribers` and `AddUserToFolderSubscribers` APIs. The response uses the same full-detail folder and document element format as `GetFoldersAndDocuments`. Optional flags control whether additional detail (folder rules, property sets, security, owner, version history) is included for each item.

## Endpoint

```
/srv.asmx/GetSubscriptions
```

## Methods

- **GET** `/srv.asmx/GetSubscriptions?authenticationTicket=...&withrules=...&withpropertysets=...&withsecurity=...&withOwner=...&withVersions=...`
- **POST** `/srv.asmx/GetSubscriptions` (form data)
- **SOAP** Action: `http://tempuri.org/GetSubscriptions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. Subscriptions are always returned for the user associated with this ticket. |
| `withrules` | bool | Yes | If `true`, include folder rules (`<Rules>` child element) for each subscribed folder. Has no effect on document items. |
| `withpropertysets` | bool | Yes | If `true`, include applied custom property set data (`<PropertySets>` child element) for each item. |
| `withsecurity` | bool | Yes | If `true`, include the access control list (`<AccessList>` child element) for each item. |
| `withOwner` | bool | Yes | If `true`, include owner user information for each item. |
| `withVersions` | bool | Yes | If `true`, include document version history (`<Versions>` child element) for each document. Has no effect on folder items. |

> **Performance tip:** Pass `false` for all boolean flags for the fastest, most compact response. Enable only the flags your application actually needs.

---

## Response

### Success Response

Returns a `<root>` element with `success="true"` containing `<folder>` and `<document>` child elements -" subscribed folders first, then subscribed documents, both sorted by name ascending. If the user has no subscriptions, an empty root element is returned (not an error).

```xml
<root success="true">

  <!-- Subscribed folder items -->
  <folder FolderID="42"
          ParentID="10"
          Name="Q1 Reports"
          Path="/Finance/Reports/Q1 Reports"
          Description="First quarter reports"
          CreationDate="2024-01-15"
          OwnerName="jsmith"
          DomainId="3"
          ClassificationLevel="NoMarkings"
          ClassificationLevelId="0"
          DeclassifyOn=""
          DowngradeOn=""
          RDDefId="0"
          RetentionDate=""
          DispositionDate=""
          CutoffDate="">

    <!-- Included only when withrules=true -->
    <Rules>
      <Rule Name="AllowableFileTypes"  Value="*" />
      <Rule Name="Checkins"            Value="allows" />
      <Rule Name="Checkouts"           Value="allows" />
      <Rule Name="DocumentDeletes"     Value="allows" />
      <Rule Name="FolderDeletes"       Value="allows" />
      <Rule Name="NewDocuments"        Value="allows" />
      <Rule Name="NewFolders"          Value="allows" />
      <Rule Name="ClassifiedDocuments" Value="disallows" />
    </Rules>

    <!-- Included only when withpropertysets=true -->
    <PropertySets> ... </PropertySets>

    <!-- Included only when withsecurity=true -->
    <AccessList DateApplied="2024-01-15" AppliedBy="admin" InheritedSecurity="false"> ... </AccessList>

    <!-- Included only when withOwner=true -->
    <User UserID="7" UserName="jsmith" FullName="John Smith" />
  </folder>

  <!-- Subscribed document items -->
  <document DocumentID="1234"
            ParentID="42"
            Name="Q1-2024-Report.pdf"
            Path="/Finance/Reports/Q1 Reports/Q1-2024-Report.pdf"
            MimeTypeDesc="PDF Document"
            DocumentSource="Upload"
            Author="jsmith"
            Language="en"
            OwnerName="jsmith"
            Importance="Normal"
            ImportanceId="1"
            ClassificationLevel="NoMarkings"
            ClassificationLevelId="0"
            DocumentType=""
            DocumentTypeId="0"
            CheckedOutBy=""
            CheckedOutById="0"
            CheckOutDate=""
            LastVersion="2000000"
            PublishedVersion="2000000"
            ReleasedVersion="2000000"
            LastUpdate="2024-06-15T10:30:00.000Z"
            LastUpdatedBy="jsmith"
            LastPublisher="jsmith"
            DocumentSize="524288"
            ApprovalStatus="Approved"
            ApprovalStatusId="2"
            FlowId="0"
            FlowName=""
            FlowStepNumber="0"
            FlowStepName=""
            ISOReviewDate=""
            ExpirationDate=""
            CutoffDate=""
            DomainId="3"
            ShortID="~D1234"
            RDDefId="0"
            RetentionDate=""
            DispositionDate=""
            IsPublished="true"
            IsDynamic="false"
            DeclassifyOn=""
            DowngradeOn="">

    <!-- Included only when withpropertysets=true -->
    <PropertySets> ... </PropertySets>

    <!-- Included only when withsecurity=true -->
    <AccessList DateApplied="2024-01-15" AppliedBy="admin" InheritedSecurity="false"> ... </AccessList>

    <!-- Included only when withOwner=true -->
    <User UserID="7" UserName="jsmith" FullName="John Smith" />

    <!-- Included only when withVersions=true -->
    <Versions> ... </Versions>
  </document>

</root>
```

### Empty Result (No Subscriptions)

```xml
<root success="true" />
```

### Error Response

```xml
<response success="false" error="[900] Authentication failed." />
```

---

## Required Permissions

Any **authenticated user** can call this API. The response always contains subscriptions for the user associated with the provided `authenticationTicket`. It is not possible to retrieve subscriptions for another user via this API.

---

## Example

### GET Request

```
GET /srv.asmx/GetSubscriptions
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &withrules=false
  &withpropertysets=false
  &withsecurity=false
  &withOwner=false
  &withVersions=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetSubscriptions HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&withrules=false
&withpropertysets=false
&withsecurity=false
&withOwner=false
&withVersions=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetSubscriptions>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:withrules>false</tns:withrules>
      <tns:withpropertysets>false</tns:withpropertysets>
      <tns:withsecurity>false</tns:withsecurity>
      <tns:withOwner>false</tns:withOwner>
      <tns:withVersions>false</tns:withVersions>
    </tns:GetSubscriptions>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Current User Only**: This API always returns subscriptions for the authenticated user. It is not possible to retrieve subscriptions for a different user.
- **Folders First**: Subscribed folders appear before subscribed documents. Within each group, items are sorted by name in ascending order.
- **Empty Response**: An empty `<root success="true" />` is returned when the user has no subscriptions -" this is not an error.
- **Event Flags Not Returned**: The response shows *which* documents and folders the user is subscribed to, but does **not** include the configured event notification flags (`ON_READ`, `ON_UPDATE`, etc.). Use `GetSubscribers` with the item's path to retrieve event flag details for a specific item.
- **Performance**: All five boolean flags add significant data to the response. Pass `false` for flags your application does not use.
- **Document vs Folder Items**: Items are distinguished by element name: `<document>` for document subscriptions, `<folder>` for folder subscriptions.

---

## Related APIs

- [AddUserToDocumentSubscribers](AddUserToDocumentSubscribers.md) - Subscribe a user to a document
- [AddUserToFolderSubscribers](AddUserToFolderSubscribers.md) - Subscribe a user to a folder
- [GetSubscribers](GetSubscribers.md) - Get all subscribers of a document or folder including event flag details
- [RemoveUserFromDocumentSubscribers](RemoveUserFromDocumentSubscribers.md) - Unsubscribe a user from a document
- [GetFavorites](GetFavorites.md) - Get the current user's favorites list (same response structure)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[347] User has been deleted` | The user account associated with the ticket no longer exists. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
