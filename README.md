# skype_log_image_renamer
Convert the SSID filename of the image in the skype log archive (tar) to a timestamp.

## how to use
+ Once you request it, the archive will be ready in a few hours to a few days, so download it when it is ready. 
+ Extract it and make the folder visible.
  + Here we assume that you have expanded to `c:\8_(skypeusername)_export\` and that you have a `media` folder.
  + Read the contents of `media` and if it succeeds in getting a timestamp, move it to `media_old`. If the file succeeds, copy it to `media_renamed`.
+ Run. You will be asked the following four questions, which can be skipped by pressing enter if there is no problem.
```
>skype_log_media_renamer_local.py
Enter the path to the target folder [.\media]:
Enter the path to the processed folder [.\media_old]:
Enter the path to the copy folder [.\media_renamed]:
Enter the timezone [Asia/Tokyo]:
```
+ 実施中以下のようなログが流れます
```
Copied .\media\0-cus-d7-b22f819c2191a2ee2483829aaf5bb9e3.1.jpeg to .\media_renamed\2017-11-13_18-49-17-775844Z_1.jpeg
Copied .\media\0-cus-d8-7d5e1e4619b410ca852bb1af56fd9f1e.1.jpeg to .\media_renamed\2017-10-14_11-26-13-738272Z_1.jpeg
```

### Errors
If it finds a json that is not tied to the filename of each multimedia attribute of media, it outputs the following error and skips it.

# skypeログの画像類のファイル名をタイムスタンプにするやつ
Convert the SSID filename of the image in the skype log archive (tar) to a timestamp.

## 使い方
+ skypeのログアーカイブ(tar)を、以下のサイトから請求し、取得してください。
  - https://go.skype.com/export
+ 申請すると数時間～数日でアーカイブができるので、出来上がったらダウンロードします。 
+ 展開し、フォルダが見られるようにします。
  + ここでは、`c:\8_(skypeusername)_export\`に展開し、`media`フォルダができているという仮定とします。
  + `media`の内容をよみとり、タイムスタンプ取得に成功すると`media_old`に移動させます。成功したファイルは`media_renamed`にコピーします。
+ 実行します。以下の4つが聞かれますが、とくに問題なければenterを押せばスキップ出来ます。
```
>skype_log_media_renamer_local.py
Enter the path to the target folder [.\media]:
Enter the path to the processed folder [.\media_old]:
Enter the path to the copy folder [.\media_renamed]:
Enter the timezone [Asia/Tokyo]:
```
+ 実施中以下のようなログが流れます
```
Copied .\media\0-cus-d7-b22f819c2191a2ee2483829aaf5bb9e3.1.jpeg to .\media_renamed\2017-11-13_18-49-17-775844Z_1.jpeg
Copied .\media\0-cus-d8-7d5e1e4619b410ca852bb1af56fd9f1e.1.jpeg to .\media_renamed\2017-10-14_11-26-13-738272Z_1.jpeg
```

## エラー
mediaの各マルチメディア属性のファイル名に紐づかないjsonを見つけると、以下のようなエラーを出力し、スキップします。
```
No associated media file found for .\media\0-cus-d7-965511ea39acf83368e5af7d575dd297.json
```
