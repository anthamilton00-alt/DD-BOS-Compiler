"""
DD-BOS System Registry

Central location for every controlled vocabulary used by the compiler.

Nothing in the compiler should hard-code owners, statuses,
document prefixes, metadata labels, or reserved values.
"""

VALID_DOCUMENT_PREFIXES = {
    "ASM",
    "DD",
    "DOC",
    "FP",
    "FRM",
    "LAB",
    "PROD",
    "ROOM",
    "SM",
}


VALID_STATUSES = {
    "ACTIVE",
    "APPROVED",
    "ARCHIVED",
    "DRAFT",
    "FROZEN",
    "RETIRED",
    "SUPERSEDED",
}


VALID_OWNERS = {
    "Assigned Internal Auditor",
    "Builder Relations Manager",
    "Digitally Defined",
    "Executive Leadership",
    "Field Operations Manager",
    "Finance Manager",
    "HR Manager",
    "Lead Technician",
    "Marketing Manager",
    "Office Administrator",
    "Operations Manager",
    "Project Manager",
    "Purchasing Manager",
    "Quality Manager",
    "Safety Manager",
    "Sales Manager",
    "Service Manager",
    "Technician",
    "Warehouse Manager",
}


INVALID_OWNER_VALUES = {
    "",
    "-",
    "--",
    "---",
    "N/A",
    "NA",
    "NONE",
    "TBD",
    "IF REQUIRED",
    "(IF REQUIRED)",
    "WHEN REQUIRED",
    "(WHEN REQUIRED)",
    "AS REQUIRED",
    "(AS REQUIRED)",
    "(AS REQUIRED PER APPROVAL MATRIX)",
    "(PROJECTS MEETING APPROVAL THRESHOLD)",
}


DOCUMENT_ID_LABELS = {
    "DOCUMENT ID",
    "ASSEMBLY ID",
    "ROOM ID",
    "FLOOR PLAN ID",
    "FORM ID",
}


TITLE_LABELS = {
    "TITLE",
    "DOCUMENT TITLE",
    "DOCUMENT NAME",
    "ASSEMBLY NAME",
    "ROOM NAME",
    "FLOOR PLAN NAME",
    "FORM NAME",
}


OWNER_LABELS = {
    "OWNER",
    "DOCUMENT OWNER",
    "PROCESS OWNER",
    "SYSTEM OWNER",
    "RESPONSIBLE OWNER",
    "RESPONSIBLE ROLE",
    "DEPARTMENT OWNER",
}


VERSION_LABELS = {
    "VERSION",
    "DOCUMENT VERSION",
}


STATUS_LABELS = {
    "STATUS",
    "DOCUMENT STATUS",
}


DATE_LABELS = {
    "EFFECTIVE DATE",
    "DATE EFFECTIVE",
    "REVISION DATE",
    "LAST REVISION DATE",
    "LAST REVISED",
}