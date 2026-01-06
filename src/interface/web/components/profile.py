from fasthtml.common import (Div, H1, A, H2, P, H3, Span, Ul, Li)   


def ProfileView():
    return Div(cls="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900")(
        hero_section(),
        about_section(),
        work_experience_section()
    )

def hero_section():
    """Hero section with name, title, and CTA buttons"""
    return Div(cls="flex flex-col items-center justify-center min-h-screen text-center px-4")(
        # Brain Icon
        Div(cls="mb-8")(
            Div(cls="w-32 h-32 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-2xl text-6xl")(
                "🧠"
            )
        ),
        
        # Name
        H1(cls="text-6xl font-bold text-white mb-4")("Kurnia Zulda Matondang"),
        
        # Title
        H2(cls="text-3xl text-blue-400 mb-6")("AI Engineer & Machine Learning Specialist"),
        
        # Description
        P(cls="text-gray-300 text-lg max-w-3xl mb-8")(
            "Passionate about building intelligent systems that solve real-world problems. ",
            "Specializing in computer vision, natural language processing, and deep learning."
        ),
        
        # Buttons
        Div(cls="flex gap-4 mb-8")(
            A(href="#contact", cls="btn btn-primary btn-lg")("Get in Touch"),
            A(href="#projects", cls="btn btn-outline btn-lg")("View Projects")
        ),
        
        # Social Links
        social_links()
    )

def social_links():
    """Social media links with icons"""
    return Div(cls="flex gap-6 text-gray-400 text-3xl")(
        A(href="#", cls="hover:text-blue-400 transition")("🔗"),
        A(href="#", cls="hover:text-blue-400 transition")("💼"),
        A(href="#", cls="hover:text-blue-400 transition")("✉️")
    )

def info_card(icon, title, description, border_color="blue"):
    """Reusable info card component
    
    Args:
        icon: Emoji icon
        title: Card title
        description: Card description
        border_color: Hover border color (blue, purple, green)
    """
    return Div(cls=f"bg-slate-800 rounded-xl p-6 border border-slate-700 hover:border-{border_color}-500 transition")(
        Div(cls="flex items-start gap-4")(
            Div(cls=f"w-12 h-12 rounded-lg bg-{border_color}-500 flex items-center justify-center flex-shrink-0 text-2xl")(
                icon
            ),
            Div()(
                H3(cls="text-xl font-bold text-white mb-2")(title),
                P(cls="text-gray-400")(description)
            )
        )
    )

def about_description():
    """About me description text"""
    return Div(cls="space-y-6 text-gray-300")(
        P(cls="text-lg leading-relaxed")(
            "As an AI Engineer with a passion for innovation, I specialize in developing cutting-edge machine learning solutions that bridge the gap between research and real-world applications."
        ),
        P(cls="text-lg leading-relaxed")(
            "My expertise spans across computer vision, natural language processing, and deep learning, with a focus on creating scalable and efficient AI systems."
        ),
        P(cls="text-lg leading-relaxed")(
            "I believe in continuous learning and staying at the forefront of AI technology to deliver solutions that make a meaningful impact."
        )
    )

def about_info_cards():
    """Info cards for education, experience, and achievements"""
    return Div(cls="space-y-6")(
        info_card(
            "🎓",
            "Education",
            "Advanced degree in Computer Science with focus on Artificial Intelligence and Machine Learning",
            "blue"
        ),
        info_card(
            "💼",
            "Experience",
            "5+ years of experience in developing and deploying AI models in production environments",
            "purple"
        ),
        info_card(
            "🏆",
            "Achievements",
            "Published research papers and contributed to open-source AI projects",
            "green"
        )
    )

def about_section():
    """Complete about section with description and info cards"""
    return Div(cls="container mx-auto px-4 py-20")(
        H2(cls="text-5xl font-bold text-white text-center mb-16")("About Me"),
        
        Div(cls="grid grid-cols-1 lg:grid-cols-2 gap-8")(
            about_description(),
            about_info_cards()
        )
    )

def achievement_item(text):
    """Single achievement list item"""
    return Li(cls="flex items-start gap-3 text-gray-300")(
        Span(cls="text-blue-500 font-bold")("•"),
        text
    )

def experience_card(title, company, company_url, date_range, description, achievements):
    """Reusable experience card component
    
    Args:
        title: Job title
        company: Company name
        company_url: Company website URL
        date_range: Employment period
        description: Job description
        achievements: List of achievement strings
    """
    return Div(cls="bg-slate-800 rounded-xl p-8 border border-slate-700 hover:border-blue-500 transition")(
        # Header
        Div(cls="flex flex-col md:flex-row md:items-center md:justify-between mb-6")(
            Div()(
                H3(cls="text-2xl font-bold text-white mb-2")(title),
                A(href=company_url, cls="text-blue-400 hover:text-blue-300 flex items-center gap-2")(
                    Span(cls="text-lg")("🏢"),
                    company
                )
            ),
            Div(cls="text-gray-400 flex items-center gap-2 mt-2 md:mt-0")(
                Span(cls="text-lg")("📅"),
                date_range
            )
        ),
        
        # Description
        P(cls="text-gray-300 mb-6 leading-relaxed")(description),
        
        # Achievements
        Div(cls="space-y-3")(
            P(cls="text-white font-semibold mb-3")("Key Achievements:"),
            Ul(cls="space-y-3 list-none")(
                *[achievement_item(achievement) for achievement in achievements]
            )
        )
    )

def work_experience_section():
    """Complete work experience section"""
    # Define achievements list
    achievements = [
        "Developed and deployed 15+ production AI models serving 1M+ users",
        "Reduced model inference time by 60% through optimization techniques",
        "Led a team of 5 ML engineers on critical AI projects"
    ]
    
    return Div(cls="container mx-auto px-4 py-20")(
        H2(cls="text-5xl font-bold text-white text-center mb-16")("Work Experience"),
        
        Div(cls="max-w-4xl mx-auto")(
            experience_card(
                title="Senior AI Engineer",
                company="Tech Innovations Inc.",
                company_url="#",
                date_range="2023 - Present",
                description="Leading AI research and development initiatives, focusing on computer vision and deep learning solutions for enterprise clients.",
                achievements=achievements
            )
        )
    )