# GetWorkflowStatistics API

Returns comprehensive statistics for a specific workflow definition, including pending, completed, and overdue flow counts, with optional date range filtering.

## Endpoint

```
/srv.asmx/GetWorkflowStatistics
```

## Methods

- **GET** `/srv.asmx/GetWorkflowStatistics?authenticationTicket=...&domainName=...&workflowName=...&startDate=...&endDate=...`
- **POST** `/srv.asmx/GetWorkflowStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetWorkflowStatistics`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `domainName` | string | Yes | Name of the domain/library containing the workflow |
| `workflowName` | string | Yes | Name of the workflow definition |
| `startDate` | DateTime | No | Start date for range filtering (null for all-time only) |
| `endDate` | DateTime | No | End date for range filtering (null for all-time only) |

## Response Behavior

### All-Time Statistics Only (No Date Range)

When `startDate` and `endDate` are not provided or null:

```
GET /srv.asmx/GetWorkflowStatistics?authenticationTicket=xxx&domainName=Engineering&workflowName=DocumentReview
```

Response includes:
- Domain and workflow information
- Average processing time (hours and text)
- Total pending count (all-time)
- Total completed count (all-time)
- Total overdue count

### With Date Range Statistics

When `startDate` and `endDate` are provided:

```
GET /srv.asmx/GetWorkflowStatistics?authenticationTicket=xxx&domainName=Engineering&workflowName=DocumentReview&startDate=2024-01-01&endDate=2024-01-31
```

Response includes all-time statistics PLUS date range specific data:
- Submitted count in range
- Completed count in range
- Pending count in range

## Response Structure

### All-Time Statistics (No Dates)

```xml
<root success="true">
  <WorkflowStatistics>
    <DomainName>Engineering</DomainName>
    <WorkflowName>DocumentReview</WorkflowName>
    <ActiveFolderPath>/Engineering/Reviews/Active</ActiveFolderPath>
    <AverageTimeSpanInHours>27</AverageTimeSpanInHours>
    <AverageTimeSpanInText>1 day 3 hours</AverageTimeSpanInText>
    <TotalPending>15</TotalPending>
    <TotalCompleted>892</TotalCompleted>
    <TotalOverdue>2</TotalOverdue>
  </WorkflowStatistics>
</root>
```

### With Date Range Statistics

```xml
<root success="true">
  <WorkflowStatistics>
    <DomainName>Engineering</DomainName>
    <WorkflowName>DocumentReview</WorkflowName>
    <ActiveFolderPath>/Engineering/Reviews/Active</ActiveFolderPath>
    
    <!-- Date range specific (only when dates provided) -->
    <PendingInRange>3</PendingInRange>
    <SubmittedInRange>45</SubmittedInRange>
    <CompletedInRange>42</CompletedInRange>
    
    <!-- All-time statistics -->
    <AverageTimeSpanInHours>27</AverageTimeSpanInHours>
    <AverageTimeSpanInText>1 day 3 hours</AverageTimeSpanInText>
    <TotalPending>15</TotalPending>
    <TotalCompleted>892</TotalCompleted>
    <TotalOverdue>2</TotalOverdue>
  </WorkflowStatistics>
</root>
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## WorkflowStatistics Properties

| Property | Type | Description | When Included |
|----------|------|-------------|---------------|
| `DomainName` | string | Name of the domain | Always |
| `WorkflowName` | string | Name of the workflow | Always |
| `ActiveFolderPath` | string | Path to workflow's active folder | Always |
| `AverageTimeSpanInHours` | integer | Average time in hours | Always |
| `AverageTimeSpanInText` | string | Human-readable average time | Always |
| `TotalPending` | integer | All-time pending count | Always |
| `TotalCompleted` | integer | All-time completed count | Always |
| `TotalOverdue` | integer | Current overdue count | Always |
| `PendingInRange` | integer (nullable) | Pending in date range | Only with dates |
| `SubmittedInRange` | integer (nullable) | Submitted in date range | Only with dates |
| `CompletedInRange` | integer (nullable) | Completed in date range | Only with dates |

## Required Permissions

- User must be authenticated (anonymous users cannot access workflow statistics)
- User must have access to the specified domain
- No specific workflow permissions required to view statistics

## Use Cases

1. **Single Workflow Monitor**
   - Track specific workflow performance
   - Monitor real-time status
   - Alert on overdue instances

2. **Monthly Performance Report**
   - Analyze workflow performance over time
   - Compare month-over-month metrics
   - Track submission and completion trends

3. **Dashboard Integration**
   - Real-time workflow status displays
   - KPI monitoring
   - Performance metrics visualization

4. **Capacity Planning**
   - Analyze workflow load
   - Identify bottlenecks
   - Plan resource allocation

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetWorkflowStatistics?authenticationTicket=abc123-def456&domainName=Engineering&workflowName=DocumentReview HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetWorkflowStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&domainName=Engineering&workflowName=DocumentReview
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetWorkflowStatistics"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetWorkflowStatistics xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <domainName>Engineering</domainName>
      <workflowName>DocumentReview</workflowName>
      <startDate></startDate>
      <endDate></endDate>
    </GetWorkflowStatistics>
  </soap:Body>
</soap:Envelope>
```

### Success Response Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="true">
  <WorkflowStatistics>
    <DomainName>Quality</DomainName>
    <WorkflowName>QualityApproval</WorkflowName>
    <ActiveFolderPath>/Quality/Pending Approvals</ActiveFolderPath>
    <AverageTimeSpanInHours>27</AverageTimeSpanInHours>
    <AverageTimeSpanInText>1 day 3 hours</AverageTimeSpanInText>
    <TotalPending>45</TotalPending>
    <TotalCompleted>892</TotalCompleted>
    <TotalOverdue>7</TotalOverdue>
  </WorkflowStatistics>
</root>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getWorkflowStats(domainName, workflowName, startDate = null, endDate = null) {
    const ticket = getUserAuthTicket();
    
    let url = `/srv.asmx/GetWorkflowStatistics?` +
              `authenticationTicket=${encodeURIComponent(ticket)}&` +
              `domainName=${encodeURIComponent(domainName)}&` +
              `workflowName=${encodeURIComponent(workflowName)}`;
    
    if (startDate && endDate) {
        url += `&startDate=${startDate.toISOString().split('T')[0]}`;
        url += `&endDate=${endDate.toISOString().split('T')[0]}`;
    }
    
    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");
    
    const root = xmlDoc.querySelector("root");
    if (root.getAttribute("success") === "true") {
        const stats = xmlDoc.querySelector("WorkflowStatistics");
        return {
            domainName: stats.querySelector("DomainName").textContent,
            workflowName: stats.querySelector("WorkflowName").textContent,
            activeFolderPath: stats.querySelector("ActiveFolderPath").textContent,
            avgTimeHours: parseInt(stats.querySelector("AverageTimeSpanInHours").textContent),
            avgTimeText: stats.querySelector("AverageTimeSpanInText").textContent,
            totalPending: parseInt(stats.querySelector("TotalPending").textContent),
            totalCompleted: parseInt(stats.querySelector("TotalCompleted").textContent),
            totalOverdue: parseInt(stats.querySelector("TotalOverdue").textContent),
            // Date range specific (if provided)
            pendingInRange: stats.querySelector("PendingInRange")?.textContent 
                ? parseInt(stats.querySelector("PendingInRange").textContent) : null,
            submittedInRange: stats.querySelector("SubmittedInRange")?.textContent 
                ? parseInt(stats.querySelector("SubmittedInRange").textContent) : null,
            completedInRange: stats.querySelector("CompletedInRange")?.textContent 
                ? parseInt(stats.querySelector("CompletedInRange").textContent) : null
        };
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function displayWorkflowMonitor() {
    try {
        const stats = await getWorkflowStats("Engineering", "DocumentReview");
        
        console.log(`Workflow: ${stats.workflowName}`);
        console.log(`Average Time: ${stats.avgTimeText} (${stats.avgTimeHours} hours)`);
        console.log(`Pending: ${stats.totalPending}`);
        console.log(`Completed: ${stats.totalCompleted}`);
        console.log(`Overdue: ${stats.totalOverdue}`);
        
        // Calculate efficiency
        const totalFlows = stats.totalCompleted + stats.totalPending;
        const completionRate = (stats.totalCompleted / totalFlows * 100).toFixed(1);
        console.log(`Completion Rate: ${completionRate}%`);
        
        // Alert on overdue
        if (stats.totalOverdue > 0) {
            alert(`Warning: ${stats.totalOverdue} overdue workflow instances!`);
        }
    } catch (error) {
        console.error("Failed to get workflow statistics:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetWorkflowStatisticsAsync(
            authTicket,
            "Engineering",
            "DocumentReview",
            null,  // startDate
            null   // endDate
        );
        
        var root = response.Root;
        if (root.Attribute("success")?.Value == "true")
        {
            var stats = root.Element("WorkflowStatistics");
            
            var workflowStats = new
            {
                DomainName = stats.Element("DomainName")?.Value,
                WorkflowName = stats.Element("WorkflowName")?.Value,
                ActiveFolderPath = stats.Element("ActiveFolderPath")?.Value,
                AvgTimeHours = int.Parse(stats.Element("AverageTimeSpanInHours")?.Value ?? "0"),
                AvgTimeText = stats.Element("AverageTimeSpanInText")?.Value,
                TotalPending = int.Parse(stats.Element("TotalPending")?.Value ?? "0"),
                TotalCompleted = int.Parse(stats.Element("TotalCompleted")?.Value ?? "0"),
                TotalOverdue = int.Parse(stats.Element("TotalOverdue")?.Value ?? "0")
            };
            
            Console.WriteLine($"Workflow: {workflowStats.WorkflowName} in {workflowStats.DomainName}");
            Console.WriteLine($"Active Folder: {workflowStats.ActiveFolderPath}");
            Console.WriteLine($"Average Time: {workflowStats.AvgTimeText} ({workflowStats.AvgTimeHours} hours)");
            Console.WriteLine($"Pending: {workflowStats.TotalPending}");
            Console.WriteLine($"Completed: {workflowStats.TotalCompleted}");
            Console.WriteLine($"Overdue: {workflowStats.TotalOverdue}");
            
            // Calculate metrics
            int totalFlows = workflowStats.TotalCompleted + workflowStats.TotalPending;
            double completionRate = totalFlows > 0 
                ? (double)workflowStats.TotalCompleted / totalFlows * 100 
                : 0;
            
            Console.WriteLine($"Completion Rate: {completionRate:F1}%");
            
            if (workflowStats.TotalOverdue > 0)
            {
                Console.WriteLine($"ALERT: {workflowStats.TotalOverdue} overdue workflow instances");
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

## Dashboard Integration

This API is ideal for building workflow monitoring dashboards:

```html
<!-- Single Workflow Statistics Dashboard -->
<div class="workflow-stats">
    <h2 id="workflow-title"></h2>
    <div class="stats-grid">
        <div class="stat-card">
            <h3>Pending</h3>
            <p id="pending-count" class="stat-value"></p>
        </div>
        <div class="stat-card">
            <h3>Completed</h3>
            <p id="completed-count" class="stat-value"></p>
        </div>
        <div class="stat-card warning">
            <h3>Overdue</h3>
            <p id="overdue-count" class="stat-value"></p>
        </div>
        <div class="stat-card">
            <h3>Avg. Time</h3>
            <p id="avg-time-text" class="stat-value"></p>
            <small id="avg-time-hours"></small>
        </div>
    </div>
    <div class="workflow-details">
        <p><strong>Active Folder:</strong> <span id="active-folder"></span></p>
    </div>
</div>

<script>
async function updateDashboard(domainName, workflowName) {
    const stats = await getWorkflowStats(domainName, workflowName);
    
    document.getElementById("workflow-title").textContent = `${stats.workflowName} (${stats.domainName})`;
    document.getElementById("active-folder").textContent = stats.activeFolderPath;
    document.getElementById("pending-count").textContent = stats.totalPending;
    document.getElementById("completed-count").textContent = stats.totalCompleted;
    document.getElementById("overdue-count").textContent = stats.totalOverdue;
    document.getElementById("avg-time-text").textContent = stats.avgTimeText;
    document.getElementById("avg-time-hours").textContent = `(${stats.avgTimeHours} hours)`;
}

// Refresh every 30 seconds
setInterval(() => updateDashboard("Engineering", "DocumentReview"), 30000);
updateDashboard("Engineering", "DocumentReview");
</script>
```

## Notes

- **TotalCompleted**: All workflow instances that have reached completion
- **TotalPending**: Workflow instances currently in progress (all-time)
- **TotalOverdue**: Workflow instances with overdue tasks
- **AverageTimeSpanInText**: Human-readable format (e.g., "2 days 5 hours")
- **AverageTimeSpanInHours**: Numeric value for programmatic comparisons
- **PendingInRange, SubmittedInRange, CompletedInRange**: Only present when date range provided
- **Real-time Data**: Statistics are calculated in real-time from current database state
- **Performance**: Optimized for single workflow - faster than bulk reporting

## Statistics Calculations

### All-Time Metrics
- **TotalCompleted**: Counts all workflow instances that reached completion
- **TotalPending**: Counts workflow instances at any step (not completed)
- **TotalOverdue**: Based on task due dates compared to current date

### Date Range Metrics (Optional)
- **SubmittedInRange**: Workflows submitted during the specified period
- **CompletedInRange**: Workflows completed during the specified period
- **PendingInRange**: Workflows still pending within the date range

### Average TimeSpan
- Calculated from workflow start to completion
- Based on completed workflow instances only
- **AverageTimeSpanInText**: Human-readable string
- **AverageTimeSpanInHours**: Numeric value for calculations
- May return 0 or empty string if no completed instances exist

## Best Practices

1. **Caching**: Cache results for 1-5 minutes for dashboard displays
2. **Monitor Overdue**: Set up alerts when overdue count exceeds threshold
3. **Date Range Queries**: Use for monthly/quarterly reporting
4. **Polling Frequency**: For real-time dashboards, poll every 30-60 seconds
5. **Error Handling**: Always handle workflow not found and access denied errors
6. **Performance**: Single workflow queries are fast and efficient

## Performance Considerations

- **Optimized**: Single workflow statistics are calculated quickly
- **Real-Time**: No caching - always returns current state
- **Efficient**: Significantly faster than bulk reporting
- **Date Range Impact**: Date range queries may take slightly longer
- **Recommended**: For bulk reporting, call API multiple times for different workflows

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |
| `Workflow definition not found` | No workflow with specified name in domain |
| `Domain not found` | Specified domain does not exist |
| `Access denied` | User does not have access to the domain |

## Benefits

? **Fast Performance**: Optimized for single workflow queries  
? **Real-Time Data**: Always returns current workflow state  
? **Flexible**: Supports all-time or date range statistics  
? **Efficient**: Minimal server load for targeted queries  
? **Simple**: Returns single object, easy to parse and use  
? **Comprehensive**: All key workflow metrics in one call  

## Related APIs

- `GetFlowDef` - Get detailed workflow definition
- `GetDomainFlows` - List all workflows in a domain (use this to get workflow names, then call GetWorkflowStatistics for each)
- `getTasks` - Get workflow tasks with filtering
- `GetTask` - Get specific task details
- `CompleteTask` - Complete a workflow task
- `ReassignTask` - Reassign task to different user

## Version History

- Compatible with infoRouter 8.7 and later
- Statistics model is serializable for client-side deserialization
- Supports both synchronous SOAP and REST access patterns
- Workflow management features may require Workflow module license

## See Also

- [GetFlowDef](./GetFlowDef.md) - Get workflow definition details
- [GetDomainFlows](./GetDomainFlows.md) - List all workflows in domain
- [getTasks](./getTasks.md) - Get workflow tasks
- Control Panel UI: `WorkflowReport.aspx` - Workflow statistics report
