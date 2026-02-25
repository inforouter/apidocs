# GetUsersTaskPerformance API

Returns a list of users with their task performance statistics, including due and overdue task counts. This API is useful for monitoring user workload and identifying bottlenecks in workflow processing.

## Endpoint

```
/srv.asmx/GetUsersTaskPerformance
```

## Methods

- **GET** `/srv.asmx/GetUsersTaskPerformance?authenticationTicket=...`
- **POST** `/srv.asmx/GetUsersTaskPerformance` (form data)
- **SOAP** Action: `http://tempuri.org/GetUsersTaskPerformance`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true">
  <ArrayOfUserTaskStatisticModel>
    <UserTaskStatisticModel>
      <AssigneeId>123</AssigneeId>
      <AssigneeName>John Smith</AssigneeName>
      <DueCount>5</DueCount>
      <OverdueCount>2</OverdueCount>
    </UserTaskStatisticModel>
    <UserTaskStatisticModel>
      <AssigneeId>456</AssigneeId>
      <AssigneeName>Jane Doe</AssigneeName>
      <DueCount>3</DueCount>
      <OverdueCount>0</OverdueCount>
    </UserTaskStatisticModel>
  </ArrayOfUserTaskStatisticModel>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## UserTaskStatisticModel Properties

| Property | Type | Description |
|----------|------|-------------|
| `AssigneeId` | integer | Unique identifier of the user |
| `AssigneeName` | string | Display name of the user |
| `DueCount` | integer | Number of active tasks assigned to the user |
| `OverdueCount` | integer | Number of overdue tasks assigned to the user |

## Required Permissions

- User must be authenticated (anonymous users cannot access this API)
- No specific administrative permissions required

## Use Cases

1. **Workload Monitoring**
   - Track task distribution across team members
   - Identify users with high task loads
   - Balance workload across the team

2. **Performance Dashboard**
   - Display real-time task statistics
   - Highlight users with overdue tasks
   - Monitor team productivity

3. **Management Reporting**
   - Generate task performance reports
   - Track overdue task trends
   - Identify bottlenecks in workflow processing

4. **Alert Systems**
   - Notify managers when users have overdue tasks
   - Trigger escalation when overdue counts exceed thresholds

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetUsersTaskPerformance?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetUsersTaskPerformance HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetUsersTaskPerformance"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetUsersTaskPerformance xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetUsersTaskPerformance>
  </soap:Body>
</soap:Envelope>
```

### Success Response Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<response success="true">
  <ArrayOfUserTaskStatisticModel>
    <UserTaskStatisticModel>
      <AssigneeId>101</AssigneeId>
      <AssigneeName>Alice Johnson</AssigneeName>
      <DueCount>8</DueCount>
      <OverdueCount>1</OverdueCount>
    </UserTaskStatisticModel>
    <UserTaskStatisticModel>
      <AssigneeId>102</AssigneeId>
      <AssigneeName>Bob Williams</AssigneeName>
      <DueCount>12</DueCount>
      <OverdueCount>3</OverdueCount>
    </UserTaskStatisticModel>
    <UserTaskStatisticModel>
      <AssigneeId>103</AssigneeId>
      <AssigneeName>Carol Davis</AssigneeName>
      <DueCount>4</DueCount>
      <OverdueCount>0</OverdueCount>
    </UserTaskStatisticModel>
  </ArrayOfUserTaskStatisticModel>
</response>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getUsersTaskPerformance() {
    const ticket = getUserAuthTicket();

    const url = `/srv.asmx/GetUsersTaskPerformance?authenticationTicket=${encodeURIComponent(ticket)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const users = xmlDoc.querySelectorAll("UserTaskStatisticModel");
        return Array.from(users).map(user => ({
            assigneeId: parseInt(user.querySelector("AssigneeId").textContent),
            assigneeName: user.querySelector("AssigneeName").textContent,
            dueCount: parseInt(user.querySelector("DueCount").textContent),
            overdueCount: parseInt(user.querySelector("OverdueCount").textContent)
        }));
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function displayTaskDashboard() {
    try {
        const users = await getUsersTaskPerformance();

        // Sort by overdue count (descending)
        users.sort((a, b) => b.overdueCount - a.overdueCount);

        console.log("User Task Performance:");
        users.forEach(user => {
            const status = user.overdueCount > 0 ? "ATTENTION" : "OK";
            console.log(`[${status}] ${user.assigneeName}: ${user.dueCount} due, ${user.overdueCount} overdue`);
        });

        // Calculate totals
        const totalDue = users.reduce((sum, u) => sum + u.dueCount, 0);
        const totalOverdue = users.reduce((sum, u) => sum + u.overdueCount, 0);
        console.log(`\nTotal: ${totalDue} due tasks, ${totalOverdue} overdue`);

    } catch (error) {
        console.error("Failed to get task performance:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetUsersTaskPerformanceAsync(authTicket);

        var root = XElement.Parse(response.ToString());
        if (root.Attribute("success")?.Value == "true")
        {
            var users = root.Descendants("UserTaskStatisticModel")
                .Select(u => new
                {
                    AssigneeId = int.Parse(u.Element("AssigneeId")?.Value ?? "0"),
                    AssigneeName = u.Element("AssigneeName")?.Value,
                    DueCount = int.Parse(u.Element("DueCount")?.Value ?? "0"),
                    OverdueCount = int.Parse(u.Element("OverdueCount")?.Value ?? "0")
                })
                .OrderByDescending(u => u.OverdueCount)
                .ToList();

            Console.WriteLine("User Task Performance Report:");
            Console.WriteLine("----------------------------");

            foreach (var user in users)
            {
                var status = user.OverdueCount > 0 ? "[!]" : "[ ]";
                Console.WriteLine($"{status} {user.AssigneeName}: {user.DueCount} due, {user.OverdueCount} overdue");
            }

            var totalDue = users.Sum(u => u.DueCount);
            var totalOverdue = users.Sum(u => u.OverdueCount);
            Console.WriteLine($"\nTotal: {totalDue} due tasks, {totalOverdue} overdue");
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

## Dashboard Integration

```html
<!-- User Task Performance Dashboard -->
<div class="task-performance-dashboard">
    <h2>User Task Performance</h2>
    <table id="task-table">
        <thead>
            <tr>
                <th>User</th>
                <th>Due Tasks</th>
                <th>Overdue</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody id="task-body"></tbody>
        <tfoot>
            <tr>
                <td><strong>Total</strong></td>
                <td id="total-due"></td>
                <td id="total-overdue"></td>
                <td></td>
            </tr>
        </tfoot>
    </table>
</div>

<script>
async function updateTaskDashboard() {
    const users = await getUsersTaskPerformance();
    const tbody = document.getElementById("task-body");
    tbody.innerHTML = "";

    let totalDue = 0;
    let totalOverdue = 0;

    users.sort((a, b) => b.overdueCount - a.overdueCount);

    users.forEach(user => {
        totalDue += user.dueCount;
        totalOverdue += user.overdueCount;

        const row = document.createElement("tr");
        row.className = user.overdueCount > 0 ? "warning" : "";
        row.innerHTML = `
            <td>${user.assigneeName}</td>
            <td>${user.dueCount}</td>
            <td class="${user.overdueCount > 0 ? 'text-red' : ''}">${user.overdueCount}</td>
            <td>${user.overdueCount > 0 ? 'Attention Required' : 'OK'}</td>
        `;
        tbody.appendChild(row);
    });

    document.getElementById("total-due").textContent = totalDue;
    document.getElementById("total-overdue").textContent = totalOverdue;
}

// Refresh every 60 seconds
setInterval(updateTaskDashboard, 60000);
updateTaskDashboard();
</script>
```

## Notes

- **DueCount**: Total number of active (started but not finished) tasks assigned to the user
- **OverdueCount**: Number of tasks where the due date has passed
- **Real-time Data**: Statistics are calculated in real-time from current database state
- **Sorted by Name**: Results are returned sorted by assignee name
- **Active Tasks Only**: Only counts tasks that have been started but not yet completed

## Statistics Calculations

### DueCount
- Counts tasks where:
  - Task is assigned to the user (ASSIGNEETYPE = USER)
  - Task has been started (STARTDATE is not null)
  - Task has not been completed (FINISHDATE is null)

### OverdueCount
- Counts tasks where:
  - All DueCount conditions apply
  - Task due date is before the current date (DUEDATE < current date)

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |

## Best Practices

1. **Polling Frequency**: For dashboards, poll every 30-60 seconds
2. **Caching**: Cache results for 1-2 minutes for high-traffic dashboards
3. **Sorting**: Sort by overdue count to highlight users needing attention
4. **Alerts**: Set up notifications when overdue count exceeds thresholds
5. **Visualization**: Use color coding to highlight overdue tasks (red) vs normal (green)

## Performance Considerations

- **Efficient**: Query is optimized with database grouping
- **Real-Time**: No caching - always returns current state
- **Scalable**: Performance is proportional to number of users with active tasks

## Related APIs

- `getTasks` - Get detailed task list with filtering
- `GetTask` - Get specific task details
- `CompleteTask` - Complete a workflow task
- `ReassignTask` - Reassign task to different user
- `GetWorkflowStatistics` - Get workflow-level statistics

## Version History

- Compatible with infoRouter 8.7 and later
- Statistics model is serializable for client-side deserialization
- Supports both synchronous SOAP and REST access patterns
- Workflow management features may require Workflow module license

## See Also

- [GetWorkflowStatistics](./GetWorkflowStatistics.md) - Get workflow statistics
- [getTasks](./getTasks.md) - Get workflow tasks
- Control Panel UI: `UserTaskReport.aspx` - User task performance report
