# Event-Driven Architecture and CI Pipelines

## Overview

This document describes the evolution of the AI To-Do App architecture to an event-driven model with automated CI/CD pipelines, enabling scalable and maintainable development workflows.

## Architecture Evolution

### Current State (Phase 1-4)
- Monolithic FastAPI backend
- Direct database access
- Synchronous request-response patterns
- Manual deployment processes

### Target State (Phase 5+)
- Event-driven communication
- Distributed state management via Dapr
- Automated CI/CD pipelines
- Infrastructure as Code

## Event-Driven Architecture

### Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| State Store | Dapr + PostgreSQL | Persistent state management |
| Pub/Sub | Dapr (Redis/NATS) | Event distribution |
| API Gateway | FastAPI | Request routing |

### Event Flow

```
User Action → Frontend → Backend API → Dapr State Store
                              ↓
                         Event Published
                              ↓
                    Event Subscribers (future)
```

### Benefits

1. **Loose Coupling**: Services communicate via events, not direct calls
2. **Scalability**: Independent scaling of producers and consumers
3. **Resilience**: Event buffering handles service failures
4. **Extensibility**: New subscribers can be added without modifying publishers

## Dapr Integration

### State Management

Dapr provides a unified API for state management:

```yaml
# State Store Configuration
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
```

### Pub/Sub Configuration

Event publishing and subscription:

```yaml
# Pub/Sub Component
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
```

### Sidecar Pattern

Dapr runs as a sidecar container alongside the application:
- No code changes required for basic operations
- HTTP/gRPC APIs for state and event operations
- Built-in observability (tracing, metrics)

## Data Model

### Todo Entity

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| title | String | Task title (required) |
| description | String | Optional details |
| priority | String | low/medium/high |
| due_date | Date | Task deadline |
| status | String | pending/completed |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## CI/CD Pipelines

### GitHub Actions Workflow

#### Pipeline Stages

1. **Checkout**: Retrieve source code
2. **Setup**: Install dependencies (Node.js, Python)
3. **Lint**: Code quality checks
4. **Test**: Run unit and integration tests
5. **Build**: Create production artifacts
6. **Security**: Dependency vulnerability scanning

#### Workflow Triggers

- Push to `main` or `phase-*` branches
- Pull requests
- Manual dispatch

### Pipeline Configuration

```yaml
name: CI Pipeline
on:
  push:
    branches: [main, phase-*]
  pull_request:
    branches: [main]
```

### Artifacts

- Frontend: Built Next.js application
- Backend: Python package with dependencies
- Docker Images: Containerized services (future)

## Directory Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yaml          # CI pipeline definition
├── dapr/
│   ├── components/
│   │   ├── statestore.yaml  # State management config
│   │   └── pubsub.yaml      # Event bus config
│   └── configurations/
│       └── appconfig.yaml   # Dapr application config
├── specs/
│   └── architecture-v2.md   # This document
└── ...
```

## Implementation Roadmap

### Phase 5 (Current)
- [x] Dapr component configurations
- [x] CI pipeline establishment
- [x] Data model with priority and due_date

### Future Phases
- [ ] Dapr sidecar integration with backend
- [ ] Event publishers for todo operations
- [ ] Event subscribers for notifications
- [ ] CD pipeline for automated deployments
- [ ] Kubernetes deployment with Dapr

## Monitoring and Observability

### Dapr Built-in Features

- **Distributed Tracing**: Zipkin/Jaeger integration
- **Metrics**: Prometheus-compatible endpoints
- **Logging**: Structured JSON logs

### Recommended Stack

- **Tracing**: Jaeger or Zipkin
- **Metrics**: Prometheus + Grafana
- **Logging**: ELK Stack or Loki

## Security Considerations

1. **Secrets Management**: Dapr secrets component for sensitive data
2. **mTLS**: Automatic service-to-service encryption
3. **Access Policies**: Dapr authorization middleware
4. **Dependency Scanning**: Automated vulnerability detection in CI

## Performance Considerations

- **State Caching**: Redis for frequently accessed data
- **Event Batching**: Batch event publishing for high throughput
- **Connection Pooling**: Database connection management via Dapr
