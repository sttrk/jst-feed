# jst-feed (Python版)

ChatGPT が参照できる **日本標準時（JST, 分精度）** のフィードを、GitHub Actions（Python）で毎分更新して公開します。

## 出力
- ファイル: `jst.json`
- 形式:
```json
{ "tz": "JST", "date": "YYYY-MM-DD", "time": "HH:MM" }
```
- 更新頻度: 毎分 (`cron`)

## 参照URL（例）
作成後、次を ChatGPT に共有してください：

```
https://raw.githubusercontent.com/<YOUR_GITHUB_USERNAME>/jst-feed/main/jst.json
```

## 優先順
1. NICT（取得できれば）
2. WorldTimeAPI
3. ランナーのシステム時刻（JST変換）
