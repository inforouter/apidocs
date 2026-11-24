# infoRouter Version 9 system requirements

Read this page before you install infoRouter Version 9 or upgrade to it. It gives the minimum and the
recommended configuration of the server and of the client workstations. You may give the server more than is
recommended here; giving it less results in poor performance.

Running infoRouter Version 8? See the
[infoRouter Version 8 System Requirements](https://support.inforouter.com/documentation/v80/inforouter-system-requirements-v8.aspx).

!!! note "Platform support policy"
    infoRouter follows Microsoft's support lifecycle. When Microsoft ends support for one of its platforms,
    infoRouter ends support for that platform on the same date. We do not recommend and do not support
    installations on platforms other than the ones named on this page.

## Requirements for the server

### Server hardware

A dedicated server class machine with at least:

| Resource | Minimum | Recommended |
|---|---|---|
| Processor | Intel Xeon or better | |
| Memory | 32 GB | 64 GB or more, especially when infoRouter Connect runs on the server |
| Disk | 100 GB to start | Additional space for the document warehouse and the search index, sized for the number of documents and their growth |

Virtual servers are supported as long as the virtual machine meets the requirements above.

Give infoRouter a server of its own, so that it does not compete with other applications for the server's
resources. Version 9 includes its own .NET runtime, so it does not conflict with the .NET versions other
applications use.

### Server operating system

| Windows Server | New installation | Upgrade of an existing installation |
|---|---|---|
| 2025 | Supported | Supported |
| 2022 | Supported | Supported |
| 2019 | Supported | Supported |
| 2016 | Not supported | Supported until 12 January 2027, the day Microsoft ends its support |
| 2012 R2 and older | Not supported | Not supported |

- A 64-bit environment is required. 32-bit platforms are not supported.
- Keep the server up to date with the current Windows updates.

### Supported DBMS platforms

One of the following is required:

| DBMS | Version |
|---|---|
| Microsoft SQL Server | 2017 or higher |
| MySQL | 8.0.28 or higher |
| Oracle Database | 19c or higher |

- The database must be case-insensitive. Case-sensitive databases are **not** supported.
- A Microsoft SQL Server instance must allow SQL Server Authentication (Mixed Mode).
- When the database runs on the same Windows Server as infoRouter, the server needs more memory than the
  figures above.
- Keep the database server up to date with its current service packs.
- Do not use the "Express" editions: they are not built to scale in busy environments.
- An installation on MySQL 5.x, or on a MySQL 8.0 version below 8.0.28, must upgrade the database server to
  MySQL 8.0.28 or higher before it upgrades to infoRouter Version 9.

### Windows software components

| Component | Notes |
|---|---|
| Internet Information Services (IIS) 10 | The "Web Server (IIS)" role of Windows Server. |
| ASP.NET Core Hosting Bundle | Current version, free of charge from [Microsoft](https://dotnet.microsoft.com/download/dotnet) (ASP.NET Core Runtime, Windows, "Hosting Bundle"). infoRouter runs as an IIS web site, and IIS needs this bundle to host it. |

The .NET runtime is included in the infoRouter installation. The .NET Framework is not required on the
server.

#### IIS features

Version 9 needs two IIS features on top of the default "Web Server (IIS)" role:

| IIS feature | Where it is in Add Roles and Features | Why infoRouter needs it |
|---|---|---|
| Request Filtering | Web Server (IIS) / Web Server / Security / Request Filtering | Carries the request size limit, which is the limit on the size of an upload. The setup raises it to 1 GB. |
| Application Initialization | Web Server (IIS) / Web Server / Application Development / Application Initialization | Starts infoRouter when the server starts, without waiting for the first request. The maintenance jobs run inside the web application since Version 9; without this feature a restarted server runs no maintenance until somebody opens a page. |

The setup program and Live Update check both features. When one is missing they offer to add it; you do
not have to add it by hand first.

The following IIS features were required by Version 8 and are **no longer required** by Version 9:

- Common HTTP Features / Default Document
- Common HTTP Features / HTTP Errors
- Common HTTP Features / Static Content
- Application Development / ISAPI Extensions
- Application Development / ISAPI Filters
- Windows PowerShell

In Version 9 the ASP.NET Core module takes every request, and infoRouter serves its own files, default
documents and error pages. You may leave these features installed; infoRouter does not use them.

#### Email

An SMTP server is required for email notifications. It may be on the infoRouter server or on another
server.

All the software named above either comes with Windows Server or can be downloaded free of charge.

### Content search

Content search is optional. infoRouter runs without it, but searching for words inside documents is then
not available. The choices are:

| Option | Where it runs | Notes |
|---|---|---|
| Windows Search | On the infoRouter server | As in Version 8. |
| infoRouter Search Service (dtSearch) | On the infoRouter server or on another Windows server | For distributed and larger installations that Windows Search cannot support. A separate Windows Service with its own installer. It must have access to the document warehouse. Licensed separately. |

## Requirements for the client

### WebDAV

- For WebDAV to work correctly, infoRouter must be installed at the root (Default Web Site) or as a web site
  of its own, not as a virtual directory.
- Some WebDAV clients require port 80. Do not put the infoRouter web site on another port when WebDAV is
  used.
- Windows clients need patches from Microsoft; which ones depends on the Windows version and architecture
  of the workstation. See the
  [WebDAV Requirements](https://support.inforouter.com/Downloads/v80/WebDAV-Requirements.pdf) document.
- Mac and Linux workstations need no patches.

### Client hardware

An internet-ready PC, Mac, laptop or tablet.

### Supported browsers

- Edge
- Firefox (latest)
- Chrome (latest)
- Safari (latest)

The browser must accept cookies and must have JavaScript enabled. Beta versions of browsers are not
supported and may produce unpredictable results. Older browsers, including Internet Explorer, are not
supported.

### Add-on modules

The optional add-on modules run on Windows workstations only: infoRouter Scan Station, infoRouter Hot
Folders, infoRouter Email Scanner, the infoRouter Import/Export tool, the infoRouter MS Office Add-in and
others. A workstation that runs one of them must have the .NET Framework 4.8 installed.

Mac and Linux workstations are fully supported for access with a browser.

### Service packs

Keep all client machines on your network up to date with the appropriate service packs and updates.

## Licensing

infoRouter Version 9 requires a Version 9 license.

To upgrade an existing installation, the license must entitle it to upgrades: it cannot be a trial key, and
the maintenance subscription must not be expired.

## Upgrading from an earlier version

| The installation is | How it is upgraded |
|---|---|
| Version 8.x or 9.x | With Live Update. |
| Version 7.x (7.2.215 and higher) | With the Version 9 setup program. |

Before the upgrade:

- An installation on MySQL 5.x, or on a MySQL 8.0 version below 8.0.28, must upgrade the database server to
  MySQL 8.0.28 or higher.
- An installation on Windows Server 2012 R2 or older must move to Windows Server 2019 or higher.

## Support

Email: [support@inforouter.com](mailto:support@inforouter.com)
