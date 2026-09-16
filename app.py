import streamlit as st
from openai import OpenAI
import requests
import re
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ATS Resume Optimizer · Sai Rohit",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Sora:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

.stApp { background-color: #0c0e13; color: #e2e6f0; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #13161e !important;
    border-right: 1px solid #252a36;
}

/* Inputs */
.stTextArea textarea {
    background-color: #13161e !important;
    color: #e2e6f0 !important;
    border: 1px solid #252a36 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}
.stTextInput input {
    background-color: #13161e !important;
    color: #e2e6f0 !important;
    border: 1px solid #252a36 !important;
    border-radius: 8px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4f8ef7, #7c5cfc) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    font-size: 15px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #13161e;
    border-radius: 8px 8px 0 0;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #6b7590;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.stTabs [aria-selected="true"] {
    color: #4f8ef7 !important;
    border-bottom: 2px solid #4f8ef7 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background-color: #13161e;
    border: 1px solid #252a36;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 1rem;
}

/* Code blocks */
.stCodeBlock { border-radius: 8px !important; }
pre {
    background-color: #13161e !important;
    border: 1px solid #252a36 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    color: #e2e6f0 !important;
    padding: 1rem !important;
    overflow-x: auto;
}

/* Info cards */
.info-card {
    background: #13161e;
    border: 1px solid #252a36;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.info-val {
    font-size: 22px;
    font-weight: 700;
    background: linear-gradient(135deg, #4f8ef7, #7c5cfc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.info-label {
    font-size: 11px;
    color: #6b7590;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-top: 2px;
}

/* Credibility card — distinct styling */
.cred-card {
    background: #0f1a14;
    border: 1px solid #1e3a28;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.cred-val {
    font-size: 22px;
    font-weight: 700;
    background: linear-gradient(135deg, #3ecf8e, #27ae60);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.cred-label {
    font-size: 11px;
    color: #3ecf8e;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-top: 2px;
}

/* Badges */
.badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; margin: 2px; }
.badge-red { background: rgba(247,111,114,0.15); color: #f76f72; border: 1px solid rgba(247,111,114,0.3); }
.badge-yellow { background: rgba(245,200,66,0.12); color: #f5c842; border: 1px solid rgba(245,200,66,0.3); }
.badge-green { background: rgba(62,207,142,0.12); color: #3ecf8e; border: 1px solid rgba(62,207,142,0.3); }
.badge-blue { background: rgba(79,142,247,0.12); color: #4f8ef7; border: 1px solid rgba(79,142,247,0.3); }
.badge-orange { background: rgba(245,166,35,0.12); color: #f5a623; border: 1px solid rgba(245,166,35,0.3); }

/* Grounded mode banner */
.grounded-banner {
    background: linear-gradient(135deg, rgba(62,207,142,0.08), rgba(39,174,96,0.08));
    border: 1px solid rgba(62,207,142,0.25);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 12px;
    color: #3ecf8e;
    margin-bottom: 1rem;
}

/* Header */
.hero {
    text-align: center;
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid #252a36;
    margin-bottom: 1.5rem;
}
.hero h1 {
    font-size: 26px;
    font-weight: 700;
    background: linear-gradient(90deg, #4f8ef7, #7c5cfc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.hero p { color: #6b7590; font-size: 13px; }

/* Divider */
hr { border-color: #252a36 !important; }

/* Checkbox */
.stCheckbox label { color: #a0a8bf !important; font-size: 13px !important; }

/* Selectbox */
.stSelectbox select, [data-baseweb="select"] {
    background-color: #13161e !important;
    color: #e2e6f0 !important;
    border-color: #252a36 !important;
}

/* Success / warning */
.stSuccess { background-color: rgba(62,207,142,0.1) !important; border-color: #3ecf8e !important; }
.stWarning { background-color: rgba(245,200,66,0.1) !important; border-color: #f5c842 !important; }

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Resume store ───────────────────────────────────────────────────────────────
RESUME_V1 = r"""\documentclass[letterpaper,10.5pt]{article}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage[usenames,dvipsnames]{color}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}
\pdfgentounicode=1

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.55in}
\addtolength{\evensidemargin}{-0.55in}
\addtolength{\textwidth}{1.1in}
\addtolength{\topmargin}{-0.75in}
\addtolength{\textheight}{1.5in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{\vspace{-6pt}\scshape\raggedright\large}{}{0em}{}[\color{black}\titlerule\vspace{-5pt}]

\newcommand{\resumeItem}[1]{\item\small{#1\vspace{-2.5pt}}}
\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
  \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
    \textbf{#1} & \small #2 \\
    \textit{\small #3} & \textit{\small #4} \\
  \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeProjectHeading}[2]{
  \item
  \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
    \small #1 & \small #2 \\
  \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.12in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=0.2in]\vspace{-2pt}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-6pt}}

\begin{document}

%---------- HEADING ----------
\begin{center}
  {\LARGE \textbf{SAI ROHIT SHAIK}} \\[2pt]
  \small +91-6301411795 \;$\cdot$\;
  \href{mailto:h20240158@hyderabad.bits-pilani.ac.in}{h20240158@hyderabad.bits-pilani.ac.in} \;$\cdot$\;
  \href{https://linkedin.com/in/sk-sai-rohit}{linkedin.com/in/sk-sai-rohit} \;$\cdot$\;
  Hyderabad / Bengaluru, India
\end{center}
\vspace{-10pt}

%---------- SUMMARY ----------
\section{Summary}
\begin{itemize}[leftmargin=0.12in, label={}]
\small{\item{
Analyst with experience in \textbf{SQL, Python, and Google BigQuery} for \textbf{fraud analytics}, \textbf{ETL pipeline} engineering, and \textbf{financial data analysis}. Proven track record of cross-functional insight delivery and \textbf{system observability} improvements in \textbf{Agile/Scrum} environments; experienced in \textbf{distributed systems}, \textbf{REST APIs}, and \textbf{anomaly detection} at HSBC.
}}
\end{itemize}\vspace{-10pt}

%---------- EDUCATION ----------
\section{Education}
\resumeSubHeadingListStart
  \resumeSubheading
    {BITS Pilani, Hyderabad Campus}{2024 -- 2026}
    {M.E. Computer Science}{CGPA: 8.53}
  \resumeSubheading
    {IIT Madras}{2022 -- 2024}
    {Foundation in Data Science and Programming}{CGPA: 5.75}
  \resumeSubheading
    {Sharda University}{2020 -- 2024}
    {B.Tech. Computer Science Engineering}{CGPA: 7.97}
\resumeSubHeadingListEnd\vspace{-4pt}

%---------- EXPERIENCE ----------
\section{Experience}
\resumeSubHeadingListStart

  %---------- REDWOOD ----------
  \resumeSubheading
    {Redwood Software Pvt. Ltd. \textnormal{$|$ Software Engineer}}{India}
    {Java $\cdot$ Spring Boot $\cdot$ Playwright $\cdot$ Cypress $\cdot$ SOAP $\cdot$ Cucumber}{Aug 2026 -- Present}
  \resumeItemListStart
    \resumeItem{Contributing to \textbf{Tidal Workload Automation}, working across its \textbf{5-layer distributed architecture} -- Client, Manager, Master, Agent, and Adapter -- for feature development and core component engineering.}
    \resumeItem{Developing and enhancing \textbf{Java/Spring Boot components} for the \textbf{2027.1 release}, working across core services and distributed job-execution workflows while maintaining compatibility with existing enterprise functionality.}
    \resumeItem{Engineering \textbf{end-to-end test automation} using \textbf{Playwright, Cypress, SOAP, and Cucumber}, covering UI, service, integration, and workload-execution scenarios across multiple Tidal components.}
    \resumeItem{Driving \textbf{product sustainability and defect resolution} through cross-component debugging, root-cause analysis, and regression validation while shadowing the \textbf{2026.4 release} and transitioning ownership toward \textbf{2027.1}.}
  \resumeItemListEnd

  \resumeSubheading
    {HSBC \textnormal{$|$ Analyst Intern -- UK Fraud Analytics}}{India}
    {Python $\cdot$ SQL $\cdot$ Google BigQuery $\cdot$ Agile/Scrum}{Jan 2026 -- Present}
  \resumeItemListStart
    \resumeItem{Evaluated vendor fraud scores across \textbf{3+ fraud typologies} using \textbf{complex SQL on BigQuery}; delivered analytical report confirming \textbf{0\% incremental lift}, preventing an estimated \textbf{\$200K+ misdirected investment} in the UK Cards portfolio.}
    \resumeItem{Validated fraud reduction claims via \textbf{multi-join SQL} across \textbf{5M+ transactions}; built \textbf{KPI baselines} enabling rigorous \textbf{before-vs-after impact measurement} across authentication and \textbf{fraud metrics}.}
    \resumeItem{Built \textbf{Python ML text classification pipeline} using topic modelling to auto-categorize \textbf{10K+ monthly complaints}, targeting \textbf{60\%+ reduction in manual triaging} and improving \textbf{regulatory reporting} accuracy.}
  \resumeItemListEnd

  \resumeSubheading
    {Codinoverse \textnormal{$|$ Software Engineer Intern -- Backend \& Distributed Systems}}{India}
    {Java $\cdot$ Scala $\cdot$ Akka $\cdot$ Apache Kafka $\cdot$ REST APIs $\cdot$ JUnit}{Feb 2024 -- Apr 2024}
  \resumeItemListStart
    \resumeItem{Architected \textbf{5+ distributed microservices} in \textbf{Java, Scala, and Akka} with \textbf{$>$90\% unit test coverage}; applied OOP design patterns for a scalable, production-ready service foundation.}
    \resumeItem{Built \textbf{event-driven pipelines} using \textbf{Apache Kafka} with \textbf{REST API} integration; enhanced \textbf{root-cause analysis} capabilities, reducing mean-time-to-detect incidents by an estimated \textbf{40\%}.}
  \resumeItemListEnd

\resumeSubHeadingListEnd\vspace{-2pt}

%---------- PROJECTS ----------
\section{Projects}
\resumeSubHeadingListStart

  \resumeProjectHeading
    {\textbf{Financial Fraud Signal Dashboard} $|$ \emph{Python, BigQuery, SQL, Airflow, GCP, Looker Studio}}{Jan -- Mar 2025}
  \resumeItemListStart
    \resumeItem{Designed an \textbf{end-to-end fraud analytics pipeline} surfacing real-time \textbf{anomalies} from large-scale operational datasets, enabling faster \textbf{risk and compliance} decisions across business units.}
    \resumeItem{Implemented using \textbf{Python + Apache Airflow} for \textbf{ETL orchestration}, \textbf{BigQuery} for complex joins and aggregations, and \textbf{Looker Studio} for KPI dashboards with \textbf{GCP monitoring} for \textbf{observability}.}
    \resumeItem{Reduced \textbf{anomaly detection latency by 45\%}; dashboards adopted by \textbf{3 cross-functional teams} with \textbf{data validation} coverage improved to \textbf{$>$95\%} across all pipeline stages.}
  \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{CampusBuddy -- Scalable Cloud Chatbot} $|$ \emph{Java, AWS Lambda, DynamoDB, CloudWatch, Amazon Lex}}{Feb -- Mar 2025}
  \resumeItemListStart
    \resumeItem{Engineered a \textbf{serverless backend} on \textbf{AWS Lambda + DynamoDB} handling high-concurrency sessions via \textbf{REST API} and JWT auth; integrated \textbf{microservices architecture} with 3-language NLP via Amazon Lex.}
    \resumeItem{Deployed \textbf{CloudWatch monitoring and alerting} for \textbf{production observability}; achieved \textbf{$<$200ms latency}, zero cold-start failures, and \textbf{30\% reduction in operational overhead} through \textbf{process optimization}.}
  \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{Distributed Task Scheduler} $|$ \emph{C++, POSIX Threads, Mutexes, Futures/Promises}}{Aug -- Sep 2024}
  \resumeItemListStart
    \resumeItem{Built a \textbf{C++ concurrent task scheduling library} over a dynamic worker thread pool; implemented \textbf{priority-based scheduling} with async execution via \textbf{futures/promises} and thread safety via \textbf{mutexes}.}
    \resumeItem{Enabled \textbf{dynamic thread pool resizing} and task cancellation; achieved \textbf{zero race conditions} at full load and improved estimated throughput by \textbf{35\%} -- validating \textbf{scalable distributed systems} design.}
  \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{Distributed Key-Value Store} $|$ \emph{Java, gRPC, Consistent Hashing, Docker Compose}}{2025}
  \resumeItemListStart
    \resumeItem{Built a \textbf{distributed key-value store} in Java implementing a \textbf{consistent hash ring} for data partitioning across nodes; supports \textbf{quorum-based replication} (read/write quorums) for fault tolerance.}
    \resumeItem{Designed \textbf{gRPC-based inter-node communication} with a \textbf{gossip protocol} for membership and failure detection; containerised the full cluster using \textbf{Docker Compose} for local multi-node testing.}
    \resumeItem{Validated correctness under \textbf{node failure scenarios} -- data remains accessible as long as quorum is maintained; documented replication lag and recovery behaviour in the README.}
  \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{PayFlow -- UPI-Style Payments Backend} $|$ \emph{Java, Spring Boot, MySQL, REST APIs, JWT}}{2025}
  \resumeItemListStart
    \resumeItem{Engineered a \textbf{Spring Boot REST API} simulating a UPI payments backend with \textbf{account management, fund transfers, and transaction history} endpoints; secured with \textbf{JWT-based authentication}.}
    \resumeItem{Implemented \textbf{optimistic locking and DB transactions} in \textbf{MySQL} to prevent double-spend race conditions under concurrent transfer requests; validated with \textbf{JUnit integration tests}.}
    \resumeItem{Structured using \textbf{layered architecture} (Controller -> Service -> Repository) with \textbf{DTO validation, global exception handling}, and Swagger/OpenAPI documentation for all endpoints.}
  \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{RideWise -- Ride-Hailing LLD} $|$ \emph{Java, SOLID Principles, Strategy Pattern, OOP}}{2025}
  \resumeItemListStart
    \resumeItem{Designed a \textbf{low-level object-oriented system} for a ride-hailing platform covering \textbf{driver matching, fare calculation, and ride lifecycle management} using \textbf{SOLID principles}.}
    \resumeItem{Applied \textbf{Strategy pattern} for pluggable fare strategies (base, surge, premium) and \textbf{Factory pattern} for ride-type creation; structured for extensibility without modifying existing classes.}
  \resumeItemListEnd

\resumeSubHeadingListEnd\vspace{-2pt}

%---------- TECHNICAL SKILLS ----------
\section{Technical Skills}
\begin{itemize}[leftmargin=0.12in, label={}]
\small{\item{
\textbf{Languages:} Python, Java, SQL, Scala, C++, JavaScript \\[0.5pt]
\textbf{Data \& Analytics:} Google BigQuery, Apache Airflow, ETL Pipelines, Apache Kafka, Anomaly Detection, Data Validation, MySQL, DynamoDB, NoSQL \\[0.5pt]
\textbf{Systems \& Backend:} Microservices, REST APIs, Event-Driven Architecture, Distributed Systems, Akka, Spring Boot \\[0.5pt]
\textbf{Cloud \& Observability:} AWS (Lambda, DynamoDB, S3, CloudWatch), GCP (BigQuery, Looker Studio), Azure, Docker \\[0.5pt]
\textbf{Engineering Practices:} Agile/Scrum, Root-Cause Analysis, System Observability, Cross-Functional Collaboration, CI/CD, Git
}}
\end{itemize}\vspace{-4pt}

%---------- POSITIONS OF RESPONSIBILITY ----------
\section{Positions of Responsibility}
\resumeSubHeadingListStart
  \resumeProjectHeading{\textbf{Teaching Assistant} $|$ \textnormal{BITS Pilani -- Operating Systems \& Algorithms}}{Sep 2024 -- Dec 2025}
  \resumeProjectHeading{\textbf{Junior Placement Coordinator} $|$ \textnormal{BITS Pilani, Hyderabad}}{Aug 2024 -- Dec 2024}
\resumeSubHeadingListEnd

\end{document}"""

RESUME_V2 = r"""\documentclass[10.5pt]{article}
\usepackage[top=0.5in, bottom=0.5in, left=0.6in, right=0.6in]{geometry}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\pagestyle{empty}

\titleformat{\section}
  {\vspace{-4pt}\scshape\raggedright\normalsize}{}{0em}{}[\titlerule\vspace{-3pt}]

\setlist[itemize]{leftmargin=*, itemsep=0pt, topsep=1pt, parsep=0pt}
\setlength{\parskip}{0pt}
\setlength{\parsep}{0pt}
\linespread{0.96}

\begin{document}

\begin{center}
  {\Large \textbf{SAI ROHIT SHAIK}} \\
  \vspace{2pt}
  \small
  +91-6301411795 $\cdot$
  \href{mailto:sai.rohit.shaik@gmail.com}{sai.rohit.shaik@gmail.com} $\cdot$
  \href{https://linkedin.com/in/sk-sai-rohit}{linkedin.com/in/sk-sai-rohit} $\cdot$
  Hyderabad, India
\end{center}
\vspace{-8pt}

\section{Summary}
\vspace{1pt}
Specialist Programmer with expertise in \textbf{AI/ML, Python, SQL, and distributed systems}.
Proven track record of building scalable, AI-powered digital solutions and delivering measurable
business impact in enterprise environments.
\vspace{-6pt}

\section{Education}
\textbf{BITS Pilani, Hyderabad} \hfill 2024 -- 2026 \\
M.E. Computer Science \hfill CGPA: 8.53 \\[2pt]
\textbf{Sharda University} \hfill 2020 -- 2024 \\
B.Tech Computer Science Engineering \hfill CGPA: 7.97
\vspace{-6pt}

\section{Experience}

%---------- REDWOOD ----------
\textbf{Software Engineer -- Redwood Software Pvt. Ltd. India} \hfill Aug 2026 -- Present \\
\textit{Java, Spring Boot, Playwright, Cypress, SOAP, Cucumber, Workload Automation}
\begin{itemize}
  \item Contributing to \textbf{Tidal Workload Automation}, working across its \textbf{5-layer distributed architecture} -- Client, Manager, Master, Agent, and Adapter -- for feature development and core component engineering.
  \item Developing and enhancing \textbf{Java/Spring Boot components} for the \textbf{2027.1 release}, working across core services and distributed job-execution workflows while maintaining compatibility with existing enterprise functionality.
  \item Engineering \textbf{end-to-end test automation} using \textbf{Playwright, Cypress, SOAP, and Cucumber}, covering UI, service, integration, and workload-execution scenarios across multiple Tidal components.
  \item Driving \textbf{product sustainability and defect resolution} through cross-component debugging, root-cause analysis, and regression validation while shadowing the \textbf{2026.4 release} and transitioning ownership toward \textbf{2027.1}.
\end{itemize}

\vspace{-2pt}
\textbf{Analyst Intern -- Fraud Analytics, HSBC India} \hfill Jan 2026 -- Present \\
\textit{Python, SQL, BigQuery, Machine Learning, Scikit-learn, Agile}
\begin{itemize}
  \item Developed \textbf{ML-powered fraud detection and classification models} using Python and
        Scikit-learn for vendor scoring and complaint triage, improving risk-identification
        accuracy by \textbf{18\%} across UK Cards Fraud Strategy workflows
  \item Analyzed large-scale fraud datasets via \textbf{SQL on BigQuery}; debugged \textbf{15+
        production incidents} through structured root-cause analysis, reducing resolution
        time and improving system observability
  \item Engineered \textbf{automated data validation pipelines} cutting manual effort by
        \textbf{40\%} and enhancing data quality across AI-powered fraud analytics systems
\end{itemize}

\vspace{-2pt}
\textbf{Software Engineer Intern -- Backend Systems, Codinoverse} \hfill Feb 2024 -- Mar 2024 \\
\textit{Java, Scala, Apache Kafka, Microservices, REST APIs}
\begin{itemize}
  \item Architected \textbf{event-driven microservices} in Java/Scala with Apache Kafka,
        enabling real-time data processing and improving backend scalability and fault tolerance
  \item Optimized \textbf{REST APIs and distributed backend services}, reducing API response
        latency by \textbf{30\%} and strengthening production monitoring and observability
\end{itemize}
\vspace{-6pt}

\section{Projects}

\textbf{CampusBuddy -- AI-Powered Serverless Chatbot} \hfill 2025 \\
\textit{Amazon Lex, AWS Lambda, DynamoDB, REST APIs, AWS Cognito, CloudWatch, React}
\begin{itemize}
  \item Built a \textbf{GenAI-powered serverless chatbot} to automate campus information
        queries using NLP-driven intent recognition, eliminating manual support overhead
        for \textbf{1,000+ users} and enabling real-time, context-aware responses
  \item Implemented using \textbf{Amazon Lex, AWS Lambda, and DynamoDB} with an event-driven
        serverless architecture, REST API integration, and secure authentication via AWS Cognito
  \item Achieved \textbf{$<$200ms response latency} with 99.5\% uptime; deployed CloudWatch
        monitoring dashboards enabling proactive anomaly detection, reducing incident
        resolution time by \textbf{25\%}
\end{itemize}

\vspace{-2pt}
\textbf{Financial Fraud Signal Dashboard} \hfill Jan -- Mar 2025 \\
\textit{Python, BigQuery, SQL, Apache Airflow, GCP, Looker Studio}
\begin{itemize}
  \item Designed an \textbf{end-to-end fraud analytics pipeline} surfacing real-time \textbf{anomalies}
        from large-scale operational datasets, enabling faster \textbf{risk and compliance} decisions
  \item Implemented \textbf{Python + Apache Airflow} for ETL orchestration, \textbf{BigQuery} for
        complex joins and aggregations, and \textbf{Looker Studio} for KPI dashboards with GCP monitoring
  \item Reduced \textbf{anomaly detection latency by an estimated 45\%}; improved \textbf{data validation}
        coverage to \textbf{$>$95\%} across all pipeline stages
\end{itemize}

\vspace{-2pt}
\textbf{Distributed Key-Value Store} \hfill 2025 \\
\textit{Java, gRPC, Consistent Hashing, Quorum Replication, Docker Compose}
\begin{itemize}
  \item Built a \textbf{distributed key-value store} in Java with a \textbf{consistent hash ring}
        for data partitioning; implemented \textbf{quorum-based replication} for fault tolerance
  \item Designed \textbf{gRPC inter-node communication} with gossip-based failure detection;
        containerised full cluster using \textbf{Docker Compose} for multi-node testing
\end{itemize}

\vspace{-2pt}
\textbf{PayFlow -- UPI-Style Payments Backend} \hfill 2025 \\
\textit{Java, Spring Boot, MySQL, REST APIs, JWT, JUnit}
\begin{itemize}
  \item Engineered a \textbf{Spring Boot REST API} for UPI-style payments with account management,
        fund transfers, and transaction history; secured with \textbf{JWT authentication}
  \item Implemented \textbf{optimistic locking and DB transactions} in MySQL to prevent double-spend
        race conditions; validated with \textbf{JUnit integration tests} and OpenAPI documentation
\end{itemize}

\vspace{-2pt}
\textbf{RideWise -- Ride-Hailing LLD} \hfill 2025 \\
\textit{Java, SOLID Principles, Strategy Pattern, Factory Pattern, OOP}
\begin{itemize}
  \item Designed a \textbf{low-level OOP system} for ride-hailing covering driver matching, fare
        calculation, and ride lifecycle using \textbf{SOLID principles} and \textbf{Strategy pattern}
        for pluggable fare strategies (base, surge, premium)
\end{itemize}
\vspace{-6pt}

\section{Technical Skills}
\textbf{Languages:} Python, Java, SQL, C, C++, Scala \\
\textbf{AI / ML:} Machine Learning, Scikit-learn, NLP, Predictive Modeling, Fraud Analytics \\
\textbf{Data \& Engineering:} Data Pipelines, ETL, BigQuery, Distributed Systems, Apache Kafka \\
\textbf{Cloud \& Tools:} AWS (Lambda, DynamoDB, S3, CloudWatch, Lex), GCP, REST APIs, Git \\
\textbf{Databases:} MySQL, DynamoDB, Oracle, NoSQL \\
\textbf{Practices:} Agile, Microservices, Root-Cause Analysis, Automation, Monitoring
\vspace{-6pt}

\section{Positions of Responsibility}
Teaching Assistant, BITS Pilani \hfill 2024 -- 2025 \\
Junior Placement Coordinator, BITS Pilani \hfill 2024

\end{document}"""

# ── Prompts ────────────────────────────────────────────────────────────────────

ATS_SYSTEM_PROMPT = """You are a senior technical recruiter and resume editor helping a final-year M.E. Computer Science student (fresher/intern-level profile) tailor their LaTeX resume to a specific job description.

CANDIDATE CONTEXT
- Profile level: Fresher / new grad. Two internships, personal projects, strong academics.
- Core identity to preserve: Backend/SDE engineer with fraud analytics internship experience.
- Do NOT reposition the candidate as a frontend, quant, infrastructure, network, or ML research engineer purely to chase JD keywords. Keep the identity stable.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1 — JD ANALYSIS & KEYWORD EXTRACTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Extract the 10–12 most important keywords/skills from the JD.
Classify each as:
  🔴 CRITICAL   — must appear if genuinely supported by experience
  🟡 IMPORTANT  — include if it fits naturally into existing bullets
  🟢 BONUS      — include only if it doesn't distort meaning

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 2 — PROJECT SELECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The candidate has 6 existing projects on file. Showing all 6 on a one-page resume is a primary cause of overflow and of generic, padded-out bullets — never include more than 3 projects in the output.

Select at most 3 projects, prioritising in this order:
  1. Direct technology/domain overlap with the JD
  2. Depth of defensible, specific outcome over a project with vaguer claims
  3. Coverage — across the 2-3 chosen projects, span different JD requirement areas rather than 3 projects proving the same single skill

If the candidate's Experience section already demonstrates the JD's top requirements, 2 projects is enough — do not pad to 3 just to fill space.
Drop the remaining projects entirely from the LaTeX output — do not compress them into a single line or keep a placeholder.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 3 — CONTENT REWRITING RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE CONSTRAINT: Every bullet must be credible and defensible in a 30-second recruiter phone screen. Prioritise honesty and specificity over impressiveness.

Bullet structure: What → How → Impact (where impact exists)

METRICS POLICY — strictly follow these rules:
  ✅ ALLOWED: Metrics already present in the resume (keep them)
  ✅ ALLOWED: Directly measurable outcomes from the work described (e.g. "10K+ records processed", "5 microservices built")
  ✅ ALLOWED: Estimates that are clearly labelled and have a defensible basis (e.g. "estimated 40% reduction based on manual timing")
  ❌ BANNED: Inventing percentage improvements with no stated basis
  ❌ BANNED: Fabricating scale claims (millions of transactions, 1000 TPS, 99.9% uptime) unless literally in the original resume
  ❌ BANNED: Adding metrics purely to fill gaps — if no metric exists, describe the outcome qualitatively

BANNED PHRASES for a fresher profile (remove or replace):
  - "production-grade", "enterprise-grade", "world-class"
  - "large-scale distributed systems", "proven expertise"
  - "fault-tolerant systems" (unless directly built and testable)
  - "millions of transactions" (unless literally true and stated in original)
  - "zero cold-start failures" (replace with measured latency data if available)

HONEST ALTERNATIVES to use instead:
  - "load-tested to ~X req/sec on [instance type]"
  - "built and deployed", "implemented and verified"
  - "reduced by an estimated X% based on [specific basis]"
  - "handles concurrent sessions via [mechanism]"

KEYWORD INTEGRATION:
  - Add keywords only where they fit naturally into existing content
  - Do not add a technology to the Skills section if it does not appear in any bullet
  - Do not mirror every JD term verbatim if the candidate hasn't actually used it
  - Skipping a keyword is better than forcing it awkwardly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 4 — ONE-PAGE FITTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Font: 10–10.5pt. Margins: 0.5–0.75in.
Priority order for trimming: weakest bullets first, then vspace adjustments, then font/margin as last resort.
Do not remove entire sections or roles to fit.
The final page must visually fill to the bottom edge — it must neither spill onto a second page nor leave a visible gap of blank space beneath the last section. If trimming leaves the page undershooting (visible dead space at the bottom), restore a previously-cut bullet or loosen \vspace values rather than leaving the bottom of the page empty.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 5 — OUTPUT FORMAT (STRICT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LaTeX output between exact markers:
===LATEX_START===
[full latex code]
===LATEX_END===

Report between exact markers:
===REPORT_START===
🔑 KEYWORDS ADDED:
[keyword — section it was placed in — one-line justification]

🚫 KEYWORDS SKIPPED:
[keyword — why it wasn't added honestly]

✅ CREDIBILITY CHECK:
[List any bullet that still sounds potentially inflated for a fresher profile, with a suggested fix]

📐 PAGE-FIT CHANGES:
[What was trimmed or adjusted and why]

🎯 GAP ANALYSIS:
[JD requirements genuinely not covered by the candidate's background — be direct]

📌 PROJECTS USED THIS RUN:
[Which of the 6 existing projects were kept (max 3) and which were dropped, with a one-line reason each]
===REPORT_END==="""

ATS_SYSTEM_PROMPT_GROUNDED = ATS_SYSTEM_PROMPT + """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GROUNDED MODE — EXTRA CREDIBILITY AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
After completing the optimization, perform a strict credibility pass:

For EVERY bullet in the final resume, ask:
  "Could a recruiter on a 30-second call ask the candidate to explain this claim, and would the candidate be able to answer confidently?"

If the answer is NO or MAYBE for any bullet:
  - Flag it explicitly in the Credibility Check section of the report
  - Rewrite it to a version that passes the test, even if it sounds less impressive
  - Add a [GROUNDED] tag next to the rewritten bullet in the report

Additionally add to the report:
🔍 GROUNDED MODE AUDIT:
[List every bullet that was revised in the credibility pass, showing original → revised version]"""

PROJECT_SUGGESTION_ADDENDUM = """

PROJECT SUGGESTION: If you detect a critical skill gap that is not covered by any existing project, suggest ONE new buildable project using the markers below.

IMPORTANT PROJECT RULES:
- The project must be genuinely buildable in 1–2 weeks
- It must result in a GitHub repo with a README, deployed demo, or architecture diagram — something a recruiter can verify
- Do not suggest projects that would require fabricating production-scale metrics
- Clearly mark suggested metrics as "in a local/test environment" if applicable

===PROJECT_START===
[PROJECT NAME]: [name]
[REPLACES]: [which existing project, and why that one]
[WHY]: [specific JD gap this addresses]
[VERIFICATION]: [what the candidate should have on GitHub/deployed before using this on the resume]

RESUME ENTRY:
[full 3-bullet latex entry ready to paste — metrics must follow the METRICS POLICY above]

BUILD GUIDE:
[concrete 1–2 week step-by-step plan with specific tools/libraries]
===PROJECT_END==="""


def parse_credibility_flags(report_text):
    """Count credibility flags from the report."""
    count = 0
    if "✅ CREDIBILITY CHECK:" in report_text:
        section = report_text.split("✅ CREDIBILITY CHECK:")[1].split("📐")[0]
        lines = [l.strip() for l in section.strip().split("\n") if l.strip()]
        clean = [l for l in lines if l.lower() not in ("none", "none.", "no issues found.", "no issues.")]
        count = len(clean)
    return count


def parse_keywords_added(report_text):
    """Count keywords added from the report."""
    count = 0
    if "🔑 KEYWORDS ADDED:" in report_text:
        section = report_text.split("🔑 KEYWORDS ADDED:")[1].split("🚫")[0]
        lines = [l.strip() for l in section.strip().split("\n") if l.strip() and "—" in l]
        count = len(lines)
    return count


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Curated ranking heuristic — used to sort/prioritise whatever free models
# OpenRouter is currently offering. Free model IDs churn often, so we never
# hardcode a single model: we fetch the live catalog and rank it.
# Substring -> priority score (higher = tried first). Coding-capable, large
# MoE reasoning models rank above small/omni/safety models.
MODEL_PRIORITY_HINTS = [
    ("coder", 100), ("qwen3-coder", 100),
    ("laguna-m", 92), ("laguna", 85),
    ("nemotron-3-ultra", 90), ("nemotron", 70),
    ("deepseek", 88),
    ("hy3", 75), ("glm", 80),
    ("north-mini-code", 72), ("code", 65),
    ("kimi", 78), ("mimo", 76),
    ("llama-3.3-70b", 60), ("llama", 50),
    ("gpt-oss", 68),
    ("gemma", 45),
    ("content-safety", -100), ("guardrail", -100), ("moderation", -100),
    ("omni", 30),  # multimodal/perception models — deprioritised for a text/LaTeX task
]

# Models known to hang or misbehave unless "thinking"/reasoning is turned off
NO_THINKING_SUBSTRINGS = ["deepseek", "hy3", "nemotron"]


def _priority_score(model_id: str) -> int:
    score = 0
    low = model_id.lower()
    for substr, weight in MODEL_PRIORITY_HINTS:
        if substr in low:
            score += weight
    return score


@st.cache_data(ttl=600, show_spinner=False)
def fetch_free_models(_api_key_present: bool):
    """Query OpenRouter's live model catalog and return free (:free / $0)
    text-output models, ranked best-first. Cached 10 min so we don't spam
    the endpoint on every rerun. Falls back to a small static list if the
    request fails (e.g. no network)."""
    fallback = [
        "qwen/qwen3-coder:free",
        "deepseek/deepseek-v4-flash:free",
        "poolside/laguna-m.1:free",
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "meta-llama/llama-3.3-70b-instruct:free",
    ]
    try:
        resp = requests.get(f"{OPENROUTER_BASE_URL}/models", timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        free_ids = []
        for m in data:
            pricing = m.get("pricing", {}) or {}
            try:
                is_free = float(pricing.get("prompt", "1")) == 0 and float(pricing.get("completion", "1")) == 0
            except (TypeError, ValueError):
                is_free = False
            out_modalities = (m.get("architecture") or {}).get("output_modalities", ["text"])
            if is_free and "text" in out_modalities:
                free_ids.append(m["id"])
        if not free_ids:
            return fallback
        free_ids.sort(key=_priority_score, reverse=True)
        return free_ids
    except Exception:
        return fallback


def run_optimization(resume_code, jd_text, suggest_project, grounded_mode, api_key, model, fallback_models=None):
    """Call an OpenRouter free model (OpenAI-compatible endpoint) and return
    parsed outputs. On failure (rate limit, model temporarily down, etc.)
    automatically retries with the next model in fallback_models."""
    client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)

    system_prompt = ATS_SYSTEM_PROMPT_GROUNDED if grounded_mode else ATS_SYSTEM_PROMPT

    if suggest_project:
        project_instruction = PROJECT_SUGGESTION_ADDENDUM
    else:
        project_instruction = "\n\nDo NOT suggest new projects — optimize using existing content only."

    user_prompt = f"""JOB DESCRIPTION:
{jd_text}

MY CURRENT LATEX RESUME CODE:
{resume_code}
{project_instruction}

Please perform the full optimization and output in the exact format specified."""

    models_to_try = [model] + [m for m in (fallback_models or []) if m != model]
    last_error = None
    used_model = model

    for candidate in models_to_try:
        try:
            kwargs = dict(
                model=candidate,
                max_tokens=8000,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                extra_headers={
                    "HTTP-Referer": "https://github.com/sairohitsk/ats-resume",
                    "X-Title": "ATS Resume Optimizer",
                },
            )
            # Some free reasoning models (DeepSeek, Hy3, Nemotron) hang or
            # burn the whole budget on hidden reasoning tokens unless it's
            # explicitly disabled.
            if any(s in candidate.lower() for s in NO_THINKING_SUBSTRINGS):
                kwargs["extra_body"] = {"reasoning": {"enabled": False}}

            completion = client.chat.completions.create(**kwargs)
            text = completion.choices[0].message.content or ""
            if not text.strip():
                raise ValueError("Empty response from model")
            used_model = candidate
            last_error = None
            break
        except Exception as e:
            last_error = e
            time.sleep(0.5)
            continue

    if last_error is not None:
        raise RuntimeError(
            f"All models failed. Tried: {', '.join(models_to_try)}. Last error: {last_error}"
        )

    latex_match   = re.search(r'===LATEX_START===([\s\S]*?)===LATEX_END===', text)
    report_match  = re.search(r'===REPORT_START===([\s\S]*?)===REPORT_END===', text)
    project_match = re.search(r'===PROJECT_START===([\s\S]*?)===PROJECT_END===', text)

    return {
        "latex":   latex_match.group(1).strip()   if latex_match   else text,
        "report":  report_match.group(1).strip()   if report_match  else "",
        "project": project_match.group(1).strip()  if project_match else "",
        "raw":     text,
        "used_model": used_model,
    }


# ── Session state init ─────────────────────────────────────────────────────────
if "resume_v1"      not in st.session_state: st.session_state.resume_v1      = RESUME_V1
if "resume_v2"      not in st.session_state: st.session_state.resume_v2      = RESUME_V2
if "results"        not in st.session_state: st.session_state.results        = None
if "active_version" not in st.session_state: st.session_state.active_version = "v1"

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ ATS Optimizer")
    st.markdown("<p style='color:#6b7590;font-size:12px'>by Sai Rohit Shaik</p>", unsafe_allow_html=True)
    st.divider()

    # API Key
    st.markdown("**🔑 OpenRouter API Key**")
    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        placeholder="sk-or-v1-...",
        help="Free — get your key at openrouter.ai/keys (no card required)",
        label_visibility="collapsed"
    )
    if api_key:
        st.markdown('<span class="badge badge-green">✓ Key loaded</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-red">⚠ Key required</span>', unsafe_allow_html=True)

    st.divider()

    # Resume version selector
    st.markdown("**📄 Resume Version**")
    version = st.selectbox(
        "Select version",
        ["v1 — Detailed (fullpage)", "v2 — Compact (geometry)"],
        label_visibility="collapsed"
    )
    st.session_state.active_version = "v1" if "v1" in version else "v2"

    # Edit resume
    with st.expander("✏️ Edit / Update Resume"):
        current_code = st.session_state.resume_v1 if st.session_state.active_version == "v1" else st.session_state.resume_v2
        new_code = st.text_area(
            "Resume LaTeX",
            value=current_code,
            height=300,
            label_visibility="collapsed"
        )
        if st.button("💾 Save Changes"):
            if st.session_state.active_version == "v1":
                st.session_state.resume_v1 = new_code
            else:
                st.session_state.resume_v2 = new_code
            st.success("Resume updated!")

    st.divider()

    # Options
    st.markdown("**⚙️ Options**")

    grounded_mode = st.checkbox(
        "🛡️ Grounded Mode — credibility audit",
        value=True,
        help="Performs an extra pass flagging every bullet that couldn't be defended in a recruiter call. Produces an original → revised audit in the report."
    )
    if grounded_mode:
        st.markdown('<span class="badge badge-green">✓ Credibility audit active</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-yellow">⚠ Credibility audit off</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    suggest_project = st.checkbox(
        "💡 Suggest project if skill gap found",
        value=True,
        help="If a critical JD skill isn't covered, the model will suggest a buildable project with a GitHub-verifiable output — not just a metrics-heavy claim."
    )

    st.divider()

    # ── Model switcher ─────────────────────────────────────────────────────────
    st.markdown("**🤖 Model (OpenRouter — free tier)**")

    col_refresh, _ = st.columns([1, 2])
    with col_refresh:
        if st.button("🔄 Refresh", help="Free model lineup on OpenRouter changes often — re-check the live catalog"):
            fetch_free_models.clear()

    free_models = fetch_free_models(bool(api_key))

    if not free_models:
        st.warning("Couldn't reach OpenRouter's model catalog. Check your internet connection.")
        selected_model = "qwen/qwen3-coder:free"
        fallback_models = []
    else:
        def _label(m):
            return m.replace(":free", "") + "  🆓"

        selected_model = st.selectbox(
            "Model",
            free_models,
            index=0,
            format_func=_label,
            label_visibility="collapsed",
            help="Ranked best-first for coding/LaTeX quality among currently free OpenRouter models. "
                 "If your pick is rate-limited or down, the app automatically retries with the next one."
        )
        # Everything else in the ranked list becomes the automatic fallback chain
        fallback_models = [m for m in free_models if m != selected_model][:4]
        st.markdown(f'<span class="badge badge-green">₹0 per run · {len(free_models)} free models available</span>', unsafe_allow_html=True)
        if fallback_models:
            st.caption(f"Fallback chain: {' → '.join(m.replace(':free','') for m in fallback_models[:3])}")

    st.divider()
    st.markdown(
        "<p style='color:#6b7590;font-size:11px'>Output: 1-page LaTeX + credibility report<br>100% free · No card, no subscription · Powered by OpenRouter</p>",
        unsafe_allow_html=True
    )

# ── MAIN AREA ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>⚡ ATS Resume Optimizer</h1>
  <p>Paste a Job Description · Get a tailored one-page LaTeX resume + credibility report</p>
</div>
""", unsafe_allow_html=True)

# JD Input
st.markdown("**📋 Job Description**")
jd_input = st.text_area(
    "JD",
    placeholder="Paste the full Job Description here — the more detail, the better the optimization...",
    height=220,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    jd_len = len(jd_input.split()) if jd_input else 0
    resume_version_label = st.session_state.active_version.upper()
    mode_label = "Grounded" if grounded_mode else "Standard"
    st.markdown(
        f"<p style='color:#6b7590;font-size:11px;margin-top:4px'>JD: {jd_len} words · Base: Resume {resume_version_label} · Mode: {mode_label}</p>",
        unsafe_allow_html=True
    )
with col3:
    run = st.button("⚡ Optimize Resume", disabled=not (api_key and jd_input.strip()))

# ── RUN ────────────────────────────────────────────────────────────────────────
if run:
    active_resume = st.session_state.resume_v1 if st.session_state.active_version == "v1" else st.session_state.resume_v2

    with st.spinner(""):
        progress_placeholder = st.empty()
        steps = [
            "🔍 Analysing JD — extracting & classifying keywords...",
            "🎯 Mapping keywords to resume sections...",
            "✍️  Rewriting bullets with credibility constraints...",
            "📐 Fitting content to exactly one page...",
            "🛡️  Running credibility audit..." if grounded_mode else "📊 Generating optimization report...",
        ]
        for i, step in enumerate(steps):
            progress_placeholder.markdown(
                f"<p style='color:#4f8ef7;font-size:13px'>{'✓ ' * i}{step}</p>",
                unsafe_allow_html=True
            )

        try:
            results = run_optimization(
                active_resume, jd_input, suggest_project, grounded_mode, api_key, selected_model,
                fallback_models=fallback_models
            )
            results["model"]    = results.get("used_model", selected_model)
            results["grounded"] = grounded_mode
            st.session_state.results = results
            progress_placeholder.empty()
            st.success("✅ Optimization complete!")
        except Exception as e:
            progress_placeholder.empty()
            st.error(f"❌ Error: {str(e)}")
            st.info("Check your API key and internet connection.")

# ── RESULTS ────────────────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results

    keywords_added    = parse_keywords_added(r["report"])
    credibility_flags = parse_credibility_flags(r["report"])

    # Grounded mode banner
    if r.get("grounded"):
        st.markdown("""
        <div class="grounded-banner">
            🛡️ <strong>Grounded Mode was active.</strong>
            Every bullet was audited for recruiter-defensibility. Check the Credibility Audit tab for any flags and rewrites.
        </div>
        """, unsafe_allow_html=True)

    # Summary metrics
    st.divider()
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""<div class="info-card">
            <div class="info-val">{keywords_added or "—"}</div>
            <div class="info-label">Keywords Added</div>
        </div>""", unsafe_allow_html=True)

    with m2:
        flag_color = "#f76f72" if credibility_flags > 0 else "#3ecf8e"
        st.markdown(f"""<div class="cred-card">
            <div class="cred-val" style="-webkit-text-fill-color:{flag_color};color:{flag_color}">{credibility_flags}</div>
            <div class="cred-label">Flags Found</div>
        </div>""", unsafe_allow_html=True)

    with m3:
        model_used = r.get("model", "")
        model_label = model_used.split("/")[-1].replace(":free", "") if model_used else "—"
        mode_label = "Grounded" if r.get("grounded") else "Standard"
        st.markdown(f"""<div class="info-card">
            <div class="info-val" style="font-size:13px">{model_label}</div>
            <div class="info-label">{mode_label} Mode</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Output tabs
    tab_labels = ["📄 LaTeX Code", "📊 Optimization Report"]
    if r.get("grounded"):
        tab_labels.append("🛡️ Credibility Audit")
    if r.get("project"):
        tab_labels.append("💡 Project Suggestion")

    tabs = st.tabs(tab_labels)

    # Tab: LaTeX
    with tabs[0]:
        col_a, col_b = st.columns([5, 1])
        with col_b:
            st.download_button(
                "⬇️ Download",
                data=r["latex"],
                file_name="resume_optimized.tex",
                mime="text/plain"
            )
        st.code(r["latex"], language="latex")

    # Tab: Optimization Report
    with tabs[1]:
        if r["report"]:
            report_display = r["report"]
            if "🔍 GROUNDED MODE AUDIT:" in report_display:
                report_display = report_display.split("🔍 GROUNDED MODE AUDIT:")[0].strip()
            st.text(report_display)
        else:
            st.info("Report not found in output. Check the Raw tab if needed.")

    # Tab: Credibility Audit (grounded mode only)
    if r.get("grounded"):
        with tabs[2]:
            if r["report"] and "🔍 GROUNDED MODE AUDIT:" in r["report"]:
                audit_section = r["report"].split("🔍 GROUNDED MODE AUDIT:")[1].strip()
                if credibility_flags == 0:
                    st.markdown('<span class="badge badge-green">✓ No credibility flags — all bullets passed</span>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<span class="badge badge-orange">⚠ {credibility_flags} bullet(s) flagged and revised</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown("<br>", unsafe_allow_html=True)
                st.text(audit_section)
            elif r["report"] and "✅ CREDIBILITY CHECK:" in r["report"]:
                cred_section = r["report"].split("✅ CREDIBILITY CHECK:")[1].split("📐")[0].strip()
                st.text(cred_section)
            else:
                st.info("No credibility audit found in this run's output.")

    # Tab: Project Suggestion
    if r.get("project"):
        with tabs[-1]:
            st.markdown('<span class="badge badge-blue">✨ Suggested Project</span>', unsafe_allow_html=True)
            st.markdown("""
            <p style='color:#f5c842;font-size:12px;margin-top:8px'>
            ⚠️ Only add this to your resume after the GitHub repo is live with a README and/or deployed demo.
            A suggested project with no verifiable output hurts more than it helps.
            </p>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.text(r["project"])

else:
    st.divider()
    st.markdown("""
    <div style="text-align:center;padding:2rem;color:#6b7590">
        <div style="font-size:40px;margin-bottom:12px">🎯</div>
        <p style="font-size:14px">Add your API key in the sidebar, paste a JD above, and hit <strong style="color:#4f8ef7">Optimize Resume</strong></p>
        <p style="font-size:12px;margin-top:8px">Your base resume (v1 & v2) is already loaded · Grounded Mode is on by default</p>
    </div>
    """, unsafe_allow_html=True)
