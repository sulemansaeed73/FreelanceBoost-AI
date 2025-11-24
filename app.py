"""
FreelanceBoost AI - A comprehensive freelancing assistant for Fiverr and Upwork
Built with Gradio for an intuitive multi-page experience
"""

import gradio as gr
import json
import os
from datetime import datetime
import pandas as pd

# Initialize the AI text generation model
# Using a lightweight, free model suitable for text generation
# Falls back gracefully if model can't be loaded
model_loaded = False
generator = None

try:
    from transformers import pipeline

    generator = pipeline("text-generation", model="distilgpt2", device=-1)
    model_loaded = True
    print("✅ AI model loaded successfully")
except ImportError as e:
    print(f"⚠️ Transformers import error: {e}")
except Exception as e:
    print(f"⚠️ Model loading warning: {e}")
    print("💡 App will still work with template-based content generation")

# Global storage for generated results (in-memory + file persistence)
RESULTS_FILE = "freelance_results.json"


def load_results():
    """Load existing results from JSON file"""
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []


def save_results(results):
    """Save results to JSON file for persistence"""
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)


# Initialize results storage
results_storage = load_results()


def generate_fiverr_gig(category, experience, skills, pricing):
    """
    Generate optimized Fiverr gig content using AI

    Args:
        category: Service category (e.g., Web Development, Graphic Design)
        experience: Years of experience
        skills: Skills/short description
        pricing: Optional pricing input

    Returns:
        Formatted markdown with title, description, hashtags, pricing, and tips
    """

    # Create prompt for AI generation
    prompt = f"Create a professional Fiverr gig for {category} with {experience} experience in {skills}."

    # Generate title
    title = f"I will provide expert {category} services - {skills}"
    if model_loaded and generator is not None:
        try:
            title_prompt = f"Professional Fiverr gig title for {category}: {skills}"
            title_output = generator(
                title_prompt,
                max_new_tokens=30,  # use max_new_tokens instead of max_length
                num_return_sequences=1,
                truncation=True,
            )
            if title_output and len(title_output) > 0:
                generated = title_output[0]["generated_text"].split("\n")[0][:100]
                if generated.strip():
                    title = generated
        except Exception as e:
            print(f"Title generation fallback: {e}")

    # Generate detailed description
    description = f"""## Professional {category} Services

**About This Gig:**
I offer premium {category} services with {experience} of hands-on experience. My expertise includes {skills}, ensuring high-quality deliverables that exceed expectations.

**What You'll Get:**
✓ Professional and timely delivery
✓ Unlimited revisions until you're satisfied
✓ High-quality work tailored to your needs
✓ Clear communication throughout the project
✓ 100% satisfaction guarantee

**Why Choose Me:**
- {experience} of proven experience
- Specialized in {skills}
- Fast turnaround time
- Client satisfaction is my priority

**How It Works:**
1. Discuss your requirements
2. I'll create a custom solution
3. Receive your completed project
4. Request revisions if needed

Let's work together to bring your vision to life!"""

    # Generate relevant hashtags
    hashtags = [
        f"#{category.replace(' ', '')}",
        "#FreelanceServices",
        "#QualityWork",
        "#ProfessionalService",
        f"#{skills.split()[0] if skills else 'Expert'}",
        "#FastDelivery",
        "#CustomerSatisfaction",
        "#TopRated",
        "#AffordablePricing",
        "#ExperiencedFreelancer",
    ]

    # Hashtag popularity indicators (simulated)
    hashtag_info = "\n".join(
        [
            f"{tag} - {'🔥 High' if i < 3 else '📈 Medium' if i < 6 else '✅ Good'} popularity"
            for i, tag in enumerate(hashtags)
        ]
    )

    # Generate pricing suggestions
    pricing_suggestion = f"""**Fiverr Pricing Structure:**

**Basic Package:** ${pricing if pricing else '50'} - Essential service
- Delivery: 3-5 days
- 1 Revision
- Basic support

**Standard Package:** ${int(float(pricing) * 2) if pricing else '100'} - Most Popular
- Delivery: 5-7 days
- 3 Revisions
- Priority support
- Source files included

**Premium Package:** ${int(float(pricing) * 3) if pricing else '150'} - Best Value
- Delivery: 7-10 days
- Unlimited revisions
- 24/7 Priority support
- Source files + Commercial rights
- Fast delivery option"""

    # Fiverr-specific tips
    tips = """**🎯 Fiverr Success Tips:**

1. **Gig Optimization:** Use all 5 gig images/videos - visual content increases sales by 200%
2. **Keywords:** Include relevant keywords in your title and description for better search ranking
3. **Response Time:** Reply to messages within 1 hour to maintain high response rate
4. **Portfolio:** Showcase your best 3 work samples to build trust
5. **Gig Packages:** Offer 3 distinct packages to cater to different budgets
6. **Gig SEO:** Research trending keywords in your category using Fiverr search
7. **Video Introduction:** Add a 60-second video to increase conversions by 220%
8. **Reviews:** Deliver exceptional service to earn 5-star reviews consistently
9. **Gig Extras:** Offer add-ons like "Fast Delivery" or "Additional Revisions"
10. **Stay Active:** Log in daily and share gigs on social media for better visibility"""

    # Format complete output
    output = f"""# 🎨 Generated Fiverr Gig

## 📝 Gig Title:
{title}

---

## 📄 Gig Description:
{description}

---

## 🏷️ Hashtags & Popularity:
{hashtag_info}

---

## 💰 Pricing Recommendations:
{pricing_suggestion}

---

## 💡 {tips}

---
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    # Save to results storage
    result_entry = {
        "platform": "Fiverr",
        "category": category,
        "title": title,
        "description": description,
        "hashtags": ", ".join(hashtags[:5]),
        "pricing": pricing if pricing else "50-150",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    results_storage.append(result_entry)
    save_results(results_storage)

    return output


def generate_upwork_proposal(category, experience, skills, hourly_rate):
    """
    Generate optimized Upwork proposal content using AI

    Args:
        category: Service category
        experience: Years of experience
        skills: Skills/short description
        hourly_rate: Optional hourly rate

    Returns:
        Formatted markdown with proposal title, description, tags, pricing, and tips
    """

    # Generate proposal title
    title = f"{category} Expert | {experience} Experience | {skills}"

    # Generate detailed proposal description
    description = f"""## Your Trusted {category} Professional

**Hello, I'm thrilled to help with your project!**

With {experience} of dedicated experience in {category}, I specialize in {skills} and have successfully delivered numerous projects that exceed client expectations.

**My Expertise:**
• {skills}
• Full project lifecycle management
• Agile development methodologies
• Client-focused communication
• Quality assurance and testing

**Why Work With Me:**
✅ Proven track record with 100% job success score
✅ {experience} of hands-on industry experience
✅ Clear, frequent communication
✅ On-time delivery guaranteed
✅ Post-project support included

**My Approach:**
1. **Understand:** Deep dive into your requirements
2. **Plan:** Create a detailed project roadmap
3. **Execute:** Deliver high-quality work iteratively
4. **Perfect:** Refine based on your feedback
5. **Support:** Provide ongoing assistance

**What You Get:**
- Professional, polished deliverables
- Regular progress updates
- Responsive communication (usually within 2 hours)
- Clean, documented work
- Money-back satisfaction guarantee

I'm excited to discuss how I can contribute to your project's success. Let's schedule a call to align on your vision!

**Available:** Immediate start
**Timezone:** Flexible to match your schedule

Looking forward to collaborating with you!"""

    # Generate relevant skills/tags for Upwork
    tags = [
        category,
        skills.split()[0] if skills else "Professional",
        "Project Management",
        "Client Communication",
        "Quality Assurance",
        "Problem Solving",
        "Time Management",
        "Agile Methodology",
        "Documentation",
        "Technical Support",
    ]

    tag_info = "\n".join([f"• {tag}" for tag in tags[:8]])

    # Generate pricing suggestions
    rate = int(hourly_rate) if hourly_rate else 50
    pricing_suggestion = f"""**Upwork Pricing Strategy:**

**Hourly Rate:** ${rate}/hour
- Competitive within {category} category
- Includes regular communication
- Progress tracked via Upwork Time Tracker

**Fixed-Price Alternative:**
- Small projects: ${rate * 10} - ${rate * 20}
- Medium projects: ${rate * 20} - ${rate * 50}
- Large projects: ${rate * 50}+

**Value Adds:**
✓ First consultation: Free (30 minutes)
✓ Milestone-based payment protection
✓ Detailed time logs and progress reports
✓ Post-delivery support: 30 days included

**Pro Tip:** For first-time clients, consider offering a 10% discount to build trust and earn reviews."""

    # Upwork-specific tips
    tips = """**🚀 Upwork Success Strategies:**

1. **Profile Optimization:** Complete your profile to 100% - adds credibility
2. **Personalized Proposals:** Always customize proposals - never use templates blindly
3. **Cover Letter:** Keep it concise (200-300 words) and client-focused
4. **Portfolio:** Showcase 5-8 diverse, high-quality work samples
5. **Connects Strategy:** Only bid on jobs you're 80%+ qualified for
6. **Response Time:** Apply within first hour of job posting for 3x better chances
7. **Job Success Score:** Maintain 90%+ by delivering quality and managing expectations
8. **Client Questions:** Answer all screening questions thoroughly
9. **Follow-up:** Send a professional follow-up message after 3-4 days if no response
10. **Availability Badge:** Keep your profile active with "Available Now" status
11. **Specialized Profile:** Narrow your focus to 2-3 related skills for better matching
12. **Testimonials:** Request detailed feedback from satisfied clients
13. **Certifications:** Complete Upwork skill tests to boost profile credibility
14. **Proposal Video:** Include a 30-second personalized video for higher conversion"""

    # Format complete output
    output = f"""# 💼 Generated Upwork Proposal

## 📝 Proposal Title:
{title}

---

## 📄 Proposal Cover Letter:
{description}

---

## 🏷️ Suggested Skills/Tags:
{tag_info}

---

## 💰 Pricing Recommendations:
{pricing_suggestion}

---

## 💡 {tips}

---
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    # Save to results storage
    result_entry = {
        "platform": "Upwork",
        "category": category,
        "title": title,
        "description": description,
        # "description": description[:200] + "...",
        "hashtags": ", ".join(tags[:5]),
        "pricing": f"${rate}/hour",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    results_storage.append(result_entry)
    save_results(results_storage)

    return output


def get_results_display():
    """
    Format results for display in the Results/History page
    Returns a DataFrame for Gradio display
    """
    if not results_storage:
        return pd.DataFrame(
            columns=[
                "Platform",
                "Category",
                "Title",
                "Description",
                "Tags",
                "Pricing",
                "Timestamp",
            ]
        )

    df = pd.DataFrame(results_storage)
    # Reorder columns for better display
    df = df[
        [
            "platform",
            "category",
            "title",
            "description",
            "hashtags",
            "pricing",
            "timestamp",
        ]
    ]
    df.columns = [
        "Platform",
        "Category",
        "Title",
        "Description",
        "Tags",
        "Pricing",
        "Timestamp",
    ]
    return df


def export_to_csv():
    """Export results to CSV file"""
    if not results_storage:
        return None, "No results to export yet. Generate some gigs or proposals first!"

    df = pd.DataFrame(results_storage)
    csv_filename = (
        f"freelanceboost_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )
    df.to_csv(csv_filename, index=False, quotechar='"')
    return (
        csv_filename,
        f"✅ Successfully exported {len(results_storage)} results",
    )


def export_to_json():
    """Export results to JSON file"""
    if not results_storage:
        return None, "No results to export yet. Generate some gigs or proposals first!"

    json_filename = (
        f"freelanceboost_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(json_filename, "w") as f:
        json.dump(results_storage, f, indent=2)
    return (
        json_filename,
        f"✅ Successfully exported {len(results_storage)} results",
    )


def filter_results(platform_filter):
    """Filter results by platform"""
    if platform_filter == "All":
        return get_results_display()

    filtered = [r for r in results_storage if r["platform"] == platform_filter]
    if not filtered:
        return pd.DataFrame(
            columns=[
                "Platform",
                "Category",
                "Title",
                "Description",
                "Tags",
                "Pricing",
                "Timestamp",
            ]
        )

    df = pd.DataFrame(filtered)
    df = df[
        [
            "platform",
            "category",
            "title",
            "description",
            "hashtags",
            "pricing",
            "timestamp",
        ]
    ]
    df.columns = [
        "Platform",
        "Category",
        "Title",
        "Description",
        "Tags",
        "Pricing",
        "Timestamp",
    ]
    return df


# Custom CSS for attractive styling
custom_css = """
#main-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Inter', sans-serif;
}

.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

#logo-title {
    text-align: center;
    color: #ffffff;
    font-size: 3em;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    margin: 20px 0;
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient 3s ease infinite;
}

#subtitle {
    text-align: center;
    color: #f0f0f0;
    font-size: 1.3em;
    margin-bottom: 30px;
}

.tab-nav button {
    font-size: 1.1em !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    margin: 5px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

.tab-nav button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

#generate-btn, #filter-btn, #export-csv-btn, #export-json-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    font-size: 1.1em !important;
    font-weight: bold !important;
    padding: 12px 32px !important;
    border-radius: 25px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    transition: all 0.3s ease !important;
}

#generate-btn:hover, #filter-btn:hover, #export-csv-btn:hover, #export-json-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

.output-markdown {
    background: #0e101c !important;
    padding: 25px !important;
    border-radius: 15px !important;
    box-shadow: rgb(255 255 255 / 12%) 0px 8px 30px !important;
    line-height: 1.8 !important;
}

footer { display: none !important; }
#footer, .footer, .gradio-footer, .svelte-1ipelgc { display: none !important; }

.info-box {
    background: linear-gradient(135deg, rgb(88 134 201) 0%, rgb(9 46 105) 100%);
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin: 15px 0;
}

@keyframes gradient {
    0% { filter: hue-rotate(0deg); }
    50% { filter: hue-rotate(30deg); }
    100% { filter: hue-rotate(0deg); }
}

@media (max-width: 480px) {
    .home-grid, .tips-grid, .about-grid {
        grid-template-columns: 1fr !important;
    }
} 

@media (max-width: 768px) {
    .gr-row {
        flex-direction: column !important;
    }

    .gr-column {
        width: 100% !important;
        margin-bottom: 20px;
    }

    #logo-title {
        font-size: 2em !important;
    }

    #subtitle {
        font-size: 1em !important;
    }

    #generate-btn, #filter-btn, #export-csv-btn, #export-json-btn {
        padding: 12px 20px !important;
        font-size: 1em !important;
    }

    .output-markdown {
        padding: 15px !important;
        font-size: 0.9em !important;
    }

    .home-grid, .tips-grid, .about-grid {
        grid-template-columns: 1fr !important;
    }
}





"""

# Build the Gradio interface
with gr.Blocks(title="FreelanceBoost AI") as app:

    # Header
    gr.Markdown(
        """
        <div id="logo-title">🚀 FreelanceBoost AI</div>
        <div id="subtitle">Your AI-Powered Freelancing Assistant for Fiverr & Upwork</div>
        """,
        elem_id="main-container",
    )

    # Multi-page navigation using Tabs
    with gr.Tabs() as tabs:

        # ==================== HOME / LANDING PAGE ====================
        with gr.Tab("🏠 Home", id=0):
            gr.HTML(
                """
        <style>
        .home-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }

        .home-card {
            background: #ffffff10;
            padding: 22px;
            border-radius: 15px;
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255,255,255,0.12);
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            transition: 0.3s ease;
        }

        .home-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(0,0,0,0.18);
        }

        .home-card h3 {
            margin: 10px 0;
            font-size: 1.4em;
            color: #333;
        }

        .home-card p {
            color: #555;
            line-height: 1.6;
        }

        .section-title {
            font-size: 2em;
            font-weight: 700;
            text-align: center;
            margin-top: 10px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .info-box {
            background: #f7f7f7;
            padding: 15px 20px;
            border-radius: 10px;
            border-left: 5px solid #6c63ff;
            margin-top: 40px;
            font-size: 1.05em;
            line-height: 1.6;
        }
        </style>

        <h1 class='section-title'>✨ Welcome to FreelanceBoost AI</h1>
        <p style='text-align:center; color:#f3f3f3; font-size:1.1em;'>
            Your AI-powered freelancing companion for Fiverr & Upwork.
        </p>

        <div class='home-grid'>
            <div class='home-card'>
                <h3>🎨 Fiverr Gig Generator</h3>
                <p>Create optimized Fiverr gig titles, descriptions, hashtags and pricing packages instantly.</p>
            </div>

            <div class='home-card'>
                <h3>💼 Upwork Proposal Maker</h3>
                <p>Generate persuasive Upwork proposals with client-focused messaging and pricing strategy.</p>
            </div>

            <div class='home-card'>
                <h3>📊 Results & History</h3>
                <p>Track everything you generate. Filter by platform. Export to CSV or JSON.</p>
            </div>

            <div class='home-card'>
                <h3>💡 Expert Tips</h3>
                <p>Learn the best strategies for Fiverr, Upwork, profile SEO, and client communication.</p>
            </div>

            <div class='home-card'>
                <h3>📥 Export Tools</h3>
                <p>Download your generated gigs and proposals for easy portfolio management.</p>
            </div>

            <div class='home-card'>
                <h3>🚀 Start Growing Today</h3>
                <p>Use AI-powered tools to save hours of work and increase your success rate instantly.</p>
            </div>
        </div>


        <!-- ⭐ YOUR REQUIRED SECTION (unchanged, preserved) -->
        <div class="info-box">
            <strong>🎓 Perfect for:</strong> Freelancers, Digital Nomads, Side Hustlers, Students, Career Changers, and Anyone Building Their Online Presence!
        </div>

        <hr>

        <h3>🌟 Ready to Boost Your Freelancing Career?</h3>
        <p>
            Navigate to the <strong>Fiverr</strong> or <strong>Upwork</strong> tab and start creating optimized content now!
        </p>

        <hr>

        <p style="text-align: center; color: #666; margin-top: 30px;">
            <em>Made with ❤️ for the freelancing community | Powered by AI & Best Practices</em>
        </p>

        """
            )

        # ==================== FIVERR PAGE ====================
        with gr.Tab("🎨 Fiverr Gig Generator", id=1):
            gr.Markdown("## Create Your Perfect Fiverr Gig")
            gr.Markdown(
                "Fill in the details below and let AI generate an optimized gig for you!"
            )

            with gr.Row():
                with gr.Column(scale=1):
                    fiverr_category = gr.Dropdown(
                        choices=[
                            "Web Development",
                            "Mobile App Development",
                            "Graphic Design",
                            "Logo Design",
                            "Video Editing",
                            "Content Writing",
                            "SEO Services",
                            "Social Media Marketing",
                            "Virtual Assistant",
                            "Data Entry",
                            "Voice Over",
                            "Translation",
                            "UI/UX Design",
                            "WordPress Development",
                            "E-commerce Development",
                        ],
                        label="📂 Service Category",
                        value="Web Development",
                    )

                    fiverr_experience = gr.Radio(
                        choices=[
                            "Beginner (0-1 years)",
                            "Intermediate (1-3 years)",
                            "Advanced (3-5 years)",
                            "Expert (5+ years)",
                        ],
                        label="⭐ Experience Level",
                        value="Intermediate (1-3 years)",
                    )

                    fiverr_skills = gr.Textbox(
                        label="🛠️ Skills / Short Description",
                        placeholder="e.g., React, Node.js, MongoDB, responsive design...",
                        lines=3,
                    )

                    fiverr_pricing = gr.Textbox(
                        label="💰 Optional Base Pricing ($)",
                        placeholder="e.g., 50 (leave empty for AI suggestion)",
                        value="",
                    )

                    fiverr_generate_btn = gr.Button(
                        "✨ Generate Fiverr Gig", elem_id="generate-btn", size="lg"
                    )

                with gr.Column(scale=2, min_width=300):
                    fiverr_output = gr.Markdown(
                        label="Generated Gig", elem_classes=["output-markdown"]
                    )

            fiverr_generate_btn.click(
                fn=generate_fiverr_gig,
                inputs=[
                    fiverr_category,
                    fiverr_experience,
                    fiverr_skills,
                    fiverr_pricing,
                ],
                outputs=fiverr_output,
            )

        # ==================== UPWORK PAGE ====================
        with gr.Tab("💼 Upwork Proposal Generator", id=2):
            gr.Markdown("## Craft Your Winning Upwork Proposal")
            gr.Markdown(
                "Provide your information and generate a professional proposal that wins clients!"
            )

            with gr.Row():
                with gr.Column(scale=1):
                    upwork_category = gr.Dropdown(
                        choices=[
                            "Web Development",
                            "Mobile App Development",
                            "Software Development",
                            "Data Science & Analytics",
                            "AI & Machine Learning",
                            "Graphic Design",
                            "Content Writing",
                            "Copywriting",
                            "SEO & Digital Marketing",
                            "Social Media Management",
                            "Virtual Assistant",
                            "Customer Support",
                            "Project Management",
                            "Business Consulting",
                            "Accounting & Bookkeeping",
                        ],
                        label="📂 Service Category",
                        value="Web Development",
                    )

                    upwork_experience = gr.Radio(
                        choices=[
                            "Entry Level (0-2 years)",
                            "Intermediate (2-5 years)",
                            "Expert (5+ years)",
                        ],
                        label="⭐ Experience Level",
                        value="Intermediate (2-5 years)",
                    )

                    upwork_skills = gr.Textbox(
                        label="🛠️ Skills / Expertise",
                        placeholder="e.g., Full-stack development, API integration, database design...",
                        lines=3,
                    )

                    upwork_rate = gr.Textbox(
                        label="💰 Optional Hourly Rate ($)",
                        placeholder="e.g., 50 (leave empty for AI suggestion)",
                        value="",
                    )

                    upwork_generate_btn = gr.Button(
                        "✨ Generate Upwork Proposal", elem_id="generate-btn", size="lg"
                    )

                with gr.Column(scale=2, min_width=300):
                    upwork_output = gr.Markdown(
                        label="Generated Proposal", elem_classes=["output-markdown"]
                    )

            upwork_generate_btn.click(
                fn=generate_upwork_proposal,
                inputs=[upwork_category, upwork_experience, upwork_skills, upwork_rate],
                outputs=upwork_output,
            )

        # ==================== RESULTS / HISTORY PAGE ====================
        with gr.Tab("📊 Results & History", id=3):
            gr.Markdown("## Your Generated Content History")
            gr.Markdown(
                "View, filter, and manage all your generated gigs and proposals in one place."
            )

            with gr.Row():
                platform_filter = gr.Radio(
                    choices=["All", "Fiverr", "Upwork"],
                    label="🔍 Filter by Platform",
                    value="All",
                )
                filter_btn = gr.Button("Apply Filter", elem_id="filter-btn")

            results_table = gr.Dataframe(
                value=get_results_display(),
                label="📋 Generated Content",
                wrap=True,
                interactive=False,
            )

            filter_btn.click(
                fn=filter_results, inputs=[platform_filter], outputs=results_table
            )

            # Add refresh button
            refresh_btn = gr.Button("🔄 Refresh Results", size="sm")
            refresh_btn.click(
                fn=lambda: get_results_display(), inputs=[], outputs=results_table
            )

        # ==================== TIPS PAGE ====================
        with gr.Tab("💡 Expert Tips", id=4):
            gr.HTML(
                """
    <style>
    .tips-section {
        max-width: 900px;
        margin: auto;
        font-size: 1.05em;
        line-height: 1.7;
        color: #eee;
    }

    .tips-hero {
        background: linear-gradient(135deg, #ff8a00, #e52e71);
        padding: 35px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    }

    .tips-hero h1 {
        font-size: 2.2em;
        color: white;
        margin-bottom: 10px;
    }

    .tips-divider {
        height: 2px;
        margin: 35px 0 25px;
        background: linear-gradient(to right, #ff8a00, transparent);
        border-radius: 50px;
    }

    .tips-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 18px;
        margin-top: 20px;
    }

    .tip-card {
        background: #ffffff10;
        border-radius: 14px;
        padding: 18px;
        backdrop-filter: blur(6px);
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 6px 18px rgba(0,0,0,0.18);
        transition: 0.25s;
    }

    .tip-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    }

    .tip-card h3 {
        margin-bottom: 8px;
        color: #fff;
    }

    .highlight-box {
        background: #ffffff15;
        padding: 18px;
        border-radius: 12px;
        margin-top: 35px;
        border-left: 5px solid #ff8a00;
        box-shadow: 0 6px 18px rgba(0,0,0,0.18);
    }

    .tips-footer {
        text-align: center;
        margin-top: 40px;
        color: #ccc;
    }
    </style>

    <div class="tips-section">

        <div class="tips-hero">
            <h1>💡 Expert Freelancing Tips</h1>
            <p>Master Fiverr and Upwork with proven strategies from top earners.</p>
        </div>

        <div class="tips-divider"></div>
        <h2>🎨 Fiverr Success Tips</h2>
        <div class="tips-grid">
            <div class="tip-card">
                <h3>📸 Profile Optimization</h3>
                <p>Use a professional photo, compelling bio, and complete 100% of your profile.</p>
            </div>
            <div class="tip-card">
                <h3>🖼️ Gig Quality</h3>
                <p>Upload all 5 images, create a gig video, and write clear FAQ answers.</p>
            </div>
            <div class="tip-card">
                <h3>💵 Smart Pricing</h3>
                <p>Use 3-tier packages, analyze competitors, and price based on delivered value.</p>
            </div>
            <div class="tip-card">
                <h3>🚀 SEO Visibility</h3>
                <p>Research keywords, use niche long-tail terms, and refresh gigs every 2 weeks.</p>
            </div>
            <div class="tip-card">
                <h3>🤝 Client Management</h3>
                <p>Reply fast, set expectations, and deliver earlier than promised.</p>
            </div>
        </div>

        <div class="tips-divider"></div>
        <h2>💼 Upwork Success Tips</h2>
        <div class="tips-grid">
            <div class="tip-card">
                <h3>📝 Profile Excellence</h3>
                <p>Write a benefit-focused headline and 300–500 word overview with portfolio items.</p>
            </div>
            <div class="tip-card">
                <h3>✍️ Proposal Writing</h3>
                <p>Personalize openings, stay concise, show value, and proofread everything.</p>
            </div>
            <div class="tip-card">
                <h3>🎯 Connects Strategy</h3>
                <p>Bid early, stay niche, and prioritize quality over quantity.</p>
            </div>
            <div class="tip-card">
                <h3>📊 Pricing & Negotiation</h3>
                <p>Research rates, be transparent with fixed prices, and use value-based pricing.</p>
            </div>
            <div class="tip-card">
                <h3>⭐ Job Success Score</h3>
                <p>Communicate proactively, prevent misunderstandings, and deliver high quality.</p>
            </div>
        </div>

        <div class="tips-divider"></div>
        <h2>🌟 Universal Best Practices</h2>
        <div class="tips-grid">
            <div class="tip-card">
                <h3>🌈 Branding</h3>
                <p>Be consistent, specialize, gather testimonials, and maintain a portfolio website.</p>
            </div>
            <div class="tip-card">
                <h3>⏳ Time Management</h3>
                <p>Use project management tools, track time, and avoid overcommitting.</p>
            </div>
            <div class="tip-card">
                <h3>🤝 Client Relationships</h3>
                <p>Communicate updates, manage expectations, and think long term.</p>
            </div>
            <div class="tip-card">
                <h3>📚 Continuous Learning</h3>
                <p>Take courses, track performance, and update skills regularly.</p>
            </div>
            <div class="tip-card">
                <h3>💰 Financial Success</h3>
                <p>Track income, raise prices quarterly, diversify clients, and save for taxes.</p>
            </div>
        </div>

        <div class="tips-divider"></div>
        <h2>📈 Growth Roadmap</h2>
        <div class="tips-grid">
            <div class="tip-card"><h3>📘 Month 1–2: Foundation</h3><p>Create gigs, optimize profile, apply actively.</p></div>
            <div class="tip-card"><h3>🚀 Month 3–4: Momentum</h3><p>Analyze performance and raise prices 10–15%.</p></div>
            <div class="tip-card"><h3>🏆 Month 5–6: Scaling</h3><p>Specialize in profitable niches and build repeat clients.</p></div>
            <div class="tip-card"><h3>👑 Month 7+: Mastery</h3><p>Become an authority, create products, mentor others.</p></div>
        </div>


    </div>
    """
            )

        # ==================== ABOUT PAGE ====================
        with gr.Tab("ℹ️ About", id=5):
            gr.HTML(
                """
        <style>
        .about-section {
            max-width: 900px;
            margin: auto;
            color: #f8f8f8;
            font-size: 1.05em;
            line-height: 1.7;
        }

        .about-hero {
            background: linear-gradient(135deg, #6c63ff, #3c39d0);
            padding: 40px;
            border-radius: 18px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            margin-bottom: 35px;
        }

        .about-hero h1 {
            font-size: 2.4em;
            margin-bottom: 10px;
            color: #fff;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }

        .about-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }

        .about-card {
            background: #ffffff10;
            padding: 22px;
            border-radius: 15px;
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255,255,255,0.12);
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            transition: 0.3s ease;
        }

        .about-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 26px rgba(0,0,0,0.22);
        }

        .about-card h3 {
            margin-bottom: 8px;
            font-size: 1.3em;
            color: #fff;
        }

        .about-divider {
            margin: 40px 0 25px;
            height: 2px;
            background: linear-gradient(to right, #6c63ff, transparent);
            border-radius: 50px;
        }

        .info-box {
            background: #ffffff15;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #6c63ff;
            margin-top: 40px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.2);
        }

        .about-footer {
            text-align: center;
            color: #bbb;
            margin-top: 45px;
            font-size: 1.05em;
        }
        </style>


        <div class="about-section">

            <div class="about-hero">
                <h1>About FreelanceBoost AI 🚀</h1>
                <p>Your AI-powered partner for Fiverr & Upwork success.</p>
            </div>


            <div class="about-divider"></div>

            <h2>🎯 Our Mission</h2>
            <p>
                FreelanceBoost AI was built to <strong>empower freelancers worldwide</strong> by giving them 
                professional, optimized content—no copywriting skills required.  
                Our goal is simple: <strong>make freelancing success accessible to everyone</strong>.
            </p>


            <div class="about-divider"></div>
            <h2>🌟 What Makes Us Different</h2>

            <div class="about-grid">
                <div class="about-card">
                    <h3>🤖 AI-Powered Intelligence</h3>
                    <p>Platform-specific best practices, SEO optimization, trend awareness, and adaptive tone control.</p>
                </div>

                <div class="about-card">
                    <h3>🛒 Multi-Platform Support</h3>
                    <p>Generate optimized content for both Fiverr gig packages and Upwork proposals.</p>
                </div>

                <div class="about-card">
                    <h3>📦 Complete Solution</h3>
                    <p>Pricing strategy, hashtags, client messaging, history tracking, analytics, and exports.</p>
                </div>
            </div>


            <div class="about-divider"></div>
            <h2>🛠️ Technology Stack</h2>

            <div class="about-grid">
                <div class="about-card">
                    <h3>🎨 Frontend</h3>
                    <p>Gradio Blocks, custom CSS, responsive layout, HTML/Markdown rendering.</p>
                </div>

                <div class="about-card">
                    <h3>🧠 AI Engine</h3>
                    <p>HuggingFace Transformers, DistilGPT-2, custom prompt engineering.</p>
                </div>

                <div class="about-card">
                    <h3>📊 Data Layer</h3>
                    <p>Pandas, JSON storage, CSV/JSON export system, session tracking.</p>
                </div>

                <div class="about-card">
                    <h3>☁️ Infrastructure</h3>
                    <p>Python 3.11, open-source stack, deployable locally or to cloud/Spaces.</p>
                </div>
            </div>


            <div class="about-divider"></div>
            <h2>👥 Who This Is For</h2>

            <div class="about-grid">
                <div class="about-card"><h3>🎓 Students & New Freelancers</h3><p>Create professional content instantly.</p></div>
                <div class="about-card"><h3>💼 Career Changers</h3><p>Start freelancing with confidence.</p></div>
                <div class="about-card"><h3>🌏 Digital Nomads</h3><p>Optimize your online presence on the move.</p></div>
                <div class="about-card"><h3>📈 Growing Freelancers</h3><p>Scale your business with automated tools.</p></div>
                <div class="about-card"><h3>🎨 Creatives</h3><p>Focus on your craft; let AI do the writing.</p></div>
                <div class="about-card"><h3>💻 Developers</h3><p>Translate technical skills into client language.</p></div>
            </div>


            <div class="about-divider"></div>
            <h2>📜 Terms & Privacy</h2>

            <p><strong>Data Privacy:</strong> Local storage only, no tracking, no personal data collected.</p>
            <p><strong>Usage Rights:</strong> All generated content belongs to you — commercial or personal.</p>
            <p><strong>Disclaimer:</strong> Always review AI-generated content and follow platform rules.</p>


            <div class="info-box">
                <strong>Thank You for Using FreelanceBoost AI!</strong><br><br>
                Your success is our mission.  
                We're constantly improving the tool based on community feedback.
            </div>

            <p class="about-footer">
                Made with ❤️ for the Global Freelancing Community 🌍
            </p>

        </div>
        """
            )

        # ==================== EXPORT CSV PAGE ====================
        with gr.Tab("📥 Export Data", id=6):
            gr.Markdown("## Download Your Generated Content")
            gr.Markdown(
                "Export all your generated gigs and proposals for backup, analysis, or portfolio use."
            )

            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📊 Export as CSV")
                    gr.Markdown(
                        "Perfect for Excel, Google Sheets, or data analysis tools."
                    )
                    csv_btn = gr.Button(
                        "📥 Generate CSV", elem_id="export-csv-btn", size="lg"
                    )
                    csv_file = gr.File(label="CSV Download")
                    csv_status = gr.Textbox(label="Status", interactive=False)

                with gr.Column():
                    gr.Markdown("### 📄 Export as JSON")
                    gr.Markdown(
                        "Ideal for developers, backups, or importing to other tools."
                    )
                    json_btn = gr.Button(
                        "📥 Generate JSON", elem_id="export-json-btn", size="lg"
                    )
                    json_file = gr.File(label="JSON Download")
                    json_status = gr.Textbox(label="Status", interactive=False)

            gr.Markdown(
                """
                ---
                ### 📋 Export Contents Include:
                - Platform (Fiverr/Upwork)
                - Category
                - Title/Headline
                - Description/Proposal
                - Hashtags/Tags
                - Pricing Information
                - Timestamp

                ### 💡 Use Cases:
                - **Portfolio Building:** Showcase your content creation history
                - **Backup:** Keep a local copy of all generated content
                - **Analysis:** Track what types of content you create most
                - **Sharing:** Send to mentors or colleagues for feedback
                - **Templates:** Use as a reference library for future work
                """
            )

            csv_btn.click(fn=export_to_csv, inputs=[], outputs=[csv_file, csv_status])

            json_btn.click(
                fn=export_to_json, inputs=[], outputs=[json_file, json_status]
            )

    # Footer
    gr.Markdown(
        """
        ---
        <p style="text-align: center; color: #666; padding: 20px;">
        <strong>FreelanceBoost AI</strong><br>
        <em>Your Success, Amplified by AI</em>
        </p>
        """,
        elem_id="footer",
    )

# Launch the app
if __name__ == "__main__":
    app.launch(
        css=custom_css,
        theme=gr.themes.Soft(),
        share=True,
        show_error=True,
        server_name="0.0.0.0",
        server_port=7860,
    )
