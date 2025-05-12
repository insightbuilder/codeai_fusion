# Recreate 70 meaningful tasks with hints and AI applicability

detailed_tasks = [
    # 1–10 (already detailed earlier)
    (
        "Email Summarization & Response Suggestions",
        "Use OpenAI API to summarize and draft email replies based on thread context.",
        "❌",
    ),
    (
        "Meeting Scheduling with Preferences",
        "Use Google Calendar API + user-defined preferences (e.g., avoid Mondays).",
        "✅",
    ),
    (
        "Daily Standup Report Generation",
        "Parse Jira tickets or Git commits and format into markdown.",
        "✅",
    ),
    (
        "Calendar Event Parsing & Reminders",
        "Use NLP to extract topics or manually define keyword-based rules.",
        "✅",
    ),
    (
        "Email Cleanup & Categorization",
        "Auto-label emails using LLM classification or rule-based filters.",
        "✅",
    ),
    (
        "Follow-up Reminders on Unreplied Emails",
        "Script to track sent emails and alert if no reply after N days.",
        "✅",
    ),
    (
        "Zoom/Meet Transcription & Action Item Extraction",
        "Use Whisper for transcription and OpenAI for action summary.",
        "❌",
    ),
    (
        "Slack Message Summaries per Channel",
        "Use Slack API + LLM to summarize daily conversation.",
        "❌",
    ),
    (
        "Voice-to-Text Note Taking",
        "Use TTS + Notion or Google Docs with Whisper or speech-to-text APIs.",
        "✅",
    ),
    (
        "Document Drafting Templates",
        "AI-generated templates for reports, proposals, and contracts.",
        "✅",
    ),
    # 11–70: Additional manually created realistic automation tasks
    (
        "Resume Screening",
        "Parse resumes and match with job descriptions using embeddings.",
        "❌",
    ),
    (
        "Auto-tagging Helpdesk Tickets",
        "Classify incoming tickets using intent detection.",
        "❌",
    ),
    (
        "System Log Alerting",
        "Pattern match logs and alert on anomalies or predefined errors.",
        "✅",
    ),
    (
        "Code Review Suggestions",
        "Use GPT to give quick code feedback or identify anti-patterns.",
        "❌",
    ),
    (
        "Invoice Data Extraction",
        "Parse PDFs for invoice fields using OCR and regex or AI.",
        "✅",
    ),
    (
        "Meeting Minutes Generation",
        "Transcribe and summarize meetings into shareable notes.",
        "❌",
    ),
    (
        "Sentiment Analysis on Customer Feedback",
        "Use NLP models to categorize sentiment from reviews or surveys.",
        "❌",
    ),
    (
        "File Renaming in Bulk",
        "Script to rename files based on patterns, dates, or metadata.",
        "✅",
    ),
    ("Monitoring Website Uptime", "Ping endpoints and notify on failure.", "✅"),
    (
        "Lead Scoring",
        "Rank CRM leads based on interaction history using predictive models.",
        "❌",
    ),
    (
        "Text Translation",
        "Translate messages between multiple languages using AI.",
        "❌",
    ),
    (
        "Backup Scheduling",
        "Automate regular cloud/database/file backups with cron jobs.",
        "✅",
    ),
    (
        "CRM Contact Deduplication",
        "Identify and merge duplicate entries using fuzzy matching.",
        "✅",
    ),
    (
        "Time Tracking from Screenshots",
        "Detect active app or extract content from screenshots using OCR.",
        "❌",
    ),
    (
        "Competitor Price Monitoring",
        "Scrape competitor websites and compare prices.",
        "✅",
    ),
    ("Proposal Generation", "Generate draft sales proposals from client data.", "❌"),
    (
        "Project Progress Summarization",
        "Summarize task and issue tracker updates.",
        "✅",
    ),
    (
        "Auto-generate Social Media Posts",
        "Create posts from blog content using LLMs.",
        "❌",
    ),
    ("Weekly Digest Emails", "Summarize top updates and email to teams.", "✅"),
    (
        "Speech-to-Text for Podcasts",
        "Convert spoken content into text and summaries.",
        "❌",
    ),
    ("Portfolio Risk Alerts", "Monitor stock/crypto volatility and notify user.", "✅"),
    (
        "Customer Call Transcripts",
        "Use Whisper or telephony logs to capture calls as text.",
        "❌",
    ),
    (
        "Sales Forecasting",
        "Use time series models or ML to forecast future revenue.",
        "❌",
    ),
    (
        "Password Rotation Script",
        "Force and log periodic password changes for internal tools.",
        "✅",
    ),
    ("Daily Check-in Bot", "Slack/Teams bot asking daily goals and summarizing.", "✅"),
    (
        "Auto-generate Meeting Agendas",
        "Draft meeting agendas based on past topics and goals.",
        "❌",
    ),
    (
        "Bug Report Categorization",
        "Classify bugs from QA reports using keyword or LLM.",
        "✅",
    ),
    (
        "Auto-generate Charts from CSV",
        "Generate matplotlib/seaborn charts on new uploads.",
        "✅",
    ),
    (
        "Security Audit Logs Summary",
        "Summarize recent security logs for suspicious activities.",
        "❌",
    ),
    (
        "Auto-fill Repetitive Forms",
        "Use browser automation to fill web forms from a config.",
        "✅",
    ),
    (
        "PDF to Excel Extraction",
        "Extract tabular data using Camelot, Tabula, or AI OCR.",
        "✅",
    ),
    (
        "OCR Business Cards to Contacts",
        "Extract text fields from images and save to CRM.",
        "✅",
    ),
    (
        "Text Deduplication",
        "Clean up duplicate phrases or paragraphs from documents.",
        "✅",
    ),
    (
        "Policy Document Generation",
        "Generate drafts of compliance docs using templates + AI.",
        "❌",
    ),
    (
        "Speech Command Automation",
        "Voice-based shortcuts to execute system functions.",
        "❌",
    ),
    (
        "Event Feedback Aggregation",
        "Aggregate event survey responses and summarize.",
        "❌",
    ),
    (
        "Pipeline Status Notifications",
        "CI/CD tools to alert build success/failure.",
        "✅",
    ),
    (
        "AI Copilot for Code Snippets",
        "Generate code snippets from docstring or description.",
        "❌",
    ),
    (
        "Auto-grading Assignments",
        "Grade code or essay submissions with a rubric and LLM.",
        "❌",
    ),
    (
        "Summarize Articles",
        "Convert long-form articles into summaries with bullet points.",
        "❌",
    ),
    (
        "Data Cleaning Automation",
        "Detect missing, duplicate, or invalid entries.",
        "✅",
    ),
    (
        "Alert on Keyword Mentions",
        "Monitor Slack, Twitter, or logs for keywords.",
        "✅",
    ),
    ("GraphQL Query Generator", "Generate queries based on UI or natural input.", "❌"),
    (
        "Internal Knowledgebase QA",
        "Ask questions against internal docs using RAG/embedding.",
        "❌",
    ),
    ("Smart Email Routing", "Route emails to relevant team based on content.", "✅"),
    ("Regex Generator from Example", "LLM to create regex from pattern example.", "❌"),
    ("Generate Compliance Checklists", "Based on regulations like GDPR/ISO/etc.", "❌"),
    (
        "Remote Work Status Updater",
        "Update Slack or calendar based on current task or GPS.",
        "✅",
    ),
    (
        "Notification Digest across Tools",
        "Combine notifications from GitHub, Jira, etc.",
        "✅",
    ),
    (
        "Daily Journal Logging",
        "Auto-append thoughts or summaries to journal from notes.",
        "❌",
    ),
    (
        "Meeting Load Balancer",
        "Avoid back-to-back meetings by rearranging events.",
        "✅",
    ),
    (
        "Slack/Teams Auto-Responder",
        "Reply with canned responses outside work hours.",
        "✅",
    ),
    (
        "Customer Complaint Routing",
        "Identify severity and assign to right agent.",
        "✅",
    ),
    (
        "Auto-Detect Unused Cloud Resources",
        "Flag idle servers and suggest shutdown.",
        "✅",
    ),
    (
        "Automatic KPI Report",
        "Generate visual weekly report from KPIs in dashboard.",
        "✅",
    ),
    (
        "Visual UI Bug Detection",
        "Compare staging vs prod screens with computer vision.",
        "❌",
    ),
    ("Repo Activity Summary", "Summarize GitHub repo activity weekly.", "✅"),
    (
        "Auto-schedule Code Deployments",
        "Trigger deployment pipelines on low-usage windows.",
        "✅",
    ),
    ("Conference Talk Summarizer", "Summarize a YouTube talk into key points.", "❌"),
    ("Generate Custom Regex", "Generate and test regex from user input via UI.", "✅"),
    (
        "Access Request Approvals",
        "Route access requests through approval workflow.",
        "✅",
    ),
    ("Onboarding Task Checklist", "Generate tailored onboarding checklists.", "✅"),
    ("Notion Doc Updater", "Use script to update progress bars and statuses.", "✅"),
    ("Translate Feedback Forms", "Multilingual feedback to English summaries.", "❌"),
    ("Custom Chatbot for Docs", "Provide AI assistant trained on internal docs.", "❌"),
    ("Auto-close Stale Issues", "Close old GitHub/Jira issues past a threshold.", "✅"),
]

can_do = 0

for task in detailed_tasks:
    if task[2] == "✅":
        can_do += 1

print("Total tasks that can be done without also:", can_do)
# 43 tasks can be done without AI
