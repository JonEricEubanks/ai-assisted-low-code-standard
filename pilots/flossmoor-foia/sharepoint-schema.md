# Flossmoor FOIA Pilot SharePoint Schema

## Environment boundary

- Site: `https://communityessentials.sharepoint.com/sites/Administration`
- Purpose: Community Essentials development pilot
- Data: Synthetic records only
- Production publication: Not authorized
- Automated retention or deletion: Not implemented
- Legal deadline calculation: Human-confirmed dates only

## Resources

### FOIA Pilot Departments

Reference list for routing and assignment.

| Internal name | Display name | Type | Required |
|---|---|---|---|
| Title | Title | Text | Yes |
| DepartmentCode | Department Code | Text | Yes |
| Active | Active | Yes/No | No |
| SortOrder | Sort Order | Number | No |
| IsPolice | Is Police | Yes/No | No |

Seeded departments:

- Administration
- Police Department
- Finance
- Planning and Zoning
- Fire Department
- Building Department
- Public Works Department

### FOIA Pilot Requests

Master request list. The built-in `Title` column stores the request number.

| Internal name | Display name | Type |
|---|---|---|
| ReceivedDate | Received Date | Date/time |
| IntakeMethod | Intake Method | Choice |
| RequestRoute | Request Route | Choice |
| CommercialPurpose | Commercial Purpose | Choice |
| RequesterFirstName | Requester First Name | Text |
| RequesterLastName | Requester Last Name | Text |
| RequesterStreetAddress | Requester Street Address | Text |
| RequesterCity | Requester City | Text |
| RequesterState | Requester State | Text |
| RequesterZip | Requester ZIP | Text |
| RequesterEmail | Requester Email | Text |
| RequesterPhone | Requester Phone | Text |
| RequestDescription | Request Description | Multiple lines |
| DeliveryFormat | Delivery Format | Choice |
| CertifiedCopies | Certified Copies | Choice |
| FeeWaiverRequested | Fee Waiver Requested | Choice |
| OverallStatus | Overall Status | Choice |
| DueDate | Due Date | Date/time |
| DueDateConfirmed | Due Date Confirmed | Yes/No |
| PrimaryDepartment | Primary Department | Lookup |
| AssignedOfficer | Assigned Officer | Person |
| ExtensionType | Extension Type | Choice |
| ExtensionDays | Extension Days | Number |
| ExtensionStatus | Extension Status | Choice |
| FinalResponseDate | Final Response Date | Date/time |
| CloseoutNotes | Closeout Notes | Multiple lines |
| SourceSubmissionId | Source Submission ID | Text |
| CurrentStageNotes | Current Stage Notes | Multiple lines |

### FOIA Pilot Assignments

Department work list. One request may have multiple assignments.

| Internal name | Display name | Type |
|---|---|---|
| Title | Title | Text |
| Request | Request | Lookup |
| Department | Department | Lookup |
| AssignedTo | Assigned To | Person |
| AssignmentStatus | Assignment Status | Choice |
| AssignmentDueDate | Assignment Due Date | Date/time |
| RedactionRequired | Redaction Required | Choice |
| DepartmentCompleteDate | Department Complete Date | Date/time |
| ResponseNotes | Response Notes | Multiple lines |
| Active | Active | Yes/No |

### FOIA Pilot Records

Document library for synthetic request, responsive-record, redaction, correspondence,
extension, and final-response artifacts.

| Internal name | Display name | Type |
|---|---|---|
| Request | Request | Lookup |
| Department | Department | Lookup |
| DocumentType | Document Type | Choice |
| RedactionStatus | Redaction Status | Choice |
| IsFinalResponse | Is Final Response | Yes/No |
| Sensitivity | Sensitivity | Choice |
| Notes | Notes | Multiple lines |

## Deliberate exclusions

- No automatic FOIA deadline calculation because commercial requests, holidays,
  statutory extensions, agreed extensions, and human classification create exceptions.
- No retention label, record declaration, or deletion flow until the applicable
  retention schedule and records authority are confirmed.
- No public-form write integration in the data provisioning step.
- No email, reminder, extension, or escalation flow in the data provisioning step.
- No item-level permission breaks until the role and access matrix is approved.

