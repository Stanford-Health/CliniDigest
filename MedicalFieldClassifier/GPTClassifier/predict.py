import openai
openai.api_key = "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"

def get_completion(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def predict(clinical_trials_descriptions):
    full_results = []
    for clinical_trial_description in clinical_trials_descriptions:
        prompt = ("Given the following classes of \"Somnology\", \"Gynecology\", \"Obstetrics\", \"Cardiology\", \"General Physiology\", \"Endocrinology\", \"Bariatrics\", \"Psychiatry\", \"Oncology\", \"Gastroenterology\", \"Pulmonology\", \"Chronic pain / diseases\", \"Other\" annotate one, two, or three classes for the following clinical trial. Note that a clinical trial doesn't necessarily need to have a secondary or tertiary medical field, but only one field should be in the primary, secondary, and tertiary fields" + clinical_trial_description)[0:4096]
        response = get_completion([{"role": "user", "content": prompt}])
        full_results.append(response)
    
    predicted_labels = [[] for _ in range(len(full_results))]
    # Note: Gastroenterolgy is omitted because it is barely labelled in manual data
    medical_fields = ["Somnology", "Gynecology", "Obstetrics", "Cardiology", "General Physiology", "Endocrinology", "Bariatrics", "Psychiatry", "Oncology", "Pulmonology", "Chronic pain/diseases", "Other"]

    for i in range(len(full_results)):
        for medical_field in medical_fields:
            if medical_field in full_results[i]:
                predicted_labels[i].append(medical_field)
        
    return predicted_labels