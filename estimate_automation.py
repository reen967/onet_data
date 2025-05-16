import pandas as pd
import os

# Set CSV file names (assumed to be in root directory)
def estimate_automation(soc_code: str, root: str = "./") -> pd.DataFrame:
    # Load relevant files
    tasks = pd.read_csv(os.path.join(root, "task_statements.csv"))
    task_ratings = pd.read_csv(os.path.join(root, "task_ratings.csv")) if os.path.exists(os.path.join(root, "task_ratings.csv")) else pd.DataFrame()
    tasks_to_dwa = pd.read_csv(os.path.join(root, "tasks_to_dwa.csv"))
    dwa_map = pd.read_csv(os.path.join(root, "work_activities_to_iwa_to_dwa.csv"))
    abilities_link = pd.read_csv(os.path.join(root, "abilities_to_work_activities.csv"))
    abilities = pd.read_csv(os.path.join(root, "abilities.csv"))
    abilities_context = pd.read_csv(os.path.join(root, "abilities_to_work_context.csv"))
    work_context = pd.read_csv(os.path.join(root, "work_context_1.csv"))
    context_categories = pd.read_csv(os.path.join(root, "work_context_categories.csv"))
    scales = pd.read_csv(os.path.join(root, "scales_reference.csv"))

    # Step 1: Get tasks for SOC
    soc_tasks = tasks[tasks["O*NET-SOC Code"] == soc_code]

    # Step 2: Add task ratings if available
    if not task_ratings.empty:
        soc_tasks = soc_tasks.merge(task_ratings, on="Task ID", how="left")

    # Step 3: Map to DWAs
    dw_ids = tasks_to_dwa[tasks_to_dwa["Task ID"].isin(soc_tasks["Task ID"])]

    # Step 4: Map DWAs to Work Activities
    wa_links = dwa_map[dwa_map["DWA Element ID"].isin(dw_ids["DWA ID"])]

    # Step 5: Map to Abilities
    ability_links = abilities_link[abilities_link["Work Activities Element Name"].isin(wa_links["Work Activities Element Name"])]
    ability_names = ability_links["Abilities Element Name"].unique()

    # Step 6: Get ability importance levels
    soc_abilities = abilities[(abilities["O*NET-SOC Code"] == soc_code) & (abilities["Abilities Element Name"].isin(ability_names))]
    soc_abilities = soc_abilities[soc_abilities["Scale Name"] == "Importance"]

    # Normalize using scale reference
    scale_max = scales.set_index("Scale ID")["Maximum"].to_dict()
    soc_abilities["Norm Importance"] = soc_abilities.apply(lambda x: x["Data Value"] / scale_max.get(x["Scale ID"], 5), axis=1)

    # Step 7: Get context variables for SOC
    soc_context = work_context[work_context["O*NET-SOC Code"] == soc_code]
    context_with_cat = soc_context.merge(context_categories, on="Work Context Element Name", how="left")

  # Simplified automation likelihood estimation (basic weights)
    avg_freq = soc_tasks["Data Value"].mean() if "Data Value" in soc_tasks else 0.5
    avg_ability = soc_abilities["Norm Importance"].mean() if not soc_abilities.empty else 0.5
    physical_difficulty = context_with_cat[context_with_cat["Work Context Element Name"].str.contains("Physical", na=False)]["Data Value"].mean()
    social_difficulty = context_with_cat[context_with_cat["Work Context Element Name"].str.contains("Social", na=False)]["Data Value"].mean()

    # Compute rough automation score (lower means less automatable)
    score = (1 * avg_freq + 0.5 * (1 - avg_ability) + 0.5 * (1 - physical_difficulty / 5) + 0.5 * (1 - social_difficulty / 5)) / 2.5

    result = pd.DataFrame({
        "SOC Code": [soc_code],
        "Avg Task Frequency": [avg_freq],
        "Avg Ability Importance": [avg_ability],
        "Physical Context Demand": [physical_difficulty],
        "Social Context Demand": [social_difficulty],
        "Automation Likelihood Score (0-1)": [round(score, 3)]
    })

    return result
