import pandas as pd

# Load all CSV files into pandas DataFrames
abilities = pd.read_csv('abilities.csv')
abilities_descriptions = pd.read_csv('abilities_descriptions.csv')
abilities_to_work_activities = pd.read_csv('abilities_to_work_activities.csv')
abilities_to_work_context = pd.read_csv('abilities_to_work_context.csv')
alternate_titles = pd.read_csv('alternate_titles.csv')
basic_interests_to_riasec = pd.read_csv('basic_interests_to_riasec.csv')
content_model_reference = pd.read_csv('content_model_reference.csv')
frequency_of_task_categories = pd.read_csv('frequency_of_task_categories.csv')
interests = pd.read_csv('interests.csv')
interests_to_illustrative_activities = pd.read_csv('interests_to_illustrative_activities.csv')
interests_to_illustrative_occupations = pd.read_csv('interests_to_illustrative_occupations.csv')
interests_to_riasec_keywords = pd.read_csv('interests_to_riasec_keywords.csv')
knowledge = pd.read_csv('knowledge.csv')
level_scale_anchors = pd.read_csv('level_scale_anchors.csv')
occupation_data = pd.read_csv('occupation_data.csv')
related_occupations = pd.read_csv('related_occupations.csv')
scales_reference = pd.read_csv('scales_reference.csv')
skills = pd.read_csv('skills.csv')
skills_to_work_activities = pd.read_csv('skills_to_work_activities.csv')
skills_to_work_context = pd.read_csv('skills_to_work_context.csv')
task_statements = pd.read_csv('task_statements.csv')
tasks_to_dwa = pd.read_csv('tasks_to_dwa.csv')
technology_skills = pd.read_csv('technology_skills.csv')
tools_used = pd.read_csv('tools_used.csv')
unspsc_reference = pd.read_csv('unspsc_reference.csv')
work_activities = pd.read_csv('work_activities.csv')
work_activities_to_iwa = pd.read_csv('work_activities_to_iwa.csv')
work_activities_to_iwa_to_dwa = pd.read_csv('work_activities_to_iwa_to_dwa.csv')
work_context_categories = pd.read_csv('work_context_categories.csv')

# Bilateral Linkages:

# 1. Linking abilities.csv with abilities_descriptions.csv (via Abilities Element ID)
abilities_with_descriptions = pd.merge(abilities, abilities_descriptions, on='Abilities Element ID', how='inner')

# 2. Linking abilities.csv with abilities_to_work_activities.csv (via Abilities Element ID)
abilities_with_activities = pd.merge(abilities_with_descriptions, abilities_to_work_activities, on='Abilities Element ID', how='inner')

# 3. Linking abilities_to_work_activities.csv with work_activities.csv (via Work Activities Element ID)
abilities_with_work_activities = pd.merge(abilities_with_activities, work_activities, on='Work Activities Element ID', how='inner')

# 4. Linking abilities.csv with abilities_to_work_context.csv (via Abilities Element ID)
abilities_with_context = pd.merge(abilities_with_descriptions, abilities_to_work_context, on='Abilities Element ID', how='inner')

# 5. Linking abilities_to_work_context.csv with work_context_categories.csv (via Work Context Element ID)
abilities_with_work_context_categories = pd.merge(abilities_with_context, work_context_categories, on='Work Context Element ID', how='inner')

# 6. Linking occupation_data.csv with abilities.csv (via O*NET-SOC Code)
occupation_with_abilities = pd.merge(occupation_data, abilities_with_work_activities, on='O*NET-SOC Code', how='inner')

# 7. Linking occupation_data.csv with skills.csv (via O*NET-SOC Code)
occupation_with_skills = pd.merge(occupation_data, skills, on='O*NET-SOC Code', how='inner')

# 8. Linking skills_to_work_activities.csv with skills.csv (via Skills Element ID)
skills_with_activities = pd.merge(skills, skills_to_work_activities, on='Skills Element ID', how='inner')

# 9. Linking skills_to_work_context.csv with skills.csv (via Skills Element ID)
skills_with_context = pd.merge(skills_with_activities, skills_to_work_context, on='Skills Element ID', how='inner')

# 10. Linking task_statements.csv with skills.csv (via O*NET-SOC Code)
task_with_skills = pd.merge(task_statements, skills_with_context, on='O*NET-SOC Code', how='inner')

# 11. Linking tasks_to_dwa.csv with task_statements.csv (via Task ID)
task_with_dwa = pd.merge(task_with_skills, tasks_to_dwa, on='Task ID', how='inner')

# 12. Linking technology_skills.csv with occupation_data.csv (via O*NET-SOC Code)
technology_with_occupation = pd.merge(technology_skills, occupation_data, on='O*NET-SOC Code', how='inner')

# 13. Linking tools_used.csv with occupation_data.csv (via O*NET-SOC Code)
tools_with_occupation = pd.merge(tools_used, occupation_data, on='O*NET-SOC Code', how='inner')

# 14. Linking interests_to_illustrative_occupations.csv with occupation_data.csv (via O*NET-SOC Code)
interests_with_occupations = pd.merge(interests_to_illustrative_occupations, occupation_data, on='O*NET-SOC Code', how='inner')

# 15. Linking work_activities_to_iwa.csv with work_activities.csv (via Work Activities Element ID)
work_activities_with_iwa = pd.merge(work_activities_to_iwa, work_activities, on='Work Activities Element ID', how='inner')

# 16. Linking work_activities_to_iwa_to_dwa.csv with work_activities_to_iwa.csv (via Work Activities Element ID)
work_activities_with_dwa = pd.merge(work_activities_with_iwa, work_activities_to_iwa_to_dwa, on='Work Activities Element ID', how='inner')

# 17. Linking work_context_categories.csv with work_activities_to_iwa.csv (via Work Context Element ID)
work_context_with_activities = pd.merge(work_context_categories, work_activities_with_dwa, on='Work Context Element ID', how='inner')

# 18. Linking unspsc_reference.csv with tools_used.csv (via Commodity Code)
tools_with_unspsc = pd.merge(tools_used, unspsc_reference, on='Commodity Code', how='inner')

# 19. Linking alternate_titles.csv with occupation_data.csv (via O*NET-SOC Code)
occupation_with_alternate_titles = pd.merge(occupation_data, alternate_titles, on='O*NET-SOC Code', how='inner')

# Now all the relevant DataFrames are linked with bilateral relations

# Example: Displaying a snippet of the merged data
print(occupation_with_abilities.head())
print(occupation_with_skills.head())
print(task_with_dwa.head())
print(work_context_with_activities.head())
