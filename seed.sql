INSERT INTO users(name,email,phone_number) VALUES
 ('Rahim Uddin','rahim@example.com','+8801712345678'),
 ('Nusrat Jahan','nusrat@example.com','+8801812345678');
INSERT INTO resumes(user_id,title,address,linkedin,career_objective) VALUES
 (1,'Software Engineer Resume','Dhaka, Bangladesh','linkedin.com/in/rahim','Motivated CSE graduate seeking a backend developer role.'),
 (2,'Data Analyst Resume','Chattogram, Bangladesh','','Detail-oriented analyst skilled in turning data into insight.');
INSERT INTO education(resume_id,institution,degree,graduation_year,result) VALUES
 (1,'North South University','BSc in Computer Science and Engineering',2024,'CGPA 3.62/4.00'),
 (2,'BUET','BSc in Statistics',2023,'CGPA 3.80/4.00');
INSERT INTO experience(resume_id,company,job_title,duration,responsibilities) VALUES
 (1,'TechNova Ltd','Intern Developer','Jun 2023 - Dec 2023','Built REST APIs with Flask and wrote unit tests.'),
 (2,'DataWorks','Junior Analyst','Jan 2024 - Present','Created dashboards and weekly KPI reports.');
INSERT INTO skills(resume_id,skill_name,category) VALUES
 (1,'Python','technical'),(1,'Flask','technical'),(1,'SQL','technical'),(1,'Teamwork','soft'),
 (1,'English','language'),(1,'Bangla','language'),(1,'AWS Cloud Practitioner','certification'),
 (2,'Excel','technical'),(2,'Power BI','technical'),(2,'Communication','soft'),(2,'English','language');
