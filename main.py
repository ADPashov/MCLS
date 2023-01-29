from mcls_main import MclsMain

# pyinstaller --onefile -w  --path venv\Lib\site-packages --add-data="Model\*;." --add-data="View\*;." --add-data="Controller\*;."  --add-data "C:/Users/ppash/AppData/Local/Programs/Python/Python310/Lib/site-packages/customtkinter;customtkinter/"--icon=mc_logo.ico main.py --hidden-import tkiner  --hidden-import=customtkinter --hidden-import=tkcalendar --hidden-import=babel.numbers
# res = requests.post('https://api.smsapi.bg/sms.do', headers = {'Authorization': 'Bearer 28jcabwPJ0yUN4An1Xm91vIXFtkRwdWikNMcHzaj'}, data = {'to': '359899819818', 'message':'poluchi li'})
# from smsapi.client import SmsApiBgClient as bg
# client = bg(access_token = token)
# send_results = client.sms.send(to="phone number", message="text message", test=1)
# for result in send_results:
#     print(result.id, result.points, result.error)


if __name__ == "__main__":
    controller = MclsMain()
