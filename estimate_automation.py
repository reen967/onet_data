import pandas as pd
import os

def task_automation_breakdown(soc_code: str, root: str = "./") -> pd.DataFrame:
    # Load all required files
    tasks = pd.read_csv(os.path.join(root, "task_statements.csv"))
    tasks_to_dwa = pd.read_csv(os.path.join(root, "tasks_to_dwa.csv"))
    dwa_map = pd.read_csv(os.path.join(root, "work_activities_to_iwa_to_dwa.csv"))
    abilities_link = pd.read_csv(os.path.join(root, "abilities_to_work_activities.csv"))
    abilities = pd.read_csv(os.path.join(root, "abilities.csv"))
    abilities_context = pd.read_csv(os.path.join(root, "abilities_to_work_context.csv"))
    wc1 = pd.read_csv(os.path.join(root, "work_context_1.csv"))
    wc2 = pd.read_csv(os.path.join(root, "work_context_2.csv"))
    work_context = pd.concat([wc1, wc2], ignore_index=True)
    context_categories = pd.read_csv(os.path.join(root, "work_context_categories.csv"))
    scales = pd.read_csv(os.path.join(root, "scales_reference.csv"))

    # Normalize scale values
    scale_max = scales.set_index("Scale ID")["Maximum"].to_dict()

    # Get tasks for SOC
    soc_tasks = tasks[tasks["O*NET-SOC Code"] == soc_code]
    result_rows = []

    for _, task_row in soc_tasks.iterrows():
        task_id = task_row["Task ID"]
        task_text = task_row["Task Title"]

        # Map to DWA
        dwa_links = tasks_to_dwa[tasks_to_dwa["Task ID"] == task_id]["DWA ID"].unique()
        work_acts = dwa_map[dwa_map["DWA Element ID"].isin(dwa_links)]["Work Activities Element Name"].unique()

        # Map to abilities
        relevant_abilities = abilities_link[abilities_link["Work Activities Element Name"].isin(work_acts)]
        ability_names = relevant_abilities["Abilities Element Name"].unique()

        ability_scores = abilities[
            (abilities["O*NET-SOC Code"] == soc_code) &
            (abilities["Abilities Element Name"].isin(ability_names)) &
            (abilities["Scale Name"] == "Importance")
        ].copy()

        ability_scores["Norm Score"] = ability_scores.apply(
            lambda x: x["Data Value"] / scale_max.get(x["Scale ID"], 5), axis=1
        )

        ability_summary = ", ".join([
            f"{row['Abilities Element Name']} ({round(row['Norm Score'],2)})"
            for _, row in ability_scores.iterrows()
        ])

        # Map abilities to work context traits
        ability_contexts = abilities_context[
            abilities_context["Abilities Element Name"].isin(ability_names)
        ]

        context_traits = work_context[
            (work_context["O*NET-SOC Code"] == soc_code) &
            (work_context["Work Context Element Name"].isin(ability_contexts["Work Context Element Name"]))
        ]

        context_with_labels = context_traits.merge(
            context_categories, on="Work Context Element Name", how="left"
        )

        social_demand = context_with_labels[
            context_with_labels["Work Context Element Name"].str.contains("Social", na=False)
        ]["Data Value"].mean()

        physical_demand = context_with_labels[
            context_with_labels["Work Context Element Name"].str.contains("Physical", na=False)
        ]["Data Value"].mean()

        # Compute automation score
        cog_load = ability_scores["Norm Score"].mean() if not ability_scores.empty else 0.5
        social_load = social_demand if not pd.isna(social_demand) else 2.5
        phys_load = physical_demand if not pd.isna(physical_demand) else 2.5

        # Simplified model: more cognitive, physical, social → lower automability
        automation_score = round(1 - ((cog_load + (social_load / 5) + (phys_load / 5)) / 3), 3)

        result_rows.append({
            "Task": task_text,
            "Work Activities": ", ".join(work_acts),
            "Abilities": ability_summary,
            "Social Demand": round(social_load, 2) if not pd.isna(social_demand) else "N/A",
            "Physical Demand": round(phys_load, 2) if not pd.isna(physical_demand) else "N/A",
            "Cognitive Load": round(cog_load, 2),
            "Estimated Automation Likelihood (0–1)": automation_score
        })

    return pd.DataFrame(result_rows)

