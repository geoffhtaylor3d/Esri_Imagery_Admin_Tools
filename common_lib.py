

def get_user_items(user, active_gis):
    user_inventory = {}
    try:  # Support arcgis json user input
        user_items = active_gis.content.search(query=f"* AND owner:{user.username}", max_items=500)
    except AttributeError:  # Support exact string for user name
        user_items = active_gis.content.search(query=f"* AND owner:{user}", max_items=500)

    for item in user_items:
        if item.type not in user_inventory:
            user_inventory[item.type] = [i
                                         for i in user_items
                                         if i.type == item.type]
    return user_inventory


def print_user_inventory(inventory):
    for itype, ilist in inventory.items():
        try:
            print(f"{itype}\n{'-'*50}")
            for i in ilist:
                print(f"{' ':3}{i.title:50}")
            print("\n")
        except Exception as e:
            print(f"\t\tOperation failed on: {i.title}")
            print(f"\t\tException: {sys.exc_info()[1]}")
            continue


def get_fs_webmaps(fs, inv):
    fs_webmap_inventory = {}
    fs_inv = []
    try:
        for wm in inv['Web Map']:
            if fs.id in get_layer_item_ids(wm):
                if wm not in fs_inv:
                    fs_inv.append(wm)
        fs_webmap_inventory[fs.title] = fs_inv
        return fs_webmap_inventory
    except KeyError as ke:
        pass


def get_layer_item_ids(wm):
    wmo = WebMap(wm)
    wm_id_list = []
    for layer in wmo.layers:
        try:
            fsvc = FeatureLayerCollection(layer['url'][:-1], active_gis)
            if not fsvc.properties['serviceItemId'] in wm_id_list:
                wm_id_list.append(fsvc.properties['serviceItemId'])
        except Exception as e:
            pass
    return wm_id_list


def get_dash_wm(dash):
    return [active_gis.content.get(widget['itemId'])
            for widget in dash.get_data()['widgets']
            if widget['type'] == "mapWidget"]


def get_fs_webscenes(fs, inv):
    fs_webscene_inventory = {}
    fs_inv = []
    try:
        for ws in inv['Web Scene']:
            if fs.id in get_layer_item_ids(ws):
                if ws not in fs_inv:
                    fs_inv.append(ws)
        fs_webscene_inventory[fs.title] = fs_inv
        return fs_webscene_inventory
    except KeyError as ke:
        pass


def get_dash_ws(dash):
    return [active_gis.content.get(widget['itemId'])
            for widget in dash.get_data()['widgets']
            if widget['type'] == "sceneWidget"]


def is_hosted(item):
    return [keyword for keyword in item.typeKeywords if "Hosted" in keyword]


def print_webmap_inventory(wm):
    wm_obj = WebMap(wm)
    print(f"{wm_obj.item.title}\n{'-'*100}")
    for wm_layer in wm_obj.layers:
        try:
            if is_hosted(Item(active_gis, wm_layer['itemId'])):
                print(f"{' '*2}{wm_layer['title']:40}HOSTED{' ':5}"
                      f"{wm_layer['layerType']:20}{dict(wm_layer)['itemId']}")
            else:
                print(f"{' '*2}{wm_layer['title']:40}other{' ':6}"
                      f"{wm_layer['layerType']:20}{wm_layer.id}")
        except:
            print(f"{' '*2}{wm_layer['title']:40}other{' ':6}"
                  f"{wm_layer['layerType']:20}{wm_layer.id}")
    print("\n")

