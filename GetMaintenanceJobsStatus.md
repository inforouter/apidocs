# GetMaintenanceJobsStatus API

Returns the status of all system maintenance jobs including their last execution time, duration, success status, schedule type, and whether they are overdue. This API is restricted to system administrators with the `ViewServerStatus` permission.

## Endpoint

```
/srv.asmx/GetMaintenanceJobsStatus
```

## Methods

- **GET** `/srv.asmx/GetMaintenanceJobsStatus?authenticationTicket=...`
- **POST** `/srv.asmx/GetMaintenanceJobsStatus` (form data)
- **SOAP** Action: `http://tempuri.org/GetMaintenanceJobsStatus`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true">
  <MaintenanceJob JobId="1" JobNameResourceId="3014" JobName="Check Notification Queue" ScheduleType="AnyTime" StartDate="2026-02-09T10:30:00" TimeElapsedMs="1250" Success="true" IsLate="false" />
  <MaintenanceJob JobId="2" JobNameResourceId="3015" JobName="Process Email Queue" ScheduleType="Hourly" StartDate="2026-02-09T09:00:00" TimeElapsedMs="3400" Success="true" IsLate="false" />
  <MaintenanceJob JobId="3" JobNameResourceId="3016" JobName="Clean Temp Files" ScheduleType="Daily" StartDate="2026-02-08T02:00:00" TimeElapsedMs="8500" Success="true" IsLate="false" />
  <MaintenanceJob JobId="4" JobNameResourceId="3017" JobName="Database Maintenance" ScheduleType="WeekLyOnMonday" StartDate="2026-02-03T03:00:00" TimeElapsedMs="45000" Success="true" IsLate="false" />
  <!-- ... additional maintenance jobs ... -->
</response>
```

### Jobs That Have Never Run

```xml
<MaintenanceJob JobId="5" JobNameResourceId="3018" JobName="Index Optimization" ScheduleType="Daily" StartDate="" TimeElapsedMs="0" Result="" IsLate="false" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## MaintenanceJob Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `JobId` | integer | Unique identifier for the maintenance job |
| `JobNameResourceId` | integer | Resource ID for the localized job name |
| `JobName` | string | Localized display name of the maintenance job |
| `ScheduleType` | string | Schedule frequency: `AnyTime`, `Hourly`, `Daily`, or `WeekLyOnMonday` |
| `StartDate` | DateTime | Last execution start date (ISO 8601), empty if never run |
| `TimeElapsedMs` | double | Duration of the last execution in milliseconds |
| `Success` | boolean | Whether the last execution completed successfully (only present if job has run) |
| `IsLate` | boolean | Whether the job is overdue based on its schedule type |

## Schedule Types

| ScheduleType | Description | IsLate Threshold |
|--------------|-------------|-----------------|
| `AnyTime` | Can run at any time | Late if last run > 1 day ago |
| `Hourly` | Runs every hour | Late if last run > 1 day ago |
| `Daily` | Runs once daily | Late if last run > 1 day ago |
| `WeekLyOnMonday` | Runs weekly on Monday | Late if last run > 7 days ago |

## Required Permissions

- Administrators only: User must have `ViewServerStatus` admin permission
- Non-admin users will receive an insufficient rights error

## Use Cases

1. **System Health Monitoring**
   - Monitor maintenance job execution status
   - Detect jobs that have failed or are overdue
   - Build automated alerting for late or failed jobs

2. **Troubleshooting**
   - Identify maintenance tasks that are not running
   - Review job execution times for performance issues

3. **Administration Dashboard**
   - Display maintenance job status on admin control panel
   - Show last run times and durations

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetMaintenanceJobsStatus?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetMaintenanceJobsStatus HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetMaintenanceJobsStatus"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetMaintenanceJobsStatus xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetMaintenanceJobsStatus>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getMaintenanceJobsStatus() {
    const ticket = getUserAuthTicket();
    const url = `/srv.asmx/GetMaintenanceJobsStatus?authenticationTicket=${encodeURIComponent(ticket)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const jobs = [];
        xmlDoc.querySelectorAll("MaintenanceJob").forEach(job => {
            jobs.push({
                jobId: parseInt(job.getAttribute("JobId")),
                jobName: job.getAttribute("JobName"),
                scheduleType: job.getAttribute("ScheduleType"),
                startDate: job.getAttribute("StartDate") || null,
                timeElapsedMs: parseFloat(job.getAttribute("TimeElapsedMs")),
                success: job.getAttribute("Success") === "true",
                isLate: job.getAttribute("IsLate") === "true"
            });
        });
        return jobs;
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function displayMaintenanceStatus() {
    try {
        const jobs = await getMaintenanceJobsStatus();

        const lateJobs = jobs.filter(j => j.isLate);
        const failedJobs = jobs.filter(j => j.startDate && !j.success);

        console.log(`Total jobs: ${jobs.length}`);
        console.log(`Late jobs: ${lateJobs.length}`);
        console.log(`Failed jobs: ${failedJobs.length}`);

        jobs.forEach(job => {
            const status = job.isLate ? "LATE" : (job.success ? "OK" : "FAILED");
            const elapsed = job.timeElapsedMs > 0 ? `${(job.timeElapsedMs / 1000).toFixed(1)}s` : "N/A";
            console.log(`[${status}] ${job.jobName} (${job.scheduleType}) - Last run: ${job.startDate || "Never"} - Duration: ${elapsed}`);
        });
    } catch (error) {
        console.error("Failed to get maintenance jobs status:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetMaintenanceJobsStatusAsync(authTicket);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            var jobs = root.Elements("MaintenanceJob")
                .Select(job => new
                {
                    JobId = int.Parse(job.Attribute("JobId")?.Value ?? "0"),
                    JobName = job.Attribute("JobName")?.Value ?? "",
                    ScheduleType = job.Attribute("ScheduleType")?.Value ?? "",
                    StartDate = job.Attribute("StartDate")?.Value ?? "",
                    TimeElapsedMs = double.Parse(job.Attribute("TimeElapsedMs")?.Value ?? "0"),
                    Success = job.Attribute("Success")?.Value == "true",
                    IsLate = job.Attribute("IsLate")?.Value == "true"
                })
                .ToList();

            foreach (var job in jobs)
            {
                var status = job.IsLate ? "LATE" : (job.Success ? "OK" : "FAILED");
                Console.WriteLine($"[{status}] {job.JobName} ({job.ScheduleType}) - Last: {(string.IsNullOrEmpty(job.StartDate) ? "Never" : job.StartDate)}");
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

- The system includes approximately 20 maintenance job types covering notification processing, cleanup, indexing, and database maintenance.
- **IsLate** calculation is based on the schedule type: daily/hourly/anytime jobs are considered late after 1 day, weekly jobs after 7 days.
- Jobs that have never been executed have an empty `StartDate`, `TimeElapsedMs` of 0, and `IsLate` of false.
- Job names are localized based on the authenticated user's language setting using the `JobNameResourceId`.
- Job logs are retrieved from the database maintenance job log table.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | User does not have `ViewServerStatus` admin permission |

## Related APIs

- `FlushApplicationCache` - Flush application cache
- `GetWarehouseStatus` - Get warehouse storage status
- `ServerInfo` - Get basic server information
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New in current version**: Provides programmatic access to maintenance job monitoring
- Admin-only for security reasons
