# Project Overview

This is a frontend application for WasteTrack, a platform for reporting and managing waste. It is built with Angular and uses Angular Material for UI components. The application allows users to report waste, view existing reports, and manage their accounts.

# Building and Running

## Development Server

To start a local development server, run:

```bash
ng serve
```

Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Building

To build the project, run:

```bash
ng build
```

The build artifacts will be stored in the `dist/` directory.

## Running Unit Tests

To run unit tests, execute:

```bash
ng test
```

# Development Conventions

## Code Style

The project follows the standard Angular coding style.

## Components

Components are organized by feature under `src/app/components`. Each component has its own folder with HTML, CSS, and TypeScript files.

## Services

Services are located in `src/app/services`. These are used for handling authentication, reporting, and other API interactions.

## Routing

The application's routes are defined in `src/app/app.routes.ts`. The main routes include landing, login, register, and report waste.
