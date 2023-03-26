import girder_client
import json

apiUrl = "https://styx.neurology.emory.edu/girder/api/v1"

gc=girder_client.GirderClient(apiUrl=apiUrl)

# https://styx.neurology.emory.edu/girder/api/v1/resource/6105948b68f4fe34fca1bf79/items?type=folder&limit=250&sort=_id&sortdir=1


folderId = '6105948b68f4fe34fca1bf79'

itemList = gc.get(f'resource/{folderId}/items?type=folder&limit=3000')
print(itemList)

with open("imageSetForCm.json","w") as fp:
    json.dump(itemList,fp)
