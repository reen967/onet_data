import pandas as pd
import os

def task_automation_breakdown(soc_code: str, root: str = "./") -> pd.DataFrame:
    tasks = pd.read_csv(os.path.join(root, "task_statements.csv"))
    task_ratings_1 = pd.read_csv(os.path.join(root, "task_ratings_1.csv"))
    task_ratings_2 = pd.read_csv(os.path.join(root, "task_ratings_2.csv"))
    task_ratings = pd.concat([task_ratings_1, task_ratings_2], ignore_index=True)
    task_freq_scale = pd.read_csv(os.path.join(root, "task_frequency_scale.csv"))
    tasks_to_dwa = pd.read_csv(os.path.join(root, "tasks_to_dwa.csv"))
    dwa_map = pd.read_csv(os.path.join(root, "work_activities_to_iwa_to_dwa.csv"))
    abilities_link = pd.read_csv(os.path.join(root, "abilities_to_work_activities.csv"))
    abilities = pd.read_csv(os.path.join(root, "abilities.csv"))
    abilities_context = pd.read_csv(os.path.join(root, "abilities_to_work_context.csv"))
    wc1 = pd.read_csv(os.path.join(root, "work_context_1.csv"))
    wc2 = pd.read_csv(os.path.join(root, "work_context_2.csv"))
    work_context = pd.concat([wc1, wc2], ignore_index=True)
    context_categories = pd.read_csv(os.path.join(root, "work_context_categories.csv"))
    context_levels = pd.read_csv(os.path.join(root, "context_level_scale.csv"))
    scales = pd.read_csv(os.path.join(root, "scales_reference.csv"))
    anchors = pd.read_csv(os.path.join(root, "ability_level_anchors.csv"))

    scale_max = scales.set_index("Scale ID")["Maximum"].to_dict()
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

        # Add anchor descriptions for abilities
        ability_scores = ability_scores.merge(
            anchors[anchors["Scale ID"] == "LV"].groupby("Abilities Element Name").apply(lambda g: g.sort_values("Anchor Value").iloc[-1]).reset_index(drop=True)[["Abilities Element Name", "Anchor Description"]],
            on="Abilities Element Name",
            how="left"
        )

        ability_summary = ", ".join([
            f"{row['Abilities Element Name']} ({round(row['Norm Score'], 2)}): {row['Anchor Description']}"
            for _, row in ability_scores.iterrows()
        ])

        ability_contexts = abilities_context[abilities_context["Abilities Element Name"].isin(ability_names)]
        context_traits = work_context[(work_context["O*NET-SOC Code"] == soc_code) &
                                      (work_context["Work Context Element Name"].isin(ability_contexts["Work Context Element Name"]))]

        context_with_labels = context_traits.merge(
            context_categories,
            on=["Work Context Element ID", "Work Context Element Name"],
            how="left"
        ).merge(
            context_levels,
            on=["Work Context Element ID", "Scale ID", "Category"],
            how="left"
        )

        context_summary = ", ".join([
            f"{row['Work Context Element Name']} ({row['Category Description']})"
            for _, row in context_with_labels.iterrows()
        ])

        social_demand = context_with_labels[context_with_labels["Category"].notna() & context_with_labels["Category"].astype(str).str.contains("Social")]["Category"].astype(float).mean()
        physical_demand = context_with_labels[context_with_labels["Category"].notna() & context_with_labels["Category"].astype(str).str.contains("Physical")]["Category"].astype(float).mean()

        cog_load = ability_scores["Norm Score"].mean() if not ability_scores.empty else 0.5
        social_load = social_demand if not pd.isna(social_demand) else 2.5
        phys_load = physical_demand if not pd.isna(physical_demand) else 2.5

        automation_score = round(1 - ((cog_load + (social_load / 5) + (phys_load / 5)) / 3), 3)

        # Add frequency of task
        task_freq_row = task_ratings[(task_ratings["Task ID"] == task_id) & (task_ratings["Scale ID"] == "FT")]
        freq_cat = task_freq_row["Category"].values[0] if not task_freq_row.empty else None
        freq_label = task_freq_scale[task_freq_scale["Category"] == freq_cat]["Category Description"].values[0] if freq_cat in task_freq_scale["Category"].values else "Unknown"

        result_rows.append({
            "Task": task_text,
            "Work Activities": ", ".join(work_acts),
            "Abilities": ability_summary,
            "Context Traits": context_summary,
            "Social Demand": round(social_load, 2) if not pd.isna(social_demand) else "N/A",
            "Physical Demand": round(phys_load, 2) if not pd.isna(physical_demand) else "N/A",
            "Cognitive Load": round(cog_load, 2),
            "Frequency": freq_label,
            "Estimated Automation Likelihood (0–1)": automation_score
        })

    return pd.DataFrame(result_rows)
