# Resilio - R4S System Mapping Tool

A comprehensive system mapping and resilience assessment tool built for GOAL Global, implementing the R4S (Resilience for Social Systems) framework.

## Overview

Resilio enables humanitarian organizations to map complex social systems (health, education, markets, etc.), assess vulnerabilities, and visualize relationships between system actors. The tool combines AI-powered analysis with interactive visualizations to support evidence-based programming.

## Features

### System Mapping
- **Actor Management**: Define system actors with types (Service Users, Service Providers, Support, Regulatory)
- **Relationship Mapping**: Track flows of goods, services, and resources between actors
- **Quality Assessment**: Rate relationship quality (Good, Stressed, Bad, Absent)
- **Risk Scenarios**: Document and assess system-level risks

### Visualizations

#### Network Graph
- Interactive canvas-based visualization of actor relationships
- Color-coded nodes by actor type:
  - Purple: Service Users
  - Green: Service Providers
  - Amber: Support Actors
  - Red: Regulatory Bodies
- **Animated relationships**: Stressed and bad relationships pulse to highlight issues
- Zoom, pan, and filter capabilities
- Hover tooltips with actor details

#### R4S Framework Visualization
- AI-generated (AWS Bedrock + Claude) three-tier diagram:
  - **Top Tier**: Supporting Functions (Leadership, Information, Service Delivery, Financing, Supply, HR)
  - **Middle Tier**: Core Service Delivery (organized by admin level: Federal → Regional → Zonal → Woreda → Kebele → Community)
  - **Bottom Tier**: Regulatory & Normative Functions
- Graphviz DOT code generation with automatic SVG rendering
- Cached visualizations with automatic regeneration on data changes

### AI-Powered Analysis
- System resilience scoring
- AI-generated summaries and insights
- Interactive chat assistant for querying system data
- Bedrock-powered visualization generation

### PDF Export
- Comprehensive system reports including:
  - GOAL-branded header
  - Key metrics summary
  - AI-generated analysis
  - Actor, relationship, risk, and component tables
  - Full R4S visualization (landscape page)
  - Page numbers and footer branding

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (Nuxt 3 + Vue 3)                   │
│  - Static site hosted on S3/CloudFront                          │
│  - shadcn-vue UI components                                     │
│  - @viz-js/viz for Graphviz rendering                          │
│  - jsPDF for PDF generation                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Backend (Django + DRF)                      │
│  - ECS Fargate deployment                                       │
│  - PostgreSQL (RDS) database                                    │
│  - REST API endpoints                                           │
│  - Bedrock integration for AI features                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AWS Infrastructure (CDK)                    │
│  - VPC with public/private subnets                              │
│  - Application Load Balancer                                    │
│  - ECS Fargate cluster                                          │
│  - RDS PostgreSQL with Secrets Manager rotation                 │
│  - S3 + CloudFront for static hosting                           │
│  - Bedrock Runtime for AI model invocation                      │
└─────────────────────────────────────────────────────────────────┘
```

## Tech Stack

### Frontend
- **Framework**: Nuxt 3 (Vue 3)
- **UI**: shadcn-vue, Tailwind CSS
- **Visualization**: @viz-js/viz (Graphviz WASM), Canvas API
- **PDF Generation**: jsPDF, jspdf-autotable
- **Icons**: Lucide Vue

### Backend
- **Framework**: Django 5.x, Django REST Framework
- **Database**: PostgreSQL 15
- **AI Integration**: AWS Bedrock (Claude 3.5 Sonnet)
- **Authentication**: JWT (djangorestframework-simplejwt)

### Infrastructure
- **IaC**: AWS CDK (TypeScript)
- **Compute**: ECS Fargate
- **Database**: RDS PostgreSQL
- **Storage**: S3
- **CDN**: CloudFront
- **Secrets**: AWS Secrets Manager (auto-rotation)

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- AWS CLI configured
- Docker (for local development)

### Local Development

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data  # Load demo data
python manage.py runserver
```

### Deployment

```bash
cd infra
npm install
AWS_PROFILE=resilio npm run cdk deploy
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/systems/` | GET | List all systems |
| `/api/systems/{slug}/` | GET | Get system details |
| `/api/systems/{slug}/actors/` | GET | List system actors |
| `/api/systems/{slug}/relationships/` | GET | List relationships |
| `/api/systems/{slug}/risks/` | GET | List risk scenarios |
| `/api/agents/visualize/{slug}/` | GET | Get cached R4S visualization |
| `/api/agents/visualize/{slug}/` | POST | Regenerate R4S visualization |

## Demo Data

The system includes demo data for an RMNCAH (Reproductive, Maternal, Newborn, Child and Adolescent Health) system in Eastern Ethiopia, featuring:

- **25 Actors** across all administrative levels (Federal to Community)
- **27 Relationships** covering referral pathways, supply chains, and oversight
- **5 Risk Scenarios** (drought, supply chain, staff turnover, disease outbreak, funding)
- Actor metadata including administrative level and service type

## Environment Variables

### Backend
```env
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=your-django-secret-key
AWS_REGION=us-west-2
DJANGO_DEBUG=False
```

### Frontend
```env
NUXT_PUBLIC_API_BASE=https://your-api-domain.com/api
```

## Project Structure

```
resilio/
├── frontend/               # Nuxt 3 frontend
│   ├── app/
│   │   ├── components/    # Vue components
│   │   ├── composables/   # Composable functions
│   │   └── pages/         # Route pages
│   └── public/            # Static assets
├── backend/               # Django backend
│   ├── config/           # Django settings
│   ├── core/             # Main app (models, views, serializers)
│   │   ├── management/   # Management commands (seed_data)
│   │   ├── migrations/   # Database migrations
│   │   └── agents.py     # Bedrock visualization endpoint
│   └── requirements.txt
└── infra/                # AWS CDK infrastructure
    └── lib/
        └── infra-stack.ts
```

## License

Proprietary - GOAL Global

## Contributors

- GOAL Global Development Team
- AWS Hackathon Dublin 2024
