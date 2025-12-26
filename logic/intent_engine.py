def analyze_problem(text: str):
    proc_text = text.lower()
    
    # We now use a set for 'emergencies' to handle multiple symptoms
    intent = {
        "emergencies": set(), 
        "urgency": "normal",
        "hospital_type": "all",
        "is_pregnancy": False
    }

    # 1. Multi-Situation Mapping
    # Cardiac
    if any(w in proc_text for w in ["chest", "heart", "attack", "सीने", "हृदय", "छाती"]):
        intent["emergencies"].add("heart")
        intent["urgency"] = "high"
    
    # Traumatic/Bleeding
    if any(w in proc_text for w in ["accident", "bleeding", "blood", "खून", "अपघात", "जखम"]):
        intent["emergencies"].add("bleeding")
        intent["urgency"] = "high"
    
    # Burn
    if any(w in proc_text for w in ["burn", "fire", "आग", "जळणे", "भाजणे"]):
        intent["emergencies"].add("burn")

    # Maternal
    if any(w in proc_text for w in ["pregnant", "delivery", "labor", "गर्भवती", "बाळंतपण"]):
        intent["emergencies"].add("maternal")
        intent["is_pregnancy"] = True
    
    # Poisoning
    if any(w in proc_text for w in ["snake", "bite", "poison", "साप", "विष"]):
        intent["emergencies"].add("poison")
        intent["urgency"] = "high"

    # Head/Neurological (New for headache/stroke detection)
    if any(w in proc_text for w in ["head", "headache", "dizzy", "stroke", "डोके", "डोकेदुखी"]):
        intent["emergencies"].add("head")

    # 2. Hospital Preference
    if any(w in proc_text for w in ["free", "government", "govt", "poor", "सरकारी", "मोफत"]):
        intent["hospital_type"] = "government"
    elif any(w in proc_text for w in ["private", "fast", "best", "खाजगी", "इन्शुरन्स"]):
        intent["hospital_type"] = "private"

    # Default to general if nothing specific detected
    if not intent["emergencies"]:
        intent["emergencies"].add("general")

    return intent

def map_support(intent, support_data):
    # If multiple intents exist, we prioritize the most critical for schemes
    ems = intent.get("emergencies", {"general"})
    
    if "maternal" in ems:
        return support_data.get("maternal", support_data["medical"])
    if "heart" in ems:
        return support_data.get("cardiac", support_data["medical"])
    
    return support_data.get("medical")
