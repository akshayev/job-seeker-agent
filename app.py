import streamlit as st
import backend

# 1. Setup
st.set_page_config(page_title="Job Seeker AI Agent", page_icon="🕵️‍♂️", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "resume_summary" not in st.session_state:
    st.session_state.resume_summary = None
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "generated_kits" not in st.session_state:
    st.session_state.generated_kits = {}

# Configure APIs
backend.configure_apis()

# 2. Sidebar
with st.sidebar:
    st.title("🕵️‍♂️ Job Seeker AI")
    st.markdown("Upload your resume to get started.")
    
    uploaded_file = st.file_uploader("Upload Resume (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Check if this file has already been analyzed
        if "analyzed_file_id" not in st.session_state or st.session_state.analyzed_file_id != uploaded_file.file_id:
            with st.spinner("Analyzing your resume automatically..."):
                summary = backend.analyze_resume(uploaded_file)
                if summary:
                    st.session_state.resume_summary = summary
                    st.session_state.analyzed_file_id = uploaded_file.file_id
                    st.success("Resume analyzed successfully!")
        
        # Always show summary if available
        if st.session_state.resume_summary:
            st.expander("View Summary").write(st.session_state.resume_summary)

# 3. Chat Interface
st.title("Find Your Dream Job")
st.markdown("Chat with the agent to find jobs that match your profile.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("What kind of job are you looking for?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Logic Flow
    with st.chat_message("assistant"):
        if not st.session_state.resume_summary:
            st.warning("Please upload and analyze your resume first!")
            st.session_state.messages.append({"role": "assistant", "content": "Please upload and analyze your resume first!"})
        else:
            # b. Generate Search Query
            with st.status("Searching for jobs...", expanded=True) as status:
                st.write("Translating request to search query...")
                search_query = backend.generate_search_query(prompt)
                st.write(f"Query: `{search_query}`")
                
                # c. Search Jobs
                st.write("Fetching job listings...")
                jobs = backend.search_jobs(search_query)
                
                if not jobs:
                    status.update(label="No jobs found.", state="error")
                    st.error("No jobs found. Try a different query.")
                    st.session_state.messages.append({"role": "assistant", "content": "No jobs found. Try a different query."})
                else:
                    # CRITICAL: Save results to session state
                    st.session_state.search_results = jobs
                    st.session_state.generated_kits = {} # Clear old kits
                    
                    status.update(label="Jobs found! Analyzing matches...", state="running")
                    
                    # Analyze matches immediately for the new results
                    analyzed_jobs = []
                    progress_bar = st.progress(0)
                    total_jobs = len(jobs)
                    
                    for i, job in enumerate(jobs):
                        match_data = backend.analyze_job_match(st.session_state.resume_summary, str(job))
                        job['match_score'] = match_data.get("score", 0)
                        job['match_reason'] = match_data.get("reason", "No reason provided.")
                        analyzed_jobs.append(job)
                        progress_bar.progress((i + 1) / total_jobs)
                    
                    st.session_state.search_results = analyzed_jobs # Update with analysis
                    
                    status.update(label="Search and Analysis Complete!", state="complete")
                    st.session_state.messages.append({"role": "assistant", "content": f"Found and analyzed {len(jobs)} jobs for you."})

# 4. Display Loop (Outside Input Block)
if st.session_state.search_results:
    st.divider()
    st.subheader(f"Found {len(st.session_state.search_results)} Jobs")
    
    for i, job in enumerate(st.session_state.search_results):
        score = job.get('match_score', 0)
        reason = job.get('match_reason', "No reason provided.")
        
        # Color code based on score
        color = "🟢" if score >= 70 else "🟡" if score >= 40 else "🔴"
        expander_label = f"{color} {score}% Match: {job['Title']}"
        
        # Expand if kit generated
        is_expanded = (i in st.session_state.generated_kits)
        
        with st.expander(expander_label, expanded=is_expanded):
            st.markdown(f"**Company/Source:** [{job['Link']}]({job['Link']})")
            st.markdown(f"**Snippet:** {job['Snippet']}")
            st.markdown(f"**Match Reason:** {reason}")
            
            # Check if kit is already generated
            if i in st.session_state.generated_kits:
                st.subheader("Cover Letter")
                cover_letter = st.session_state.generated_kits[i]
                st.code(cover_letter, language='markdown')
                
                # Generate PDF
                pdf_data = backend.create_pdf(cover_letter)
                if pdf_data:
                    st.download_button(
                        label="Download Cover Letter (PDF)",
                        data=pdf_data,
                        file_name=f"Cover_Letter_{job['Title']}.pdf",
                        mime="application/pdf",
                        key=f"dl_{i}"
                    )
            else:
                # Generate Application Button
                if st.button(f"Generate Application for {job['Title']}", key=f"btn_{i}"):
                    with st.spinner("Generating application kit..."):
                        company_name = "the company" 
                        cover_letter = backend.generate_application_kit(st.session_state.resume_summary, job['Title'], company_name)
                        
                        # Save to session state
                        st.session_state.generated_kits[i] = cover_letter
                        st.rerun()
