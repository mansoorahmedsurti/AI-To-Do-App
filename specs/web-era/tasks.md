# Phase II Tasks: Monorepo & Auth

## Phase 1: Project Restructuring

### Task 1.1: Create project structure
- **Description**: Create the required directory structure for the monorepo
- **Steps**:
  - Create /frontend directory for Next.js app
  - Create /backend directory for FastAPI app
  - Create root docker-compose.yml for PostgreSQL
- **Acceptance Criteria**: Clean directory structure with proper organization
- **Dependencies**: None

### Task 1.2: Set up PostgreSQL with Docker Compose
- **Description**: Configure local PostgreSQL using Docker
- **Steps**:
  - Create docker-compose.yml with PostgreSQL service
  - Configure user: postgres, DB: todos
  - Test database connection
- **Acceptance Criteria**: PostgreSQL container runs locally and accepts connections
- **Dependencies**: Task 1.1

### Task 1.3: Remove JSON file persistence
- **Description**: Eliminate any JSON file usage to comply with constitution
- **Steps**:
  - Remove any JSON file references in backend
  - Update data models to use only PostgreSQL
  - Ensure no JSON persistence remains
- **Acceptance Criteria**: Zero JSON file usage, all data stored in PostgreSQL
- **Dependencies**: Task 1.2

## Phase 2: Backend Implementation

### Task 2.1: Initialize FastAPI project with SQLModel
- **Description**: Set up the backend with PostgreSQL integration
- **Steps**:
  - Create FastAPI app structure in /backend
  - Install required packages (FastAPI, SQLModel, PostgreSQL driver)
  - Set up database connection to PostgreSQL
- **Acceptance Criteria**: Functional FastAPI app connected to PostgreSQL
- **Dependencies**: Task 1.2

### Task 2.2: Create SQLModel data models
- **Description**: Define User and Todo models using SQLModel
- **Steps**:
  - Create User model with Better Auth compatibility
  - Create Todo model with proper relationships
  - Set up proper indexing and constraints
- **Acceptance Criteria**: Complete SQLModel definitions with no custom auth logic
- **Dependencies**: Task 2.1

### Task 2.3: Implement API endpoints
- **Description**: Create backend API endpoints with authentication
- **Steps**:
  - Create auth endpoints (registration, login)
  - Create todo management endpoints
  - Implement proper authentication with Better Auth JWTs
- **Acceptance Criteria**: All required API endpoints functional with JWT auth
- **Dependencies**: Task 2.2

## Phase 3: Frontend Implementation

### Task 3.1: Initialize Next.js 15 project
- **Description**: Set up the frontend Next.js application
- **Steps**:
  - Create Next.js 15 app in /frontend directory
  - Configure App Router
  - Install Tailwind CSS and Shadcn UI
- **Acceptance Criteria**: Functional Next.js 15 app with styling framework
- **Dependencies**: Task 1.1

### Task 3.2: Integrate Better Auth
- **Description**: Set up Better Auth for frontend authentication
- **Steps**:
  - Install Better Auth packages
  - Configure Better Auth in Next.js
  - Create auth context and components
- **Acceptance Criteria**: Better Auth properly integrated with no custom auth logic
- **Dependencies**: Task 3.1

### Task 3.3: Create todo management UI
- **Description**: Build user interface for todo management
- **Steps**:
  - Create todo list display component
  - Create todo creation/editing forms
  - Implement proper state management
- **Acceptance Criteria**: Complete UI for managing todos with authentication
- **Dependencies**: Task 3.2

### Task 3.4: Connect frontend to backend API
- **Description**: Integrate frontend with backend API
- **Steps**:
  - Implement API client with JWT handling
  - Connect UI components to API endpoints
  - Handle authentication headers properly
- **Acceptance Criteria**: Frontend successfully communicates with backend API
- **Dependencies**: Task 3.3, Task 2.3