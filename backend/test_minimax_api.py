"""
Test Minimax API Token
Quick verification of your Minimax API access
"""

import requests
import json
import base64

def decode_jwt_info(token):
    """Decode JWT token info (just the payload part)"""
    try:
        # Split JWT token (header.payload.signature)
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decode payload (middle part)
        payload = parts[1]
        # Add padding if needed
        payload += '=' * (4 - len(payload) % 4)
        
        decoded = base64.b64decode(payload)
        return json.loads(decoded)
    except:
        return None

def test_minimax_api(api_token):
    """Test Minimax API with your token"""
    
    print("🔑 Testing Minimax API Token")
    print("=" * 50)
    
    # Decode token info
    token_info = decode_jwt_info(api_token)
    if token_info:
        print("📊 Token Information:")
        print(f"   User: {token_info.get('UserName', 'Unknown')}")
        print(f"   Group: {token_info.get('GroupName', 'Unknown')}")
        print(f"   Email: {token_info.get('Mail', 'Unknown')}")
        print(f"   Created: {token_info.get('CreateTime', 'Unknown')}")
        print()
    
    # Test different Minimax endpoints
    endpoints = [
        "https://api.minimax.chat/v1",
        "https://api.minimax.io/v1",
        "https://open-api.minimax.io/v1"
    ]
    
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    working_endpoint = None
    
    for endpoint in endpoints:
        print(f"🧪 Testing endpoint: {endpoint}")
        
        try:
            # Test basic API connectivity
            response = requests.get(f"{endpoint}/model/list", headers=headers, timeout=10)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ SUCCESS - Endpoint working!")
                working_endpoint = endpoint
                
                # Show available models
                try:
                    data = response.json()
                    if 'model_list' in data:
                        models = data['model_list']
                        audio_models = [m for m in models if 'audio' in m.get('model_id', '').lower() or 'speech' in m.get('model_id', '').lower()]
                        print(f"   📊 Found {len(audio_models)} audio models")
                        for model in audio_models[:3]:  # Show first 3
                            print(f"      - {model.get('model_id', 'Unknown')}")
                except:
                    print("   📊 Response format different than expected")
                break
                
            elif response.status_code == 401:
                print("   ❌ Authentication failed - check API token")
            elif response.status_code == 403:
                print("   ❌ Access forbidden - check permissions")
            else:
                print(f"   ⚠️  Unexpected response: {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print("   ⏱️  Timeout - endpoint may be slow")
        except requests.exceptions.ConnectionError:
            print("   🌐 Connection error - check network")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    if working_endpoint:
        print(f"🎉 SUCCESS! Working endpoint found: {working_endpoint}")
        
        # Test voice/audio capabilities
        print("\n🎙️ Testing voice/audio capabilities...")
        
        try:
            # Test text-to-speech endpoint
            tts_url = f"{working_endpoint}/text_to_speech"
            
            test_data = {
                "text": "Hello, this is a test of Minimax voice synthesis.",
                "model": "speech-01",
                "voice": "default"
            }
            
            response = requests.post(tts_url, json=test_data, headers=headers, timeout=15)
            
            if response.status_code == 200:
                print("   ✅ TTS endpoint working!")
                return working_endpoint
            else:
                print(f"   ⚠️  TTS test: {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"   ⚠️  TTS test failed: {e}")
        
        return working_endpoint
    else:
        print("❌ No working endpoints found")
        print("\n💡 Troubleshooting:")
        print("   1. Check if API token is correct")
        print("   2. Verify network connectivity")
        print("   3. Try accessing minimax.io directly in browser")
        return None

if __name__ == "__main__":
    # Your API token
    API_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJQcmFzYWQgS2FubmF3YXIiLCJVc2VyTmFtZSI6InBkZiB0byBwb2RjYXN0IiwiQWNjb3VudCI6IiIsIlN1YmplY3RJRCI6IjE5ODkwNDA1OTI4MjY0MDU1NzMiLCJQaG9uZSI6IiIsIkdyb3VwSUQiOiIxOTg5MDQwNTkyODIyMjE1MzY1IiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoicHJhc2Fka2FubmF3YXIyODFAZ21haWwuY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMTEtMTQgMDM6MjI6NDQiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.kfMosZ5mQIIAiH73vp5G_a2OaIm48Zecnn93dYyExosoQXfY6sA8ATh12KPdsuUQ0yUlLZ57CUNXwMrzrFsYXdeUhscLNl19fi68D0WOIYQJm2sD-U7lfwCoxJC1aGczJj9hHhl394_Vm8SeGQvX2eHKhDajdRrwzsPODKPVMVCplzCOxiqtzoErQE_NNapFpVRnS9cjMhtTgGB0RsIT_No6UGpcFfUonqndQvlDZXdMczWLoV5UQK1i1ZztxUZ0uNdEut8fNdANItm2OrYa-mLm7kpkKfmrtY2QOGsMubUV8OuGjbLDltXVz65yPoKjShFp62zguTFB4N3dGHYqEw"
    
    working_endpoint = test_minimax_api(API_TOKEN)
    
    if working_endpoint:
        print(f"\n🚀 READY FOR INTEGRATION!")
        print(f"   Working endpoint: {working_endpoint}")
        print(f"   Your API token: VALID ✅")
        print(f"\n📝 Next steps:")
        print(f"   1. Set environment variable: MINIMAX_API_KEY")
        print(f"   2. Update minimax_voice_cloner.py with working endpoint")
        print(f"   3. Test voice cloning integration")
    else:
        print(f"\n🔧 TROUBLESHOOTING NEEDED")
        print(f"   Check network connectivity and API token")
