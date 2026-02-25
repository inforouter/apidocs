# getTasks API

Returns a filtered list of workflow tasks based on XML search criteria. Tasks can be filtered by completion status, priority, date range, assignee, supervisor, workflow definition, document, and more. Results can be sorted by various task properties in ascending or descending order.

## Endpoint

```
/srv.asmx/getTasks
```

## Methods

- **GET** `/srv.asmx/getTasks?AuthenticationTicket=...&xmlcriteria=...&SortBy=...&AscendingOrder=...`
- **POST** `/srv.asmx/getTasks` (form data)
- **SOAP** Action: `http://tempuri.org/getTasks`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `xmlcriteria` | string | Yes | XML string containing filter criteria (see XML Criteria Format below) |
| `SortBy` | string | Yes | Sort field name from `TaskSortOption` enum (see Sort Options below) |
| `AscendingOrder` | boolean | Yes | `true` for ascending sort, `false` for descending |

## XML Criteria Format

The `xmlcriteria` parameter accepts an XML string with `<param>` elements, each specifying a `NAME` and `VALUE` attribute. All filter parameters are optional - omit a parameter to skip that filter.

```xml
<criteria>
  <param NAME="TASKCOMPLETIONSTATUS" VALUE="Due" />
  <param NAME="PRIORITY" VALUE="High" />
  <param NAME="STARTDATE" VALUE="2026-01-01" />
  <param NAME="ENDDATE" VALUE="2026-12-31" />
  <param NAME="DOMAINID" VALUE="1" />
  <param NAME="ASSIGNEEID" VALUE="42" />
  <param NAME="ASSIGNEDBYID" VALUE="15" />
  <param NAME="SUPERVISORID" VALUE="10" />
  <param NAME="WORKFLOWDEFID" VALUE="5" />
  <param NAME="DOCUMENTID" VALUE="100" />
  <param NAME="FLOWID" VALUE="200" />
  <param NAME="DOCUMENTTYPE" VALUE="Invoice" />
</criteria>
```

### Filter Parameters

| NAME | Value Type | Description |
|------|-----------|-------------|
| `TASKCOMPLETIONSTATUS` | string (enum) | Filter by task completion status (see values below) |
| `PRIORITY` | string (enum) | Filter by task priority (see values below) |
| `STARTDATE` | DateTime | Filter tasks with start date on or after this date |
| `ENDDATE` | DateTime | Filter tasks with start date on or before this date |
| `DOMAINID` / `LIBRARYID` | integer | Filter by domain/library ID (both names accepted) |
| `ASSIGNEEID` | integer | Filter by assignee user ID |
| `ASSIGNEDBYID` | integer | Filter by the user ID who assigned the task |
| `SUPERVISORID` | integer | Filter by supervisor user ID |
| `WORKFLOWDEFID` | integer | Filter by workflow definition ID |
| `DOCUMENTID` | integer | Filter by document ID |
| `FLOWID` | integer | Filter by workflow instance (flow) ID |
| `DOCUMENTTYPE` | string | Filter by document type name |

### TaskCompletionStatus Values

| Value | Description |
|-------|-------------|
| `NoCompletionStatus` | No filter (default) |
| `Due` | Tasks that are currently due |
| `OverDue` | Tasks that are past their due date |
| `Completed` | Completed tasks |
| `NotStarted` | Tasks that have not been started yet |
| `Reassigned` | Tasks that have been reassigned |
| `Dropped` | Tasks that have been dropped |
| `Archived` | Archived tasks |

### TaskPriority Values

| Value | Description |
|-------|-------------|
| `NoPriortySetting` | No priority filter (default) |
| `Low` | Low priority |
| `Normal` | Normal priority |
| `High` | High priority |
| `Urgent` | Urgent priority |

## Sort Options

The `SortBy` parameter accepts one of the following `TaskSortOption` values:

| Value | Description |
|-------|-------------|
| `DefaultSort` | Default sort order |
| `DocumentID` | Sort by document ID |
| `Instruction` | Sort by task instruction |
| `DateAssigned` | Sort by date assigned |
| `RecurringEndBy` | Sort by recurring end date |
| `DueDate` | Sort by due date |
| `ReminderDate` | Sort by reminder date |
| `Priority` | Sort by priority level |
| `TaskStatus` | Sort by task status |
| `FinishDate` | Sort by finish date |
| `Assignee` | Sort by assignee name |
| `AssignedBy` | Sort by assigner name |
| `WorkflowName` | Sort by workflow name |
| `DocTypeName` | Sort by document type name |
| `DocumentLibrary` | Sort by document library |
| `DocumentName` | Sort by document name |
| `SuperVisor` | Sort by supervisor name |

## Response Structure

### Success Response

```xml
<response success="true">
  <tasks>
    <Task>
      <TaskID>301</TaskID>
      <TaskName>Review Document</TaskName>
      <ShortInstruction>Please review and approve this document.</ShortInstruction>
      <StepNumber>2</StepNumber>
      <StepName>Review Step</StepName>
      <FlowID>50</FlowID>
      <FlowName>Document Approval</FlowName>
      <FlowDefID>5</FlowDefID>
      <Priority>High</Priority>
      <TaskStatus>InProgress</TaskStatus>
      <ApprovalStatus>Pending</ApprovalStatus>
      <StartDtae>2026-02-01 09:00:00</StartDtae>
      <FinishDate></FinishDate>
      <DueDate>2026-02-15 17:00:00</DueDate>
      <ShortComments></ShortComments>
      <TaskDefID>101</TaskDefID>
      <LinkedTaskID>0</LinkedTaskID>
      <AssigneeID>42</AssigneeID>
      <AssigneeType>User</AssigneeType>
      <AssigneeName>John Smith</AssigneeName>
      <AssignedByID>15</AssignedByID>
      <AssignedByName>Jane Doe</AssignedByName>
      <SuperVisorID>10</SuperVisorID>
      <SupervisorName>Admin User</SupervisorName>
      <DocumentID>1234</DocumentID>
      <DocumentName>Q1_Report.docx</DocumentName>
      <StartVersionNumber>1.0</StartVersionNumber>
      <EndVersionNumber>0.0</EndVersionNumber>
      <DocumentTypeId>3</DocumentTypeId>
      <DocumentTypeName>Report</DocumentTypeName>
      <DocumentFolderID>500</DocumentFolderID>
      <DocumentLibraryID>1</DocumentLibraryID>
      <DocumentLibraryName>Main Library</DocumentLibraryName>
      <DocumentCheckedOutByID>0</DocumentCheckedOutByID>
      <DocumentCheckedOutByName></DocumentCheckedOutByName>
      <DocumentTemplateID>0</DocumentTemplateID>
      <RedirectedFrom_UserID>0</RedirectedFrom_UserID>
      <RedirectedFrom_UserName></RedirectedFrom_UserName>
      <AdHoc>false</AdHoc>
      <DeadLine>14</DeadLine>
      <RequirementDetails>
        <Requirement>
          <Name>Approval Required</Name>
          <RequirementType>Approval</RequirementType>
          <Definition>Manager approval needed</Definition>
          <ObjectId>1</ObjectId>
        </Requirement>
      </RequirementDetails>
      <Requirements></Requirements>
      <Supervisor_NotificationOnDue>1</Supervisor_NotificationOnDue>
      <SupervisorNotificationDate>2026-02-14 09:00:00</SupervisorNotificationDate>
      <AllowedStartTimeSpan>0</AllowedStartTimeSpan>
      <AllowedStartDate></AllowedStartDate>
      <ReminderTimeSpan>1</ReminderTimeSpan>
      <ReminderDate>2026-02-14 09:00:00</ReminderDate>
      <Attachments>
        <Attachment>
          <AttachmentDate>2026-02-05 10:30:00</AttachmentDate>
          <DocumentId>1235</DocumentId>
          <WorkflowId>50</WorkflowId>
          <StepNumber>1</StepNumber>
          <StepName>Submit Step</StepName>
          <UserId>15</UserId>
        </Attachment>
      </Attachments>
    </Task>
    <!-- ... additional tasks ... -->
  </tasks>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Task Element Properties

| Element | Type | Description |
|---------|------|-------------|
| `TaskID` | integer | Unique identifier of the task instance |
| `TaskName` | string | Name of the task |
| `ShortInstruction` | string | Brief instruction text for the assignee |
| `StepNumber` | integer | Step number within the workflow |
| `StepName` | string | Name of the workflow step |
| `FlowID` | integer | Workflow instance (flow) ID |
| `FlowName` | string | Name of the workflow definition |
| `FlowDefID` | integer | Workflow definition ID |
| `Priority` | string | Task priority: `Low`, `Normal`, `High`, `Urgent` |
| `TaskStatus` | string | Current task status |
| `ApprovalStatus` | string | Approval status of the task |
| `StartDtae` | DateTime | Task start date |
| `FinishDate` | DateTime | Task completion date (empty if not finished) |
| `DueDate` | DateTime | Task due date |
| `ShortComments` | string | Brief comments on the task |
| `TaskDefID` | integer | Task definition ID |
| `LinkedTaskID` | integer | ID of a linked task (0 if none) |
| `AssigneeID` | integer | User ID of the task assignee |
| `AssigneeType` | string | Type of assignee: `User` or `Group` |
| `AssigneeName` | string | Display name of the assignee |
| `AssignedByID` | integer | User ID of who assigned the task |
| `AssignedByName` | string | Display name of the assigner |
| `SuperVisorID` | integer | User ID of the task supervisor |
| `SupervisorName` | string | Display name of the supervisor |
| `DocumentID` | integer | ID of the document associated with the task |
| `DocumentName` | string | Name of the associated document |
| `StartVersionNumber` | string | Document version when the task started |
| `EndVersionNumber` | string | Document version when the task ended |
| `DocumentTypeId` | integer | Document type definition ID |
| `DocumentTypeName` | string | Document type name |
| `DocumentFolderID` | integer | Folder ID containing the document |
| `DocumentLibraryID` | integer | Library/domain ID of the document |
| `DocumentLibraryName` | string | Library/domain name |
| `DocumentCheckedOutByID` | integer | User ID who has the document checked out (0 if not checked out) |
| `DocumentCheckedOutByName` | string | Name of user who has document checked out |
| `DocumentTemplateID` | integer | Template ID used for the document (0 if none) |
| `RedirectedFrom_UserID` | integer | Original assignee user ID if task was redirected (0 if not redirected) |
| `RedirectedFrom_UserName` | string | Original assignee name if redirected |
| `AdHoc` | boolean | Whether this is an ad-hoc task |
| `DeadLine` | integer | Deadline in days |
| `RequirementDetails` | XML | Nested list of task requirements |
| `Requirements` | string | Requirements summary |
| `Supervisor_NotificationOnDue` | integer | Days before due date to notify supervisor |
| `SupervisorNotificationDate` | DateTime | Date when supervisor notification is sent |
| `AllowedStartTimeSpan` | integer | Time span before task can be started |
| `AllowedStartDate` | DateTime | Earliest allowed start date |
| `ReminderTimeSpan` | integer | Reminder time span in days |
| `ReminderDate` | DateTime | Date when reminder is sent |
| `Attachments` | XML | Nested list of workflow attachments |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- Anonymous users cannot call this API (returns insufficient rights error)
- Tasks returned are scoped to the authenticated user's permissions

## Use Cases

1. **Task Dashboard**
   - Display all due tasks assigned to the current user
   - Show overdue tasks requiring attention

2. **Workflow Monitoring**
   - List all tasks for a specific workflow definition
   - Filter tasks by document or library

3. **Workload Management**
   - Review tasks assigned by or to a specific user
   - Filter by priority to focus on urgent items

4. **Reporting**
   - Query completed tasks within a date range
   - Analyze task distribution across supervisors

## Example Requests

### Request (GET)

```
GET /srv.asmx/getTasks?AuthenticationTicket=abc123-def456&xmlcriteria=%3Ccriteria%3E%3Cparam%20NAME%3D%22TASKCOMPLETIONSTATUS%22%20VALUE%3D%22Due%22%20%2F%3E%3C%2Fcriteria%3E&SortBy=DueDate&AscendingOrder=true HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/getTasks HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123-def456&xmlcriteria=<criteria><param NAME="TASKCOMPLETIONSTATUS" VALUE="Due" /></criteria>&SortBy=DueDate&AscendingOrder=true
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/getTasks"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getTasks xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <xmlcriteria><![CDATA[<criteria><param NAME="TASKCOMPLETIONSTATUS" VALUE="Due" /><param NAME="PRIORITY" VALUE="High" /></criteria>]]></xmlcriteria>
      <SortBy>DueDate</SortBy>
      <AscendingOrder>true</AscendingOrder>
    </getTasks>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getTasks(filters, sortBy = "DueDate", ascending = true) {
    const ticket = getUserAuthTicket();

    // Build XML criteria
    let xmlCriteria = "<criteria>";
    for (const [name, value] of Object.entries(filters)) {
        xmlCriteria += `<param NAME="${name}" VALUE="${value}" />`;
    }
    xmlCriteria += "</criteria>";

    const response = await fetch("/srv.asmx/getTasks", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `AuthenticationTicket=${encodeURIComponent(ticket)}&xmlcriteria=${encodeURIComponent(xmlCriteria)}&SortBy=${sortBy}&AscendingOrder=${ascending}`
    });

    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const tasks = [];
        xmlDoc.querySelectorAll("Task").forEach(task => {
            tasks.push({
                taskId: parseInt(task.querySelector("TaskID").textContent),
                taskName: task.querySelector("TaskName").textContent,
                flowName: task.querySelector("FlowName").textContent,
                priority: task.querySelector("Priority").textContent,
                taskStatus: task.querySelector("TaskStatus").textContent,
                dueDate: task.querySelector("DueDate").textContent,
                assigneeName: task.querySelector("AssigneeName").textContent,
                supervisorName: task.querySelector("SupervisorName").textContent,
                documentName: task.querySelector("DocumentName").textContent,
                instruction: task.querySelector("ShortInstruction").textContent
            });
        });
        return tasks;
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage examples
async function displayDueTasks() {
    try {
        const tasks = await getTasks({ TASKCOMPLETIONSTATUS: "Due" }, "DueDate", true);

        console.log(`Due tasks: ${tasks.length}`);
        tasks.forEach(task => {
            console.log(`[${task.priority}] ${task.taskName} - ${task.flowName} (Due: ${task.dueDate})`);
        });
    } catch (error) {
        console.error("Failed to get tasks:", error);
    }
}

async function getHighPriorityOverdueTasks() {
    try {
        const tasks = await getTasks({
            TASKCOMPLETIONSTATUS: "OverDue",
            PRIORITY: "High"
        }, "Priority", false);

        console.log(`High priority overdue tasks: ${tasks.length}`);
        tasks.forEach(task => {
            console.log(`${task.taskName} assigned to ${task.assigneeName} (Due: ${task.dueDate})`);
        });
    } catch (error) {
        console.error("Failed to get tasks:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        // Build XML criteria for due tasks in a specific library
        string xmlCriteria = @"<criteria>
            <param NAME=""TASKCOMPLETIONSTATUS"" VALUE=""Due"" />
            <param NAME=""DOMAINID"" VALUE=""1"" />
        </criteria>";

        var response = await client.getTasksAsync(authTicket, xmlCriteria, "DueDate", true);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            var tasks = root.Descendants("Task")
                .Select(t => new
                {
                    TaskId = int.Parse(t.Element("TaskID")?.Value ?? "0"),
                    TaskName = t.Element("TaskName")?.Value ?? "",
                    FlowName = t.Element("FlowName")?.Value ?? "",
                    Priority = t.Element("Priority")?.Value ?? "",
                    TaskStatus = t.Element("TaskStatus")?.Value ?? "",
                    DueDate = t.Element("DueDate")?.Value ?? "",
                    AssigneeName = t.Element("AssigneeName")?.Value ?? "",
                    DocumentName = t.Element("DocumentName")?.Value ?? ""
                })
                .ToList();

            Console.WriteLine($"Found {tasks.Count} tasks");
            foreach (var task in tasks)
            {
                Console.WriteLine($"[{task.Priority}] {task.TaskName} - {task.FlowName}");
                Console.WriteLine($"  Assignee: {task.AssigneeName} | Document: {task.DocumentName}");
                Console.WriteLine($"  Due: {task.DueDate} | Status: {task.TaskStatus}");
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

- The `xmlcriteria` parameter must be valid XML. An empty criteria element `<criteria></criteria>` returns all tasks visible to the authenticated user.
- Filter parameters are case-insensitive for the `NAME` attribute (internally converted to uppercase).
- Unrecognized parameter names in `xmlcriteria` will cause an error response.
- Invalid enum values for `SortBy`, `TASKCOMPLETIONSTATUS`, or `PRIORITY` will return a descriptive error.
- The `StartDtae` element name in the response contains a known typo (retained for backward compatibility).
- Task requirements and attachments are dynamically loaded for each task in the result set.
- Version numbers are returned in external format (e.g., `1.0`, `2.0`).

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated (anonymous) |
| `[SortBy] error:...` | Invalid `SortBy` value - must be a valid `TaskSortOption` enum name |
| `xmlcriteria parsing error:...` | The `xmlcriteria` parameter is not valid XML |
| `[PARAMETER_NAME] error:...` | Invalid value for a specific filter parameter |
| `[PARAMETER_NAME] Parameter not found` | Unrecognized parameter name in `xmlcriteria` |

## Related APIs

- `getTask` - Get a single task by task ID
- `GetUsersTaskPerformance` - Get user task performance statistics (due and overdue task counts)
- `GetWorkflowStatistics` - Get workflow performance statistics
- `GetUsersWorkflowRoles` - Get workflow roles assigned to a user
- `ActivateFlowDef` - Activate a workflow definition
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- Available to all authenticated users
- Supports comprehensive filtering via XML criteria for flexible task queries
