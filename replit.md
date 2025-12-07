# AutoArch - AI-Powered Smart Architecture Designer

## Overview

AutoArch is a browser-based architectural design tool that transforms user requirements into 2D floor plans and interactive 3D models. The application uses AI assistance to generate smart layouts from simple inputs, allowing users to create, edit, and export architectural designs entirely within the web browser. It targets residential planning with features for floor plan generation, 3D visualization, furniture placement, and multi-format exports.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript for type safety and modern development
- **Routing**: Wouter for lightweight client-side routing
- **UI Components**: shadcn/ui component library built on Radix UI primitives for accessible, customizable components
- **Styling**: Tailwind CSS with CSS variables for theming and responsive design
- **State Management**: Zustand for client-side state management with separate stores for projects and editor state
- **Data Fetching**: TanStack Query for server state management, caching, and synchronization
- **3D Rendering**: Planned Three.js integration for 3D visualization and interaction
- **Build Tool**: Vite for fast development and optimized production builds

### Backend Architecture  
- **Runtime**: Node.js with Express.js web framework
- **Language**: TypeScript with ES modules for modern JavaScript features
- **Authentication**: Replit OIDC-based authentication with Passport.js strategy
- **Session Management**: Express sessions with PostgreSQL session store
- **API Design**: RESTful APIs with structured error handling and request logging

### Data Storage Solutions
- **Database**: PostgreSQL with Neon serverless hosting
- **ORM**: Drizzle ORM for type-safe database operations and migrations
- **Schema**: Comprehensive schema covering users, projects, plans, furniture, and exports
- **Session Storage**: PostgreSQL-backed session storage for authentication state

### Authentication and Authorization
- **Provider**: Replit OIDC integration for seamless platform authentication
- **Session Security**: HTTP-only cookies with secure flags and configurable TTL
- **Authorization**: Route-level protection with middleware for authenticated endpoints
- **User Management**: Automatic user creation and profile management from OIDC claims

### Key Services and Features
- **Constraint Solver**: AI-powered layout generation service that converts user requirements into optimized floor plans
- **Export Service**: Multi-format export system supporting PDF floor plans, high-resolution images, walkthrough videos, and 3D models
- **Furniture System**: Categorized furniture library with placement rules and collision detection
- **Plan Generation**: Automated room layout, wall generation, and opening placement based on architectural constraints

## External Dependencies

### Core Infrastructure
- **Database Hosting**: Neon PostgreSQL serverless database
- **Authentication**: Replit OIDC service for user authentication
- **Development Platform**: Replit hosting and development environment

### Frontend Libraries
- **UI Framework**: React ecosystem with Radix UI component primitives
- **Styling**: Tailwind CSS with PostCSS processing
- **State Management**: Zustand for lightweight state management
- **Data Fetching**: TanStack Query for server state synchronization
- **Form Handling**: React Hook Form with Zod validation schemas
- **3D Graphics**: Three.js (planned integration) for 3D scene rendering

### Backend Services
- **Web Framework**: Express.js with TypeScript support
- **Database Access**: Drizzle ORM with PostgreSQL driver
- **Authentication**: Passport.js with OpenID Connect strategy
- **File Processing**: Sharp for image processing and jsPDF for document generation
- **Development Tools**: Vite for frontend bundling and esbuild for backend compilation

### Development and Build Tools
- **Package Manager**: npm with lockfile for dependency management
- **TypeScript**: Full TypeScript support across frontend and backend
- **Build Pipeline**: Vite for frontend, esbuild for backend production builds
- **Development Server**: Hot module replacement and runtime error overlay for development experience