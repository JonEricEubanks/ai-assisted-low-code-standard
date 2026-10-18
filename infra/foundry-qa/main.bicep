targetScope = 'resourceGroup'

@minLength(1)
param foundryAccountName string = 'cog-mgp-foundry-qa-dev'

@minLength(1)
param foundryProjectName string = 'prj-mgp-foundry-qa-dev'

param location string = 'eastus2'
param deployFoundation bool = false
param skuName string = ''
param publicNetworkAccess string = ''
param diagnosticsEnabled bool = false
param diagnosticsWorkspaceName string = ''

assert skuRequiredWhenDeploying = !deployFoundation || !empty(skuName)
assert networkChoiceRequiredWhenDeploying = !deployFoundation || contains([
  'Enabled'
  'Disabled'
], publicNetworkAccess)
assert workspaceRequiredWhenEnablingDiagnostics = !diagnosticsEnabled || !empty(diagnosticsWorkspaceName)

resource foundryAccount 'Microsoft.CognitiveServices/accounts@2024-10-01' = if (deployFoundation) {
  name: foundryAccountName
  location: location
  kind: 'AIServices'
  sku: {
    name: skuName
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: foundryAccountName
    disableLocalAuth: true
    publicNetworkAccess: publicNetworkAccess
  }
}

resource foundryProject 'Microsoft.CognitiveServices/accounts/projects@2024-10-01' = if (deployFoundation) {
  name: '${foundryAccount.name}/${foundryProjectName}'
  properties: {
    displayName: foundryProjectName
  }
}

resource foundryDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (deployFoundation && diagnosticsEnabled) {
  name: '${foundryAccountName}-diagnostics'
  scope: foundryAccount
  properties: {
    workspaceId: resourceId('Microsoft.OperationalInsights/workspaces', diagnosticsWorkspaceName)
    logs: [
      {
        categoryGroup: 'allLogs'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}
