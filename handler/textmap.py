_D='Please send the link to the second JSON file.'
_C='awaiting_file'
_B='file1'
_A='file2'
import tempfile,requests,json
from telegram import Update
from telegram.ext import ContextTypes
def download_file(url):
	A=requests.get(url);A.raise_for_status();B=tempfile.NamedTemporaryFile(delete=False,suffix='.json')
	with open(B.name,'wb')as C:C.write(A.content)
	return B.name
def compare_json_files(file1,file2):
	with open(file1,'r')as A,open(file2,'r')as C:D=json.load(A);B=json.load(C)
	E={A:B[A]for A in B if A not in D and B[A]!='...'};return E
async def textmapdiff_command(update,context):
	B=update;A=context.user_data
	if _B not in A:await B.message.reply_text('Please send the link to the first JSON file.');A[_C]=_B;return
	elif _A not in A:await B.message.reply_text(_D);A[_C]=_A;return
async def handle_url(update,context):
	B=update;F=B.message.text;A=context.user_data
	if _C in A:
		C=A[_C]
		try:
			G=download_file(F);A[C]=G;del A[_C];await B.message.reply_text(f"Successfully downloaded the file for {C}.")
			if C==_B:await B.message.reply_text(_D);A[_C]=_A;return
			elif C==_A:
				if _B in A and _A in A:
					H=A[_B];I=A[_A];D=compare_json_files(H,I)
					if D:
						E=tempfile.NamedTemporaryFile(delete=False,suffix='.json')
						with open(E.name,'w')as J:json.dump(D,J,indent=4)
						await B.message.reply_document(document=open(E.name,'rb'),filename='TextMapDiff.json')
					else:await B.message.reply_text('No differences found between the two JSON files.')
					del A[_B];del A[_A]
		except Exception as K:await B.message.reply_text(f"Failed to download the file: {K}");return