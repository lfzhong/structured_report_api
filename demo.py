import asyncio
import threading
import time
import httpx
from structured_report.main import app
import uvicorn

def start_server():
    """Start the server in a separate thread"""
    uvicorn.run(app, host="0.0.0.0", port=8000)

async def run_demo():
    """Run the demo requests"""
    async with httpx.AsyncClient() as client:
        try:
            # 1. Get API key
            response = await client.post("http://localhost:8000/api-keys",
                                       json={"name": "demo", "email": "demo@example.com"})
            response.raise_for_status()
            api_key = response.json()["api_key"]
            print(f"Got API key: {api_key[:20]}...")

            # 2. Analyze text
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {"content": "AI will change the world dramatically.", "model": "deepseek"}

            response = await client.post("http://localhost:8000/v1/report/insight",
                                       json=data, headers=headers)

            if response.status_code != 200:
                print(f"Error response: {response.text}")
                response.raise_for_status()

            result = response.json()
            print(f"Core claim: {result['core_claim']}")
            print(f"Supporting arguments: {result['supporting_arguments']}")
            print(f"Assumptions: {result['assumptions']}")
            print(f"Speaker position: {result['speaker_position']}")
            print(f"My evaluation: {result['my_evaluation']}")
            print(f"Personal impact: {result['personal_impact']}")
            print(f"Meta principle: {result['meta_principle']}")
            print(f"Falsifiability: {result['falsifiability']}")
            print(f"Keywords: {result['keywords']}")
            print(f"Related insights: {result['related_insights']}")
            print(f"Meta questions: {result['meta_questions']}")

        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Error: {e}")

# Start server in background thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(2)

# Run the demo
asyncio.run(run_demo())

# Keep the server running for a bit so the user can see it
print("Demo completed. Server will shut down in 5 seconds...")
time.sleep(5)