"""
Management command to seed the database with demo data.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import System, Risk, Actor, Relationship


class Command(BaseCommand):
    help = 'Seeds the database with demo system data'

    def handle(self, *args, **options):
        self.stdout.write('='*60)
        self.stdout.write('SEED_DATA: Starting database seeding...')
        self.stdout.write('='*60)

        # Create RMNCAH System
        system, created = System.objects.update_or_create(
            slug='rmncah-eastern-ethiopia',
            defaults={
                'name': 'RMNCAH Health System - Eastern Ethiopia',
                'description': 'Reproductive, Maternal, Newborn, Child and Adolescent Health system serving rural communities in Eastern Ethiopia. This system supports approximately 2.3 million people across 12 woredas.',
                'region': 'Eastern Region',
                'country': 'Ethiopia',
                'sector': 'health',
                'subsector': 'RMNCAH',
                'assessment_date': '2024-03-15',
                'version': '2.1',
            }
        )
        self.stdout.write(f"  {'Created' if created else 'Updated'} system: {system.name}")

        # Create actors with enhanced metadata for R4S visualization
        # admin_level: federal, regional, zonal, woreda, kebele, community
        # service_type: curative, preventive, both
        # support_category: leadership, information, service_delivery, financing, supply, human_resources
        actors_data = [
            # SERVICE USERS (rightmost in visualization)
            {
                'slug': 'families',
                'name': 'Families',
                'actor_type': 'service_user',
                'function': 'Households seeking health services for family members',
                'needs': 'Access to affordable quality healthcare',
                'worries': 'Cost, distance, quality of care',
                'metadata': {'admin_level': 'community', 'service_type': 'both'},
            },
            {
                'slug': 'pregnant-women-mothers',
                'name': 'Pregnant Women & Mothers',
                'actor_type': 'service_user',
                'function': 'Primary beneficiaries requiring antenatal care, delivery services, and postnatal care',
                'needs': 'Access to quality maternal health services',
                'worries': 'Distance to health facilities, cost of care',
                'metadata': {'admin_level': 'community', 'service_type': 'both'},
            },
            {
                'slug': 'children-under-5',
                'name': 'Children Under 5',
                'actor_type': 'service_user',
                'function': 'Recipients of immunization, nutrition services, and treatment for common childhood illnesses',
                'needs': 'Immunization, nutrition support, treatment for illnesses',
                'worries': 'Malnutrition, preventable diseases',
                'metadata': {'admin_level': 'community', 'service_type': 'both'},
            },
            # SERVICE PROVIDERS - FEDERAL LEVEL
            {
                'slug': 'federal-ministry-health',
                'name': 'Federal Ministry of Health',
                'actor_type': 'service_provider',
                'function': 'National health policy, standards, and strategic direction',
                'needs': 'Budget, qualified staff, partner coordination',
                'worries': 'Funding gaps, policy implementation',
                'metadata': {'admin_level': 'federal', 'service_type': 'both'},
            },
            # SERVICE PROVIDERS - REGIONAL LEVEL
            {
                'slug': 'regional-hospital',
                'name': 'Regional Hospital',
                'actor_type': 'service_provider',
                'function': 'Tertiary care facility for complex referrals and specialized services',
                'needs': 'Specialists, equipment, referral system',
                'worries': 'Overcrowding, specialist retention',
                'metadata': {'admin_level': 'regional', 'service_type': 'curative'},
            },
            # SERVICE PROVIDERS - ZONAL LEVEL
            {
                'slug': 'zonal-hospital',
                'name': 'Zonal Hospital',
                'actor_type': 'service_provider',
                'function': 'Secondary care facility for referrals requiring advanced medical interventions',
                'needs': 'Specialists, equipment, supplies, referral system',
                'worries': 'Overcrowding, equipment failure, staff retention',
                'metadata': {'admin_level': 'zonal', 'service_type': 'curative'},
            },
            {
                'slug': 'zonal-health-department',
                'name': 'Zonal Health Department',
                'actor_type': 'service_provider',
                'function': 'Coordinates health services across woredas in the zone',
                'needs': 'Budget, data, coordination capacity',
                'worries': 'Resource allocation, reporting quality',
                'metadata': {'admin_level': 'zonal', 'service_type': 'both'},
            },
            # SERVICE PROVIDERS - WOREDA LEVEL
            {
                'slug': 'health-centers',
                'name': 'Health Centers',
                'actor_type': 'service_provider',
                'function': 'Provide comprehensive primary healthcare including maternal and child health services',
                'needs': 'Supplies, trained staff, infrastructure',
                'worries': 'Stock-outs, staff shortages, equipment failure',
                'metadata': {'admin_level': 'woreda', 'service_type': 'curative'},
            },
            {
                'slug': 'private-clinics',
                'name': 'Private Clinics',
                'actor_type': 'service_provider',
                'function': 'Private sector primary care facilities',
                'needs': 'Licenses, supplies, patients',
                'worries': 'Regulation, competition',
                'metadata': {'admin_level': 'woreda', 'service_type': 'curative'},
            },
            {
                'slug': 'private-pharmacies',
                'name': 'Private Pharmacies',
                'actor_type': 'service_provider',
                'function': 'Commercial outlets providing medications and basic health products',
                'needs': 'Supply chain, licenses, customers',
                'worries': 'Competition, regulation, stock-outs',
                'metadata': {'admin_level': 'woreda', 'service_type': 'curative'},
            },
            # SERVICE PROVIDERS - KEBELE LEVEL
            {
                'slug': 'health-posts',
                'name': 'Health Posts',
                'actor_type': 'service_provider',
                'function': 'Community-level health facility staffed by Health Extension Workers',
                'needs': 'Supplies, supervision, referral pathway',
                'worries': 'Stock-outs, workload, transportation',
                'metadata': {'admin_level': 'kebele', 'service_type': 'preventive'},
            },
            {
                'slug': 'health-extension-workers',
                'name': 'Health Extension Workers',
                'actor_type': 'service_provider',
                'function': 'Community-based health workers providing preventive care and health education',
                'needs': 'Training, supplies, supervision',
                'worries': 'Workload, lack of supplies, transportation',
                'metadata': {'admin_level': 'kebele', 'service_type': 'preventive'},
            },
            {
                'slug': 'traditional-birth-attendants',
                'name': 'Traditional Birth Attendants',
                'actor_type': 'service_provider',
                'function': 'Community members assisting with home deliveries and maternal care referrals',
                'needs': 'Training on referral, basic supplies',
                'worries': 'Complications during delivery',
                'metadata': {'admin_level': 'kebele', 'service_type': 'preventive'},
            },
            {
                'slug': 'community-health-volunteers',
                'name': 'Community Health Volunteers',
                'actor_type': 'service_provider',
                'function': 'Volunteer health promoters conducting outreach and education',
                'needs': 'Training, materials, recognition',
                'worries': 'Motivation, workload',
                'metadata': {'admin_level': 'kebele', 'service_type': 'preventive'},
            },
            # REGULATORY ACTORS
            {
                'slug': 'woreda-health-office',
                'name': 'Woreda Health Office',
                'actor_type': 'regulatory',
                'function': 'Local government authority responsible for health service coordination and oversight',
                'needs': 'Budget, qualified staff, data for planning',
                'worries': 'Inadequate funding, coordination challenges',
                'metadata': {'admin_level': 'woreda', 'regulatory_category': 'leadership'},
            },
            {
                'slug': 'regional-health-bureau',
                'name': 'Regional Health Bureau',
                'actor_type': 'regulatory',
                'function': 'Regional authority managing health policy, budgets, and pharmaceutical supply',
                'needs': 'Federal support, accurate data, partner coordination',
                'worries': 'Supply chain disruptions, budget constraints',
                'metadata': {'admin_level': 'regional', 'regulatory_category': 'leadership'},
            },
            {
                'slug': 'food-drug-authority',
                'name': 'Food & Drug Authority',
                'actor_type': 'regulatory',
                'function': 'Regulates quality and safety of pharmaceuticals and medical supplies',
                'needs': 'Inspection capacity, laboratory facilities',
                'worries': 'Counterfeit drugs, quality assurance',
                'metadata': {'admin_level': 'federal', 'regulatory_category': 'supply'},
            },
            # SUPPORT ACTORS
            {
                'slug': 'goal-ethiopia',
                'name': 'GOAL Ethiopia',
                'actor_type': 'support',
                'function': 'International NGO providing technical support, training, and supplementary supplies',
                'needs': 'Donor funding, government partnership, community access',
                'worries': 'Funding uncertainty, access constraints',
                'metadata': {'support_category': 'service_delivery'},
            },
            {
                'slug': 'unicef',
                'name': 'UNICEF',
                'actor_type': 'support',
                'function': 'UN agency providing vaccines, nutrition supplies, and technical assistance',
                'needs': 'Government cooperation, funding, logistics capacity',
                'worries': 'Cold chain failures, access issues',
                'metadata': {'support_category': 'supply'},
            },
            {
                'slug': 'who',
                'name': 'WHO',
                'actor_type': 'support',
                'function': 'Technical guidance, disease surveillance, and emergency response coordination',
                'needs': 'Government cooperation, data sharing',
                'worries': 'Outbreak response capacity',
                'metadata': {'support_category': 'information'},
            },
            {
                'slug': 'community-leaders',
                'name': 'Community Leaders',
                'actor_type': 'support',
                'function': 'Traditional and religious leaders who influence health-seeking behaviors',
                'needs': 'Information, recognition, engagement',
                'worries': 'Erosion of traditional authority',
                'metadata': {'support_category': 'leadership'},
            },
            {
                'slug': 'health-financing-agency',
                'name': 'Health Insurance Agency',
                'actor_type': 'support',
                'function': 'Manages community-based health insurance schemes',
                'needs': 'Enrollment, premium collection, claims processing',
                'worries': 'Coverage gaps, sustainability',
                'metadata': {'support_category': 'financing'},
            },
            {
                'slug': 'medical-supply-agency',
                'name': 'EPSA (Medical Supply Agency)',
                'actor_type': 'support',
                'function': 'National pharmaceutical procurement and distribution agency',
                'needs': 'Funding, logistics, forecasting data',
                'worries': 'Stock-outs, expiry, distribution',
                'metadata': {'support_category': 'supply'},
            },
            {
                'slug': 'training-institutions',
                'name': 'Health Training Institutions',
                'actor_type': 'support',
                'function': 'Medical schools, nursing colleges, and HEW training centers',
                'needs': 'Funding, faculty, clinical placement sites',
                'worries': 'Quality, retention of graduates',
                'metadata': {'support_category': 'human_resources'},
            },
        ]

        actor_objects = {}
        for actor_data in actors_data:
            actor, created = Actor.objects.update_or_create(
                system=system,
                slug=actor_data['slug'],
                defaults=actor_data
            )
            actor_objects[actor_data['slug']] = actor
            self.stdout.write(f"    {'Created' if created else 'Updated'} actor: {actor.name}")

        # Create relationships with enhanced service flow data
        relationships_data = [
            # Service User → Service Provider (Patient Flow)
            {
                'from_slug': 'families',
                'to_slug': 'health-posts',
                'goods_services': 'Primary care seeking, health education',
                'quality': 'good',
            },
            {
                'from_slug': 'families',
                'to_slug': 'health-centers',
                'goods_services': 'Curative care, maternal services',
                'quality': 'stressed',
            },
            {
                'from_slug': 'pregnant-women-mothers',
                'to_slug': 'health-centers',
                'goods_services': 'Antenatal care, delivery services',
                'quality': 'stressed',
            },
            {
                'from_slug': 'pregnant-women-mothers',
                'to_slug': 'health-extension-workers',
                'goods_services': 'Health education, referrals',
                'quality': 'good',
            },
            {
                'from_slug': 'children-under-5',
                'to_slug': 'health-centers',
                'goods_services': 'Immunization, treatment',
                'quality': 'good',
            },
            {
                'from_slug': 'children-under-5',
                'to_slug': 'health-posts',
                'goods_services': 'Growth monitoring, immunization',
                'quality': 'good',
            },
            # Referral Pathways (Curative)
            {
                'from_slug': 'health-posts',
                'to_slug': 'health-centers',
                'goods_services': 'Patient referrals',
                'quality': 'good',
            },
            {
                'from_slug': 'health-centers',
                'to_slug': 'zonal-hospital',
                'goods_services': 'Emergency referrals, complicated cases',
                'quality': 'stressed',
            },
            {
                'from_slug': 'zonal-hospital',
                'to_slug': 'regional-hospital',
                'goods_services': 'Tertiary referrals',
                'quality': 'stressed',
            },
            {
                'from_slug': 'traditional-birth-attendants',
                'to_slug': 'health-centers',
                'goods_services': 'Emergency referrals',
                'quality': 'bad',
            },
            {
                'from_slug': 'private-clinics',
                'to_slug': 'health-centers',
                'goods_services': 'Patient referrals',
                'quality': 'absent',
            },
            # Supply Chain
            {
                'from_slug': 'medical-supply-agency',
                'to_slug': 'regional-health-bureau',
                'goods_services': 'Drug supply, medical equipment',
                'quality': 'stressed',
            },
            {
                'from_slug': 'regional-health-bureau',
                'to_slug': 'zonal-health-department',
                'goods_services': 'Supplies, guidelines, budget',
                'quality': 'stressed',
            },
            {
                'from_slug': 'zonal-health-department',
                'to_slug': 'health-centers',
                'goods_services': 'Supplies, supervision',
                'quality': 'stressed',
            },
            {
                'from_slug': 'health-centers',
                'to_slug': 'health-posts',
                'goods_services': 'Supplies, supervision',
                'quality': 'good',
            },
            {
                'from_slug': 'unicef',
                'to_slug': 'regional-health-bureau',
                'goods_services': 'Vaccines, cold chain equipment',
                'quality': 'good',
            },
            # Technical Support & Training
            {
                'from_slug': 'goal-ethiopia',
                'to_slug': 'health-extension-workers',
                'goods_services': 'Training, mentorship, supplies',
                'quality': 'good',
            },
            {
                'from_slug': 'who',
                'to_slug': 'federal-ministry-health',
                'goods_services': 'Technical guidance, surveillance support',
                'quality': 'good',
            },
            {
                'from_slug': 'training-institutions',
                'to_slug': 'health-centers',
                'goods_services': 'Trained health workers',
                'quality': 'stressed',
            },
            # Regulatory & Oversight
            {
                'from_slug': 'woreda-health-office',
                'to_slug': 'health-centers',
                'goods_services': 'Coordination, monitoring, supervision',
                'quality': 'stressed',
            },
            {
                'from_slug': 'woreda-health-office',
                'to_slug': 'health-posts',
                'goods_services': 'Supervision, reporting',
                'quality': 'good',
            },
            {
                'from_slug': 'food-drug-authority',
                'to_slug': 'private-pharmacies',
                'goods_services': 'Licensing, inspection',
                'quality': 'stressed',
            },
            # Financing
            {
                'from_slug': 'health-financing-agency',
                'to_slug': 'health-centers',
                'goods_services': 'Insurance reimbursements',
                'quality': 'stressed',
            },
            {
                'from_slug': 'health-financing-agency',
                'to_slug': 'families',
                'goods_services': 'Insurance coverage, cost protection',
                'quality': 'bad',
            },
            # Community Engagement
            {
                'from_slug': 'community-leaders',
                'to_slug': 'families',
                'goods_services': 'Social influence, mobilization',
                'quality': 'good',
            },
            {
                'from_slug': 'community-health-volunteers',
                'to_slug': 'families',
                'goods_services': 'Health education, home visits',
                'quality': 'good',
            },
            {
                'from_slug': 'health-extension-workers',
                'to_slug': 'community-health-volunteers',
                'goods_services': 'Training, coordination',
                'quality': 'good',
            },
        ]

        for rel_data in relationships_data:
            from_actor = actor_objects.get(rel_data['from_slug'])
            to_actor = actor_objects.get(rel_data['to_slug'])
            if from_actor and to_actor:
                rel, created = Relationship.objects.update_or_create(
                    system=system,
                    from_actor=from_actor,
                    to_actor=to_actor,
                    defaults={
                        'goods_services': rel_data['goods_services'],
                        'quality': rel_data['quality'],
                    }
                )
                self.stdout.write(f"    {'Created' if created else 'Updated'} relationship: {from_actor.name} -> {to_actor.name}")

        # Create risks
        risks_data = [
            {
                'slug': 'drought-food-insecurity',
                'name': 'Drought & Food Insecurity',
                'category': 'climate',
                'likelihood': 'likely',
                'description': 'Recurring droughts leading to malnutrition, population displacement, and increased demand for health services',
            },
            {
                'slug': 'supply-chain-disruption',
                'name': 'Supply Chain Disruption',
                'category': 'economic',
                'likelihood': 'possible',
                'description': 'Disruption to pharmaceutical and medical supply chains due to funding gaps or logistics challenges',
            },
            {
                'slug': 'staff-turnover',
                'name': 'Staff Turnover',
                'category': 'economic',
                'likelihood': 'likely',
                'description': 'Loss of trained health workers to urban areas or better-paying positions',
            },
            {
                'slug': 'disease-outbreak',
                'name': 'Disease Outbreak',
                'category': 'health',
                'likelihood': 'possible',
                'description': 'Outbreak of infectious diseases such as cholera, measles, or respiratory infections',
            },
            {
                'slug': 'funding-reduction',
                'name': 'Funding Reduction',
                'category': 'political',
                'likelihood': 'possible',
                'description': 'Reduction in government or donor funding for health programs',
            },
        ]

        for risk_data in risks_data:
            risk, created = Risk.objects.update_or_create(
                system=system,
                slug=risk_data['slug'],
                defaults=risk_data
            )
            self.stdout.write(f"    {'Created' if created else 'Updated'} risk: {risk.name}")

        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('SEED_DATA: Successfully seeded database!'))
        self.stdout.write(f'SEED_DATA: Created system slug: {system.slug}')
        self.stdout.write('='*60)
