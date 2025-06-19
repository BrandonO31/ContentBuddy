import webbrowser
import json
import urllib.parse
from pathlib import Path
import requests

IMGUR_CLIENT_ID = "145f8718a15deca"

def automate_thumbnail_with_photopea(screenshot_path: str, episode_num: int):
    imgur_url = upload_image_to_imgur(screenshot_path)

    psd_url = "https://raw.githubusercontent.com/BrandonO31/.psd_file/main/standardThumbnailTemplateV3.psd"

    script = f"""
try {{
    var doc = app.documents[0];
    var img = app.documents[1];
    img.resizeImage(1920, 1080);
    app.activeDocument = doc;

    var dayLayer = doc.artLayers.getByName("DayText");
    dayLayer.kind = LayerKind.TEXT;
    dayLayer.textItem.contents = "Day";
    dayLayer.textItem.position = [68.5, 268.6];
    dayLayer.layerEffects = {{
    stroke: {{
        enabled: true,
        size: 5,
        color: [0, 0, 0], // black
        position: "outside",
        opacity: 100
    }}
    }};
    var white = new SolidColor();
    white.rgb.red = 255;
    white.rgb.green = 255;
    white.rgb.blue = 255;
    dayLayer.textItem.color = white;

    var numLayer = null;
    for (var i = 0; i < doc.artLayers.length; i++) {{
        if (doc.artLayers[i].name == "EpisodeNumber") {{
        numLayer = doc.artLayers[i];
        break;
    }}
    }}

    if (!numLayer) {{
        numLayer = doc.artLayers.add();
        numLayer.name = "EpisodeNumber";
    }}
    app.activeDocument.activeLayer = numLayer;
    numLayer.kind = LayerKind.TEXT;
    numLayer.textItem.contents = "{episode_num}";
    numLayer.textItem.size = 145;
    numLayer.textItem.position = [370, 268.6]; 

    var yellow = new SolidColor();
    yellow.rgb.red = 220;
    yellow.rgb.green = 213;
    yellow.rgb.blue = 25;
    numLayer.textItem.color = yellow;
    numLayer.layerEffects = null;
    numLayer.layerEffects = {{
    stroke: {{
        enabled: true,
        size: 5,
        color: [0, 0, 0], // black
        position: "outside",
        opacity: 100
    }}
    }};


    app.activeDocument = doc;
    var alreadyExists = false;
    for (var i = 0; i < doc.artLayers.length; i++) {{
        if (doc.artLayers[i].name === "ImportedImage copy") {{
            alreadyExists = true;
            break;
        }}
    }}

    if (!alreadyExists) {{
        app.activeDocument = img;
        var imageLayer = img.activeLayer;
        imageLayer.name = "ImportedImage";
        imageLayer.duplicate(doc);
        app.activeDocument = doc;
    }}

    var allLayers = doc.artLayers;
    var targetLayer = doc.artLayers.getByName("ImportedImage copy");
    var secondToLastLayer = allLayers[allLayers.length - 1];
    targetLayer.move(secondToLastLayer, ElementPlacement.PLACEBEFORE);
    alert("Attemtping Select Subject on Image");
    
    doc.activeLayer = targetLayer;

    // Run Select Subject

    var idautoCutout = stringIDToTypeID("autoCutout");
    var desc01 = new ActionDescriptor;
    var idsampleAllLayers = stringIDToTypeID("sampleAllLayers");
    desc01.putBoolean(idsampleAllLayers, false );
    executeAction (idautoCutout, descO1, DialogModes.NO);
        
    //var desc = new ActionDescriptor();
    //desc.putBoolean(stringIDToTypeID("sampleAllLayers"), false);
    //desc.putString(stringIDToTypeID("output"), "selection");
    //executeAction(stringIDToTypeID("Ct  "), desc, DialogModes.NO);


    alert("Successfully updated DayText and added episode number layer.");
}} catch (e) {{
    alert("Script failed: " + e);
}}
"""







    config = {
    "files": [psd_url, imgur_url],
    "script": script 
}

    encoded = urllib.parse.quote(json.dumps(config))
    url = f"https://www.photopea.com#{encoded}"
    webbrowser.open(url)
    print(f"Opened Photopea for episode #{episode_num}")


def upload_image_to_imgur(image_path: str) -> str:
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    with open(image_path, 'rb') as f:
        files = {'image': (Path(image_path).name, f, 'image/png')}
        response = requests.post("https://api.imgur.com/3/image", headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json()['data']['link']
    else:
        raise Exception(f"Imgur upload failed: {response.json()}")
    
def main():
    screenshot_path = "Screenshots/ep51_face_frame.png"
    episode_num = 51

    try:
        print("Starting thumbnail automation...")
        automate_thumbnail_with_photopea(screenshot_path, episode_num)
    except Exception as e:
        print(f"Error during thumbnail automation: {e}")

if __name__ == "__main__":
    main()

