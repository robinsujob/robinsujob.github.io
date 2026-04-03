# Building Resilient Azure AI Architecture with API Management Gateway

As enterprise demand for AI capabilities continues to grow, more and more organizations are deeply integrating model services from Microsoft Foundry into their core business systems. When AI services transition from the experimental phase to production environments, the focus of architecture design shifts accordingly—**high availability, elastic scaling, unified governance, and security controls** become critical themes that enterprise-grade AI architectures cannot avoid.

In a production-grade AI architecture, relying on a single service instance under a single subscription often cannot meet enterprise requirements for **service continuity, stability, and large-scale throughput capacity**—**limited quotas** cannot support large-scale concurrency, **single points of failure** impact service availability, and **single-region deployments** lack disaster recovery capabilities. A mature architecture should possess the ability to consolidate resources across subscriptions, **aggregating AI resource quotas across multiple subscriptions** to maximize available throughput, while combining traffic distribution, automatic failover, and unified identity authentication and access control to ensure AI services can respond reliably when facing various runtime challenges.

**Azure API Management (APIM)**, as Azure's native API gateway service, is naturally suited to take on this role. By deploying APIM as the unified entry point for AI services, combined with the following core capabilities, we can build an **enterprise-grade, highly resilient AI service architecture**:

- 🔀 **Backend Load Balancing Pool** — Load balancing and failover across multiple subscriptions and multiple Microsoft Foundry resource instances, aggregating quota capacity distributed across different subscriptions
- 🔐 **Managed Identity** — Zero-key secure authentication between APIM and backend AI services, eliminating credential management burden
- 🛡️ **Unified API Governance** — Implementing request routing, traffic control, log auditing, and policy management at the gateway layer, providing consistent governance capabilities for all AI calls

This article will walk through a complete hands-on example, detailing how to use APIM to build a resilient gateway architecture targeting multiple Microsoft Foundry resources—from resource deployment and identity configuration to load balancing policies, step by step building a solution ready for production use.

## Architecture Overview

![1-Architecture](assets/1-Architecture-en.png)

This architecture adopts a **centralized API gateway + multi-subscription backend pattern**, using Azure API Management as the unified gateway entry point, distributing requests through APIM's Backend Load Balancing Pool in a round-robin fashion to Microsoft Foundry resource instances distributed across multiple subscriptions and regions.

Core design principles include:

- **Unified Entry Point** — Clients only need to access the APIM endpoint, without needing to know the location or number of backend resources; the Backend Load Balancing Pool uses a Round-Robin strategy by default, evenly distributing requests across all healthy instances
- **Simplified Security Authentication** — APIM and backend Foundry resources communicate securely through Managed Identity with zero keys; externally, APIM provides a unified API Key, and clients only need to hold this Key to access all backend AI resources
- **Cross-Subscription Quota Aggregation** — Consolidating Foundry resource quotas distributed across different subscriptions into a unified capacity pool, breaking through single-subscription quota limits
- **Cross-Region Disaster Recovery** — Resources are distributed across different regions; when a region becomes unavailable, APIM automatically routes traffic to healthy instances

Beyond the above architecture-level design, APIM's Policy engine also provides flexible traffic control capabilities for this architecture:

- **Targeted Routing** — Through custom request headers, such as `X-AI-Foundry-Target`, callers can precisely route requests to a specified backend instance, suitable for session affinity, debugging, or data isolation scenarios; when not specified, requests automatically enter the load balancing pool for round-robin distribution
- **Automatic Failover** — By configuring a `retry` policy in the `backend` policy section, when the backend returns 4xx/5xx errors or connection failures, it automatically retries and switches to other healthy backends in the pool, using exponential backoff strategy to avoid generating a burst of retry requests in a short period
- **Request Tracing** — In the `outbound` policy section, the response header `X-AI-Foundry-Backend` returns the identifier of the backend that actually processed the request, facilitating client tracking and operational troubleshooting

Next, we will complete the entire architecture setup step by step:

| Section | Action | Objective | Platform |
|---------|--------|-----------|----------|
| 1 | Create APIM Instance | Set up the unified gateway entry point, enable Managed Identity | Azure Portal |
| 2 | Create Foundry Resources | Build the backend resource pool across multiple subscriptions and regions | Azure Portal |
| 3 | Deploy AI Models | Enable AI service capabilities on backend resources (using Sora2 as an example) | Foundry Portal |
| 4 | Configure RBAC | Grant APIM managed identity permissions to access backends | Azure Portal |
| 5 | Configure Backend + LB Pool | Register backends and assemble the load balancing pool | Azure Portal (APIM) |
| 6 | Create API + Policy | Define API entry points, configure routing and failover | Azure Portal (APIM) |
| 7 | Test & Validate | Verify load balancing and pinned backend routing | curl / Postman |

---

### 1. Create APIM Instance

Create an API Management instance in the Azure Portal, select a v2 Tier (Basicv2 / Standardv2 / Premiumv2), and enable **System Assigned Managed Identity** during creation.

**Portal Steps:** Search `API Management Service` → + Create → Fill in configuration → Enable on Managed identity tab → Review + install

![](assets/2-3-basics-config.png)

![](assets/2-4-managed-identity.png)

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

**After creation, verify:**
- Status: **Online**
- Record the **Gateway URL** (e.g., `https://<apim-name>.azure-api.net`)
- Record the Managed Identity's **Object (principal) ID** (needed for RBAC later)

![](assets/2-6-apim-dashboard.png)

---

### 2. Create Foundry Resources

Create Foundry resources across multiple subscriptions and regions. Each resource needs a corresponding project.

**Portal Steps:** Search `Microsoft Foundry` → Create a resource → Fill in Subscription / Region / Name / Project name → Create

![](assets/3-3-create-foundry-resource.png)

**CLI Alternative (create resource + project):**

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
|--------------|--------|---------------|
| Subscription A | East US 2 | foundry-eastus2-01 |
| Subscription A | Sweden Central | foundry-swedencentral-01 |
| Subscription B | East US 2 | foundry-eastus2-02 |
| Subscription B | Sweden Central | foundry-swedencentral-02 |

---

### 3. Deploy Models

Deploy AI models for each resource in the Foundry Portal.

**Portal Steps:** In [Foundry Portal](https://ai.azure.com/nextgen/), select the target project → Build → Models → Deploy a base model → Search for model (e.g., `sora-2`) → Deploy → Default settings

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

> Model names, versions, SKUs, and other parameters vary by region. See: Models and Region Availability: https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure

---

### 4. Configure RBAC

Grant the `Cognitive Services OpenAI User` role to APIM's Managed Identity on **each Foundry resource**.

**Portal Steps:** Go to Foundry resource → Access control (IAM) → + Add → Add role assignment → Search `Cognitive Services OpenAI User` → Members select Managed identity → Select API Management service → Review + assign

![](assets/5-3-select-role.png)

![](assets/5-4-select-managed-identity.png)

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

> `Cognitive Services OpenAI User` is the least-privilege role that allows inference calls but does not allow modifying resource configurations.

---

### 5. Configure Backend + Load Balancing Pool

#### 5a) Create Backends

Create a Backend for each Foundry resource with Managed Identity authentication.

**Get OpenAI Endpoint:** In [Foundry Portal](https://ai.azure.com/nextgen/), select the target project, find **Azure OpenAI endpoint** on the Home page (format: `https://<foundry-resource-name>.openai.azure.com/`). You can also get it via CLI:

```bash
az cognitiveservices account show \
  --subscription <subscription-id> \
  --resource-group <resource-group> \
  --name <foundry-resource-name> \
  --query "properties.endpoints.\"OpenAI Language Model Instance API\"" -o tsv
```

**Portal Steps:** APIM → Backends → + Create new backend → Fill in Name / Runtime URL → Switch to Managed Identity tab → Client identity select System assigned → Resource ID enter `https://cognitiveservices.azure.com` → Create

![](assets/6-3-create-backend.png)

**Key Configuration Details:**

| Configuration | Example Value | Description |
|---------------|---------------|-------------|
| Name | `<foundry-resource-name>` | Recommended to match the Foundry resource name for easier management |
| Runtime URL | `https://<foundry-resource-name>.openai.azure.com/openai/v1` | Foundry-provided OpenAI endpoint (+`openai/v1`) |
| Client identity | System assigned identity | Uses APIM's system-assigned managed identity |
| Resource ID | `https://cognitiveservices.azure.com` | Token audience, universal for all Foundry resources, **fixed value** |

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

#### 5b) Create Load Balancing Pool

**Portal Steps:** APIM → Backends → Load balancer tab → + Create new pool → Fill in Pool Name → Select all Backends → Choose Send requests evenly (Round-robin) → Create

![](assets/6-6-create-pool.png)

> The Portal provides two load balancing options: **Send requests evenly** (Round-robin for even distribution) and **Customize weight and priority** (custom weights and priorities).

---

### 6. Create API + Policy

#### 6a) Create API

**Portal Steps:** APIM → APIs → + Add API → HTTP → Fill in Display name / API URL suffix (`openai/v1`) → Leave Web service URL empty → Create

Then add Operations: + Add operation → Create `/*` wildcard path for each of POST / GET / DELETE.

> This example uses the wildcard path `/*` to forward all requests to the backend, suitable for scenarios where all APIs are proxied uniformly. For finer-grained control, you can create operations for specific business scenarios. For example, with Sora2 video generation, you could match only the `/videos/*` path.

#### 6b) Configure Policy

Select All operations → Click the `</>` icon in Inbound processing → Paste the following Policy → Save

```xml
<policies>
    <inbound>
        <base />
        <!-- Read request header to allow callers to specify a specific backend -->
        <set-variable name="target" value="@(context.Request.Headers.GetValueOrDefault("X-AI-Foundry-Target", ""))" />
        <!-- Backend load balancing pool name -->
        <set-variable name="pool_name" value="<your-ai-hub-pool-name>" />
        <choose>
            <!-- Caller specified a target backend, route directly -->
            <when condition="@(context.Variables.GetValueOrDefault<string>("target") != "")">
                <set-backend-service backend-id="@(context.Variables.GetValueOrDefault<string>("target"))" />
            </when>
            <!-- No target specified, use load balancing pool for round-robin distribution -->
            <otherwise>
                <set-backend-service backend-id="@((string)context.Variables["pool_name"])" />
            </otherwise>
        </choose>
    </inbound>
    <outbound>
        <base />
        <!-- Return the actual backend identifier in the response header -->
        <set-header name="X-AI-Foundry-Backend" exists-action="override">
            <value>@(context.Request.Url.Host.Split('.')[0])</value>
        </set-header>
    </outbound>
    <on-error>
        <base />
    </on-error>
    <backend>
        <choose>
            <!-- Pinned backend mode: forward directly, no retry -->
            <when condition="@(context.Variables.GetValueOrDefault<string>("target") != "")">
                <forward-request buffer-request-body="true" />
            </when>
            <otherwise>
                <!-- Round-robin mode: automatically retry and switch backends on connection failure/4xx/5xx -->
                <!-- Exponential backoff: approximately 0s → 3s → 5s (cap), first retry executes immediately -->
                <retry condition="@(context.Response == null || context.Response.StatusCode >= 400)" count="3" interval="1" delta="1" max-interval="5" first-fast-retry="true">
                    <set-backend-service backend-id="@((string)context.Variables["pool_name"])" />
                    <forward-request buffer-request-body="true" />
                </retry>
            </otherwise>
        </choose>
    </backend>
</policies>
```

**Policy Core Logic:**

| Section | Function |
|---------|----------|
| **inbound** | Reads the `X-AI-Foundry-Target` request header; if a value is present, routes to the specified backend; otherwise uses the LB Pool for round-robin |
| **outbound** | Returns the actual backend name in the `X-AI-Foundry-Backend` response header for tracking and debugging |
| **backend** | Pinned backend forwards directly; round-robin mode automatically retries and switches backends on errors (up to 3 times, exponential backoff) |

---

### 7. Test & Validate

**Preparation:**
- Get Gateway URL: APIM → Overview → Gateway URL
- Get API Key: APIM → Subscriptions → Built-in all-access → Show keys → Primary key

![](assets/8-2-subscription-key.png)

#### Test 1: Load Balancing

Send consecutive requests and observe the `X-AI-Foundry-Backend` response header rotating among multiple backends:

```bash
curl -D - -o /dev/null --location \
  'https://<apim-gateway-url>/openai/v1/videos' \
  --header 'Ocp-Apim-Subscription-Key: <your-subscription-key>'
```

Expected: The `X-AI-Foundry-Backend` value differs with each request, proving Round-robin is working.

![](assets/8-3-round-robin-test.png)

#### Test 2: Pinned Backend Routing

Lock to a specific backend using the `X-AI-Foundry-Target` request header:

```bash
curl -s -D - -o /dev/null --location \
  'https://<apim-gateway-url>/openai/v1/responses' \
  --header 'Content-Type: application/json' \
  --header 'Ocp-Apim-Subscription-Key: <your-subscription-key>' \
  --header 'X-AI-Foundry-Target: <backend-name>' \
  --data '{"model": "<model-name>", "input": "Hello"}' \
  | grep -i X-AI-Foundry-Backend
```

Expected: The `X-AI-Foundry-Backend` consistently returns the specified backend name across multiple requests.

![](assets/8-4-pinned-backend-test.png)

---

### FAQ

**Q: Why not use APIM Backend's Circuit Breaker?**

The goal of this architecture is load balancing and quota aggregation. Circuit Breaker would "break the circuit" when a backend fails, but in our scenario, one backend's model being throttled (429) should not block access to other models on that backend. The simple failover achieved through `retry` + `set-backend-service` is more suitable for this scenario.

**Q: Is this architecture only applicable to Sora2?**

No. It applies to any Foundry / Azure OpenAI model service (Responses API, Chat Completions, Embeddings, Image Generation, etc.). Simply point the Backend URL to the corresponding endpoint.

---

### Reference Documentation

- Microsoft Foundry Overview: https://learn.microsoft.com/azure/foundry/what-is-foundry
- Foundry RBAC: https://learn.microsoft.com/azure/foundry-classic/openai/how-to/role-based-access-control
- APIM v2 Tier: https://learn.microsoft.com/azure/api-management/v2-service-tiers-overview
- Backends and Load Balancing Pool: https://learn.microsoft.com/azure/api-management/backends
- APIM Managed Identity: https://learn.microsoft.com/azure/api-management/api-management-howto-use-managed-service-identity
- Retry Policy: https://learn.microsoft.com/azure/api-management/retry-policy
- Sora2 Video Generation: https://learn.microsoft.com/azure/foundry/openai/concepts/video-generation
- Models and Region Availability: https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure
- Azure OpenAI Error Codes: https://learn.microsoft.com/azure/foundry/openai/supported-languages#error-handling

---

### Change Log

| Date | Changes |
|------|---------|
| 2026-03-20 | Initial release |
