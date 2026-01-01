import os import requests

class VoiceCallManager: def init(self): self.api_key = os.getenv("RETELL_API_KEY") self.agent_id = os.getenv("RETELL_AGENT_ID") self.base_url = "https://api.retellai.com"

async def initiate_outbound(self, to_number, context):
    """
    Connects with Retell AI to start a call with pre-defined context.
    """
    payload = {
        "from_number": os.getenv("TWILIO_NUMBER"),
        "to_number": to_number,
        "metadata": context,
        "retell_llm_dynamic_variables": {
            "customer_name": context['name'],
            "product_name": context['product']
        }
    }
    
    response = requests.post(
        f"{self.base_url}/create-phone-call",
        json=payload,
        headers={"Authorization": f"Bearer {self.api_key}"}
    )
    return response.json().get('call_id')