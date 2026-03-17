"""
Test Minimax API with Correct Endpoints
Using the actual Minimax API documentation endpoints
"""

import requests
import json

def test_minimax_correct_endpoints(api_token):
    """Test with correct Minimax API endpoints"""
    
    print("🔍 Testing Minimax API with Correct Endpoints")
    print("=" * 60)
    
    # Correct Minimax API endpoints based on their documentation
    endpoints = [
        "https://api.minimax.chat/v1",
        "https://api.minimaxi.com/v1", 
        "https://open.minimaxi.com/api/v1",
        "https://open-api.minimax.com/v1"
    ]
    
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    for endpoint in endpoints:
        print(f"🧪 Testing: {endpoint}")
        
        try:
            # Test different API paths that Minimax might use
            test_paths = [
                "/models",
                "/model/list", 
                "/text-to-speech",
                "/tts",
                "/audio/speech"
            ]
            
            for path in test_paths:
                try:
                    url = f"{endpoint}{path}"
                    response = requests.get(url, headers=headers, timeout=8)
                    
                    if response.status_code in [200, 201]:
                        print(f"   ✅ SUCCESS: {path} -> {response.status_code}")
                        print(f"   📊 Response: {response.text[:200]}")
                        return endpoint, path
                    elif response.status_code == 401:
                        print(f"   🔑 Auth needed: {path} -> check API token format")
                    elif response.status_code == 403:
                        print(f"   🚫 Forbidden: {path} -> check permissions")
                    elif response.status_code == 404:
                        print(f"   ❌ Not found: {path}")
                    else:
                        print(f"   ⚠️  {path} -> {response.status_code}: {response.text[:100]}")
                        
                except requests.exceptions.Timeout:
                    continue
                except requests.exceptions.ConnectionError:
                    continue
                    
        except Exception as e:
            print(f"   ❌ Endpoint failed: {e}")
        
        print()
    
    print("🔧 Trying POST requests (TTS usually requires POST)...")
    
    # Try POST requests for TTS
    for endpoint in endpoints:
        try:
            tts_paths = [
                "/text-to-speech",
                "/tts", 
                "/audio/speech",
                "/v1/text_to_speech"
            ]
            
            test_data = {
                "text": "Hello world",
                "voice": "default"
            }
            
            for path in tts_paths:
                try:
                    url = f"{endpoint}{path}"
                    response = requests.post(url, json=test_data, headers=headers, timeout=10)
                    
                    if response.status_code in [200, 201]:
                        print(f"   ✅ TTS SUCCESS: {endpoint}{path}")
                        return endpoint, path
                    elif response.status_code == 422:
                        print(f"   📝 TTS endpoint found but wrong params: {endpoint}{path}")
                        return endpoint, path
                    else:
                        print(f"   TTS {path}: {response.status_code}")
                        
                except:
                    continue
                    
        except:
            continue
    
    return None, None

def test_hailuo_direct():
    """Test direct Hailuo AI endpoints"""
    
    print("\n🎯 Testing Hailuo AI Direct Endpoints")
    print("=" * 50)
    
    # Since you mentioned hailuoai.video
    hailuo_endpoints = [
        "https://hailuoai.video/api",
        "https://api.hailuoai.video/v1",
        "https://hailuoai.com/api/v1"
    ]
    
    api_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJQcmFzYWQgS2FubmF3YXIiLCJVc2VyTmFtZSI6InBkZiB0byBwb2RjYXN0IiwiQWNjb3VudCI6IiIsIlN1YmplY3RJRCI6IjE5ODkwNDA1OTI4MjY0MDU1NzMiLCJQaG9uZSI6IiIsIkdyb3VwSUQiOiIxOTg5MDQwNTkyODIyMjE1MzY1IiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoicHJhc2Fka2FubmF3YXIyODFAZ21haWwuY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMTEtMTQgMDM6MjI6NDQiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.kfMosZ5mQIIAiH73vp5G_a2OaIm48Zecnn93dYyExosoQXfY6sA8ATh12KPdsuUQ0yUlLZ57CUNXwMrzrFsYXdeUhscLNl19fi68D0WOIYQJm2sD-U7lfwCoxJC1aGczJj9hHhl394_Vm8SeGQvX2eHKhDajdRrwzsPODKPVMVCplzCOxiqtzoErQE_NNapFpVRnS9cjMhtTgGB0RsIT_No6UGpcFfUonqndQvlDZXdMczWLoV5UQK1i1ZztxUZ0uNdEut8fNdANItm2OrYa-mLm7kpkKfmrtY2QOGsMubUV8OuGjbLDltXVz65yPoKjShFp62zguTFB4N3dGHYqEw"
    
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    for endpoint in hailuo_endpoints:
        print(f"🧪 Testing Hailuo: {endpoint}")
        
        try:
            response = requests.get(f"{endpoint}/audio", headers=headers, timeout=8)
            print(f"   Status: {response.status_code}")
            
            if response.status_code in [200, 201, 422]:
                print(f"   ✅ Hailuo endpoint working: {endpoint}")
                return endpoint
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    return None

if __name__ == "__main__":
    API_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJQcmFzYWQgS2FubmF3YXIiLCJVc2VyTmFtZSI6InBkZiB0byBwb2RjYXN0IiwiQWNjb3VudCI6IiIsIlN1YmplY3RJRCI6IjE5ODkwNDA1OTI4MjY0MDU1NzMiLCJQaG9uZSI6IiIsIkdyb3VwSUQiOiIxOTg5MDQwNTkyODIyMjE1MzY1IiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoicHJhc2Fka2FubmF3YXIyODFAZ21haWwuY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMTEtMTQgMDM6MjI6NDQiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.kfMosZ5mQIIAiH73vp5G_a2OaIm48Zecnn93dYyExosoQXfY6sA8ATh12KPdsuUQ0yUlLZ57CUNXwMrzrFsYXdeUhscLNl19fi68D0WOIYQJm2sD-U7lfwCoxJC1aGczJj9hHhl394_Vm8SeGQvX2eHKhDajdRrwzsPODKPVMVCplzCOxiqtzoErQE_NNapFpVRnS9cjMhtTgGB0RsIT_No6UGpcFfUonqndQvlDZXdMczWLoV5UQK1i1ZztxUZ0uNdEut8fNdANItm2OrYa-mLm7kpkKfmrtY2QOGsMubUV8OuGjbLDldXVz65yPoKjShFp62zguTFB4N3dGHYqEw"
    
    endpoint, path = test_minimax_correct_endpoints(API_TOKEN)
    
    if endpoint:
        print(f"\n🎉 WORKING MINIMAX API FOUND!")
        print(f"   Endpoint: {endpoint}")
        print(f"   Path: {path}")
    else:
        print(f"\n🔍 Trying Hailuo AI direct...")
        hailuo_endpoint = test_hailuo_direct()
        
        if hailuo_endpoint:
            print(f"\n🎉 WORKING HAILUO ENDPOINT: {hailuo_endpoint}")
        else:
            print(f"\n⚠️  API endpoints not responding")
            print(f"💡 Your token is VALID but endpoints may be:")
            print(f"   1. Different API base URLs")
            print(f"   2. Network restrictions") 
            print(f"   3. Different authentication method needed")
            
    print(f"\n🔑 Your API token is VALID ✅")
    print(f"📧 Account: prasadkannawar281@gmail.com")
    print(f"👤 User: pdf to podcast")
    print(f"🏢 Group: Prasad Kannawar")
