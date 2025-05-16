import pandas as pd
from flask import Flask, render_template, request

# Initialize the Flask app
app = Flask(__name__)

# Load CSV files
abilities = pd.read_csv('data/abilities.csv')
work_context_categories = pd.read_csv('data/work_context_categories.csv')
frequency_of_task_categories = pd.read_csv('data/frequency_of_task_categories.csv')
scales_reference = pd.read_csv('data/scales_reference.csv')

# Merge the data to easily work with the scales
abilities_with_scale = pd.merge(abilities, scales_reference, on='Scale ID', how='inner')
work_context_with_scale = pd.merge(work_context_categories, scales_reference, on='Scale ID', how='inner')
frequency_with_scale = pd.merge(frequency_of_task_categories, scales_reference, on='Scale ID', how='inner')

@app.route('/')
def home():
    # Retrieve possible filter options
    scale_names = scales_reference['Scale Name'].unique()
    return render_template('index.html', scale_names=scale_names)

@app.route('/filter_results', methods=['POST'])
def filter_results():
    # Get the selected scale and filter inputs
    selected_scale_name = request.form['scale_name']
    selected_data_value = float(request.form['data_value'])

    # Filter data based on selected Scale Name
    filtered_abilities = abilities_with_scale[abilities_with_scale['Scale Name'] == selected_scale_name]
    filtered_abilities = filtered_abilities[filtered_abilities['Data Value'] >= selected_data_value]

    filtered_work_context = work_context_with_scale[work_context_with_scale['Scale Name'] == selected_scale_name]
    filtered_work_context = filtered_work_context[filtered_work_context['Data Value'] >= selected_data_value]

    filtered_frequency = frequency_with_scale[frequency_with_scale['Scale Name'] == selected_scale_name]
    filtered_frequency = filtered_frequency[filtered_frequency['Data Value'] >= selected_data_value]

    # Handle dynamic filter for context-based scale (e.g., CXP)
    context_options = []
    if selected_scale_name == "Context":
        context_options = filtered_work_context['Work Context Element Name'].unique()

    # Return the filtered results and context-specific options
    return render_template('index.html', scale_names=scales_reference['Scale Name'].unique(),
                           filtered_abilities=filtered_abilities.to_html(),
                           filtered_work_context=filtered_work_context.to_html(),
                           filtered_frequency=filtered_frequency.to_html(),
                           selected_scale_name=selected_scale_name,
                           selected_data_value=selected_data_value,
                           context_options=context_options)

if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
