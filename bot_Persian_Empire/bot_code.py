from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def generate_python_code(prompt, max_length=10000):
    """
    این تابع متن ورودی prompt رو می‌گیره
    و یک کد پایتون تولید می‌کنه.
    
    Args:
        prompt (str): توضیح کد پایتون
        max_length (int): حداکثر تعداد توکن تولید شده
        
    Returns:
        str: کد پایتون تولید شده
    """
    model_name = "Salesforce/codegen-350M-mono"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=-1  # اجرا روی CPU
# بدونه مقدار اجرا روی GPU
    )
    
    result = generator(prompt, max_length=max_length)
    return result[0]["generated_text"]
