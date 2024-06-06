from PIL import Image 
import requests 
from transformers import AutoModelForCausalLM 
from transformers import AutoProcessor 

model_id = "microsoft/Phi-3-vision-128k-instruct" 

model = AutoModelForCausalLM.from_pretrained(model_id, device_map="cuda", trust_remote_code=True, torch_dtype="auto", _attn_implementation="eager")

processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True) 

messages = [
{"role":"system","content":"You are an Image Analyser with 20 years of experience. Your job is to help the user with the instructions given by them based on the image they upload."},
{"role":"user","content":"<|image_1|>\nWrite a short poem based on this image"}
] 

#For reading a url
#url = "https://assets-c4akfrf5b4d3f4b7.z01.azurefd.net/assets/2024/04/BMDataViz_661fb89f3845e.png" 
#image = Image.open(requests.get(url, stream=True).raw) 

#For reading an image file
img = "sunset.jpeg"
image = Image.open(img)

prompt = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

inputs = processor(prompt, [image], return_tensors="pt").to("cuda:0") 

generation_args = { 
    "max_new_tokens": 500, 
    "temperature": 0.0, 
    "do_sample": False, 
} 

generate_ids = model.generate(**inputs, eos_token_id=processor.tokenizer.eos_token_id, **generation_args) 	

# remove input tokens 
generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0] 

print(response)
