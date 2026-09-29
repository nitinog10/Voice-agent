import os, sys
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError

load_dotenv()
region = os.getenv("AWS_REGION")
model  = os.getenv("BEDROCK_MODEL_ID")
key    = os.getenv("AWS_ACCESS_KEY_ID", "")
print(f"[cfg] region={region}  model={model}  key={key[:4]}...{key[-4:] if len(key)>8 else ''}")

def try_model(client, model_id):
    resp = client.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": "Reply with exactly: OK"}]}],
        inferenceConfig={"maxTokens": 20, "temperature": 0},
    )
    return resp["output"]["message"]["content"][0]["text"].strip()

try:
    client = boto3.client(
        "bedrock-runtime",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    out = try_model(client, model)
    print(f"[OK] Bedrock replied: {out!r}")
    sys.exit(0)
except ClientError as e:
    code = e.response.get("Error", {}).get("Code")
    msg  = e.response.get("Error", {}).get("Message")
    print(f"[FAIL] {code}: {msg}")
    # Common fix for regions that need an inference profile (e.g. ap-south-1)
    if code in ("ValidationException", "AccessDeniedException") and region == "ap-south-1":
        alt = "apac." + model if not model.startswith("apac.") else model
        print(f"[retry] trying inference profile {alt} ...")
        try:
            out = try_model(client, alt)
            print(f"[OK] Bedrock replied with {alt}: {out!r}")
            print(f"[hint] set BEDROCK_MODEL_ID={alt} in your .env")
            sys.exit(0)
        except ClientError as e2:
            print(f"[FAIL] {e2.response.get('Error',{}).get('Code')}: "
                  f"{e2.response.get('Error',{}).get('Message')}")
    sys.exit(1)
except (NoCredentialsError, EndpointConnectionError) as e:
    print(f"[FAIL] {type(e).__name__}: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[FAIL] {type(e).__name__}: {e}")
    sys.exit(1)
