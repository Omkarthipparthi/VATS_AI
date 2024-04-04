jobs = {"1": {"Job Title": "Data & Systems Assistant (FWS Eligible)", "Matching Score": "90%", "Description": "The applicant has a Master's degree in Computer Science and a Bachelor's degree in Electronics and Instrumentation Engineering. His technical skills, which include Python, C++, HTML/CSS, JavaScript, SQL, and GraphQL, are a great fit for a data and systems role. He has experience with AWS, which could be useful in problem-solving and project management. His work experience as a Software Engineer also demonstrates his ability to work in a team environment and complete tasks independently, which is a requirement for this job."},
"2": {"Job Title": "Front Office Aide (FWS Eligible)", "Matching Score": "75%", "Description": "The applicant has strong technical skills and experience in customer service, which would be valuable in a front office role. His experience in software engineering also demonstrates his ability to work independently and as part of a team and his strong problem-solving skills, which is necessary for this role. However, his qualifications and skills seem to be more suited for a technical job."},
"3": {"Job Title": "Summer Community Assistant: West Housing ", "Matching Score": "65%", "Description": "While the applicant does not have direct experience in residential life or community assistance, his leadership experience in software engineering projects demonstrates his ability to manage tasks and work in a team. His strong communication skills, which are evident from his customer service experience, would also be beneficial in this role. However, his technical skills and qualifications seem to be underutilized in this position."}}

op = ""
for i in jobs:
    op += i + "\n"
    for j in jobs[i].keys():
        op += j + ": " + jobs[i][j] +"\n"

print(op)