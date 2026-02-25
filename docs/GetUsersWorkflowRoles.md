# GetUsersWorkflowRoles API

Returns all workflow roles assigned to a specified user, including supervisor and assignee roles across all workflow definitions. A user may appear in the results because they are directly assigned to a task, assigned through group membership, or designated as a task supervisor.

## Endpoint

```
/srv.asmx/GetUsersWorkflowRoles
```

## Methods

- **GET** `/srv.asmx/GetUsersWorkflowRoles?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/GetUsersWorkflowRoles` (form data)
- **SOAP** Action: `http://tempuri.org/GetUsersWorkflowRoles`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `userName` | string | Yes | The user name to retrieve workflow roles for |

## Response Structure

### Success Response

```xml
<response success="true">
  <WorkflowRoles>
    <WorkflowRole TaskDefId="101" TaskName="Review Document" FlowDefId="5" FlowName="Document Approval" StepNumber="2" SupervisorId="42" SupervisorName="John Smith" />
    <WorkflowRole TaskDefId="205" TaskName="Final Sign-Off" FlowDefId="8" FlowName="Contract Workflow" StepNumber="1" SupervisorId="15" SupervisorName="Jane Doe" />
  </WorkflowRoles>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## WorkflowRole Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `TaskDefId` | integer | Unique identifier of the task definition |
| `TaskName` | string | Name of the task definition |
| `FlowDefId` | integer | Unique identifier of the workflow definition |
| `FlowName` | string | Name of the workflow definition |
| `StepNumber` | integer | Step number within the workflow where this task is defined |
| `SupervisorId` | integer | User ID of the task supervisor |
| `SupervisorName` | string | Display name of the task supervisor |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- Caller must have `ListingUserOwnerships` admin permission for the target user
- Non-authorized users will receive an insufficient rights error

## Use Cases

1. **User Administration**
   - View all workflow assignments for a user before account changes
   - Audit user participation across workflow definitions

2. **Workflow Management**
   - Identify which workflows a user is involved in
   - Determine supervisor vs. assignee relationships

3. **Workload Analysis**
   - Review task distribution for a specific user
   - Plan task reassignment when a user leaves the organization

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetUsersWorkflowRoles?authenticationTicket=abc123-def456&userName=jsmith HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetUsersWorkflowRoles HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetUsersWorkflowRoles"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetUsersWorkflowRoles xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
    </GetUsersWorkflowRoles>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getUsersWorkflowRoles(userName) {
    const ticket = getUserAuthTicket();
    const url = `/srv.asmx/GetUsersWorkflowRoles?authenticationTicket=${encodeURIComponent(ticket)}&userName=${encodeURIComponent(userName)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const roles = [];
        const roleElements = xmlDoc.querySelectorAll("WorkflowRole");
        roleElements.forEach(role => {
            roles.push({
                taskDefId: parseInt(role.getAttribute("TaskDefId")),
                taskName: role.getAttribute("TaskName"),
                flowDefId: parseInt(role.getAttribute("FlowDefId")),
                flowName: role.getAttribute("FlowName"),
                stepNumber: parseInt(role.getAttribute("StepNumber")),
                supervisorId: parseInt(role.getAttribute("SupervisorId")),
                supervisorName: role.getAttribute("SupervisorName")
            });
        });
        return roles;
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function displayUserWorkflowRoles(userName) {
    try {
        const roles = await getUsersWorkflowRoles(userName);

        roles.forEach(role => {
            console.log(`${role.flowName} - Step ${role.stepNumber}: ${role.taskName} (Supervisor: ${role.supervisorName})`);
        });

    } catch (error) {
        console.error("Failed to get workflow roles:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetUsersWorkflowRolesAsync(authTicket, userName);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            var roles = root.Descendants("WorkflowRole")
                .Select(r => new
                {
                    TaskDefId = int.Parse(r.Attribute("TaskDefId")?.Value ?? "0"),
                    TaskName = r.Attribute("TaskName")?.Value ?? "",
                    FlowDefId = int.Parse(r.Attribute("FlowDefId")?.Value ?? "0"),
                    FlowName = r.Attribute("FlowName")?.Value ?? "",
                    StepNumber = int.Parse(r.Attribute("StepNumber")?.Value ?? "0"),
                    SupervisorId = int.Parse(r.Attribute("SupervisorId")?.Value ?? "0"),
                    SupervisorName = r.Attribute("SupervisorName")?.Value ?? ""
                })
                .ToList();

            foreach (var role in roles)
            {
                Console.WriteLine($"{role.FlowName} - Step {role.StepNumber}: {role.TaskName} (Supervisor: {role.SupervisorName})");
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

- A user appears in the results if they are a **direct assignee**, assigned through **group membership**, or designated as the **task supervisor**.
- To determine the user's role type, compare the `SupervisorName` attribute with the queried `userName`. If they match, the user is the supervisor for that task. The user may also be an assignee of the same task.
- The response includes roles from all active workflow definitions across all domains.
- The `WorkflowRoles` element will be empty if the user has no workflow role assignments.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | Caller does not have `ListingUserOwnerships` admin permission for the target user |

## Related APIs

- `GetUsersTaskPerformance` - Get user task performance statistics (due and overdue task counts)
- `GetWorkflowStatistics` - Get workflow performance statistics
- `GetFlowDef` - Get a workflow definition
- `GetFolderFlows` - Get workflow definitions for a folder
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New**: Added to provide programmatic access to user workflow role information previously only available through the Control Panel UI
