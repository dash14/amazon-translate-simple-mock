# Amazon Translate Simple Mock

[English](./README.md) •
[日本語 (Japanese)](./README.ja.md)

This is a simple mock for Amazon Translate real-time translation API.

![Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdash14%2Famazon-translate-simple-mock%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.version&label=version)
[![License](https://img.shields.io/github/license/dash14/amazon-translate-simple-mock)](./LICENSE)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/dash14/amazon-translate-simple-mock/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/dash14/amazon-translate-simple-mock)

[Docker Image on Docker Hub](https://hub.docker.com/r/dash14/amazon-translate-simple-mock)  
[Docker Image on ghcr.io](https://github.com/users/dash14/packages/container/package/amazon-translate-simple-mock)

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
| ja (auto) | en | Convert Japanese to Romaji | `明日は晴れです` -> `ashita ha hare desu` |
| en (auto) | ja | Convert Romaji to Hiragana | `ashita ha hare desu` -> `あした は はれ です` |
| Any | Other than en/ja | Output specified parameters in JSON | (Value specified for parameter) |

## Message Commands

Put the following command in the text to be translated and it will return
a response according to the command.

Note: Error responses are not highly reproducible. Avoid implementations
that compare error response strings with exact matches, Check Amazon's
original error response if necessary.

| Command string | Behavior |
| ------------ | --- |
| @return RequestedBody | Returns the requested body as-is as a translation result |
| @sleep {SECONDS} | Waits for the specified seconds and returns the result. Can be used with other commands |
| @raise ThrottlingException | Returns ThrottlingException (status code: 429) |
| @raise InternalServerException | Returns InternalServerException (status code: 500) |
| @raise LimitExceededException | Returns LimitExceededException (status code: 400) |
| @raise ServiceUnavailableException | Returns ServiceUnavailableException (status code: 500) |
| @raise TooManyRequestsException | Returns TooManyRequestsException (status code: 400) |
| @raise UnsupportedLanguagePairException | Returns UnsupportedLanguagePairException (status code: 400) |
| @return SourceLanguageCode {code} | Returns the specified code in the SourceLanguageCode field. Cannot be used with @raise |

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
$ docker compose up -d app
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
