# SetDomainPolicies API

Sets the policies for a domain/library.

## Endpoint

```
/srv.asmx/SetDomainPolicies
```

## Methods

- **GET** `/srv.asmx/SetDomainPolicies?authenticationTicket=...&domainName=...&xmlPolicies=...`
- **POST** `/srv.asmx/SetDomainPolicies` (form data)
- **SOAP** Action: `http://tempuri.org/SetDomainPolicies`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `domainName` | string | Yes | Name of the domain/library to update |
| `xmlPolicies` | string | Yes | XML containing policy settings (see format below) |

## XML Format

```xml
<Policies>
  <DomainRules>
    <AnonymousHideIncomplete>true|false</AnonymousHideIncomplete>
    <ReaderHideIncomplete>true|false</ReaderHideIncomplete>
    <AnonymousHideUnapproved>true|false</AnonymousHideUnapproved>
    <ReaderHideUnapproved>true|false</ReaderHideUnapproved>
    <AnonymousHideExpired>true|false</AnonymousHideExpired>
    <ReaderHideExpired>true|false</ReaderHideExpired>
    <AnonymousHideUnpublished>true|false</AnonymousHideUnpublished>
    <ReaderHideUnpublished>true|false</ReaderHideUnpublished>
    <PublishReqDoctype>true|false</PublishReqDoctype>
    <PublishReqRetention>true|false</PublishReqRetention>
    <PublishReqCompletion>true|false</PublishReqCompletion>
    <PublishReqApproval>true|false</PublishReqApproval>
    <PublishReqUnexpiration>true|false</PublishReqUnexpiration>
    <DisallowDragDropUploads>true|false</DisallowDragDropUploads>
  </DomainRules>
  <ActionPolicies>
    <Policy Action="DocumentDelete"
            RightAnonymous="false"
            RightDomainManager="true"
            RightObjectOwner="true"
            RightSubobjectOwner="false"
            RightRequired="FULLCONTROL"
            LogAction="true"/>
    <!-- Additional Policy elements -->
  </ActionPolicies>
</Policies>
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

| Attribute | Type | Description |
|-----------|------|-------------|
| `Action` | string | The action type (see valid values below) |
| `RightAnonymous` | boolean | Allow anonymous users to perform this action |
| `RightDomainManager` | boolean | Allow domain managers to perform this action. Also accepted: `RightDomainmanager` |
| `RightObjectOwner` | boolean | Allow object owners to perform this action. Also accepted: `RightObjectowner` |
| `RightSubobjectOwner` | boolean | Allow sub-object owners to perform this action. Also accepted: `RightSubobjectowner` |
| `RightRequired` | string | Required right level (see valid values below) |
| `LogAction` | boolean | Enable audit logging for this action |

Attribute names are case sensitive. The three role attributes above accept two spellings: the one
`GetDomainPolicies` writes, and the lower-case-second-word spelling this operation documented
earlier. When both are present on one `Policy` element, the `GetDomainPolicies` spelling wins.

## Valid Action Values

| Action | Description |
|--------|-------------|
| `DocumentDelete` | Delete documents |
| `FolderDelete` | Delete folders |
| `VersionDelete` | Delete document versions |
| `DocumentCheckout` | Check out documents |
| `DocumentCheckIn` | Check in documents |
| `MetaDataAddChange` | Add or change metadata |
| `MetaDataRemove` | Remove metadata |
| `FolderRuleSet` | Set folder rules |
| `DocumentPropertyChange` | Change document properties |
| `DocumentCompletion` | Set document completion status |
| `OwnerShipChange` | Change ownership |
| `SecurityChange` | Change security settings |
| `RetentionPeriodChange` | Change retention period |
| `ChangeClassification` | Change document classification |
| `DocumentCommentAdds` | Add document comments |
| `DocumentCommentsChangeDelete` | Change or delete comments |
| `FolderCompact` | Compact folder |
| `FolderPropertyChange` | Change folder properties |
| `DocumentAddTask` | Add tasks to documents |
| `DocumentRemoveTask` | Remove tasks from documents |
| `DocumentForceCheckin` | Force check-in documents |
| `AddRemoveSubscription` | Add or remove subscriptions |
| `DocumentSubmitWorkflow` | Submit documents to workflow |
| `DocumentRemoveWorkflow` | Remove documents from workflow |
| `DeleteClassificationLog` | Delete classification log |
| `DocumentRead` | Read documents |
| `DocumentReadComment` | Read document comments |
| `DocumentReadViewLog` | Read view log |
| `ReadSecurityAccessList` | Read security access list |
| `ReadSubscriberList` | Read subscriber list |
| `DocumentReadReviewLog` | Read review log |
| `DocumentReadSoxLog` | Read SOX compliance log |
| `DocumentReadIsoLog` | Read ISO compliance log |
| `DocumentReadClassificationLog` | Read classification log |
| `MoveInside` | Move within domain |
| `MoveToOutSide` | Move outside domain |
| `DocumentCreate` | Create documents |
| `FolderCreate` | Create folders |
| `ChangeDocumentType` | Change document type |
| `SetDocumentType` | Set document type |
| `AccessToDocumentVersions` | Access document versions |

## Valid RightRequired Values

| Value | Description |
|-------|-------------|
| `NOACCESS` | No access allowed |
| `LIST` | List permission |
| `READ` | Read permission |
| `ADD` | Add permission |
| `ADDREAD` | Add and read permission |
| `CHANGE` | Change permission |
| `FULLCONTROL` | Full control permission |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The caller must have **UpdateLibraryPolicies** permission on the specified domain.

## Example

### Request (POST)

```
POST /srv.asmx/SetDomainPolicies HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&domainName=MyLibrary&xmlPolicies=<Policies><DomainRules><AnonymousHideIncomplete>true</AnonymousHideIncomplete></DomainRules><ActionPolicies><Policy Action="DocumentDelete" RightDomainManager="true" RightObjectOwner="true" RightRequired="FULLCONTROL" LogAction="true"/></ActionPolicies></Policies>
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/SetDomainPolicies"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SetDomainPolicies xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <domainName>MyLibrary</domainName>
      <xmlPolicies><![CDATA[
        <Policies>
          <DomainRules>
            <AnonymousHideIncomplete>true</AnonymousHideIncomplete>
            <ReaderHideIncomplete>false</ReaderHideIncomplete>
          </DomainRules>
          <ActionPolicies>
            <Policy Action="DocumentDelete"
                    RightAnonymous="false"
                    RightDomainManager="true"
                    RightObjectOwner="true"
                    RightSubobjectOwner="false"
                    RightRequired="CHANGE"
                    LogAction="true"/>
          </ActionPolicies>
        </Policies>
      ]]></xmlPolicies>
    </SetDomainPolicies>
  </soap:Body>
</soap:Envelope>
```

## Notes

- The XML `GetDomainPolicies` returns can be fed straight back in: pass its `<DomainPolicies>` element as `xmlPolicies`, the root element name being ignored
- Policies not specified in the XML will retain their current values
- `RightRequired` is applied only when it names one of that policy's `AllowedRights`, which `GetDomainPolicies` reports; any other value leaves the current requirement alone
- System policies cannot be modified and will be ignored
- The `DocumentDelete` and `FolderDelete` actions always have logging enabled regardless of the `LogAction` setting
- The `DocumentRead` action always applies to anonymous users regardless of the `RightAnonymous` setting
- Archive domains have checkout disabled regardless of policy settings
