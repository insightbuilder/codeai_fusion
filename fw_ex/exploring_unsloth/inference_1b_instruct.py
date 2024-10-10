# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv
from time import time

load_dotenv("../../../python_de_learners_data/.env")

tokenizer = AutoTokenizer.from_pretrained("unsloth/Llama-3.2-1B-Instruct")
model = AutoModelForCausalLM.from_pretrained("unsloth/Llama-3.2-1B-Instruct")
print("loaded model\n")

start = time()
prompt = "Hey, are you conscious? Can you talk to me?"
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
generate_ids = model.generate(inputs.input_ids, max_length=100)
gen_complete = time()
print(f"generated output in {gen_complete - start} secs\n")
decode_ids = tokenizer.batch_decode(
    generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
)[0]

print("Decoded IDs:", end="\n")

print(decode_ids)
