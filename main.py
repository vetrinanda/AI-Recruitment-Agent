from app.main import process_application

def main():
    # Use the sample resume text for better testing
    sample_resume = """
**ALEX JOHNSON**
Seattle, WA 98101 | (555) 123-4567 | alex.johnson@email.com | linkedin.com/in/alexjohnson | github.com/alexjohnson

**SUMMARY**
Recent Computer Science graduate with hands-on experience in software development, network administration, and technical support. Strong problem-solving abilities with a passion for learning new technologies and delivering user-focused solutions.

**EDUCATION**
**Bachelor of Science in Computer Science**
University of Washington, Seattle, WA
Graduated: May 2024 | GPA: 3.6/4.0

Relevant Coursework: Data Structures, Database Management, Network Security, Web Development, Operating Systems

**TECHNICAL SKILLS**
- **Programming Languages:** Python, Java, JavaScript, SQL, HTML/CSS
- **Tools & Technologies:** Git, Linux, Windows Server, MySQL, MongoDB, React, Node.js
- **Networking:** TCP/IP, DNS, DHCP, VPN configuration
- **Certifications:** CompTIA A+ (in progress), Google IT Support Professional Certificate

**EXPERIENCE**
**IT Support Intern**
TechStart Solutions, Seattle, WA | June 2023 – August 2023
- Provided technical support to 50+ end users, resolving hardware and software issues with 95% first-contact resolution rate
- Assisted in maintaining network infrastructure and troubleshooting connectivity issues
- Created documentation for common IT procedures, reducing ticket resolution time by 20%
- Helped deploy new workstations and performed software installations and updates

**Computer Lab Assistant**
University of Washington, Seattle, WA | September 2022 – May 2024
- Assisted students and faculty with technical issues across 100+ workstations
- Maintained computer lab equipment and performed routine maintenance tasks
- Managed printer systems and resolved printing-related issues
- Provided basic training on software applications including Microsoft Office and Adobe Creative Suite

**PROJECTS**
**Personal Portfolio Website** | October 2023
- Developed responsive personal website using React and Node.js to showcase projects and skills
- Implemented contact form with backend email functionality and deployed on AWS

**Network Security Lab** | March 2024
- Configured virtual network environment to simulate common security threats
- Implemented firewall rules and intrusion detection systems using pfSense and Snort

**ADDITIONAL INFORMATION**
- Active member of University Cybersecurity Club
- Volunteer tech support for local non-profit organization (10 hours/month)
- Fluent in English and Spanish

"""

    print("--- Test Case 1: Senior Python Dev ---")
    result = process_application(application_text=sample_resume, job_role="Python Developer")
    print("Final Result:", result)

    print("\n--- Test Case 2: Marketing Role (Mismatch) ---")
    result_mismatch = process_application(application_text=sample_resume, job_role="Marketing Manager")
    print("Final Result:", result_mismatch)

if __name__ == "__main__":
    main()
