import os
import json
import base64
import requests
import argparse
import numpy as np
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer, util

# --- Configuration ---
ENDPOINT_URL = "https://ggmnc9stoewr89x4.us-east-1.aws.endpoints.huggingface.cloud"
HF_TOKEN = os.getenv("HF_TOKEN")
# ---

def image_to_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"❌ Error: Image file not found at '{path}'.")
        return None

def query_hf_endpoint(image_path, prompt):
    base64_image = image_to_base64(image_path)
    if not base64_image:
        return "Error: Could not encode image."

    payload = {
        "prompt": prompt,
        "image_b64": base64_image,
        "max_new_tokens": 200,
        "lora_path": "Abdulmateen/llava-finetuned"
    }
    
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(ENDPOINT_URL, headers=headers, json={"inputs": payload}, timeout=120)
        
        if response.status_code != 200:
            return f"Error: Request failed with status code {response.status_code}. Details: {response.text}"

        response_json = response.json()
        
        # --- FIX IS HERE ---
        # Handles the case where the response is a dictionary: {'generated_text': '...'}
        if isinstance(response_json, dict) and 'generated_text' in response_json:
            return response_json['generated_text']
        # Handles the original expected case where response is a list: [{'generated_text': '...'}]
        elif isinstance(response_json, list) and len(response_json) > 0 and 'generated_text' in response_json[0]:
            return response_json[0]['generated_text']
        # If neither format matches, return an error
        else:
            return f"Error: Unexpected response format: {response_json}"

    except requests.exceptions.RequestException as e:
        return f"Error: API request failed: {e}"

def main(gold_standard_file):
    if HF_TOKEN is None:
        print("❌ Error: Set the HF_TOKEN environment variable.")
        return

    if not os.path.exists(gold_standard_file):
        print(f"❌ Error: Gold standard file not found at '{gold_standard_file}'")
        return

    # Load scoring models once to be efficient
    print("Loading scoring models...")
    semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
    rouge = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    print("Models loaded.")

    with open(gold_standard_file, 'r') as f:
        evaluation_data = json.load(f)

    all_semantic_scores = []
    all_rouge_scores = []

    print(f"\n🚀 Starting evaluation of {len(evaluation_data)} images...")

    for i, item in enumerate(evaluation_data):
        image_path = item["image_path"]
        print("\n" + "="*80)
        print(f"Evaluating Image {i+1}/{len(evaluation_data)}: {os.path.basename(image_path)}")
        print("="*80)

        if not os.path.exists(image_path):
            print(f"⚠️  Warning: Skipping image, file not found: {image_path}")
            continue

        for j, eval_case in enumerate(item["evaluations"]):
            prompt = eval_case["prompt"]
            gold_answer = eval_case["gold_answer"]

            print(f"\n--- Prompt {j+1}: {prompt} ---\n")
            
            model_response = query_hf_endpoint(image_path, prompt).strip()

            print("✅ **Gold Standard Answer:**")
            print(f"{gold_answer}\n")
            print("🤖 **LLaVA Model's Response:**")
            print(f"{model_response}\n")

            # --- SCORING ---
            if "Error:" not in model_response and model_response:
                # 1. Semantic Similarity Score
                gold_embedding = semantic_model.encode(gold_answer, convert_to_tensor=True)
                model_embedding = semantic_model.encode(model_response, convert_to_tensor=True)
                cosine_score = util.pytorch_cos_sim(gold_embedding, model_embedding).item()
                all_semantic_scores.append(cosine_score)

                # 2. ROUGE-L Score
                rouge_l_score = rouge.score(gold_answer, model_response)['rougeL'].fmeasure
                all_rouge_scores.append(rouge_l_score)

                print("--- SCORES ---")
                print(f"📊 Semantic Similarity (Cosine): {cosine_score:.4f}")
                print(f"📊 ROUGE-L (F1-Score):           {rouge_l_score:.4f}")
                print("-"*80)
            else:
                print("--- SCORES ---")
                print("Skipping scoring due to error in model response.")
                print("-"*80)


    # --- FINAL SUMMARY ---
    print("\n\n" + "="*80)
    print("✅ Evaluation Complete: Final Summary")
    print("="*80)
    if all_semantic_scores and all_rouge_scores:
        avg_semantic = np.mean(all_semantic_scores)
        avg_rouge = np.mean(all_rouge_scores)
        print(f"📈 **Average Semantic Similarity Score:** {avg_semantic:.4f}")
        print(f"📈 **Average ROUGE-L Score:** {avg_rouge:.4f}")
    else:
        print("No scores were calculated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a fine-tuned LLaVA model via a Hugging Face Endpoint.")
    parser.add_argument("--gold_standard_file", type=str, default="gold_standard.json")
    args = parser.parse_args()
    main(args.gold_standard_file)