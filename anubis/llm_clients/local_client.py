from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
import os

# Load model ID based on speed preference
model_id = "deepseek-ai/deepseek-llm-7b-chat"
if os.getenv("USE_FAST_LLM") == "True":
    model_id = "mistralai/Mistral-7B-Instruct"  # Lightweight fallback for speed

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    trust_remote_code=True
)
model.to(device)
model.eval()

def build_chat_inputs(prompt: str):
    """Format input prompt and tokenize it for the LLM."""
    messages = [
        {"role": "system", "content": "You are a fantasy football expert."},
        {"role": "user", "content": prompt},
    ]

    # Apply chat formatting without tokenization (return raw string)
    prompt_text = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=False
    )

    # Convert prompt text to token IDs and attention mask
    return tokenizer(
        prompt_text,
        return_tensors="pt",
        padding=True,
        truncation=True
    ).to(device)

def anubis_decide(prompt: str) -> str:
    """Run local LLM inference on the draft prompt."""
    print("⚡ Calling DeepSeek inference...")
    start = time.time()

    try:
        inputs = build_chat_inputs(prompt)
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']

        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        # Extract generated tokens after input length
        generated_tokens = output[0][inputs['input_ids'].shape[-1]:]
        result = tokenizer.decode(generated_tokens, skip_special_tokens=True)

        print(f"✅ DeepSeek returned in {time.time() - start:.2f}s")
        print("🧠 AI Result:", result)
        return result

    except Exception as e:
        print("❌ Error during DeepSeek call:", str(e))
        return "Player Name: Marvin Harrison\nExplanation: Fallback pick due to error."