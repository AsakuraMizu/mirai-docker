import asyncio
import json
import pathlib
import sys

import aiofiles
import httpx
import tqdm


async def fetch(url, name):
    if pathlib.Path(name).exists():
        tqdm.tqdm.write(f'{name} already exists.')
        return True
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', url, timeout=None) as stream:
            try:
                stream.raise_for_status()
            except:
                code = stream.status_code
                tqdm.tqdm.write(
                    f'Failed to fetch {name}, status code: {code}.',
                    sys.stderr)
                tqdm.tqdm.write('Plz check your version number.', sys.stderr)
                return False
            length = int(stream.headers.get('content-length'))
            bar = tqdm.tqdm(None, name, length, unit='B', unit_scale=True)
            async with aiofiles.open(name, 'wb') as f:
                async for chuck in stream.aiter_bytes():
                    bar.update(len(chuck))
                    if chuck:
                        await f.write(chuck)
    return True


async def fetch_wrapper(version):
    return await fetch(
        'https://github.com/mamoe/mirai-console/releases/download/' \
        f'wrapper-{version}/mirai-console-wrapper-{version}.jar',
        f'mirai-console-wrapper-{version}.jar')


async def fetch_mirai(pkg, version):
    return await fetch(
        f'https://pan.jasonczc.cn/?/mirai/mirai-{pkg}/mirai-{pkg}-{version}.mp4',
        f'content/mirai-{pkg}-{version}.jar')


async def fetch_plugin(plugin, version):
    return await fetch(
        f'https://pan.jasonczc.cn/?/mirai/plugins/{plugin}/{plugin}-{version}.mp4',
        f'plugins/{plugin}-{version}.jar',)


async def main():
    pathlib.Path('content').mkdir(exist_ok=True)
    pathlib.Path('plugins').mkdir(exist_ok=True)

    async with aiofiles.open('versions.json') as f:
        content = await f.read()
        VER = json.loads(content)

    coros = [
        fetch_mirai('console', VER['console']),
        fetch_mirai('core-qqandroid', VER['core-qq-android']),
        fetch_plugin('mirai-api-http', VER['mirai-api-http']),
        fetch_wrapper(VER['wrapper'])
    ]
    res = await asyncio.gather(*coros)

    if not all(res):
        sys.exit(1)

asyncio.run(main())
