# Mirai Docker 化

实为 [Mirai Console](https://github.com/mamoe/mirai-console) + [Mirai API HTTP](https://github.com/mamoe/mirai-api-http)

## 需要的软件

+ docker
+ docker-compose

## 使用方法

1. 克隆本仓库
2. 编辑 MiraiAPIHTTP.yml 文件（主要是`authKey`），该文件将被复制到`运行时目录/plugins/MiraiAPIHTTP/setting.yml`
3. 修改 docker-compose.yml 文件中的 ACCOUNT 和 PASSWORD
4. 在终端中执行：
```bash
docker-compose up -d
```

## 其他

1. `versions.json` 用来控制各个模块的版本。正常情况下，该文件中配置好的版本都是能够完全适配的，建议不要修改此文件。
2. 由于 Mirai Console Wrapper 是直接从 GitHub Releases 上下载的，可能速度会很慢，您可以将该文件手动下载后放置于本目录，构建镜像时将自动使用此文件而不是重新下载。类似的，您也可以将 Mirai Core QQ Android 手动下载后放置于 `content` 目录，Mirai API HTTP 手动下载后放置于 `plugins` 目录。**注意：您手动下载的版本应与 `version.json` 中的一致，否则将无法识别。如果您坚持使用您提供的版本，您可以自行修改 `versions.json` 文件。**
