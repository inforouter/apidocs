# GetDomainPolicies API

Gets the policies and domain rules for a domain/library, including per-policy metadata describing allowed configuration ranges.

## Endpoint

```
/srv.asmx/GetDomainPolicies
```

## Methods

- **GET** `/srv.asmx/GetDomainPolicies?authenticationTicket=...&domainName=...`
- **POST** `/srv.asmx/GetDomainPolicies` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomainPolicies`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `domainName` | string | Yes | Name of the domain/library to retrieve policies for |

## Response

### Success Response

```xml
<root success="true">
  <DomainPolicies domainName="MyLibrary" isArchive="false">
    <DomainRules>
      <AnonymousHideIncomplete>false</AnonymousHideIncomplete>
      <ReaderHideIncomplete>false</ReaderHideIncomplete>
      <AnonymousHideUnapproved>false</AnonymousHideUnapproved>
      <ReaderHideUnapproved>false</ReaderHideUnapproved>
      <AnonymousHideExpired>false</AnonymousHideExpired>
      <ReaderHideExpired>false</ReaderHideExpired>
      <AnonymousHideUnpublished>false</AnonymousHideUnpublished>
      <ReaderHideUnpublished>false</ReaderHideUnpublished>
      <PublishReqDoctype>false</PublishReqDoctype>
      <PublishReqRetention>false</PublishReqRetention>
      <PublishReqCompletion>false</PublishReqCompletion>
      <PublishReqApproval>false</PublishReqApproval>
      <PublishReqUnexpiration>false</PublishReqUnexpiration>
      <DisallowDragDropUploads>false</DisallowDragDropUploads>
    </DomainRules>
    <ActionPolicies>
      <Policy Action="DocumentCreate"
              RightAnonymous="false" RightDomainManager="true" RightObjectOwner="true"
              RightSubobjectOwner="false" RightRequired="ADD" LogAction="false"
              AnonymousApplies="false" DomainManagerApplies="true" OwnershipApplies="true"
              SubObjectOwnerApplies="false" SecurityApplies="true"
              AllowedRights="|ADD" LogOption="true" />
      <Policy Action="DocumentDelete"
              RightAnonymous="false" RightDomainManager="true" RightObjectOwner="true"
              RightSubobjectOwner="false" RightRequired="FULLCONTROL" LogAction="true"
              AnonymousApplies="false" DomainManagerApplies="true" OwnershipApplies="true"
              SubObjectOwnerApplies="false" SecurityApplies="true"
              AllowedRights="|FULLCONTROL" LogOption="false" />
      <!-- ... additional Policy elements for all configurable actions ... -->
    </ActionPolicies>
  </DomainPolicies>
</root>
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## DomainRules Elements

| Element | Description |
|---------|-------------|
| `AnonymousHideIncomplete` | Hide incomplete documents from anonymous users |
| `ReaderHideIncomplete` | Hide incomplete documents from read-only users |
| `AnonymousHideUnapproved` | Hide unapproved documents from anonymous users |
| `ReaderHideUnapproved` | Hide unapproved documents from read-only users |
| `AnonymousHideExpired` | Hide expired documents from anonymous users |
| `ReaderHideExpired` | Hide expired documents from read-only users |
| `AnonymousHideUnpublished` | Hide unpublished documents from anonymous users |
| `ReaderHideUnpublished` | Hide unpublished documents from read-only users |
| `PublishReqDoctype` | Require document type for publishing |
| `PublishReqRetention` | Require retention period for publishing |
| `PublishReqCompletion` | Require completion status for publishing |
| `PublishReqApproval` | Require approval for publishing |
| `PublishReqUnexpiration` | Require unexpired status for publishing |
| `DisallowDragDropUploads` | Disable drag-and-drop uploads in this domain |

## ActionPolicies Attributes

Each `<Policy>` element contains two groups of attributes: **current values** and **metadata**.

### Current Values

These reflect the domain's current policy configuration:

| Attribute | Type | Description |
|-----------|------|-------------|
| `Action` | string | The action type (see valid values below) |
| `RightAnonymous` | boolean | Whether anonymous users can perform this action |
| `RightDomainManager` | boolean | Whether domain managers can perform this action |
| `RightObjectOwner` | boolean | Whether object owners can perform this action |
| `RightSubobjectOwner` | boolean | Whether sub-object owners can perform this action |
| `RightRequired` | string | Required right level (see valid values below). Empty string if no right applies |
| `LogAction` | boolean | Whether audit logging is enabled for this action |

### Metadata

These describe the configuration options available for each policy (used by UI to render the correct controls):

| Attribute | Type | Description |
|-----------|------|-------------|
| `AnonymousApplies` | boolean | Whether the anonymous user option is configurable for this policy |
| `DomainManagerApplies` | boolean | Whether the domain manager option is configurable for this policy |
| `OwnershipApplies` | boolean | Whether the object owner option is configurable for this policy |
| `SubObjectOwnerApplies` | boolean | Whether the sub-object owner option is available for this policy |
| `SecurityApplies` | boolean | Whether the rights level dropdown applies to this policy |
| `AllowedRights` | string | Pipe-delimited list of selectable right levels (e.g., `\|CHANGE\|FULLCONTROL`). Empty string when `SecurityApplies` is `false` |
| `LogOption` | boolean | Whether audit logging is optional (configurable) for this policy. When `false`, the log setting is fixed and cannot be changed |

## Valid Action Values

| Action | Description |
|--------|-------------|
| `DocumentCreate` | Create documents |
| `DocumentCheckout` | Check out documents |
| `DocumentCheckIn` | Check in documents |
| `DocumentDelete` | Delete documents |
| `VersionDelete` | Delete document versions |
| `DocumentForceCheckin` | Force check-in documents |
| `DocumentPropertyChange` | Change document properties |
| `DocumentCommentAdds` | Add document comments |
| `DocumentCommentsChangeDelete` | Change or delete comments |
| `DocumentRead` | Read documents |
| `AccessToDocumentVersions` | Access document versions |
| `FolderCompact` | Compact folder |
| `FolderCreate` | Create folders |
| `FolderDelete` | Delete folders |
| `FolderRuleSet` | Set folder rules |
| `FolderPropertyChange` | Change folder properties |
| `ReadSecurityAccessList` | Read security access list |
| `SecurityChange` | Change security settings |
| `OwnerShipChange` | Change ownership |
| `DocumentReadComment` | Read document comments |
| `ReadSubscriberList` | Read subscriber list |
| `MetaDataAddChange` | Add or change metadata |
| `MetaDataRemove` | Remove metadata |
| `SetDocumentType` | Set document type |
| `ChangeDocumentType` | Change document type |
| `RetentionPeriodChange` | Change retention period |
| `ChangeClassification` | Change document classification |
| `DocumentCompletion` | Set document completion status |
| `DocumentAddTask` | Add tasks to documents |
| `DocumentRemoveTask` | Remove tasks from documents |
| `DocumentSubmitWorkflow` | Submit documents to workflow |
| `DocumentRemoveWorkflow` | Remove documents from workflow |
| `DocumentReadReviewLog` | Read review log |
| `DocumentReadViewLog` | Read view log |
| `DocumentReadSoxLog` | Read SOX compliance log |
| `DocumentReadIsoLog` | Read ISO compliance log |
| `DocumentReadClassificationLog` | Read classification log |
| `DeleteClassificationLog` | Delete classification log |
| `MoveInside` | Move within domain |
| `MoveToOutSide` | Move outside domain |
| `AddRemoveSubscription` | Add or remove subscriptions |

## Valid RightRequired / AllowedRights Values

| Value | Description |
|-------|-------------|
| `NOACCESS` | No access allowed |
| `LIST` | List permission |
| `READ` | Read permission |
| `ADD` | Add permission |
| `ADDREAD` | Add and read permission |
| `CHANGE` | Change permission |
| `FULLCONTROL` | Full control permission |

## Required Permissions

The caller must have **UpdateLibraryPolicies** permission on the specified domain.

## Example

### Request (GET)

```
GET /srv.asmx/GetDomainPolicies?authenticationTicket=abc123-def456&domainName=MyLibrary HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetDomainPolicies HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&domainName=MyLibrary
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetDomainPolicies"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetDomainPolicies xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <domainName>MyLibrary</domainName>
    </GetDomainPolicies>
  </soap:Body>
</soap:Envelope>
```

## Notes

- This API is the read counterpart of `SetDomainPolicies`
- The response includes all configurable (non-system) policies
- The `AllowedRights` attribute is a pipe-delimited string with a leading pipe (e.g., `|CHANGE|FULLCONTROL`). It is empty when `SecurityApplies` is `false`
- The `DocumentRead` policy has `SecurityApplies="false"` and an empty `AllowedRights` since the read right level is fixed
- The `DocumentCheckIn` policy has `DomainManagerApplies="false"` and `OwnershipApplies="false"` because check-in rights are determined by the checkout holder, not by role
- The `AccessToDocumentVersions` policy has `DomainManagerApplies="false"` and `OwnershipApplies="false"` with `AnonymousApplies="true"`
