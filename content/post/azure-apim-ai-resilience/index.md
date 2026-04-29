---
slug: "azure-apim-ai-resilience"
title: "Building Resilient Azure AI Architecture with API Management Gateway"
date: 2026-04-03
weight: 1
description: "Build an enterprise-grade, highly resilient AI architecture with Azure APIM for cross-subscription quota aggregation, load balancing, automatic failover, and unified governance."
image: images/cover.png
categories:
  - Azure
tags:
  - Azure
  - API Management
  - AI
  - High Availability
  - Load Balancing
  - Managed Identity
  - Microsoft Foundry
  - Enterprise Architecture
series:
  - "Azure APIM AI Resilience"
---

As enterprise demand for AI capabilities grows, organizations are deeply integrating Microsoft Foundry model services into core business systems. As AI moves from experimentation to production, **high availability, elastic scaling, unified governance, and security controls** become unavoidable themes.

In production, a single subscription instance fails to meet requirements for **continuity, stability, and throughput**. A mature architecture consolidates resources across subscriptions, **aggregating AI quotas** to maximize throughput, with traffic distribution, automatic failover, and unified access control.

Azure API Management (APIM), as Azure's native API gateway, is naturally suited for this role. By deploying APIM as the unified entry point, combined with the following capabilities, we can build an **enterprise-grade, highly resilient AI architecture**:

- 🔀 **Backend Load Balancing Pool** — Load balancing and failover across subscriptions and Foundry instances, aggregating distributed quotas
- 🔐 **Managed Identity** — Zero-key secure authentication between APIM and backend AI services
- 🛡️ **Unified API Governance** — Request routing, traffic control, log auditing, and policy management at the gateway layer

This article walks through a complete hands-on example: from resource deployment and identity configuration to load balancing policies, building a production-ready resilient gateway architecture targeting multiple Microsoft Foundry resources.

## Architecture Overview

![1-Architecture](images/1-Architecture-en.png)

This architecture uses a **centralized API gateway + multi-subscription backend pattern**, with APIM as the unified entry point, distributing requests round-robin to Foundry instances across multiple subscriptions and regions.

Core design principles:

- **Unified Entry Point** — Clients only need the APIM endpoint; the pool uses Round-Robin by default
- **Simplified Security Authentication** — Zero-key communication via Managed Identity; clients only need a single API Key
- **Cross-Subscription Quota Aggregation** — Aggregate quotas across subscriptions into a unified capacity pool
- **Cross-Region Disaster Recovery** — APIM automatically routes to healthy instances when a region becomes unavailable

APIM's Policy engine also provides flexible traffic control:

- **Pinned Routing** — via `X-AI-Foundry-Target` header
- **Auto Failover** — Auto-retry with exponential backoff on 4xx/5xx
- **Request Tracing** — `X-AI-Foundry-Backend` response header for tracing

Architecture setup steps:

| Section | Action | Goal | Platform |
|------|------|------|------|
| 1 | Create APIM instance | Set up the unified gateway entry point and enable Managed Identity | Azure Portal |
| 2 | Create Foundry resources | Build the backend resource pool across multiple subscriptions and regions | Azure Portal |
| 3 | Deploy AI models | Enable AI service capability on backend resources (using Sora2 as an example) | Foundry Portal |
| 4 | Configure RBAC | Grant APIM Managed Identity permission to access backends | Azure Portal |
| 5 | Configure Backend + LB Pool | Register backends and create the load balancing pool | Azure Portal (APIM) |
| 6 | Create API + Policy | Define the API entry point and configure routing and failover | Azure Portal (APIM) |
| 7 | Test and validate | Verify load balancing and pinned backend routing | curl / Postman |

---

## Create APIM Instance

Create an API Management instance in Azure Portal, selecting v2 Tier, and enable **System Assigned Managed Identity** during creation.

**Portal Steps:** Search `API Management Service` → + Create → Fill in configuration → Enable on the Managed identity tab → Review + install

![](images/2-3-basics-config.png)

![](images/2-4-managed-identity.png)

**CLI Alternative:**

```bash
az rest --method PUT \
  --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.ApiManagement/service/<apim-name>?api-version=2024-05-01" \
  --body '{
    "location": "<region>",
    "sku": { "name": "<BasicV2|StandardV2|PremiumV2>", "capacity": 1 },
    "identity": { "type": "SystemAssigned" },
    "properties": {
      "publisherName": "<organization-name>",
      "publisherEmail": "<admin-email>"
    }
  }'
```

**After Creation:**

- Status: **Online**
- Record **Gateway URL** (for example: `https://<apim-name>.azure-api.net`)
- Record the Managed Identity **Object (principal) ID** for RBAC

![](images/2-6-apim-dashboard.png)

---

## Create Foundry Resources

Create Foundry resources across multiple subscriptions and regions, each with a corresponding project.

**Portal Steps:** Search `Microsoft Foundry` → Create a resource → Fill in Subscription / Region / Name / Project name → Create

![](images/3-3-create-foundry-resource.png)

**CLI Alternative:**

```bash
az cognitiveservices account create \
  --subscription <subscription-id> \
  --resource-group <resource-group> \
  --name <foundry-resource-name> \
  --location <region-code> \
  --kind AIServices --sku S0 \
  --custom-domain <foundry-resource-name> \
  --allow-project-management && \
az cognitiveservices account project create \
  --subscription <subscription-id> \
  --name <foundry-resource-name> \
  --resource-group <resource-group> \
  --project-name <project-name> \
  --location <region-code>
```

**Example Resource Distribution:**

| Subscription | Region | Resource Name |
|------|------|---------|
| Subscription A | East US 2 | foundry-eastus2-01 |
| Subscription A | Sweden Central | foundry-swedencentral-01 |
| Subscription B | East US 2 | foundry-eastus2-02 |
| Subscription B | Sweden Central | foundry-swedencentral-02 |

---

## Deploy Models

Deploy AI models in each Foundry resource via the Foundry Portal.

**Portal Steps:** In [Foundry Portal](https://ai.azure.com/nextgen/), select the target project → Build → Models → Deploy a base model → Search for a model (for example `sora-2`) → Deploy → Default settings

![](images/4-2-search-sora2.png)

![](images/4-5-playground.png)

**CLI Alternative:**

```bash
az cognitiveservices account deployment create \
  --subscription <subscription-id> \
  --resource-group <resource-group> \
  --name <foundry-resource-name> \
  --deployment-name <deployment-name> \
  --model-name <model-name> \
  --model-version <model-version> \
  --model-format <model-format> \
  --sku-name <sku-name> \
  --sku-capacity <capacity>
```

> Model names, versions, and SKUs vary by region. See: [Models and Region Availability](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)

---

## Configure RBAC

Grant the `Cognitive Services OpenAI User` role to APIM's Managed Identity on **each Foundry resource**.

**Portal Steps:** Go to the Foundry resource → Access control (IAM) → + Add → Add role assignment → Search `Cognitive Services OpenAI User` → In Members choose Managed identity → Select the API Management service → Review + assign

![](images/5-3-select-role.png)

![](images/5-4-select-managed-identity.png)

**CLI Alternative:**

```bash
# Get APIM Managed Identity Principal ID
az apim show \
  --subscription <subscription-id> \
  --name <apim-name> \
  --resource-group <resource-group> \
  --query "identity.principalId" -o tsv

# Assign role for each Foundry resource
az role assignment create \
  --assignee <principal-id> \
  --role "Cognitive Services OpenAI User" \
  --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>
```

> `Cognitive Services OpenAI User` is the minimum permission role—allows inference calls but not resource configuration changes.

---

## Configure Backend + LB Pool

### Create Backend

Create a Backend for each Foundry resource with Managed Identity authentication.

**Get OpenAI Endpoint:** On the project Home page in [Foundry Portal](https://ai.azure.com/nextgen/), find **Azure OpenAI endpoint**, or use the CLI:

```bash
az cognitiveservices account show \
  --subscription <subscription-id> \
  --resource-group <resource-group> \
  --name <foundry-resource-name> \
  --query "properties.endpoints.\"OpenAI Language Model Instance API\"" -o tsv
```

**Portal Steps:** APIM → Backends → + Create new backend → Fill in Name / Runtime URL → Managed Identity tab → Client identity = System assigned → Resource ID = `https://cognitiveservices.azure.com` → Create

![](images/6-3-create-backend.png)

**Key Configuration:**

| Configuration | Example Value | Description |
|--------|--------|------|
| Name | `<foundry-resource-name>` | Recommended to match the Foundry resource name |
| Runtime URL | `https://<foundry-resource-name>.openai.azure.com/openai/v1` | Foundry OpenAI endpoint (+ `openai/v1`) |
| Client identity | System assigned identity | Use APIM system-assigned managed identity |
| Resource ID | `https://cognitiveservices.azure.com` | Token audience, **fixed value** |

**CLI Alternative:**

```bash
az rest --method PUT \
  --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.ApiManagement/service/<apim-name>/backends/<backend-name>?api-version=2024-05-01" \
  --body '{
    "properties": {
      "url": "https://<foundry-resource-name>.openai.azure.com/openai/v1",
      "protocol": "http",
      "credentials": {
        "managedIdentity": {
          "clientId": null,
          "resource": "https://cognitiveservices.azure.com"
        }
      }
    }
  }'
```

### Create LB Pool

**Portal Steps:** APIM → Backends → Load balancer tab → + Create new pool → Fill in Pool Name → Select all Backends → Send requests evenly (Round-robin) → Create

![](images/6-6-create-pool.png)

> Portal provides two options: **Send requests evenly** (Round-robin) or **Customize weight and priority**.

---

## Create API + Policy

### Create API

**Portal Steps:** APIM → APIs → + Add API → HTTP → Fill in Display name / API URL suffix (`openai/v1`) → Leave Web service URL empty → Create

Then add Operations: create `/*` wildcard path for POST, GET, and DELETE.

> This example uses wildcard `/*` to proxy all requests. For finer control, create operations for specific paths like `/videos/*` for Sora2.

### Configure Policy

Select All operations → click `</>` in Inbound processing → paste the policy below, update the pool name → Save

```xml
<policies>
    <inbound>
        <base />
        <!-- Read request header so callers can pin a backend -->
        <set-variable name="target" value="@(context.Request.Headers.GetValueOrDefault("X-AI-Foundry-Target", ""))" />
        <!-- Backend load balancing pool name -->
        <set-variable name="pool_name" value="<your-ai-hub-pool-name>" />
        <choose>
            <when condition="@(context.Variables.GetValueOrDefault<string>("target") != "")">
                <set-backend-service backend-id="@(context.Variables.GetValueOrDefault<string>("target"))" />
            </when>
            <otherwise>
                <set-backend-service backend-id="@((string)context.Variables["pool_name"])" />
            </otherwise>
        </choose>
    </inbound>
    <outbound>
        <base />
        <set-header name="X-AI-Foundry-Backend" exists-action="override">
            <value>@(context.Request.Url.Host.Split('.')[0])</value>
        </set-header>
    </outbound>
    <on-error>
        <base />
    </on-error>
    <backend>
        <choose>
            <when condition="@(context.Variables.GetValueOrDefault<string>("target") != "")">
                <forward-request buffer-request-body="true" />
            </when>
            <otherwise>
                <retry condition="@(context.Response == null || context.Response.StatusCode >= 400)" count="3" interval="1" delta="1" max-interval="5" first-fast-retry="true">
                    <set-backend-service backend-id="@((string)context.Variables["pool_name"] )" />
                    <forward-request buffer-request-body="true" />
                </retry>
            </otherwise>
        </choose>
    </backend>
</policies>
```

![](images/7-5-policy-editor-en.png)

**Policy Logic:**

| Area | Function |
|------|------|
| **inbound** | Read `X-AI-Foundry-Target`; if present, route to the specified backend, otherwise use the LB Pool round-robin |
| **outbound** | Return the actual backend name in the `X-AI-Foundry-Backend` response header |
| **backend** | Forward directly for pinned routing; in pool mode, auto-retry and switch backend on failure (up to 3 attempts with exponential backoff) |

---

## Test and Validate

**Prerequisites:**

Gather the following before testing:

- Get Gateway URL: APIM → Overview → Gateway URL
- Get API Key: APIM → Subscriptions → Built-in all-access → Show keys → Primary key

![](images/8-2-subscription-key.png)

### Test 1: Load Balancing

Send consecutive requests without `X-AI-Foundry-Target`, and observe `X-AI-Foundry-Backend` rotating across backends:

```bash
curl -D - -o /dev/null --location \
  'https://<apim-gateway-url>/openai/v1/videos' \
  --header 'Ocp-Apim-Subscription-Key: <your-subscription-key>'
```

Expected: `X-AI-Foundry-Backend` changes with each request, confirming Round-robin is working.

![](images/8-3-round-robin-test.png)

### Test 2: Pinned Backend Routing

Use `X-AI-Foundry-Target` header to pin to a specific backend:

```bash
curl -s -D - -o /dev/null --location \
  'https://<apim-gateway-url>/openai/v1/responses' \
  --header 'Content-Type: application/json' \
  --header 'Ocp-Apim-Subscription-Key: <your-subscription-key>' \
  --header 'X-AI-Foundry-Target: <backend-name>' \
  --data '{"model": "<model-name>", "input": "Hello"}' \
  | grep -i X-AI-Foundry-Backend
```

Expected: `X-AI-Foundry-Backend` consistently returns the specified backend name.

![](images/8-4-pinned-backend-test.png)

---

## FAQ

**Q: Why not use APIM Backend's Circuit Breaker?**

This architecture targets load balancing and quota aggregation. Circuit Breaker would "break" on backend failure, but a 429 on one model shouldn't block other models on the same backend. Simple failover via `retry` + `set-backend-service` is more appropriate.

**Q: Is this architecture only for Sora2?**

No. It applies to any Foundry / Azure OpenAI model service (Responses API, Chat Completions, Embeddings, Image Generation, etc.)—just point the Backend URL to the corresponding endpoint.

---

## Reference Documentation

- Microsoft Foundry Overview: https://learn.microsoft.com/azure/foundry/what-is-foundry
- Foundry RBAC: https://learn.microsoft.com/azure/foundry-classic/openai/how-to/role-based-access-control
- APIM v2 Tier: https://learn.microsoft.com/azure/api-management/v2-service-tiers-overview
- Backends & LB Pool: https://learn.microsoft.com/azure/api-management/backends
- Managed Identity: https://learn.microsoft.com/azure/api-management/api-management-howto-use-managed-service-identity
- Retry Policy: https://learn.microsoft.com/azure/api-management/retry-policy
- Video Generation / Sora2: https://learn.microsoft.com/azure/foundry/openai/concepts/video-generation
- Models & Regions: https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure
- Error Codes: https://learn.microsoft.com/azure/foundry/openai/supported-languages#error-handling

---

