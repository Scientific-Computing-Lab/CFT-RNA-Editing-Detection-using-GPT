import os
import sys
import json
from openai import AzureOpenAI

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 4:
    print("Usage: python script.py <input_file_path> <output_file_path> <temperature>")
    sys.exit(1)

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]
temperature_test = float(sys.argv[3])

# Check if the AZURE_OPENAI_API_KEY environment variable is set
api_key = os.getenv("AZURE_OPENAI_API_KEY")
if not api_key:
    print("Error: AZURE_OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

# Check if the AZURE_OPENAI_ENDPOINT environment variable is set
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
if not endpoint:
    print("Error: AZURE_OPENAI_ENDPOINT environment variable is not set.")
    sys.exit(1)

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-15-preview"
)

# Initialize meta-statistics counts
total_fp = total_fn = total_tp = total_tn = 0

# Create a log file
log_file = os.path.splitext(output_file_path)[0] + "_log.txt"

def log(message):
    with open(log_file, 'a') as logf:
        logf.write(message + '\n')


# Function to compare two binary strings and calculate FP, FN, TP, TN
def compare_annotation_strings(true_string, predicted_string):
    fp = fn = tp = tn = 0

    if true_string == "yes" and predicted_string == "yes":
        tp += 1
    elif true_string == "no" and predicted_string == "yes":
        fp += 1
    elif true_string == "yes" and predicted_string == "no":
        fn += 1
    elif true_string == "no" and predicted_string == "no":
        tn += 1

    return fp, fn, tp, tn

# Function to process each line of the JSONL file, generate predictions, and compare results
def extract_and_process_jsonl(input_path, output_path):
    global total_fp, total_fn, total_tp, total_tn
    
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            data = json.loads(line)
            messages = data.get('messages', [])
            user_content = ""
            assistant_content = ""

            for message in messages:
                if message['role'] == 'user':
                    user_content = message['content']
                elif message['role'] == 'assistant':
                    assistant_content = message['content']

            if user_content and assistant_content:
                log("Processing user content: " + user_content)
                
                # Constructing message_text as a list of dictionaries
                message_text = [
                    {
                        "role": "system",
                        "content": "Predict if the central adenosine (A) in the given RNA sequence context within an Alu element will be edited to inosine (I) by ADAR enzymes. yes or no:"
                    },
                    {
                        "role": "user",
                        "content": user_content
                    }
                ]
                
                log("Sending request to OpenAI API...")
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini-2024-07-18-liver_15_only",
                        messages=message_text,
                        temperature=temperature_test,
                        max_tokens=1, # logprobs=True, top_logprobs=5,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stop=None
                    )
                except openai.NotFoundError as e:
                    print(f"Error: {e}")
                    print("Deployment not found. Check your Azure OpenAI deployment status.")
                    sys.exit(1)


                log("Received response from OpenAI API.")
                generated_response = response.choices[0].message.content.strip()
                
                log("Generated response: " + generated_response)
                log("Comparing true and predicted strings...")
                
                fp, fn, tp, tn = compare_annotation_strings(assistant_content, generated_response)
                
                log("*******************************")
                log(f"FP, FN, TP, TN: {fp}, {fn}, {tp}, {tn}")
                log("*******************************")
                                
                # Update meta-statistics counts
                total_fp += fp
                total_fn += fn
                total_tp += tp
                total_tn += tn

                result = {
                    "user_content": user_content,
                    "assistant_content": assistant_content,
                    "generated_response": generated_response,
                    "fp": fp,
                    "fn": fn,
                    "tp": tp,
                    "tn": tn
                }

                outfile.write(json.dumps(result) + '\n')
                log("Result saved to output file.")
                log("-" * 50)

# Run the function to process the JSONL file
log("Starting processing...")
extract_and_process_jsonl(input_file_path, output_file_path)

# Calculate meta-statistics
total_samples = total_fp + total_fn + total_tp + total_tn
meta_statistics = {
    "total_samples": total_samples,
    "total_fp": total_fp,
    "total_fn": total_fn,
    "total_tp": total_tp,
    "total_tn": total_tn,
    "meta_fp": total_fp / total_samples if total_samples > 0 else 0,
    "meta_fn": total_fn / total_samples if total_samples > 0 else 0,
    "meta_tp": total_tp / total_samples if total_samples > 0 else 0,
    "meta_tn": total_tn / total_samples if total_samples > 0 else 0
}

log("\nMeta-Statistics:")
log(json.dumps(meta_statistics, indent=4))

# Save meta-statistics in a separate file
meta_stats_file = os.path.splitext(output_file_path)[0] + "_meta_stats.json"
with open(meta_stats_file, 'w') as metafile:
    json.dump(meta_statistics, metafile)

log(f"Meta-statistics saved in {meta_stats_file}")

