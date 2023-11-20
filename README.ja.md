# Amazon Translate Simple Mock

[English](./README.md) •
[日本語 (Japanese)](./README.ja.md)

Amazon Translate リアルタイム翻訳APIの簡易モックです。

## 対応API
* TranslateText
* TranslateDocument (text/htmlのみ)

## 特徴
* ゼロコンフィグですぐに使い始められる
* 固定応答ではなく、en <-> ja のローマ字変換を行う
* 外部サービスに依存せずスタンドアローンで動作する

## 対応言語と挙動

| Source | Target | 挙動 | Example |
| ------ | ------ | --- | ------- |
| ja (auto) | en | 日本語をローマ字に変換する | `明日は晴れです！` -> `ashita ha hare desu!` |
| en (auto) | ja | ローマ字をひらがなに変換する | `ashita ha hare desu!` -> `あした は はれ です` |
| 全て | en・ja以外 | 指定したパラメータをJSONで出力する | (パラメータに指定した値) |

## メッセージコマンド

翻訳対象の本文に以下のコマンドを入れると、そのコマンドに応じた応答を返します。

注意: エラー応答の再現度は高くありません。エラー応答の文字列を完全一致で比較するような実装は避け、
必要に応じてAmazonの本来のエラー応答を確認してください。
Amazon から得られるエラー情報に近づけるための Pull Request は常に歓迎しています。

| コマンド文字列 | 挙動 |
| ------------ | --- |
| EchoRequestBody | リクエストした内容のJSONをそのまま翻訳結果の本文として返す |
| ThrottlingException | ThrottlingException (status code: 429) を返却する |
| InternalServerException | InternalServerException (status code: 500) を返却する |
| LimitExceededException | LimitExceededException (status code: 400) を返却する |
| ServiceUnavailableException | ServiceUnavailableException (status code: 500) を返却する |
| TooManyRequestsException | TooManyRequestsException (status code: 400) を返却する |
| UnsupportedLanguagePairException | UnsupportedLanguagePairException (status code: 400) を返却する |

## Getting Started

### サービスの起動

```sh
$ docker compose up -d
```

### 使用例: aws-cliでTranslateTextを実行する

```sh
$ aws translate translate-text \
    --endpoint-url http://localhost:8080 \
    --source-language-code ja \
    --target-language-code en \
    --settings Formality=FORMAL \
    --text "明日は晴れです。" \
    --terminology-names "custom"
```

レスポンス:

```json
{
    "TranslatedText": "ashita ha hare desu.",
    "SourceLanguageCode": "ja",
    "TargetLanguageCode": "en",
    "AppliedTerminologies": [
        {
            "Name": "custom",
            "Terms": []
        }
    ],
    "AppliedSettings": {
        "Formality": "FORMAL"
    }
}
```

### 使用例: aws-cliでTranslateDocumentを実行する

```sh
$ echo "<p>明日は晴れです。</p>" > source.txt
$ aws translate translate-document \
    --endpoint-url http://localhost:8080 \
    --document '{"ContentType":"text/html"}' \
    --source-language-code ja \
    --target-language-code en \
    --settings Formality=FORMAL \
    --document-content fileb://source.txt \
    --terminology-names "custom"
```

レスポンス:

```json
{
    "TranslatedDocument": {
        "Content": "PHA+YXNoaXRhIGhhIGhhcmUgZGVzdS48L3A+"
    },
    "SourceLanguageCode": "ja",
    "TargetLanguageCode": "en",
    "AppliedTerminologies": [
        {
            "Name": "custom",
            "Terms": []
        }
    ],
    "AppliedSettings": {
        "Formality": "FORMAL"
    }
}
```

### サービスの停止

```sh
$ docker compose down
```


## License

MIT license です。  
詳細は[LICENSE](./LICENSE)ファイルを参照してください。

## Contributing

対応APIの追加やエラー差異の改善、バグやドキュメント誤記などありましたら、
ぜひ気軽に Issue や Pull Request をお送りください！
