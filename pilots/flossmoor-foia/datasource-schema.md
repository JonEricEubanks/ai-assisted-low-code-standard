# FOIA App Connected Data Source Schema

Extracted from the saved FOIA App package (Community Essentials). Use these exact data source names and logical column names in Power Fx.

Site: `https://communityessentials.sharepoint.com/sites/Administration`

## FOIA Pilot Assignments
- List GUID: `ff97ee20-c7a9-4c4c-ac32-7c329c5fab57`
- Writable: True

| Logical name | Display name | Type | Notes |
|---|---|---|---|
| ID | ID | integer | int64 |
| Title | Title | string |  |
| AssignmentStatus | Assignment Status | object | Lookup/Choice record (.Value, .Id) |
| Request | Request | object | Lookup/Choice record (.Value, .Id) |
| Department | Department | object | Lookup/Choice record (.Value, .Id) |
| AssignedTo | Assigned To | object | Person record (.DisplayName, .Email, .Claims) |
| AssignmentDueDate | Assignment Due Date | string | date |
| RedactionRequired | Redaction Required | object | Lookup/Choice record (.Value, .Id) |
| DepartmentCompleteDate | Department Complete Date | string | date |
| ResponseNotes | Response Notes | string |  |
| Active | Active | boolean |  |
| Modified | Modified | string | date-time |
| Created | Created | string | date-time |
| Author | Created By | object | Person record (.DisplayName, .Email, .Claims) |
| Editor | Modified By | object | Person record (.DisplayName, .Email, .Claims) |

## FOIA Pilot Departments
- List GUID: `afbfa1b0-47ef-41dc-ac89-32ba142ddeef`
- Writable: True

| Logical name | Display name | Type | Notes |
|---|---|---|---|
| ID | ID | integer | int64 |
| Title | Title | string |  |
| DepartmentCode | Department Code | string |  |
| Active | Active | boolean |  |
| SortOrder | Sort Order | number | double |
| IsPolice | Is Police | boolean |  |
| Modified | Modified | string | date-time |
| Created | Created | string | date-time |
| Author | Created By | object | Person record (.DisplayName, .Email, .Claims) |
| Editor | Modified By | object | Person record (.DisplayName, .Email, .Claims) |

## FOIA Pilot Records
- List GUID: `2b47c60b-057c-498d-ab75-0097a8abeb74`
- Writable: True

| Logical name | Display name | Type | Notes |
|---|---|---|---|
| ID | ID | integer | int64 |
| Title | Title | string |  |
| Modified | Modified | string | date-time |
| Editor | Modified By | object | Person record (.DisplayName, .Email, .Claims) |
| DocumentType | Document Type | object | Lookup/Choice record (.Value, .Id) |
| OData__ExtendedDescription | Description | string |  |
| Request | Request | object | Lookup/Choice record (.Value, .Id) |
| Department | Department | object | Lookup/Choice record (.Value, .Id) |
| RedactionStatus | Redaction Status | object | Lookup/Choice record (.Value, .Id) |
| IsFinalResponse | Is Final Response | boolean |  |
| Sensitivity | Sensitivity | object | Lookup/Choice record (.Value, .Id) |
| Notes | Notes | string |  |
| Created | Created | string | date-time |
| Author | Created By | object | Person record (.DisplayName, .Email, .Claims) |
| CheckoutUser | Checked Out To | object | Person record (.DisplayName, .Email, .Claims) |
| OData__DisplayName | Sensitivity | string |  |

## FOIA Pilot Requests
- List GUID: `f99e0269-3061-4892-87ac-3dabba92d416`
- Writable: True

| Logical name | Display name | Type | Notes |
|---|---|---|---|
| ID | ID | integer | int64 |
| Title | Title | string |  |
| ReceivedDate | Received Date | string | date |
| IntakeMethod | Intake Method | object | Lookup/Choice record (.Value, .Id) |
| RequestRoute | Request Route | object | Lookup/Choice record (.Value, .Id) |
| RequestDescription | Request Description | string |  |
| OverallStatus | Overall Status | object | Lookup/Choice record (.Value, .Id) |
| CommercialPurpose | Commercial Purpose | object | Lookup/Choice record (.Value, .Id) |
| RequesterFirstName | Requester First Name | string |  |
| RequesterLastName | Requester Last Name | string |  |
| RequesterStreetAddress | Requester Street Address | string |  |
| RequesterCity | Requester City | string |  |
| RequesterState | Requester State | string |  |
| RequesterZip | Requester ZIP | string |  |
| RequesterEmail | Requester Email | string |  |
| RequesterPhone | Requester Phone | string |  |
| DeliveryFormat | Delivery Format | object | Lookup/Choice record (.Value, .Id) |
| CertifiedCopies | Certified Copies | object | Lookup/Choice record (.Value, .Id) |
| FeeWaiverRequested | Fee Waiver Requested | object | Lookup/Choice record (.Value, .Id) |
| DueDate | Due Date | string | date |
| DueDateConfirmed | Due Date Confirmed | boolean |  |
| PrimaryDepartment | Primary Department | object | Lookup/Choice record (.Value, .Id) |
| AssignedOfficer | Assigned Officer | object | Person record (.DisplayName, .Email, .Claims) |
| ExtensionType | Extension Type | object | Lookup/Choice record (.Value, .Id) |
| ExtensionDays | Extension Days | number | double |
| ExtensionStatus | Extension Status | object | Lookup/Choice record (.Value, .Id) |
| FinalResponseDate | Final Response Date | string | date |
| CloseoutNotes | Closeout Notes | string |  |
| CurrentStageNotes | Current Stage Notes | string |  |
| Modified | Modified | string | date-time |
| Created | Created | string | date-time |
| Author | Created By | object | Person record (.DisplayName, .Email, .Claims) |
| Editor | Modified By | object | Person record (.DisplayName, .Email, .Claims) |
