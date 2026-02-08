# Tasks: CLI To-Do Application

**Feature**: CLI To-Do Application
**Date**: 2026-02-04
**Branch**: phase-1
**Plan**: specs/phase-1/plan.md
**Input**: specs/phase-1/spec.md (user stories), specs/phase-1/data-model.md (entities), specs/phase-1/contracts/cli-api-contract.md (APIs)

## Implementation Strategy

**MVP Scope**: User Story 1 (Add Todo) implemented with foundational components, allowing for incremental delivery and testing of each feature.

**Delivery Order**: Tasks organized by user story priority, enabling independent implementation and testing of each story. Each story builds on foundational components while remaining independently testable.

## Dependencies

- User Story 1 (Add Todo) → foundational components (setup, models, services)
- User Story 2 (List Todos) → User Story 1 dependencies + table formatting
- User Story 3 (Complete Todo) → User Story 1 dependencies + update capability
- User Story 4 (Delete Todo) → User Story 1 dependencies
- User Story 5 (Update Todo) → User Story 1 dependencies + full update capability

## Parallel Opportunities

- [US2, US3, US4]: Can be implemented in parallel after US1 foundational components exist
- Unit tests can be written in parallel with feature implementations
- CLI command implementations can be developed separately after core services exist

---

## Phase 1: Setup

- [x] T001 Initialize project structure (app/, tests/, data/ directories)
- [x] T002 Create requirements.txt with dependencies (typer, rich, pytest)
- [x] T003 Setup virtual environment (venv)
- [x] T004 Create .gitignore for Python project

---

## Phase 2: Foundational Components

- [x] T005 Create data/todos.json with empty array
- [x] T006 [P] Create app/models/todo.py with Todo class and validation
- [x] T007 [P] Create app/utils/file_utils.py with load/save functions
- [x] T008 [P] Create app/__init__.py and constants
- [x] T009 Create app/services/todo_service.py skeleton

---

## Phase 3: [US1] Add New Todo

- [x] T010 [US1] Implement Todo model validation in app/models/todo.py
- [x] T011 [US1] Implement add_todo function in app/services/todo_service.py
- [x] T012 [US1] [P] Create unit tests for Todo model in tests/unit/models/test_todo.py
- [x] T013 [US1] [P] Create unit tests for add_todo in tests/unit/services/test_todo_service.py
- [x] T014 [US1] Implement CLI add command in app/main.py
- [x] T015 [US1] Create integration test for add command in tests/integration/test_cli.py
- [x] T016 [US1] Test adding a todo with title and priority using pytest

---

## Phase 4: [US2] List Todos

- [ ] T017 [US2] Implement get_all_todos function in app/services/todo_service.py
- [ ] T018 [US2] [P] Create unit tests for get_all_todos in tests/unit/services/test_todo_service.py
- [ ] T019 [US2] Format output as table using Rich in app/main.py
- [ ] T020 [US2] Implement CLI list command in app/main.py
- [ ] T021 [US2] Create integration test for list command in tests/integration/test_cli.py
- [ ] T022 [US2] Test displaying todos with different priorities and statuses using pytest

---

## Phase 5: [US3] Complete Todo

- [ ] T023 [US3] Implement update_todo function in app/services/todo_service.py
- [ ] T024 [US3] [P] Create unit tests for update_todo in tests/unit/services/test_todo_service.py
- [ ] T025 [US3] Implement CLI complete command in app/main.py
- [ ] T026 [US3] Create integration test for complete command in tests/integration/test_cli.py
- [ ] T026 [US3] Test marking a todo as completed using pytest

---

## Phase 6: [US4] Delete Todo

- [ ] T028 [US4] Implement delete_todo function in app/services/todo_service.py
- [ ] T029 [US4] [P] Create unit tests for delete_todo in tests/unit/services/test_todo_service.py
- [ ] T030 [US4] Implement CLI delete command in app/main.py
- [ ] T031 [US4] Create integration test for delete command in tests/integration/test_cli.py
- [ ] T032 [US4] Test removing a todo from the list using pytest

---

## Phase 7: [US5] Update Todo

- [ ] T033 [US5] Enhance update_todo function for partial updates in app/services/todo_service.py
- [ ] T034 [US5] [P] Create unit tests for partial updates in tests/unit/services/test_todo_service.py
- [ ] T035 [US5] Implement CLI update command in app/main.py
- [ ] T036 [US5] Create integration test for update command in tests/integration/test_cli.py
- [ ] T037 [US5] Test modifying todo details (title, description, priority) using pytest

---

## Phase 8: Polish & Cross-Cutting

- [ ] T038 Implement proper error handling and validation
- [ ] T039 Add CLI help and documentation
- [ ] T040 Make app/main.py executable as CLI tool
- [ ] T041 Update requirements.txt with all dependencies
- [ ] T042 Perform end-to-end testing of all commands using pytest
- [ ] T043 Document usage in README.md