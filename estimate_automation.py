import pandas as pd
import os

def task_automation_breakdown(soc_code: str, root: str = "./") -> pd.DataFrame:
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
    anchors = pd.read_csv(os.path.join(root, "level_scale_anchors.csv"))

    scale_max = scales.set_index("Scale ID")["Maximum"].to_dict()
    anchor_map = anchors[anchors["Scale Name"] == "Level"].set_index(["Abilities Element Name", "Anchor Value"])["Anchor Description"].to_dict()

    soc_tasks = tasks[tasks["O*NET-SOC Code"] == soc_code]
    result_rows = []

    for _, task_row in soc_tasks.iterrows():
        task_id = task_row["Task ID"]
        task_text = task_row["Task Title"]

        dwa_ids = tasks_to_dwa[tasks_to_dwa["Task ID"] == task_id]["DWA ID"].unique()
        work_acts = dwa_map[dwa_map["DWA Element ID"].isin(dwa_ids)]["Work Activities Element Name"].unique()

        relevant_abilities = abilities_link[abilities_link["Work Activities Element Name"].isin(work_acts)]
        ability_names = relevant_abilities["Abilities Element Name"].unique()

        ability_scores = abilities[(abilities["O*NET-SOC Code"] == soc_code) &
                                   (abilities["Abilities Element Name"].isin(ability_names)) &
                                   (abilities["Scale Name"] == "Importance")].copy()

        ability_scores["Norm Score"] = ability_scores.apply(
            lambda x: x["Data Value"] / scale_max.get(x["Scale ID"], 5), axis=1
        )

        ability_with_anchor = []
        for _, row in ability_scores.iterrows():
            name = row["Abilities Element Name"]
            norm = round(row["Norm Score"], 2)
            val = round(row["Data Value"])
            desc = anchor_map.get((name, val), "")
            ability_with_anchor.append(f"{name} ({norm}) - {desc}")

        ability_summary = "; ".join(ability_with_anchor)

        ability_contexts = abilities_context[abilities_context["Abilities Element Name"].isin(ability_names)]
        context_traits = work_context[(work_context["O*NET-SOC Code"] == soc_code) &
                                      (work_context["Work Context Element Name"].isin(ability_contexts["Work Context Element Name"]))]

        context_with_labels = context_traits.merge(
            context_categories,
            on=["Work Context Element ID", "Work Context Element Name"],
            how="left"
        )

        context_summary = ", ".join([
            f"{row['Work Context Element Name']} ({row['Category']})"
            for _, row in context_with_labels.iterrows()
        ])

        social_demand = context_with_labels[context_with_labels["Category"].str.contains("Social", na=False)]
        physical_demand = context_with_labels[context_with_labels["Category"].str.contains("Physical", na=False)]

        cog_load = ability_scores["Norm Score"].mean() if not ability_scores.empty else 0.5
        social_load = social_demand["Data Value"].mean() if not social_demand.empty else 2.5
        phys_load = physical_demand["Data Value"].mean() if not physical_demand.empty else 2.5

        automation_score = round(1 - ((cog_load + (social_load / 5) + (phys_load / 5)) / 3), 3)

        result_rows.append({
            "Task": task_text,
            "Work Activities": ", ".join(work_acts),
            "Abilities": ability_summary,
            "Context Traits": context_summary,
            "Social Demand": round(social_load, 2) if not pd.isna(social_load) else "N/A",
            "Physical Demand": round(phys_load, 2) if not pd.isna(phys_load) else "N/A",
            "Cognitive Load": round(cog_load, 2),
            "Estimated Automation Likelihood (0–1)": automation_score
        })

    return pd.DataFrame(result_rows)
