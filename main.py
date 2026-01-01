import os from fastapi import FastAPI, WebSocket, Request from voice_engine.call_handler import VoiceCallManager from voice_engine.crm_sync import HubSpotSync

app = FastAPI(title="Staqlt Autonomous Voice Engine") call_manager = VoiceCallManager() crm = HubSpotSync()

@app.post("/v1/start-call") async def trigger_call(contact_id: str): """ Triggers an outbound call for a specific CRM contact. """ contact_info = await crm.get_contact_data(contact_id) if not contact_info: return {"status": "error", "message": "Contact not found"}

call_id = await call_manager.initiate_outbound(
    to_number=contact_info['phone'],
    context={"name": contact_info['firstname'], "product": "AI Automation"}
)
return {"status": "dialing", "call_id": call_id}


@app.post("/v1/webhook/call-ended") async def handle_call_summary(request: Request): """ Receives call summary and transcription to update CRM. """ data = await request.json() summary = data.get('summary') contact_id = data.get('metadata', {}).get('contact_id')

await crm.log_call_outcome(contact_id, summary)
return {"status": "crm_updated"}


if name == "main": import uvicorn uvicorn.run(app, host="0.0.0.0", port=8000)