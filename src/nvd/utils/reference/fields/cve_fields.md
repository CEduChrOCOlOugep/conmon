Here is a list of all the fields extracted from the JSON schema:

### Top-Level Fields
- $schema
- title
- definitions
- type
- properties
- required
- additionalProperties

### Definitions
#### def_cve_item
- properties
  - cve
- required
- additionalProperties

#### cve_item
- type
- properties
  - id
  - sourceIdentifier
  - vulnStatus
  - published
  - lastModified
  - evaluatorComment
  - evaluatorSolution
  - evaluatorImpact
  - cisaExploitAdd
  - cisaActionDue
  - cisaRequiredAction
  - cisaVulnerabilityName
  - cveTags
    - type
    - items
      - properties
        - sourceIdentifier
        - tags
  - descriptions
  - references
  - metrics
    - description
    - type
    - properties
      - cvssMetricV40
      - cvssMetricV31
      - cvssMetricV30
      - cvssMetricV2
  - weaknesses
  - configurations
  - vendorComments
- required

#### cvss-v2
- properties
  - source
  - type
  - cvssData
  - baseSeverity
  - exploitabilityScore
  - impactScore
  - acInsufInfo
  - obtainAllPrivilege
  - obtainUserPrivilege
  - obtainOtherPrivilege
  - userInteractionRequired
- required
- additionalProperties

#### cvss-v30
- properties
  - source
  - type
  - cvssData
  - exploitabilityScore
  - impactScore
- required
- additionalProperties

#### cvss-v31
- properties
  - source
  - type
  - cvssData
  - exploitabilityScore
  - impactScore
- required
- additionalProperties

#### cvss-v40
- properties
  - source
  - type
  - cvssData
- required
- additionalProperties

#### cve_id
- type
- pattern

#### lang_string
- type
- properties
  - lang
  - value
- required
- additionalProperties

#### reference
- type
- properties
  - url
  - source
  - tags
- required

#### vendorComment
- type
- properties
  - organization
  - comment
  - lastModified
- required
- additionalProperties

#### weakness
- properties
  - source
  - type
  - description
- required
- additionalProperties

#### config
- properties
  - operator
  - negate
  - nodes
- required

#### node
- description
- properties
  - operator
  - negate
  - cpeMatch
- required

#### cpe_match
- description
- type
- properties
  - vulnerable
  - criteria
  - matchCriteriaId
  - versionStartExcluding
  - versionStartIncluding
  - versionEndExcluding
  - versionEndIncluding
- required

#### def_subscore
- description
- type
- minimum
- maximum

### Properties
- resultsPerPage
- startIndex
- totalResults
- format
- version
- timestamp
- vulnerabilities