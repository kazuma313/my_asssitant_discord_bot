from fasthtml.common import (Div, H1, H2, P, H3, Span, Strong, Img, Video)   

def ComputerVisionView():
    return Div(cls="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900")(
        cv_hero_section_1(),  # Worker Activity Recognition
        cv_hero_section_2(),  # PPE Compliance Detection
        cv_hero_section_3(),  # Automated Quality Inspection
        cv_use_cases_section()
    )


def cv_showcase_item(title, description, media_type="image", media_url=None, technologies=None):
    """Reusable showcase item for computer vision projects
    
    Args:
        title: Project title
        description: Project description
        media_type: "image" or "video"
        media_url: URL to the media file (optional)
        technologies: List of technologies used (optional)
    """
    return Div(cls="bg-slate-800 rounded-xl overflow-hidden border border-slate-700 hover:border-blue-500 transition")(
        # Media Container
        Div(cls="relative bg-slate-900 aspect-video flex items-center justify-center")(
            # If media_url is provided, use it, otherwise show placeholder
            Img(src=media_url, alt=title, cls="w-full h-full object-cover") if media_url and media_type == "image"
            else Video(src=media_url, controls=True, cls="w-full h-full") if media_url and media_type == "video"
            else Div(cls="text-center p-8")(
                Div(cls="text-5xl mb-4")("🎬" if media_type == "video" else "📸"),
                P(cls="text-gray-500")(f"{media_type.title()} Preview")
            )
        ),
        
        # Content
        Div(cls="p-6 space-y-4")(
            H3(cls="text-2xl font-bold text-white")(title),
            P(cls="text-gray-300 leading-relaxed")(description),
            
            # Technologies badges
            Div(cls="flex flex-wrap gap-2")(
                *[tech_badge(tech) for tech in (technologies or [])]
            ) if technologies else None
        )
    )

def tech_badge(tech):
    """Technology badge"""
    return Span(cls="badge badge-outline badge-primary")(tech)

def cv_showcase_section():
    """Showcase section with project examples"""
    
    # Sample projects - replace with actual data
    projects = [
        {
            "title": "Worker Activity Recognition",
            "description": "Real-time detection and tracking of worker activities in manufacturing environments. Monitors safety compliance and productivity metrics using pose estimation and action recognition.",
            "media_type": "video",
            "media_url": None,  # Add your video URL here
            "technologies": ["YOLO", "OpenPose", "PyTorch", "OpenCV"]
        },
        {
            "title": "Abnormal Behavior Detection",
            "description": "Automated system for detecting unusual patterns and behaviors in surveillance footage. Uses temporal analysis and anomaly detection algorithms to identify potential safety hazards.",
            "media_type": "video",
            "media_url": None,  # Add your video URL here
            "technologies": ["3D CNN", "LSTM", "TensorFlow", "Scikit-learn"]
        },
        {
            "title": "Visual Quality Inspection",
            "description": "Automated defect detection system for manufacturing quality control. Identifies surface defects, dimensional inconsistencies, and assembly errors with high precision.",
            "media_type": "image",
            "media_url": None,  # Add your image URL here
            "technologies": ["ResNet", "Faster R-CNN", "Keras", "OpenCV"]
        },
        {
            "title": "PPE Compliance Detection",
            "description": "Safety monitoring system that verifies personal protective equipment usage in real-time. Detects helmets, vests, gloves, and other safety gear to ensure workplace compliance.",
            "media_type": "video",
            "media_url": None,  # Add your video URL here
            "technologies": ["YOLO v8", "DeepSORT", "PyTorch", "FastAPI"]
        }
    ]
    
    return Div(cls="container mx-auto px-8 py-20")(
        H2(cls="text-5xl font-bold text-white text-center mb-16")("Project Showcase"),
        
        # Grid of showcase items
        Div(cls="grid grid-cols-1 md:grid-cols-2 gap-8")(
            *[cv_showcase_item(**project) for project in projects]
        )
    )


def cv_hero_section_1():
    """Example 1: Worker Activity Recognition"""
    return Div(cls="container mx-auto px-8 py-20")(
        Div(cls="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start")(
            # Left side - Text content
            Div(cls="space-y-8")(
                H1(cls="text-5xl lg:text-6xl font-bold text-white leading-tight")(
                    "Worker Activity Recognition"
                ),
                
                P(cls="text-xl text-gray-300 leading-relaxed")(
                    "Real-time monitoring and analysis of worker activities in industrial environments. Track movements, identify tasks, ensure safety compliance, and optimize workflow efficiency using advanced pose estimation and action recognition."
                ),
                
                # Use Cases Section
                Div(cls="space-y-4 pt-4")(
                    H3(cls="text-2xl font-bold text-white")("USE CASES"),
                    
                    Div(cls="flex flex-wrap gap-3")(
                        use_case_badge("Track employee productivity and task completion"),
                        use_case_badge("Monitor ergonomic postures and prevent injuries"),
                        use_case_badge("Detect unauthorized access to restricted areas"),
                        use_case_badge("Analyze workflow bottlenecks and optimize processes")
                    )
                ),
                
                # Ideal For Section
                Div(cls="pt-6")(
                    P(cls="text-lg text-gray-400")(
                        Strong(cls="text-white")("IDEAL FOR: "),
                        "Manufacturing Plants, Warehouses, Assembly Lines"
                    )
                )
            ),
            
            # Right side - Featured video/image
            Div(cls="lg:sticky lg:top-8")(
                Div(cls="bg-slate-800 rounded-2xl overflow-hidden border-2 border-blue-500 shadow-2xl aspect-video flex items-center justify-center")(
                    Div(cls="text-center p-12")(
                        Div(cls="text-7xl mb-4")("👷"),
                        P(cls="text-gray-400 text-xl")("Worker Activity Demo")
                    )
                )
            )
        )
    )

def cv_hero_section_2():
    """Example 2: PPE Compliance Detection"""
    return Div(cls="container mx-auto px-8 py-20")(
        Div(cls="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start")(
            # Left side - Text content
            Div(cls="space-y-8")(
                H1(cls="text-5xl lg:text-6xl font-bold text-white leading-tight")(
                    "PPE Compliance Detection"
                ),
                
                P(cls="text-xl text-gray-300 leading-relaxed")(
                    "Automated safety monitoring system that verifies personal protective equipment compliance in real-time. Detect helmets, safety vests, gloves, masks, and other required safety gear to ensure workplace safety standards are met."
                ),
                
                # Use Cases Section
                Div(cls="space-y-4 pt-4")(
                    H3(cls="text-2xl font-bold text-white")("USE CASES"),
                    
                    Div(cls="flex flex-wrap gap-3")(
                        use_case_badge("Verify hard hat and safety helmet usage"),
                        use_case_badge("Detect missing high-visibility vests"),
                        use_case_badge("Monitor proper mask and glove compliance"),
                        use_case_badge("Generate automated safety violation alerts")
                    )
                ),
                
                # Ideal For Section
                Div(cls="pt-6")(
                    P(cls="text-lg text-gray-400")(
                        Strong(cls="text-white")("IDEAL FOR: "),
                        "Construction Sites, Oil & Gas, Mining Operations"
                    )
                )
            ),
            
            # Right side - Featured video/image
            Div(cls="lg:sticky lg:top-8")(
                Div(cls="bg-slate-800 rounded-2xl overflow-hidden border-2 border-green-500 shadow-2xl aspect-video flex items-center justify-center")(
                    Div(cls="text-center p-12")(
                        Div(cls="text-7xl mb-4")("🦺"),
                        P(cls="text-gray-400 text-xl")("PPE Detection Demo")
                    )
                )
            )
        )
    )

def cv_hero_section_3():
    """Example 3: Visual Quality Inspection"""
    return Div(cls="container mx-auto px-8 py-20")(
        Div(cls="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start")(
            # Left side - Text content
            Div(cls="space-y-8")(
                H1(cls="text-5xl lg:text-6xl font-bold text-white leading-tight")(
                    "Automated Quality Inspection"
                ),
                
                P(cls="text-xl text-gray-300 leading-relaxed")(
                    "AI-powered visual inspection system for manufacturing quality control. Identify defects, scratches, dimensional errors, and assembly mistakes with precision that exceeds human inspection capabilities. Reduce costs and improve product consistency."
                ),
                
                # Use Cases Section
                Div(cls="space-y-4 pt-4")(
                    H3(cls="text-2xl font-bold text-white")("USE CASES"),
                    
                    Div(cls="flex flex-wrap gap-3")(
                        use_case_badge("Detect surface defects and scratches"),
                        use_case_badge("Verify dimensional accuracy and alignment"),
                        use_case_badge("Identify missing components in assemblies"),
                        use_case_badge("Classify product quality grades automatically")
                    )
                ),
                
                # Ideal For Section
                Div(cls="pt-6")(
                    P(cls="text-lg text-gray-400")(
                        Strong(cls="text-white")("IDEAL FOR: "),
                        "Electronics Assembly, Automotive Parts, Food & Beverage"
                    )
                )
            ),
            
            # Right side - Featured video/image
            Div(cls="lg:sticky lg:top-8")(
                Div(cls="bg-slate-800 rounded-2xl overflow-hidden border-2 border-purple-500 shadow-2xl aspect-video flex items-center justify-center")(
                    Div(cls="text-center p-12")(
                        Div(cls="text-7xl mb-4")("🔍"),
                        P(cls="text-gray-400 text-xl")("Quality Inspection Demo")
                    )
                )
            )
        )
    )

def use_case_badge(text):
    """Reusable badge for use cases"""
    return Div(cls="badge badge-lg bg-slate-800 border-slate-700 text-white px-4 py-4 hover:border-blue-500 transition cursor-default")(
        text
    )

def cv_capability_card(icon, title, description):
    """Card for showcasing capabilities"""
    return Div(cls="bg-slate-800 rounded-xl p-6 border border-slate-700 hover:border-purple-500 transition")(
        Div(cls="flex flex-col items-center text-center space-y-4")(
            Div(cls="text-5xl")(icon),
            H3(cls="text-xl font-bold text-white")(title),
            P(cls="text-gray-400")(description)
        )
    )

def cv_use_cases_section():
    """Additional use cases and capabilities"""
    
    capabilities = [
        {
            "icon": "👁️",
            "title": "Object Detection",
            "description": "Identify and locate multiple objects in images and video streams with bounding boxes and confidence scores."
        },
        {
            "icon": "🎯",
            "title": "Object Tracking",
            "description": "Track objects across video frames maintaining unique IDs for each detected entity throughout the sequence."
        },
        {
            "icon": "🤖",
            "title": "Action Recognition",
            "description": "Classify human actions and activities in video sequences for behavior analysis and monitoring."
        },
        {
            "icon": "📊",
            "title": "Pose Estimation",
            "description": "Detect and track human body keypoints for posture analysis, ergonomics, and movement assessment."
        },
        {
            "icon": "🔍",
            "title": "Defect Detection",
            "description": "Automated visual inspection for quality control identifying defects, scratches, and anomalies."
        },
        {
            "icon": "⚠️",
            "title": "Safety Monitoring",
            "description": "Real-time monitoring of safety protocols including PPE detection and hazardous behavior alerts."
        }
    ]
    
    return Div(cls="container mx-auto px-8 py-20")(
        H2(cls="text-5xl font-bold text-white text-center mb-16")("Capabilities"),
        
        Div(cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6")(
            *[cv_capability_card(**cap) for cap in capabilities]
        )
    )