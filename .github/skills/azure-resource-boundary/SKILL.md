---
name: azure-resource-boundary
description: "Use when: doing any Azure work, using Azure CLI, Azure MCP, SDKs, REST, azd, Bicep, or Terraform; creating a resource group or subscription boundary; or turning on Azure guardrails. Covers Foundry, OCR, Document Intelligence, storage, and other workloads in Microsoft Azure Sponsorship. Require an explicitly approved resource group per workload and verify the executing identity before writes."
---

# Azure Resource Boundary

Follow the governed [Azure resource-boundary procedure](../../../skills/azure-resource-boundary/SKILL.md) before Azure operations.

Require an explicitly approved resource group for each workload in Microsoft Azure Sponsorship. Never silently reuse the Foundry QA group for OCR or other workloads.

A skill is guidance, not a permissions sandbox. Verify the executing CLI, MCP, SDK, or workflow identity; an Owner login remains broadly privileged.
