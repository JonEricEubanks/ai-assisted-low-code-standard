# Survey123 Public Intake Form — XLSForm Schema

Pilot: Flossmoor FOIA (synthetic data only)
Target: ArcGIS Survey123 Connect → hosted feature layer → Power Automate ArcGIS connector trigger
Governing schema: `../../sharepoint-schema.md`, `../../datasource-schema.md`

## Design rule

Every survey question `name` is **identical to the SharePoint internal column name** on
`FOIA Pilot Requests`. The flow maps `feature.attributes.<name>` → `item/<name>` 1:1 with
no translation table. Choice `name` values are the exact SharePoint choice values except
`Departments`, where XLSForm forbids spaces in choice names (see "Departments choice names").

Field names are case-sensitive in the webhook payload. Build the form with the exact casing
below; do not let Survey123 Connect auto-lowercase (it preserves case for new feature layers,
but verify with the first trigger sample — see `README.md` → "Trigger sample").

## `survey` sheet

| type | name | label | required | relevant | appearance | constraint | constraint_message | hint | bind::esri:fieldType | bind::esri:fieldLength |
|---|---|---|---|---|---|---|---|---|---|---|
| begin group | grpRequester | About you | | | field-list | | | | | |
| text | RequesterFirstName | First name | no | | | | | | esriFieldTypeString | 100 |
| text | RequesterLastName | Last name | no | | | | | | esriFieldTypeString | 100 |
| text | RequesterEmail | Email address | `${DeliveryFormat} = 'Electronic'` | | | `regex(., '^[^@\s]+@[^@\s]+\.[^@\s]+$')` | Enter a valid email address (name@example.com). | Required if you want records delivered electronically. We will send your confirmation here. | esriFieldTypeString | 255 |
| text | RequesterPhone | Phone number | no | | numbers | | | Optional. | esriFieldTypeString | 30 |
| text | RequesterStreetAddress | Street address | `${DeliveryFormat} = 'Paper'` | | | | | Required if you want paper copies mailed. | esriFieldTypeString | 255 |
| text | RequesterCity | City | `${DeliveryFormat} = 'Paper'` | | | | | | esriFieldTypeString | 100 |
| text | RequesterState | State | `${DeliveryFormat} = 'Paper'` | | | `string-length(.) = 2` | Use the two-letter state code (for example, IL). | | esriFieldTypeString | 2 |
| text | RequesterZip | ZIP code | `${DeliveryFormat} = 'Paper'` | | numbers | `regex(., '^[0-9]{5}(-[0-9]{4})?$')` | Enter a 5-digit ZIP or ZIP+4. | | esriFieldTypeString | 10 |
| end group | | | | | | | | | | |
| begin group | grpRequest | Your request | | | field-list | | | | | |
| text | RequestDescription | Describe the records you are requesting | yes | | multiline | `string-length(.) <= 4000` | Please keep the description under 4,000 characters. | Be as specific as you can: record type, date range, department, names or addresses involved. | esriFieldTypeString | 4000 |
| select_multiple departments | Departments | Which department(s) do you believe hold these records? | no | | | | | Select all that apply. Leave blank if unsure — the FOIA officer will route it. | esriFieldTypeString | 255 |
| select_one yesno | CommercialPurpose | Is this request for a commercial purpose? | yes | | horizontal | | | Illinois FOIA allows a longer response period for commercial requests. | esriFieldTypeString | 3 |
| end group | | | | | | | | | | |
| begin group | grpDelivery | Delivery and fees | | | field-list | | | | | |
| select_one deliveryformat | DeliveryFormat | How would you like to receive the records? | yes | | horizontal | | | | esriFieldTypeString | 20 |
| select_one yesno | CertifiedCopies | Do you need certified copies? | yes | | horizontal | | | Certified copies may carry a fee. | esriFieldTypeString | 3 |
| select_one yesno | FeeWaiverRequested | Are you requesting a fee waiver? | yes | | horizontal | | | | esriFieldTypeString | 3 |
| note | noteFeeWaiver | A fee waiver requires a statement of the public-interest purpose of your request. Attach it below. | | `${FeeWaiverRequested} = 'Yes'` | | | | | | |
| file | FeeWaiverStatement | Fee waiver statement (attach a document) | `${FeeWaiverRequested} = 'Yes'` | `${FeeWaiverRequested} = 'Yes'` | | | | Accepted: PDF, DOCX, JPG, PNG. One file. | | |
| end group | | | | | | | | | | |
| note | noteSubmit | After you submit, you will receive an email confirmation with your request number if you provided an email address. Staff will confirm the response date. | | | | | | | | |

Notes on the `survey` sheet:

- No `geopoint` question. The feature layer is a non-spatial table; nothing geographic is collected.
- `required` accepts expressions, so email is mandatory only for electronic delivery and
  postal fields only for paper delivery. This matches the flow's receipt rule (decision 8):
  the flow still validates `RequesterEmail` independently and never assumes the form enforced it.
- `FeeWaiverStatement` is the **only** attachment question. The flow reads
  `feature.attachments.FeeWaiverStatement[]`. Adding a second attachment question requires a
  flow change (see `flow-design.md` → Known limitations).
- `bind::esri:fieldLength` for `RequestDescription` is 4000 to match a SharePoint
  multiple-lines column; the default 255 would truncate requests.
- `RequesterState`/`RequesterZip`/`RequesterPhone` are strings, not integers, to preserve
  leading zeros and formatting and to match the SharePoint Text columns.

## `choices` sheet

| list_name | name | label |
|---|---|---|
| yesno | Yes | Yes |
| yesno | No | No |
| deliveryformat | Electronic | Electronic (email) |
| deliveryformat | Paper | Paper (mail or pickup) |
| departments | Administration | Administration |
| departments | Police_Department | Police Department |
| departments | Finance | Finance |
| departments | Planning_and_Zoning | Planning and Zoning |
| departments | Fire_Department | Fire Department |
| departments | Building_Department | Building Department |
| departments | Public_Works_Department | Public Works Department |

### Departments choice names

XLSForm choice names cannot contain spaces. The `departments` list therefore uses the
SharePoint `FOIA Pilot Departments.Title` with spaces replaced by underscores. The stored
attribute is a comma-separated string of choice names, e.g. `Police_Department,Finance`.
The flow reverses the substitution with `replace(trim(item()), '_', ' ')` before matching on
`Title`. Any new department must be added in **both** places (SharePoint list and this
choices sheet) with the same underscore convention; the flow needs no change.

## `settings` sheet

| form_title | form_id | instance_name | default_language | version | submission_url |
|---|---|---|---|---|---|
| Village FOIA Request (Pilot) | foia_pilot_requests | `concat(${RequesterLastName}, ", ", ${RequesterFirstName})` | English (en) | `yyyymmdd` of publish | *(blank — Survey123 creates the hosted layer)* |

Publish settings in Survey123 Connect / survey website:

- Sharing: **Public (Everyone)** for the form item; the feature layer remains org-only.
  The public submits through Survey123's proxy; the Power Automate connection uses an
  org account and can read attachments.
- Webhook: not configured in Survey123 directly. The Power Automate ArcGIS trigger
  registers its own webhook on the survey when the flow is saved.
- Allow "Submit to feature service" only; disable editing of existing responses so the
  trigger never receives `editData` events (the flow subscribes only to `addData`).
- Thank-you screen text: "Your request was received. If you provided an email, a
  confirmation with your request number is on its way." — no internal links.

## Field map (survey → SharePoint `FOIA Pilot Requests`)

| Survey attribute | SharePoint column | Transform in flow |
|---|---|---|
| RequesterFirstName | RequesterFirstName | trim |
| RequesterLastName | RequesterLastName | trim |
| RequesterEmail | RequesterEmail | trim; validated before receipt |
| RequesterPhone | RequesterPhone | none |
| RequesterStreetAddress | RequesterStreetAddress | none |
| RequesterCity | RequesterCity | none |
| RequesterState | RequesterState | none |
| RequesterZip | RequesterZip | none |
| RequestDescription | RequestDescription | none |
| Departments | PrimaryDepartment (lookup), RequestRoute (choice) | split → route table → `Get items` on Departments by Title |
| CommercialPurpose | CommercialPurpose | choice `{Value}` passthrough |
| DeliveryFormat | DeliveryFormat | choice `{Value}` passthrough |
| CertifiedCopies | CertifiedCopies | choice `{Value}` passthrough |
| FeeWaiverRequested | FeeWaiverRequested | choice `{Value}` passthrough |
| FeeWaiverStatement (attachment) | `FOIA Pilot Records` file + metadata | downloaded and filed, not a column |
| globalid / objectid | SourceSubmissionId | `coalesce(globalid, objectid)` |
| *(system)* | Title | `"<Last>, <First>"` or `"Anonymous request"` |
| *(system)* | ReceivedDate | Central-time date of trigger |
| *(system)* | DueDate / DueDateConfirmed | +5 business days / `false` |
| *(system)* | IntakeMethod | `"Online Form"` |
| *(system)* | OverallStatus | `"New"` |

Not collected by the survey (set by staff later in the app): AssignedOfficer, ExtensionType,
ExtensionDays, ExtensionStatus, FinalResponseDate, CloseoutNotes, CurrentStageNotes.
