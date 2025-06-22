import langchain as lc
from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Job Schema

class Job(BaseModel):
    """Information about a job listing."""

    title: Optional[str] = Field(default=None, description="Job title")
    company: Optional[str] = Field(default=None, description="Company name")
    location: Optional[str] = Field(default=None, description="Job location")
    pay: Optional[str] = Field(default=None, description="Job pay")
    description: Optional[str] = Field(default=None, description="Full job description")
    date_posted: Optional[str] = Field(default=None, description="Date when the job was posted")
    responsibilities: Optional[str] = Field(default=None, description="Key responsibilities listed in the job")
    requirements: Optional[str] = Field(default=None, description="Key required knowledge, skills, and abilities")
    preferred_qualifications: Optional[str] = Field(default=None, description="Preferred (not required) qualifications")

class Data(BaseModel):
    """Extracted data about jobs"""
    jobs: list[Job] = Field(description="List of jobs")

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value"
        ),
        # Example 1
        (
            "user",
            "United States · 2 days ago · Over 100 people clicked apply Promoted by hirer · Responses managed off LinkedIn $25/hr - $30/hr"
            "About the job POSITION OVERVIEW Formstack is hiring two AI Interns for a 4-month fixed term to help drive one of the boldest transformations in our company’s journey: making"
            "AI second nature across every role, team, and function. These roles are a core part of our evolution from AI-forward to AI-native—and they’re a big deal. "
            "As an AI Intern, you’ll partner directly with our CIO, People team, and leaders across the business to accelerate adoption, experimentation, and fluency. "
            "This isn’t about theory—it’s about real-world use cases, workflow breakthroughs, and wow moments. If you’re curious, resourceful, and energized by the idea of helping a "
            "high-growth tech company thrive on the edge of innovation, we want to hear from you. candidates based in Denver or San Francisco, but we’re open to remote candidates who are an exceptional fit."
            "RESPONSIBILITIES Collaborate with our CIO, People team, and department leaders to scale AI adoption across the org Build and maintain an internal library of high-impact prompts, sorted by function and workflow "
            "Shadow teams to uncover friction points and identify AI-enabled solutions that drive productivity Support the creation of onboarding materials, live demos, job aids, and training for employees at all levels"
            "Pilot and document real-world AI use cases that align with business priorities and unlock new ways of working Help build excitement and momentum through internal campaigns, peer training, and success stories "
            "Track adoption metrics and employee feedback to iterate and improve continuously Stay on top of emerging AI tools (ChatGPT, Claude, Gemini, etc.) and evaluate their potential for team use "
            "Contribute to a culture of experimentation, continuous learning, and responsible AI use aligned to The Formstack Standard KNOWLEDGE, SKILLS, AND ABILITIES // REQUIRED"
            "Currently pursuing a Bachelor’s or Master’s degree in Computer Science, Data Science, Human-Computer Interaction, Organizational Psychology, or a related field—or equivalent experience"
            "Google Cloud Certified in Generative AI or similar (or committed to completing certification before start) Strong understanding of generative AI tools, prompt design, and how AI can augment human performance"
            "Clear communicator who can simplify technical concepts and inspire teams to embrace new tools Creative problem-solver with a bias for action, experimentation, and iteration"
            "Highly organized and able to work independently in a fast-paced, ever-evolving environment Enthusiastic about helping others adopt new technology with empathy and clarity"
            "Basic coding skills (such as python or java) to help bridge the no-code gap or better integrate tools. KNOWLEDGE, SKILLS, AND ABILITIES // PREFERRED Experience with enablement, instructional design, or internal communications Familiarity with low-code/no-code tools (e.g., Notion, Airtable, Zapier, n8n, MCP)"
            "Background in workshop facilitation or content creation Exposure to prompt engineering or AI knowledge base development WHY JOIN FORMSTACK?"
            "At Formstack, we don’t just use AI—we live it. We believe in thriving on the edge, delivering wow moments, and combining human ingenuity with intelligent systems. You’ll join a culture that’s hungry to learn, values speed and substance, and empowers every team member to drive meaningful change. This is more than an internship. It’s your chance to shape what modern work can look like."
            "Don’t meet every single requirement? Studies have shown that women and people of color are less likely to apply to jobs unless they meet every single qualification. At Formstack, we are dedicated to building a diverse, inclusive and authentic workplace, so if you’re excited about this role but your past experience doesn’t align perfectly with every qualification in the job description, we encourage you to apply anyway. You may be just the right candidate for this or other roles."
        ),
        ("assistant",
         """{
         "title": AI Intern",
         "company:" "Formstack",
         "location": "Remote, Denver or San Francisco preferred",
         "pay": 25-30/hr
         "description": "Formstack is hiring two AI Interns for a 4-month fixed term to help drive AI transformation making AI second nature across every role, team, and function.",
         "date_posted": null,
         "responsibilities": "Collaborate with CIO and department leads, build internal prompt libraries, support onboarding and training, document AI use cases, track adoption metrics, stay updated on emerging AI tools.",
         "requirements": "Pursuing degree in CS, Data Science, or related field; understanding of generative AI; strong communication; basic Python or Java. Google Cloud certified",
         "preferred_qualifications": "Experience with enablement, no-code tools like Notion or Zapier, workshop facilitation, content creation.",
         """
         ),
        ("job", "{text}"),
    ]
)