/**
 * Mock systems data for demonstration
 */

export interface MockActor {
  id: string
  name: string
  actor_type: 'service_user' | 'service_provider' | 'support' | 'regulatory'
  actor_type_display: string
  function: string
  position_x: number
  position_y: number
  sensitivity: 'low' | 'medium' | 'high'
  exposure: 'low' | 'medium' | 'high'
  capacity: 'low' | 'medium' | 'high'
}

export interface MockRelationship {
  id: string
  from_actor: string
  from_actor_name: string
  to_actor: string
  to_actor_name: string
  goods_services: string
  quality: 'good' | 'stressed' | 'bad' | 'absent'
  quality_display: string
  criticality: 'low' | 'medium' | 'high'
}

export interface MockComponent {
  id: string
  name: string
  category: 'infrastructure' | 'human_resource' | 'financial' | 'information' | 'governance'
  category_display: string
  status: 'functional' | 'degraded' | 'non_functional'
  status_display: string
  description: string
  dependencies: string[]
}

export interface MockRisk {
  id: string
  name: string
  category: 'climate' | 'conflict' | 'economic' | 'health' | 'political'
  category_display: string
  likelihood: 'low' | 'medium' | 'high'
  likelihood_display: string
  impact: 'low' | 'medium' | 'high'
  description: string
}

export interface MockSystem {
  id: string
  slug: string
  name: string
  description: string
  region: string
  country: string
  sector: string
  sector_display: string
  subsector: string
  assessment_date: string
  version: string
  actor_count: number
  relationship_count: number
  component_count: number
  risk_count: number
  ai_summary: string
  resilience_score: number
  vulnerability_score: number
  actors: MockActor[]
  relationships: MockRelationship[]
  components: MockComponent[]
  risks: MockRisk[]
}

const mockSystems: MockSystem[] = [
  {
    id: '1',
    slug: 'rmncah-eastern-ethiopia',
    name: 'RMNCAH Health System - Eastern Ethiopia',
    description: 'Reproductive, Maternal, Newborn, Child and Adolescent Health system serving rural communities in Eastern Ethiopia. This system supports approximately 2.3 million people across 12 woredas.',
    region: 'Eastern Region',
    country: 'Ethiopia',
    sector: 'health',
    sector_display: 'Health',
    subsector: 'RMNCAH',
    assessment_date: '2024-03-15',
    version: '2.1',
    actor_count: 12,
    relationship_count: 18,
    component_count: 8,
    risk_count: 5,
    resilience_score: 62,
    vulnerability_score: 38,
    ai_summary: `## System Overview

The RMNCAH Health System in Eastern Ethiopia demonstrates **moderate resilience** with significant strengths in community health worker networks and NGO partnerships. However, the system faces notable vulnerabilities in supply chain management and infrastructure maintenance.

### Key Findings

1. **Strong Community Networks**: The Health Extension Worker (HEW) program provides effective last-mile delivery of basic health services, achieving 78% coverage in target communities.

2. **Critical Dependencies**: The system heavily relies on the regional health bureau for pharmaceutical supplies, creating a single point of failure that was exposed during the 2023 supply disruption.

3. **Governance Gaps**: Coordination between woreda health offices and NGO partners lacks formal mechanisms, leading to service duplication in some areas and gaps in others.

### Vulnerability Assessment

- **Climate Exposure**: High - Recurring droughts affect 60% of service areas
- **Infrastructure Sensitivity**: Medium - Health facilities require generator backup due to unreliable grid power
- **Adaptive Capacity**: Medium - Strong informal networks compensate for formal system weaknesses

### Recommendations

1. Establish buffer stock mechanisms at zonal level to reduce supply chain vulnerability
2. Formalize coordination protocols between government and NGO actors
3. Invest in solar power systems for health facilities to reduce grid dependency`,
    actors: [
      {
        id: 'a1',
        name: 'Pregnant Women & Mothers',
        actor_type: 'service_user',
        actor_type_display: 'Service User',
        function: 'Primary beneficiaries requiring antenatal care, delivery services, and postnatal care',
        position_x: 100,
        position_y: 200,
        sensitivity: 'high',
        exposure: 'high',
        capacity: 'low'
      },
      {
        id: 'a2',
        name: 'Children Under 5',
        actor_type: 'service_user',
        actor_type_display: 'Service User',
        function: 'Recipients of immunization, nutrition services, and treatment for common childhood illnesses',
        position_x: 100,
        position_y: 320,
        sensitivity: 'high',
        exposure: 'high',
        capacity: 'low'
      },
      {
        id: 'a3',
        name: 'Health Centers',
        actor_type: 'service_provider',
        actor_type_display: 'Service Provider',
        function: 'Provide comprehensive primary healthcare including maternal and child health services',
        position_x: 330,
        position_y: 80,
        sensitivity: 'medium',
        exposure: 'medium',
        capacity: 'medium'
      },
      {
        id: 'a4',
        name: 'Health Extension Workers',
        actor_type: 'service_provider',
        actor_type_display: 'Service Provider',
        function: 'Community-based health workers providing preventive care and health education',
        position_x: 330,
        position_y: 200,
        sensitivity: 'medium',
        exposure: 'high',
        capacity: 'medium'
      },
      {
        id: 'a5',
        name: 'Traditional Birth Attendants',
        actor_type: 'service_provider',
        actor_type_display: 'Service Provider',
        function: 'Community members assisting with home deliveries and maternal care referrals',
        position_x: 330,
        position_y: 320,
        sensitivity: 'low',
        exposure: 'medium',
        capacity: 'low'
      },
      {
        id: 'a6',
        name: 'Woreda Health Office',
        actor_type: 'regulatory',
        actor_type_display: 'Regulatory',
        function: 'Local government authority responsible for health service coordination and oversight',
        position_x: 560,
        position_y: 80,
        sensitivity: 'low',
        exposure: 'low',
        capacity: 'medium'
      },
      {
        id: 'a7',
        name: 'Regional Health Bureau',
        actor_type: 'regulatory',
        actor_type_display: 'Regulatory',
        function: 'Regional authority managing health policy, budgets, and pharmaceutical supply',
        position_x: 560,
        position_y: 200,
        sensitivity: 'low',
        exposure: 'low',
        capacity: 'high'
      },
      {
        id: 'a8',
        name: 'GOAL Ethiopia',
        actor_type: 'support',
        actor_type_display: 'Support',
        function: 'International NGO providing technical support, training, and supplementary supplies',
        position_x: 560,
        position_y: 320,
        sensitivity: 'low',
        exposure: 'low',
        capacity: 'high'
      },
      {
        id: 'a9',
        name: 'UNICEF',
        actor_type: 'support',
        actor_type_display: 'Support',
        function: 'UN agency providing vaccines, nutrition supplies, and technical assistance',
        position_x: 560,
        position_y: 440,
        sensitivity: 'low',
        exposure: 'low',
        capacity: 'high'
      },
      {
        id: 'a10',
        name: 'Community Leaders',
        actor_type: 'support',
        actor_type_display: 'Support',
        function: 'Traditional and religious leaders who influence health-seeking behaviors',
        position_x: 100,
        position_y: 440,
        sensitivity: 'low',
        exposure: 'medium',
        capacity: 'medium'
      },
      {
        id: 'a11',
        name: 'Private Pharmacies',
        actor_type: 'service_provider',
        actor_type_display: 'Service Provider',
        function: 'Commercial outlets providing medications and basic health products',
        position_x: 330,
        position_y: 440,
        sensitivity: 'medium',
        exposure: 'medium',
        capacity: 'medium'
      },
      {
        id: 'a12',
        name: 'Zonal Hospital',
        actor_type: 'service_provider',
        actor_type_display: 'Service Provider',
        function: 'Secondary care facility for referrals requiring advanced medical interventions',
        position_x: 700,
        position_y: 80,
        sensitivity: 'medium',
        exposure: 'low',
        capacity: 'high'
      }
    ],
    relationships: [
      {
        id: 'r1',
        from_actor: 'a1',
        from_actor_name: 'Pregnant Women & Mothers',
        to_actor: 'a3',
        to_actor_name: 'Health Centers',
        goods_services: 'Antenatal care, delivery services',
        quality: 'stressed',
        quality_display: 'Stressed',
        criticality: 'high'
      },
      {
        id: 'r2',
        from_actor: 'a1',
        from_actor_name: 'Pregnant Women & Mothers',
        to_actor: 'a4',
        to_actor_name: 'Health Extension Workers',
        goods_services: 'Health education, referrals',
        quality: 'good',
        quality_display: 'Good',
        criticality: 'high'
      },
      {
        id: 'r3',
        from_actor: 'a2',
        from_actor_name: 'Children Under 5',
        to_actor: 'a3',
        to_actor_name: 'Health Centers',
        goods_services: 'Immunization, treatment',
        quality: 'good',
        quality_display: 'Good',
        criticality: 'high'
      },
      {
        id: 'r4',
        from_actor: 'a3',
        from_actor_name: 'Health Centers',
        to_actor: 'a12',
        to_actor_name: 'Zonal Hospital',
        goods_services: 'Emergency referrals',
        quality: 'stressed',
        quality_display: 'Stressed',
        criticality: 'high'
      },
      {
        id: 'r5',
        from_actor: 'a7',
        from_actor_name: 'Regional Health Bureau',
        to_actor: 'a3',
        to_actor_name: 'Health Centers',
        goods_services: 'Supplies, guidelines, supervision',
        quality: 'stressed',
        quality_display: 'Stressed',
        criticality: 'high'
      },
      {
        id: 'r6',
        from_actor: 'a8',
        from_actor_name: 'GOAL Ethiopia',
        to_actor: 'a4',
        to_actor_name: 'Health Extension Workers',
        goods_services: 'Training, supplies, mentorship',
        quality: 'good',
        quality_display: 'Good',
        criticality: 'medium'
      },
      {
        id: 'r7',
        from_actor: 'a9',
        from_actor_name: 'UNICEF',
        to_actor: 'a7',
        to_actor_name: 'Regional Health Bureau',
        goods_services: 'Vaccines, technical support',
        quality: 'good',
        quality_display: 'Good',
        criticality: 'high'
      },
      {
        id: 'r8',
        from_actor: 'a6',
        from_actor_name: 'Woreda Health Office',
        to_actor: 'a3',
        to_actor_name: 'Health Centers',
        goods_services: 'Coordination, monitoring',
        quality: 'stressed',
        quality_display: 'Stressed',
        criticality: 'medium'
      },
      {
        id: 'r9',
        from_actor: 'a10',
        from_actor_name: 'Community Leaders',
        to_actor: 'a1',
        to_actor_name: 'Pregnant Women & Mothers',
        goods_services: 'Social influence, mobilization',
        quality: 'good',
        quality_display: 'Good',
        criticality: 'medium'
      },
      {
        id: 'r10',
        from_actor: 'a5',
        from_actor_name: 'Traditional Birth Attendants',
        to_actor: 'a3',
        to_actor_name: 'Health Centers',
        goods_services: 'Emergency referrals',
        quality: 'bad',
        quality_display: 'Bad',
        criticality: 'high'
      }
    ],
    components: [
      {
        id: 'c1',
        name: 'Health Facility Infrastructure',
        category: 'infrastructure',
        category_display: 'Infrastructure',
        status: 'degraded',
        status_display: 'Degraded',
        description: 'Physical buildings, equipment, water and sanitation facilities at health centers',
        dependencies: ['Power supply', 'Water system', 'Road access']
      },
      {
        id: 'c2',
        name: 'Pharmaceutical Supply Chain',
        category: 'infrastructure',
        category_display: 'Infrastructure',
        status: 'degraded',
        status_display: 'Degraded',
        description: 'System for procurement, storage, and distribution of medicines and supplies',
        dependencies: ['Regional warehouse', 'Transport network', 'Cold chain']
      },
      {
        id: 'c3',
        name: 'Health Workforce',
        category: 'human_resource',
        category_display: 'Human Resource',
        status: 'functional',
        status_display: 'Functional',
        description: 'Trained health professionals including nurses, midwives, and health officers',
        dependencies: ['Training institutions', 'Salary payments', 'Housing']
      },
      {
        id: 'c4',
        name: 'Community Health Workers',
        category: 'human_resource',
        category_display: 'Human Resource',
        status: 'functional',
        status_display: 'Functional',
        description: 'Health Extension Workers and volunteers providing community-level services',
        dependencies: ['Supervision', 'Supplies', 'Incentives']
      },
      {
        id: 'c5',
        name: 'Health Financing',
        category: 'financial',
        category_display: 'Financial',
        status: 'degraded',
        status_display: 'Degraded',
        description: 'Government budget allocation, donor funding, and community contributions',
        dependencies: ['Government budget', 'Donor commitments', 'Insurance schemes']
      },
      {
        id: 'c6',
        name: 'Health Information System',
        category: 'information',
        category_display: 'Information',
        status: 'functional',
        status_display: 'Functional',
        description: 'DHIS2-based system for health data collection, reporting, and analysis',
        dependencies: ['Internet connectivity', 'Trained staff', 'Hardware']
      },
      {
        id: 'c7',
        name: 'Referral System',
        category: 'infrastructure',
        category_display: 'Infrastructure',
        status: 'degraded',
        status_display: 'Degraded',
        description: 'Ambulance services and communication systems for emergency referrals',
        dependencies: ['Vehicles', 'Fuel', 'Communication network']
      },
      {
        id: 'c8',
        name: 'Governance & Coordination',
        category: 'governance',
        category_display: 'Governance',
        status: 'degraded',
        status_display: 'Degraded',
        description: 'Coordination mechanisms between government, NGOs, and community structures',
        dependencies: ['Meeting platforms', 'Leadership', 'Clear mandates']
      }
    ],
    risks: [
      {
        id: 'risk1',
        name: 'Drought & Food Insecurity',
        category: 'climate',
        category_display: 'Climate',
        likelihood: 'high',
        likelihood_display: 'High',
        impact: 'high',
        description: 'Recurring droughts leading to malnutrition, population displacement, and increased demand for health services'
      },
      {
        id: 'risk2',
        name: 'Supply Chain Disruption',
        category: 'economic',
        category_display: 'Economic',
        likelihood: 'medium',
        likelihood_display: 'Medium',
        impact: 'high',
        description: 'Disruption to pharmaceutical and medical supply chains due to funding gaps or logistics challenges'
      },
      {
        id: 'risk3',
        name: 'Staff Turnover',
        category: 'economic',
        category_display: 'Economic',
        likelihood: 'high',
        likelihood_display: 'High',
        impact: 'medium',
        description: 'Loss of trained health workers to urban areas or better-paying positions'
      },
      {
        id: 'risk4',
        name: 'Disease Outbreak',
        category: 'health',
        category_display: 'Health',
        likelihood: 'medium',
        likelihood_display: 'Medium',
        impact: 'high',
        description: 'Outbreak of infectious diseases such as cholera, measles, or respiratory infections'
      },
      {
        id: 'risk5',
        name: 'Funding Reduction',
        category: 'political',
        category_display: 'Political',
        likelihood: 'medium',
        likelihood_display: 'Medium',
        impact: 'high',
        description: 'Reduction in government or donor funding for health programs'
      }
    ]
  },
  {
    id: '2',
    slug: 'market-system-south-sudan',
    name: 'Agricultural Market System - South Sudan',
    description: 'Food and agricultural market system connecting smallholder farmers to markets in Greater Bahr el Ghazal region.',
    region: 'Greater Bahr el Ghazal',
    country: 'South Sudan',
    sector: 'market',
    sector_display: 'Market',
    subsector: 'Agriculture',
    assessment_date: '2024-01-20',
    version: '1.3',
    actor_count: 9,
    relationship_count: 14,
    component_count: 6,
    risk_count: 4,
    resilience_score: 45,
    vulnerability_score: 55,
    ai_summary: `## System Overview

The Agricultural Market System in South Sudan faces **significant challenges** due to ongoing conflict, poor infrastructure, and climate variability. Despite these challenges, informal trader networks demonstrate remarkable adaptability.

### Key Findings

1. **Informal Networks**: Cross-border trade with Uganda and Sudan provides critical market access when formal channels fail.

2. **Infrastructure Gaps**: Only 15% of roads are passable year-round, severely limiting market access during rainy seasons.

3. **Price Volatility**: Staple food prices fluctuate by up to 300% seasonally due to supply constraints.

### Recommendations

1. Support trader associations to formalize coordination mechanisms
2. Invest in strategic road rehabilitation for key market corridors
3. Establish community grain storage facilities to buffer price shocks`,
    actors: [],
    relationships: [],
    components: [],
    risks: []
  },
  {
    id: '3',
    slug: 'wash-system-zimbabwe',
    name: 'WASH System - Matabeleland',
    description: 'Water, Sanitation and Hygiene system serving rural communities in Matabeleland South province.',
    region: 'Matabeleland South',
    country: 'Zimbabwe',
    sector: 'water',
    sector_display: 'Water',
    subsector: 'WASH',
    assessment_date: '2024-02-28',
    version: '1.0',
    actor_count: 8,
    relationship_count: 11,
    component_count: 5,
    risk_count: 3,
    resilience_score: 58,
    vulnerability_score: 42,
    ai_summary: `## System Overview

The WASH system in Matabeleland shows **moderate resilience** with strong community-based management structures but faces chronic infrastructure challenges.

### Key Findings

1. **Community Management**: Village Water Committees effectively manage 70% of water points, demonstrating strong local ownership.

2. **Infrastructure Age**: 45% of boreholes are over 15 years old and require rehabilitation or replacement.

3. **Climate Vulnerability**: Groundwater levels declining due to reduced rainfall, affecting 30% of water sources.

### Recommendations

1. Accelerate borehole rehabilitation program
2. Introduce rainwater harvesting at institutional level
3. Strengthen spare parts supply chain through local entrepreneurs`,
    actors: [],
    relationships: [],
    components: [],
    risks: []
  }
]

export function useMockSystems() {
  const systems = ref<MockSystem[]>(mockSystems)

  function getSystemBySlug(slug: string): MockSystem | undefined {
    return systems.value.find(s => s.slug === slug)
  }

  function getAllSystems(): MockSystem[] {
    return systems.value
  }

  return {
    systems,
    getSystemBySlug,
    getAllSystems
  }
}

export type { MockSystem, MockActor, MockRelationship, MockComponent, MockRisk }
