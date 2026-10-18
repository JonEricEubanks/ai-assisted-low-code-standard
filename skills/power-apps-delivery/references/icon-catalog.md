# Modern Icon catalog (Fluent) — authoritative names for `Icon`, `ModernIcon`, `ModernButton.Icon`, `ModernBadge.Icon`, toast `Icon`

Captured 2026-10-17 from the Power Apps Studio icon picker DOM (181 names). The authoring service exposes `Icon` as free `Text` and does **not** validate it — a misspelled name compiles clean and renders blank. **Only use names from this list.** `IconStyle` is `IconStyle.Outline` (default) or `IconStyle.Filled`.

## Full list (alphabetical)

Add, Airplane, Alert, AppsList, AppsListDetail, ArrowCircleLeft, ArrowCircleRight, ArrowClockwise, ArrowDown, ArrowDownload, ArrowExit, ArrowExport, ArrowImport, ArrowLeft, ArrowRedo, ArrowReply, ArrowReset, ArrowRight, ArrowSort, ArrowSwap, ArrowSync, ArrowTrending, ArrowUndo, ArrowUp, Attach, BookClock, BookContacts, Bookmark, BoxMultiple, BriefcaseMedical, Bug, Building, BuildingFactory, BuildingRetail, Calculator, Calendar, CalendarAdd, CalendarMonth, Call, CallEnd, Camera, CameraDome, Cart, CellularData, Chat, Checkmark, CheckmarkCircle, ChevronDown, ChevronLeft, ChevronRight, ChevronUp, Circle, CircleHalfFill, ClipboardPaste, Clock, ClockAlarm, Compose, Copy, CropInterim, Cube, CurrencyDollarEuro, Cut, Database, Delete, Desktop, Diamond, Dismiss, DismissCircle, DividerTall, Document, DocumentAdd, DocumentArrowUp, DocumentBulletList, DocumentCheckmark, DocumentPdf, DrawShape, Edit, Emoji, EmojiSad, EmojiSmileSlight, Eraser, ErrorCircle, Eye, Eyedropper, EyeOff, Filter, Flag, Flash, Folder, Food, FullScreenMaximize, FullScreenMinimize, Globe, GlobeArrowUp, GlobeClock, GlobeError, GlobeProhibited, GlobeSync, GlobeWarning, GridDots, Heart, HeartPulse, History, Home, Image, Info, Key, Laptop, Layer, Library, Lightbulb, LineHorizontal, Link, Location, LockClosed, LockOpen, Mail, Mic, Money, MoreHorizontal, Navigation, NavigationLocationTarget, NetworkCheck, News, Note, Notebook, NumberSymbol, Open, PanelLeft, PanelRight, People, PeopleAdd, Person, PersonAdd, PersonSupport, Phone, PhoneDesktop, Pin, Print, Prohibited, PulseSquare, Question, QuestionCircle, Radar, Ribbon, Save, SaveCopy, Scan, Search, Send, ServiceBell, Settings, Share, ShareCloseTray, Sparkle, Star, Subtract, Tablet, Tag, TextBulletListDismiss, TextBulletListSquare, TextBulletListSquareClock, TextBulletListSquareSettings, TextBulletListSquareSparkle, TextCaseTitle, ThumbDislike, ThumbLike, ThumbLikeDislike, Toolbox, VehicleBus, VehicleCar, VehicleSubway, VehicleTruck, Video, Warning, WeatherPartlyCloudyDay, WeatherRainShowersDay, Wrench, XboxController, ZoomIn, ZoomOut

## Semantic mapping (use these first)

| Purpose | Icon | Style |
|---|---|---|
| Success / complete / closed | `CheckmarkCircle` | Filled for toast & badges, Outline in rails |
| Error / failed | `DismissCircle` or `ErrorCircle` | Filled |
| Warning / due soon / overdue | `Warning` | Filled |
| Info / neutral notice | `Info` | Outline |
| Primary create action | `Add` | — |
| Save / submit | `Save` | — |
| Refresh / reload | `ArrowClockwise` | — |
| Reset filters | `ArrowReset` | — |
| Back | `ArrowLeft` | — |
| Open detail / drill-in | `ChevronRight` | — |
| Expand / collapse rail | `GridDots` (expander), `PanelLeft` / `PanelRight` | — |
| Home | `Home` | Filled when active |
| New request / compose | `Compose` or `DocumentAdd` | — |
| Requests / records / documents | `Document`, `DocumentBulletList`, `DocumentCheckmark`, `DocumentPdf` | — |
| Open queue / in progress | `Clock` or `History` | — |
| Assignments / departments / people | `People`, `PeopleAdd`, `Person`, `PersonAdd`, `Building` | — |
| Search | `Search` | — |
| Filter | `Filter` | — |
| Settings | `Settings` | — |
| Notifications | `Alert` | — |
| Attachments | `Attach` | — |
| Calendar / dates / due | `Calendar`, `CalendarAdd`, `CalendarMonth`, `ClockAlarm` | — |
| Email / phone / chat | `Mail`, `Call`, `Phone`, `Chat` | — |
| Location | `Location`, `NavigationLocationTarget` | — |
| Dismiss / close | `Dismiss` | — |
| More actions | `MoreHorizontal` | — |
| Pin / flag / star | `Pin`, `Flag`, `Star` | — |
| Delete | `Delete` | — |
| Edit | `Edit` | — |
| Copy / print / share | `Copy`, `Print`, `Share` | — |
| Approve / reject | `ThumbLike`, `ThumbDislike` | — |
| Metric tile icons | `Document`, `Clock`, `Warning`, `CheckmarkCircle`, `People`, `Money` | Filled in the tinted chip |

## Names that do NOT exist (common guesses — never use)

`DocumentSearch`, `Clipboard` (use `ClipboardPaste`), `Briefcase` (use `BriefcaseMedical`), `Trash` (use `Delete`), `Close` (use `Dismiss`), `Check` (use `Checkmark`), `User`/`Users` (use `Person`/`People`), `Bell` (use `Alert`), `Refresh` (use `ArrowClockwise`), `Menu`/`Hamburger` (use `LineHorizontal` or `Navigation`), `Plus` (use `Add`), `Minus` (use `Subtract`), `Cancel`, `Exit` (use `ArrowExit`), `Upload` (use `ArrowImport`/`DocumentArrowUp`), `Download` (use `ArrowDownload`), `Globe2`, `Eye2`, `Weather`, `TextBulletList`, `LineHorizontal3`.

## Rules for builders

1. Before writing any `Icon:` value, confirm it is in the list above. The compiler will not catch a typo.
2. Pass icon names as plain text strings (`Icon: ="CheckmarkCircle"`); for `ModernButton` the property is also `Icon` (text) with `Layout`/`IconBefore` controlling placement.
3. Visual QA must include a check that every icon actually rendered (a blank 20-px square where an icon should be is a failed name).
4. Re-scrape this list when Microsoft adds icons: open the Icon dropdown in Studio and read the tile `title`/`aria-label` attributes.
