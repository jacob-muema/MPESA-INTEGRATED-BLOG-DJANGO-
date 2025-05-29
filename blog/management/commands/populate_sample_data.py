from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, UserProfile
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populate the blog with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create admin user if not exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@techpulse.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: admin/admin123')

        # Create sample authors
        authors_data = [
            {'username': 'david_park', 'first_name': 'David', 'last_name': 'Park', 'email': 'david@techpulse.com'},
            {'username': 'priya_sharma', 'first_name': 'Priya', 'last_name': 'Sharma', 'email': 'priya@techpulse.com'},
            {'username': 'alex_morgan', 'first_name': 'Alex', 'last_name': 'Morgan', 'email': 'alex@techpulse.com'},
            {'username': 'sarah_johnson', 'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah@techpulse.com'},
            {'username': 'michael_chen', 'first_name': 'Michael', 'last_name': 'Chen', 'email': 'michael@techpulse.com'},
        ]
        
        authors = []
        for author_data in authors_data:
            author, created = User.objects.get_or_create(
                username=author_data['username'],
                defaults=author_data
            )
            if created:
                author.set_password('password123')
                author.save()
            authors.append(author)

        # Create author profiles
        profiles_data = [
            {'user': authors[0], 'bio': 'Senior Technology Writer with 10+ years of experience covering emerging tech trends.', 'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face'},
            {'user': authors[1], 'bio': 'AI and Machine Learning specialist, passionate about ethical technology development.', 'avatar_url': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face'},
            {'user': authors[2], 'bio': 'Startup ecosystem expert and venture capital analyst covering climate tech innovations.', 'avatar_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face'},
            {'user': authors[3], 'bio': 'Metaverse and virtual reality researcher exploring the future of digital experiences.', 'avatar_url': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face'},
            {'user': authors[4], 'bio': 'Cybersecurity expert specializing in quantum encryption and digital privacy.', 'avatar_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face'},
        ]
        
        for profile_data in profiles_data:
            UserProfile.objects.get_or_create(
                user=profile_data['user'],
                defaults={
                    'bio': profile_data['bio'],
                    'avatar_url': profile_data['avatar_url']
                }
            )

        # Create categories
        categories_data = [
            {'name': 'Tech', 'color': '#3b82f6', 'description': 'Latest technology news and innovations'},
            {'name': 'AI', 'color': '#8b5cf6', 'description': 'Artificial Intelligence and Machine Learning'},
            {'name': 'Startups', 'color': '#10b981', 'description': 'Startup news and entrepreneurship'},
            {'name': 'Gadgets', 'color': '#f59e0b', 'description': 'Latest gadgets and consumer electronics'},
            {'name': 'Software', 'color': '#06b6d4', 'description': 'Software development and programming'},
            {'name': 'Security', 'color': '#ef4444', 'description': 'Cybersecurity and digital privacy'},
            {'name': 'Metaverse', 'color': '#ec4899', 'description': 'Virtual reality and metaverse technologies'},
            {'name': 'Reviews', 'color': '#64748b', 'description': 'Product reviews and comparisons'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category

        # Create tags
        tags_data = ['machine-learning', 'artificial-intelligence', 'blockchain', 'cryptocurrency', 'cloud-computing', 
                     'cybersecurity', 'mobile-apps', 'web-development', 'data-science', 'iot', 'quantum-computing',
                     'virtual-reality', 'augmented-reality', 'fintech', 'healthtech', 'edtech', 'climate-tech']
        
        tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags[tag_name] = tag

        # Create sample posts
        posts_data = [
            {
                'title': 'The Future of AI: How Machine Learning is Transforming Industries',
                'content': '''Artificial Intelligence is no longer science fiction. From healthcare to finance, AI is revolutionizing how businesses operate and how we live our daily lives.

Machine learning algorithms are now capable of diagnosing diseases with greater accuracy than human doctors, predicting market trends with unprecedented precision, and automating complex tasks that once required human intelligence.

The healthcare industry has seen remarkable advances with AI-powered diagnostic tools that can detect cancer in medical images, predict patient outcomes, and personalize treatment plans. In finance, algorithmic trading and fraud detection systems process millions of transactions in real-time.

However, with great power comes great responsibility. As AI becomes more prevalent, we must address concerns about job displacement, privacy, and the ethical implications of automated decision-making.

The future of AI lies not in replacing humans, but in augmenting human capabilities and solving complex global challenges like climate change, poverty, and disease.''',
                'excerpt': 'Artificial Intelligence is no longer science fiction. From healthcare to finance, AI is revolutionizing how businesses operate and how we live our daily lives.',
                'category': categories['AI'],
                'author': authors[1],
                'featured_image_url': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=400&fit=crop',
                'is_featured': True,
                'read_time': 8,
                'tags': ['artificial-intelligence', 'machine-learning', 'healthtech']
            },
            {
                'title': 'The Rise of Low-Code Development Platforms',
                'content': '''Low-code platforms are democratizing software development, allowing non-technical users to build applications. This shift is transforming how businesses approach digital transformation and internal tools.

These platforms provide visual interfaces and pre-built components that enable rapid application development without extensive coding knowledge. Companies are using low-code solutions to create customer portals, internal workflows, and data visualization dashboards.

The benefits include faster time-to-market, reduced development costs, and the ability to iterate quickly based on user feedback. However, concerns about scalability, security, and vendor lock-in remain valid considerations.

As the technology matures, we're seeing enterprise-grade low-code platforms that can handle complex business logic and integrate with existing systems. The future of software development may well be a hybrid approach combining traditional coding with low-code solutions.''',
                'excerpt': 'Low-code platforms are democratizing software development, allowing non-technical users to build applications. This shift is transforming how businesses approach digital transformation and internal tools.',
                'category': categories['Tech'],
                'author': authors[0],
                'featured_image_url': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=400&fit=crop',
                'read_time': 6,
                'tags': ['web-development', 'software']
            },
            {
                'title': 'AI Ethics Boards: Are They Actually Making a Difference?',
                'content': '''As AI becomes more integrated into critical systems, ethics boards have been established to guide development. We investigate whether these oversight bodies are effective or merely corporate window dressing.

Major tech companies have formed AI ethics committees to address bias, fairness, and transparency in their algorithms. These boards typically include ethicists, researchers, and community representatives who review AI projects and provide guidance.

However, critics argue that many ethics boards lack real authority and are primarily used for public relations purposes. Some high-profile resignations from these boards have highlighted tensions between ethical considerations and business objectives.

The challenge lies in translating ethical principles into practical guidelines that can be implemented by development teams. Effective AI ethics requires not just oversight, but also technical tools and processes that can detect and mitigate bias in real-time.

The future of AI ethics may depend on regulatory frameworks that give these boards more authority and establish industry-wide standards for responsible AI development.''',
                'excerpt': 'As AI becomes more integrated into critical systems, ethics boards have been established to guide development. We investigate whether these oversight bodies are effective or merely corporate window dressing.',
                'category': categories['AI'],
                'author': authors[1],
                'featured_image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=400&fit=crop',
                'read_time': 9,
                'tags': ['artificial-intelligence', 'ethics']
            },
            {
                'title': 'Climate Tech Startups Secure Record $40 Billion in Funding',
                'content': '''Venture capital is flowing into climate technology at unprecedented rates. From carbon capture to sustainable agriculture, we profile the hottest startups tackling the climate crisis.

The climate tech sector has attracted massive investment as investors recognize both the urgency of climate change and the enormous market opportunity. Startups are developing innovative solutions across energy storage, renewable energy, carbon capture, and sustainable materials.

Notable funding rounds include battery technology companies developing next-generation energy storage, vertical farming startups revolutionizing agriculture, and carbon capture technologies that can remove CO2 directly from the atmosphere.

The success of companies like Tesla has proven that sustainable technologies can be both profitable and scalable. This has encouraged more traditional investors to enter the climate tech space, bringing both capital and expertise.

However, the challenge remains in scaling these technologies quickly enough to make a meaningful impact on global emissions. The next decade will be critical in determining which climate tech solutions can achieve the scale needed to address the climate crisis.''',
                'excerpt': 'Venture capital is flowing into climate technology at unprecedented rates. From carbon capture to sustainable agriculture, we profile the hottest startups tackling the climate crisis.',
                'category': categories['Startups'],
                'author': authors[2],
                'featured_image_url': 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=800&h=400&fit=crop',
                'read_time': 7,
                'tags': ['climate-tech', 'startups', 'fintech']
            },
            {
                'title': 'The Metaverse Economy: Virtual Real Estate Boom Creates New Millionaires',
                'content': '''Virtual land sales are skyrocketing as major brands and investors rush to claim their space in the metaverse. We explore how this digital gold rush is creating a new class of digital property tycoons.

Platforms like Decentraland, The Sandbox, and Horizon Worlds have seen virtual real estate prices soar as companies purchase digital land for virtual stores, events, and experiences. Some virtual properties have sold for millions of dollars.

Major brands including Nike, Adidas, and Gucci have established virtual storefronts, while celebrities and influencers are hosting events in virtual spaces. This has created a new economy where digital architects, event planners, and virtual world developers are in high demand.

The speculation around virtual real estate mirrors historical real estate booms, with investors betting on future development and increased user adoption. However, questions remain about the long-term value and utility of virtual properties.

As the metaverse evolves, we may see new models of virtual property ownership and governance that differ significantly from traditional real estate markets.''',
                'excerpt': 'Virtual land sales are skyrocketing as major brands and investors rush to claim their space in the metaverse. We explore how this digital gold rush is creating a new class of digital property tycoons.',
                'category': categories['Metaverse'],
                'author': authors[3],
                'featured_image_url': 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&h=400&fit=crop',
                'read_time': 8,
                'tags': ['virtual-reality', 'blockchain', 'cryptocurrency']
            },
            {
                'title': 'Quantum Encryption: The Future of Cybersecurity',
                'content': '''As quantum computing advances, traditional encryption methods become vulnerable. Learn how quantum encryption is stepping in to protect our digital future.

Quantum computers pose a significant threat to current cryptographic systems, as they can potentially break RSA and other widely-used encryption algorithms. This has sparked a race to develop quantum-resistant security measures.

Quantum key distribution (QKD) offers a solution by using the principles of quantum mechanics to detect any attempt to intercept communications. This technology is already being deployed by governments and financial institutions for highly sensitive communications.

The challenge lies in scaling quantum encryption for widespread use. Current quantum communication systems require specialized hardware and are limited by distance, making them impractical for many applications.

Researchers are working on quantum repeaters and satellite-based quantum communication to overcome these limitations. The goal is to create a global quantum internet that provides unbreakable security for all digital communications.''',
                'excerpt': 'As quantum computing advances, traditional encryption methods become vulnerable. Learn how quantum encryption is stepping in to protect our digital future.',
                'category': categories['Security'],
                'author': authors[4],
                'featured_image_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=400&fit=crop',
                'read_time': 7,
                'tags': ['quantum-computing', 'cybersecurity']
            },
            {
                'title': 'Smart Home Revolution: IoT Devices That Actually Make Life Easier',
                'content': '''The smart home market is flooded with gadgets, but which ones deliver real value? We review the latest IoT devices that are genuinely improving daily life.

Smart home technology has evolved from novelty gadgets to practical solutions that enhance comfort, security, and energy efficiency. The key is choosing devices that integrate well and provide measurable benefits.

Smart thermostats like Nest and Ecobee can reduce energy bills by 10-15% through intelligent scheduling and learning user preferences. Smart security systems provide peace of mind with real-time monitoring and alerts.

Voice assistants have become central hubs for controlling multiple devices, while smart lighting systems can improve sleep quality and reduce energy consumption. The latest smart appliances can even order groceries when supplies run low.

However, privacy and security concerns remain significant challenges. Many IoT devices have poor security implementations, making them vulnerable to hacking and data breaches.

The future of smart homes lies in better integration, improved security standards, and AI that can truly understand and anticipate user needs.''',
                'excerpt': 'The smart home market is flooded with gadgets, but which ones deliver real value? We review the latest IoT devices that are genuinely improving daily life.',
                'category': categories['Gadgets'],
                'author': authors[0],
                'featured_image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=400&fit=crop',
                'read_time': 6,
                'tags': ['iot', 'smart-home', 'gadgets']
            },
            {
                'title': 'The Rise of No-Code: Democratizing App Development',
                'content': '''No-code platforms are empowering non-programmers to build sophisticated applications. This movement is reshaping the software industry and creating new opportunities for innovation.

Traditional software development requires years of training and technical expertise. No-code platforms eliminate this barrier by providing visual interfaces and pre-built components that anyone can use to create applications.

Platforms like Bubble, Webflow, and Airtable have enabled entrepreneurs, designers, and business professionals to build everything from simple websites to complex business applications without writing a single line of code.

The benefits extend beyond individual empowerment. Companies are using no-code tools to rapidly prototype ideas, automate workflows, and create internal tools without relying on overloaded development teams.

However, no-code solutions have limitations in terms of customization, performance, and scalability. They work best for specific use cases and may not be suitable for complex enterprise applications.

The future likely involves a hybrid approach where no-code tools handle routine development tasks while traditional coding focuses on complex, custom solutions.''',
                'excerpt': 'No-code platforms are empowering non-programmers to build sophisticated applications. This movement is reshaping the software industry and creating new opportunities for innovation.',
                'category': categories['Software'],
                'author': authors[0],
                'featured_image_url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop',
                'read_time': 5,
                'tags': ['web-development', 'software', 'no-code']
            }
        ]

        # Create posts
        for i, post_data in enumerate(posts_data):
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'content': post_data['content'],
                    'excerpt': post_data['excerpt'],
                    'category': post_data['category'],
                    'author': post_data['author'],
                    'featured_image_url': post_data['featured_image_url'],
                    'status': 'published',
                    'is_featured': post_data.get('is_featured', False),
                    'read_time': post_data['read_time'],
                    'views': random.randint(100, 5000),
                    'published_at': timezone.now()
                }
            )
            
            if created:
                # Add tags
                for tag_name in post_data['tags']:
                    if tag_name in tags:
                        post.tags.add(tags[tag_name])
                
                self.stdout.write(f'Created post: {post.title}')

        # Create some breaking news
        breaking_posts = Post.objects.filter(status='published')[:2]
        for post in breaking_posts:
            post.is_breaking = True
            post.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))
        self.stdout.write(f'Created {Post.objects.count()} posts')
        self.stdout.write(f'Created {Category.objects.count()} categories')
        self.stdout.write(f'Created {Tag.objects.count()} tags')
        self.stdout.write(f'Created {User.objects.count()} users')
