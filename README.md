# Amazon Translate Simple Mock

[English](./README.md) •
[日本語 (Japanese)](./README.ja.md)

This is a simple mock for Amazon Translate real-time translation API.

## Supported APIs
* TranslateText
* TranslateDocument (text/html only)

## Features
* Zero-config and ready to use
* Converts en <-> ja romanization instead of fixed response
* Works stand-alone, independent of external services

## Supported Languages and Behaviors

| Source | Target | Behaviors | Example |
| ------ | ------ | --- | ------- |
| ja (auto) | en | Convert Japanese to Romaji | `明日は晴れです！` -> `ashita ha hare desu!` |
| en (auto) | ja | Convert Romaji to Hiragana | `ashita ha hare desu!` -> `あした は はれ です` |
| Any | Other than en/ja | Output specified parameters in JSON | (Value specified for parameter) |

## Message Commands

Put the following command in the text to be translated and it will return
a response according to the command.

Note: Error responses are not highly reproducible. Avoid implementations
that compare error response strings with exact matches, Check Amazon's
original error response if necessary.

| Command string | Behavior |
| ------------ | --- |
| EchoRequestBody | Returns the JSON of the requested content as-is as the body of the translation result |
| ThrottlingException | Returns ThrottlingException (status code: 429) |
| InternalServerException | Returns InternalServerException (status code: 500) |
| LimitExceededException | Returns LimitExceededException (status code: 400) |
| ServiceUnavailableException | Returns ServiceUnavailableException (status code: 500) |
| TooManyRequestsException | Returns TooManyRequestsException (status code: 400) |
| UnsupportedLanguagePairException | Returns UnsupportedLanguagePairException (status code: 400) |

## Getting Started

### Start service

#### from Docker Hub

```sh
$ docker pull dash14/amazon-translate-simple-mock:latest
$ docker run -it dash14/amazon-translate-simple-mock
```

#### from GitHub Repository (for develop)

```sh
$ git clone https://github.com/dash14/amazon-translate-simple-mock.git
$ cd amazon-translate-simple-mock/
$ docker compose up -d
```

### Usage example: Calling TranslateText with aws-cli

```sh
$ aws translate translate-text \
    --endpoint-url http://localhost:8080 \
    --source-language-code ja \
    --target-language-code en \
    --settings Formality=FORMAL \
    --text "明日は晴れです。" \
    --terminology-names "custom"
```

Response:

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

### Usage example: Calling TranslateDocument with aws-cli

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

Response:

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

## License

Under the MIT license.  
See [LICENSE](./LICENSE) file for more details.

## Contributing

Please feel free to send us an Issue or Pull Request if there are additional
APIs to be supported, error variances to be improved, bugs, documentation
errors, and so on!
