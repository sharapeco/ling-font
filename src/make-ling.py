from os import path, makedirs
from base64 import b64encode
from fontTools.ttLib import TTFont

cd = path.dirname(__file__)
src = TTFont(path.join(cd, 'Null-R.ttf'))
fontDir = path.join(cd, '../dist/fonts')
cssDir = path.join(cd, '../dist/css')

if not path.exists(fontDir):
	makedirs(fontDir)

if not path.exists(cssDir):
	makedirs(cssDir)

# フォント名を設定
nameRecords = []
for nameRecord in src['name'].names:
	if nameRecord.nameID == 1:
		nameRecord.string = 'Ling'
	if nameRecord.nameID == 5:
		nameRecord.string = 'v1.0'
	if nameRecord.platformID == 3 and nameRecord.nameID <= 6:
		nameRecords.append(nameRecord)
src['name'].names = nameRecords

src['OS/2'].achVendID = 'sszm'

# 不要テーブルを削る
del src['GSUB']
del src['DSIG']

# 50から250まで10きざみで
for width in range(50, 260, 10):
	# フォント名を設定
	for nameRecord in src['name'].names:
		if nameRecord.nameID == 2:
			nameRecord.string = f'{width}'
		if nameRecord.nameID == 3:
			nameRecord.string = f'1.0;sszm;Ling-{width}'
		if nameRecord.nameID == 4 or nameRecord.nameID == 6:
			nameRecord.string = f'Ling-{width}'

	# グリフ幅を設定
	for glyphName in src['hmtx'].metrics.keys():
		src['hmtx'].metrics[glyphName] = (width, 0)

	# フォントファイルを保存して Data URI を記述した CSS ファイルを生成
	fontPath = path.join(fontDir, f'ling-{width}.woff2')
	src.save(fontPath)
	with open(fontPath, 'rb') as f:
		fontData = f.read()
		encodedData = b64encode(fontData)
		with open(path.join(cssDir, f'ling-{width}.css'), 'w') as cssFile:
			cssFile.write(f'''\
@font-face {{
	font-family: Ling-{width};
	src: url("data:font/woff2;base64,{encodedData.decode()}") format("woff2");
}}
''')
