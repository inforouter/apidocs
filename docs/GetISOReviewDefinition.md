# GetISOReviewDefinition API

Returns the ISO review schedule definition currently set on a document. Includes the schedule, reviewer assignment, deadline, task permissions, and task requirements.

## Endpoint

```
/srv.asmx/GetISOReviewDefinition
```

## Methods

- **GET** `/srv.asmx/GetISOReviewDefinition?authenticationTicket=...&documentPath=...`
- **POST** `/srv.asmx/GetISOReviewDefinition` (form data)
- **SOAP** Action: `http://tempuri.org/GetISOReviewDefinition`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `documentPath` | string | Yes | Full path of the document |

## Response

### Success Response

```xml
<root success="true">
  <isoDef
    scheduleDef="MONTHLY-ON,12,1"
    nextReviewDate="2025-06-01T00:00:00.0000000"
    reviewById="-5"
    reviewByName="(Document Owner)"
    reviewInstructions="Annual policy review required"
    workflowId="0"
    workflowName=""
    deadlineHours="168"
    priority="1"
    assignerById="42"
    assignerByName="John Doe"
    assignmentDate="2024-06-01T10:30:00.0000000"
    permissionChangeDueDate="false"
    permissionChangePriority="false"
    permissionChangeFinishDate="false"
    taskRequirements="16" />
</root>
```

When no ISO review is defined on the document, `scheduleDef` will be empty and all other fields will reflect default/zero values.

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## isoDef Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `scheduleDef` | string | Schedule definition string (empty if none set) |
| `nextReviewDate` | ISO 8601 datetime | Next scheduled review date |
| `reviewById` | int | Reviewer user ID; `-5` = DocumentOwner, `-8` = Submitter |
| `reviewByName` | string | Reviewer display name |
| `reviewInstructions` | string | Instructions shown to the reviewer (task mode) |
| `workflowId` | int | Workflow definition ID; `0` = task mode |
| `workflowName` | string | Workflow definition name (empty if task mode) |
| `deadlineHours` | int | Task deadline in hours from the review trigger date |
| `priority` | int | Task priority: `0` = Low, `1` = Normal, `2` = High, `3` = Urgent |
| `assignerById` | int | ID of the user who set the ISO review definition |
| `assignerByName` | string | Full name of the user who set the ISO review definition |
| `assignmentDate` | ISO 8601 datetime | Date the ISO review definition was last assigned |
| `permissionChangeDueDate` | bool | Whether the reviewer may change the due date |
| `permissionChangePriority` | bool | Whether the reviewer may change the priority |
| `permissionChangeFinishDate` | bool | Whether the reviewer may change the finish date |
| `taskRequirements` | int | Bitmask of task requirement flags (XOR of `EnumTaskRequirement` values) |

### taskRequirements Bitmask Values

| Value | Requirement |
|-------|-------------|
| `1` | Sign |
| `2` | Edit |
| `4` | Read latest version |
| `8` | Read published version |
| `16` | Add comments |
| `32` | Approval |
| `64` | ISO Review |
| `128` | SOX Review |
| `512` | Archive |
| `1024` | Downgrade |
| `2048` | Declassify |

## Required Permissions

The caller must have read access to the document.

## Example

### Get ISO review definition (GET)

```
GET /srv.asmx/GetISOReviewDefinition?authenticationTicket=abc123-def456&documentPath=/Library/Policies/policy.pdf HTTP/1.1
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetISOReviewDefinition"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetISOReviewDefinition xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <documentPath>/Library/Policies/policy.pdf</documentPath>
    </GetISOReviewDefinition>
  </soap:Body>
</soap:Envelope>
```

## Notes

- When no ISO review schedule is set, `scheduleDef` is empty and `nextReviewDate` reflects the system base date
- The `taskRequirements` bitmask can be combined with the values in `ISOReviewDefinitionModel` when calling `SetISOReviewDefinition`

## Related APIs

- [`SetISOReviewDefinition`](SetISOReviewDefinition.md) — Set the ISO review schedule on a document
- [`RemoveISOReviewDefinition`](RemoveISOReviewDefinition.md) — Remove the ISO review schedule from a document
