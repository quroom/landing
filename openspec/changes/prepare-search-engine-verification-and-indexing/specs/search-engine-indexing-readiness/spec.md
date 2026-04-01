# search-engine-indexing-readiness Specification

## Purpose
사이트가 Google, Bing, Naver, Daum 등록 전에 필요한 최소 검색엔진 준비 상태를 제공하도록 정의한다.

## Requirements
### Requirement: Site MUST expose a crawlable robots.txt
The system MUST provide a public `robots.txt` that allows search engines to crawl the public landing pages and references the canonical sitemap URL.

#### Scenario: Crawler requests robots.txt
- **WHEN** a crawler requests `/robots.txt`
- **THEN** the system MUST return HTTP 200 with a plain text robots response
- **AND** the response MUST include a `Sitemap:` line pointing to the canonical sitemap URL

#### Scenario: Operator needs to append provider-specific robots lines
- **WHEN** an operator is asked by a search provider to add an additional line at the bottom of `robots.txt`
- **THEN** the system or documented procedure MUST support adding that line without breaking the default crawlable robots structure

### Requirement: Site MUST expose a canonical sitemap.xml
The system MUST provide a public `sitemap.xml` that includes the primary landing URLs intended for indexing.

#### Scenario: Search engine requests sitemap.xml
- **WHEN** a crawler requests `/sitemap.xml`
- **THEN** the system MUST return HTTP 200 with sitemap XML content
- **AND** the sitemap MUST include the homepage and key public landing routes

### Requirement: Site MUST define a canonical site URL for indexing
The system MUST define a single canonical site URL for sitemap, robots, and indexing-related meta references.

#### Scenario: Operator checks indexing base URL
- **WHEN** an operator reads the indexing configuration or runbook
- **THEN** they MUST be able to identify the canonical site URL used for sitemap and robots references

### Requirement: Registration runbook MUST define manual console steps
The repository MUST document the manual registration flow for Google, Bing, Naver, and Daum after the site is prepared.

#### Scenario: Operator follows registration runbook
- **WHEN** an operator reads the runbook
- **THEN** they MUST be able to identify the canonical site URL, sitemap URL, and service-by-service registration order
- **AND** the runbook MUST distinguish between verification-based consoles and Daum's registration request flow
