#!/usr/bin/env python3
import os
import requests


async def emote(ctx, search, add):

    await ctx.respond(content="*⏳ Loading...*")

    query = {
  "operationName": "SearchEmotes",
  "variables": {
    "query": search,
    "limit": 1,
    "page": 1,
    "sort": {
      "value": "popularity",
      "order": "DESCENDING"
    },
    "filter": {
      "category": "TOP",
      "exact_match": False,
      "case_sensitive": False,
      "ignore_tags": False,
      "zero_width": False,
      "animated": False,
      "aspect_ratio": ""
    }
  },
  "query": """query SearchEmotes(
  $query: String!
  $page: Int
  $sort: Sort
  $limit: Int
  $filter: EmoteSearchFilter
) {
  emotes(
    query: $query
    page: $page
    sort: $sort
    limit: $limit
    filter: $filter
  ) {
    count
    items {
      id
      name
      state
      trending
      owner {
        id
        username
        display_name
        style {
          color
          paint_id
          __typename
        }
        __typename
      }
      flags
      host {
        url
        files {
          name
          format
          width
          height
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}
"""}

    headers = {"authorization": str(os.getenv('7TV_TOKEN')), "content-type": "application/json"}

    r = requests.post("https://7tv.io/v3/gql", headers=headers, json=query).json()
    try:
        url = "http:" + r["data"]["emotes"]["items"][0]["host"]["url"]
        uri = "/2x.png"
        name = r["data"]["emotes"]["items"][0]["name"]

        imageReq = requests.get(url + uri)
        image = imageReq.content

        if imageReq.status_code == 404:
            uri = "/1x.gif"
            image = requests.get(url + uri).content

        content = url + uri

        if add == "True":
            emote = await ctx.guild.create_custom_emoji(name=name, image=image)
            content = f"✅   **Emote Added To Server**   {emote}"

    except:
        content = "❌   **Emote Not Found! Try Again**"
        pass

    await ctx.edit(content=content)
