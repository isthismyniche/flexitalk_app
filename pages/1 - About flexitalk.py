from helper_functions.utility import check_password  
import streamlit as st

# Check if the password is correct.  
if not check_password():  
    st.stop()

st.header("About _flexitalk_")

st.divider()

st.markdown("""
## Project Scope

_flexitalk_ is a platform for supervisors to **practise having difficult conversations** with their staff about **flexible work arrangements**, and to explore the types of flexible work arrangements that may be most suitable in their business context.

Flexible work arrangements, and **telecommuting in particular**, are a contested topic in today’s workplace. While the **COVID-19 pandemic transformed the landscape of flexible work**, in 2024 many businesses have implemented full-time return-to-office mandates. Given the **importance of flexible work arrangements to employees**, this sets the scene for a flashpoint between businesses and employees, with supervisors placed in the **unenviable position** of enforcing company policies while keeping staff engaged.

_flexitalk_ is an attempt to use **Large Language Models** and **Retrieval Augmented Generation (RAG)** to develop chatbots that can assist supervisors in navigating this reality.

This project was undertaken as part of the **Whole-of-Government Artificial Intelligence (AI) Bootcamp 2024**. Participants were required to complete a capstone project that featured their key takeaways from the bootcamp. It is the developer’s first published web application!

---

## Features

### Practise _flexitalk_
This feature allows supervisors to **prepare for a difficult conversation** with their staff about flexible work arrangements. Supervisors can put themselves in the shoes of their staff and pose **challenging questions and lines of inquiry** that they anticipate. The bot will respond as a supervisor, which will help the user imagine different ways to navigate the situation and arrive at an **amicable and fruitful outcome** with their staff.

### Unlock _flexiwork_
This feature allows supervisors to **brainstorm and unlock flexible work arrangements** that are suitable for their business context. While company policy may restrict the range of options for arrangements such as telecommuting, there are many other flexible work arrangements that supervisors can explore to benefit their staff. This bot is well-versed in **Singapore’s tripartite guidelines** for flexible work arrangements, as well as the latest global trends and research, and will provide **valuable insights** for curious supervisors.

---

## Data Sources

### Practise _flexitalk_
Developed using prompt engineering on OpenAI’s **GPT-4o-mini**, without any additional data sources for ingestion.

### Unlock _flexiwork_
Developed using **GPT-4o-mini**, and ingested the following publicly-available data sources for RAG:

**Information from MOM and Tripartite Alliance Limited:**
- Conditions of Employment Survey, 2022
- FAQs on Tripartite Guidelines about Flexible Work Arrangements
- Types of Flexible Work Arrangements (MOM)
- Tripartite Guidelines on Flexible Work Arrangement Requests
- Tripartite Work Group Report on Flexible Work Arrangements

**Information from research and consultancy:**
- Why does working from home vary across countries and people (Zarate et al, 2024)
- Global survey of working arrangements (Aksoy et al, 2023)
- The evolution of work from home (Barrero et al, 2023)
- Time savings from working from home (Aksoy et al, 2023)
- A new future of work (McKinsey, 2024)
- What is the future of work (McKinsey, 2023)
- Defining the skills citizens will need in the future of work (McKinsey, 2021)
- The future of work after COVID-19 (McKinsey, 2021)
""")
