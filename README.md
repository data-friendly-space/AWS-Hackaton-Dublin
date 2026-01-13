# Resilio - R4S Social System Mapping Platform

An AI-assisted digitalization tool for GOAL Global's Resilience for Social Systems (R4S) methodology. Resilio dramatically reduces the time and cost of social system mapping from months to weeks.

**Live Demo:** https://d18cm0umrsa2ex.cloudfront.net

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Data Models](#data-models)
- [Frontend Components](#frontend-components)

---

## Overview

Resilio is built for the AWS Generative AI Hackathon 2025 in partnership with GOAL Global. It provides:

- **System Mapping**: Visualize complex social systems with actors, relationships, and dependencies
- **Actor Assessment**: Identify and assess key actors (service users, providers, support, regulatory)
- **Vulnerability Analysis**: Evaluate sensitivity, exposure, and capacity across risk scenarios
- **AI-Powered Insights**: Leverage Claude Opus 4.5 via Amazon Bedrock for analysis

### Target Metrics
- **Mapping Time**: 3 weeks (down from 3+ months)
- **Cost per System**: <€3,000 (down from €30,000+)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CloudFront CDN                           │
│                   (d18cm0umrsa2ex.cloudfront.net)               │
├─────────────────────────────────────────────────────────────────┤
│                              │                                   │
│    ┌─────────────────────┐   │   ┌─────────────────────────┐    │
│    │   S3 Static Site    │   │   │   Application Load      │    │
│    │   (Nuxt 3 SSG)      │◄──┼───┤   Balancer (/api/*)     │    │
│    └─────────────────────┘   │   └───────────┬─────────────┘    │
│                              │               │                   │
│                              │   ┌───────────▼─────────────┐    │
│                              │   │   ECS Fargate           │    │
│                              │   │   (Django REST API)     │    │
│                              │   └───────────┬─────────────┘    │
│                              │               │                   │
│                              │   ┌───────────▼─────────────┐    │
│                              │   │   RDS PostgreSQL        │    │
│                              │   │   (Private Subnet)      │    │
│                              │   └─────────────────────────┘    │
│                              │                                   │
│                              │   ┌─────────────────────────┐    │
│                              │   │   Amazon Bedrock        │    │
│                              │   │   (Claude Opus 4.5)     │    │
│                              │   └─────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### AWS Services Used

| Service | Purpose |
|---------|---------|
| **CloudFront** | CDN for static frontend + API proxy |
| **S3** | Static website hosting |
| **ECS Fargate** | Containerized Django backend |
| **RDS PostgreSQL** | Relational database |
| **Application Load Balancer** | Backend traffic routing |
| **VPC** | Network isolation (public/private subnets) |
| **Secrets Manager** | Database credentials |
| **Amazon Bedrock** | AI/ML inference (Claude Opus 4.5) |

---

## Features

### Authentication & Authorization
- JWT-based authentication with access/refresh tokens
- Role-based access control (RBAC)
  - **Superadmin**: Full system access
  - **R4S Manager**: Project and system management
  - **Project Staff**: View and contribute to assigned projects

### Systems Management
- Create and manage social system mappings
- Define actors with types (Service User, Service Provider, Support, Regulatory)
- Map relationships between actors with quality assessments
- Track system components (Infrastructure, Human Resources, Financial, Information, Governance)
- Document risk scenarios with likelihood and impact ratings

### AI-Powered Analysis
- **AI Summary**: Automated system analysis with resilience scoring
- **Chatbot Interface**: Interactive Q&A about system vulnerabilities, actors, and recommendations
- **Claude Opus 4.5**: Powered by Amazon Bedrock for natural language understanding

### Visualization
- Interactive system diagrams
- Actor relationship mapping
- Quality indicators (Good, Stressed, Bad, Absent)
- Component status tracking

### Admin Dashboard
- User management (CRUD operations)
- Project management
- System oversight

---

## Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12 | Runtime |
| Django | 5.x | Web framework |
| Django REST Framework | 3.16 | API framework |
| Simple JWT | 5.x | JWT authentication |
| PostgreSQL | 15 | Database (production) |
| SQLite | 3 | Database (development) |
| Gunicorn | 23.x | WSGI server |
| WhiteNoise | 6.x | Static file serving |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Vue.js | 3.5 | UI framework |
| Nuxt | 4.2 | Vue meta-framework |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 4.x | Styling |
| shadcn-vue | - | UI component library |
| Radix Vue | - | Headless UI primitives |
| Lucide | - | Icon library |

### Infrastructure
| Technology | Version | Purpose |
|------------|---------|---------|
| AWS CDK | 2.x | Infrastructure as Code |
| TypeScript | 5.x | CDK language |
| Docker | - | Containerization |

---

## Project Structure

```
resilio/
├── backend/                    # Django REST API
│   ├── config/                 # Django settings
│   │   ├── settings.py         # Main configuration
│   │   ├── urls.py             # Root URL routing
│   │   └── wsgi.py             # WSGI application
│   ├── core/                   # Core R4S models
│   │   ├── models.py           # System, Actor, Relationship, etc.
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API viewsets
│   │   └── urls.py             # API routes
│   ├── users/                  # User management
│   │   ├── models.py           # Custom User model
│   │   ├── permissions.py      # RBAC permissions
│   │   ├── serializers.py      # Auth serializers
│   │   ├── views.py            # Auth endpoints
│   │   └── urls.py             # Auth routes
│   ├── Dockerfile              # Container definition
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # Nuxt 3 SPA/SSG
│   ├── app/
│   │   ├── components/         # Vue components
│   │   │   └── ui/             # shadcn-vue components
│   │   │       ├── button/
│   │   │       ├── card/
│   │   │       ├── badge/
│   │   │       ├── input/
│   │   │       ├── label/
│   │   │       ├── progress/
│   │   │       └── tabs/
│   │   ├── composables/        # Vue composables
│   │   │   ├── useApi.ts       # API client
│   │   │   ├── useAuth.ts      # Authentication
│   │   │   └── useMockSystems.ts # Mock data
│   │   ├── layouts/
│   │   │   └── default.vue     # Main layout
│   │   ├── pages/
│   │   │   ├── index.vue       # Landing page
│   │   │   ├── login.vue       # Login page
│   │   │   ├── about.vue       # About page
│   │   │   ├── profile.vue     # User profile
│   │   │   ├── systems/        # System pages
│   │   │   │   ├── index.vue   # Systems list
│   │   │   │   └── [slug].vue  # System detail
│   │   │   └── admin/          # Admin pages
│   │   │       ├── index.vue   # Admin dashboard
│   │   │       ├── users/      # User management
│   │   │       └── projects/   # Project management
│   │   └── lib/
│   │       └── utils.ts        # Utility functions
│   ├── public/
│   │   └── images/
│   │       └── system-diagram.svg
│   ├── nuxt.config.ts          # Nuxt configuration
│   └── tailwind.config.ts      # Tailwind configuration
│
├── infra/                      # AWS CDK Infrastructure
│   ├── bin/
│   │   └── infra.ts            # CDK app entry point
│   ├── lib/
│   │   └── infra-stack.ts      # Main stack definition
│   ├── cdk.json                # CDK configuration
│   └── package.json            # Node dependencies
│
├── examples/                   # DSL examples
├── deploy.sh                   # Deployment script
└── README.md                   # This file
```

---

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.12+
- Docker Desktop
- AWS CLI configured
- AWS CDK installed globally (`npm install -g aws-cdk`)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run generate
```

### Environment Variables

**Backend (.env)**
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Production database (optional)
DB_HOST=
DB_NAME=resilio
DB_USER=
DB_PASSWORD=
DB_PORT=5432
```

**Frontend (nuxt.config.ts)**
```typescript
runtimeConfig: {
  public: {
    apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api',
  },
}
```

---

## Deployment

### AWS Deployment

1. **Configure AWS CLI**
   ```bash
   aws configure --profile resilio
   ```

2. **Bootstrap CDK** (first time only)
   ```bash
   cd infra
   npx cdk bootstrap --profile resilio
   ```

3. **Deploy Infrastructure**
   ```bash
   npx cdk deploy --profile resilio
   ```

4. **Build and Deploy Frontend**
   ```bash
   cd frontend
   npm run generate
   aws s3 sync .output/public s3://resilio-frontend-ACCOUNT-REGION --delete --profile resilio
   aws cloudfront create-invalidation --distribution-id DIST_ID --paths "/*" --profile resilio
   ```

5. **Run Database Migrations**
   ```bash
   # Via ECS run-task with command override
   aws ecs run-task --cluster CLUSTER --task-definition TASK_DEF \
     --overrides '{"containerOverrides":[{"name":"web","command":["python","manage.py","migrate"]}]}'
   ```

### Deployment Outputs

| Resource | Value |
|----------|-------|
| CloudFront URL | https://d18cm0umrsa2ex.cloudfront.net |
| S3 Bucket | resilio-frontend-460832197675-us-west-2 |
| ALB Endpoint | Resili-Backe-*.us-west-2.elb.amazonaws.com |
| Database | resiliostack-resiliodbad3c7389-*.rds.amazonaws.com |

---

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login with email/password |
| POST | `/api/auth/refresh/` | Refresh access token |
| POST | `/api/auth/logout/` | Logout (blacklist refresh token) |

### User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List users (admin only) |
| POST | `/api/users/` | Create user (admin only) |
| GET | `/api/users/me/` | Get current user |
| PATCH | `/api/users/me/` | Update current user |
| POST | `/api/users/change_password/` | Change password |

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/systems/` | List systems |
| POST | `/api/systems/` | Create system |
| GET | `/api/systems/{slug}/` | Get system details |
| GET | `/api/systems/{slug}/export/` | Export system DSL |
| GET | `/api/actors/` | List actors |
| GET | `/api/relationships/` | List relationships |
| GET | `/api/risks/` | List risk scenarios |
| GET | `/api/health/` | Health check |

### Request/Response Examples

**Login**
```bash
curl -X POST https://example.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

**Response**
```json
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "superadmin"
  }
}
```

---

## Data Models

### User Model
```python
class User:
    id: UUID
    email: str (unique)
    first_name: str
    last_name: str
    role: 'superadmin' | 'r4s_manager' | 'project_staff'
    title: str
    country: str
    department: str
    job_title: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: datetime
```

### System Model
```python
class System:
    id: UUID
    slug: str (unique)
    name: str
    description: str
    sector: 'health' | 'education' | 'market' | 'water' | ...
    subsector: str
    region: str
    country: str
    assessment_date: date
    version: str
    created_by: User
    project: Project
```

### Actor Model
```python
class Actor:
    id: UUID
    system: System
    name: str
    slug: str
    actor_type: 'service_user' | 'service_provider' | 'support' | 'regulatory'
    function: str
    position_x: int
    position_y: int
```

### Relationship Model
```python
class Relationship:
    id: UUID
    system: System
    from_actor: Actor
    to_actor: Actor
    relationship_type: str
    goods_services: str
    quality: 'good' | 'stressed' | 'bad' | 'absent'
```

### Component Model
```python
class Component:
    id: UUID
    system: System
    name: str
    category: 'infrastructure' | 'human_resource' | 'financial' | ...
    status: 'functional' | 'degraded' | 'non_functional'
    description: str
```

### Risk Model
```python
class Risk:
    id: UUID
    system: System
    name: str
    category: 'climate' | 'conflict' | 'economic' | 'health' | 'political'
    likelihood: 'low' | 'medium' | 'high'
    impact: 'low' | 'medium' | 'high'
    description: str
```

---

## Frontend Components

### UI Components (shadcn-vue)

| Component | Path | Description |
|-----------|------|-------------|
| Button | `components/ui/button` | Primary action buttons |
| Card | `components/ui/card` | Content containers |
| Badge | `components/ui/badge` | Status indicators |
| Input | `components/ui/input` | Form inputs |
| Label | `components/ui/label` | Form labels |
| Progress | `components/ui/progress` | Progress bars |
| Tabs | `components/ui/tabs` | Tab navigation |

### Composables

| Composable | Description |
|------------|-------------|
| `useAuth()` | Authentication state and methods |
| `useApi()` | API client for backend requests |
| `useMockSystems()` | Mock data for demo purposes |

### Pages

| Route | Component | Description |
|-------|-----------|-------------|
| `/` | `index.vue` | Landing page with hero and features |
| `/login` | `login.vue` | User authentication |
| `/systems` | `systems/index.vue` | Systems list with stats |
| `/systems/:slug` | `systems/[slug].vue` | System detail with 4 tabs |
| `/profile` | `profile.vue` | User profile management |
| `/admin` | `admin/index.vue` | Admin dashboard |
| `/admin/users` | `admin/users/index.vue` | User management |
| `/admin/projects` | `admin/projects/index.vue` | Project management |
| `/about` | `about.vue` | About R4S methodology |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project was created for the AWS Generative AI Hackathon 2025 in partnership with GOAL Global.

---

## Acknowledgments

- **GOAL Global** - R4S Methodology and partnership
- **AWS** - Generative AI Hackathon hosting
- **Anthropic** - Claude AI models via Amazon Bedrock
