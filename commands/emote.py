#!/usr/bin/env python3
import os
import requests


async def emote(ctx, search, add):

    await ctx.respond(content="⏳ Loading...")

    query = {
        "operationName": "EmoteSearch",
        "query": "query EmoteSearch($query: String, $tags: [String!]!, $sortBy: SortBy!, $filters: Filters, $page: Int, $perPage: Int!, $isDefaultSetSet: Boolean!, $defaultSetId: Id!) {\n  emotes {\n    search(\n      query: $query\n      tags: {tags: $tags, match: ANY}\n      sort: {sortBy: $sortBy, order: DESCENDING}\n      filters: $filters\n      page: $page\n      perPage: $perPage\n    ) {\n      items {\n        id\n        defaultName\n        owner {\n          mainConnection {\n            platformDisplayName\n            __typename\n          }\n          style {\n            activePaint {\n              id\n              name\n              data {\n                layers {\n                  id\n                  ty {\n                    __typename\n                    ... on PaintLayerTypeSingleColor {\n                      color {\n                        hex\n                        __typename\n                      }\n                      __typename\n                    }\n                    ... on PaintLayerTypeLinearGradient {\n                      angle\n                      repeating\n                      stops {\n                        at\n                        color {\n                          hex\n                          __typename\n                        }\n                        __typename\n                      }\n                      __typename\n                    }\n                    ... on PaintLayerTypeRadialGradient {\n                      repeating\n                      stops {\n                        at\n                        color {\n                          hex\n                          __typename\n                        }\n                        __typename\n                      }\n                      shape\n                      __typename\n                    }\n                    ... on PaintLayerTypeImage {\n                      images {\n                        url\n                        mime\n                        size\n                        scale\n                        width\n                        height\n                        frameCount\n                        __typename\n                      }\n                      __typename\n                    }\n                  }\n                  opacity\n                  __typename\n                }\n                shadows {\n                  color {\n                    hex\n                    __typename\n                  }\n                  offsetX\n                  offsetY\n                  blur\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          highestRoleColor {\n            hex\n            __typename\n          }\n          __typename\n        }\n        deleted\n        flags {\n          defaultZeroWidth\n          publicListed\n          __typename\n        }\n        imagesPending\n        images {\n          url\n          mime\n          size\n          scale\n          width\n          frameCount\n          __typename\n        }\n        ranking(ranking: TRENDING_WEEKLY)\n        inEmoteSets(emoteSetIds: [$defaultSetId]) @include(if: $isDefaultSetSet) {\n          emoteSetId\n          emote {\n            id\n            alias\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      totalCount\n      pageCount\n      __typename\n    }\n    __typename\n  }\n}",
        "variables": {
            "defaultSetId": "",
            "filters": {"exactMatch": True},
            "isDefaultSetSet": False,
            "page": 1,
            "perPage": 1,
            "query": search,
            "sortBy": "TOP_ALL_TIME",
            "tags": [],
        },
    }

    headers = {
        "authorization": str(os.getenv("7TV_TOKEN")),
        "content-type": "application/json",
    }
    try:
        r = requests.post("https://7tv.io/v4/gql", headers=headers, json=query).json()
        images = r["data"]["emotes"]["search"]["items"][0]["images"]
        webp_2x = next(
            img for img in images if img["mime"] == "image/webp" and img["scale"] == 2
        )
        url = webp_2x["url"]
        name = r["data"]["emotes"]["search"]["items"][0]["defaultName"]
    except:
        content = "❌   **Emote Not Found! Try Again**"
        await ctx.edit(content=content)
        return

    imageReq = requests.get(url)
    image = imageReq.content
    content = url

    if add:
        emote = await ctx.guild.create_custom_emoji(name=name, image=image)
        content = f"✅   **Emote Added To Server**   {emote}"

    await ctx.edit(content=content)
