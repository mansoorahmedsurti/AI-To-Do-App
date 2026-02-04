# Agent Context

## Project: To-Do CLI Application

### Technology Stack
- **Runtime**: Node.js 18+
- **Language**: JavaScript (ES2022+)
- **CLI Framework**: commander.js
- **Styling**: chalk
- **Testing**: Jest
- **Build Tool**: npm

### Project Structure
- `src/models/todo.js` - Data model definitions
- `src/services/todoService.js` - Business logic
- `src/utils/fileUtils.js` - File operations
- `src/cli/index.js` - CLI interface
- `tests/` - Test files
- `data/todos.json` - Default data storage

### Key Dependencies
- commander: ^10.0.0 - Command-line interface parsing
- chalk: ^5.0.0 - Terminal string styling
- uuid: ^9.0.0 - Unique identifier generation

### Architecture Patterns
- Separation of concerns (models, services, CLI)
- File-based persistence
- Immutable data structures where possible
- Functional programming principles

### Coding Standards
- Use modern ES6+ features
- Consistent error handling
- Comprehensive test coverage
- Clear, descriptive variable names
- Proper validation and sanitization