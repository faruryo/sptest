# sptest

![Test](https://github.com/faruryo/sptest/workflows/Test/badge.svg)
![Docker](https://github.com/faruryo/sptest/workflows/Docker/badge.svg)

Tool to run speedtest and data upload

## sample

![](docs/images/ambient-sample.png)

## Development

### Remote - Containers

1. vscode install
1. vscode Extension
  - Remote - Containers

### Ambient

[Ambient – IoTデーター可視化サービス](https://ambidata.io/)

1. User Registration
1. Channel creation
1. Edit [sample/config.yaml](sample/config.yaml)

### virtualenv create

Run in vscode's integrated terminal

```sh
poetry install
```

### Test run in Remote - Containers

```
(.venv) $ python -m sptest servers
```