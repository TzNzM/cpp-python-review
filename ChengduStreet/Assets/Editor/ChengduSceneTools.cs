using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class ChengduSceneTools
{
    const string ScenePath = "Assets/Scenes/Chengdu.unity";

    [MenuItem("Chengdu/Generate and save street scene")]
    public static void Generate()
    {
        if (!Application.isBatchMode && !EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo()) return;
        EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        var builder = new GameObject("Scene Generator").AddComponent<ChengduStreet>();
        builder.Build();
        Directory.CreateDirectory("Assets/Generated/Materials");
        AssetDatabase.Refresh();
        var saved = new Dictionary<string, Material>();
        foreach (Renderer renderer in Object.FindObjectsOfType<Renderer>())
        {
            Material[] materials = renderer.sharedMaterials;
            for (int i = 0; i < materials.Length; i++)
                if (materials[i]) materials[i] = Persist(materials[i], saved);
            renderer.sharedMaterials = materials;
        }
        if (RenderSettings.skybox) RenderSettings.skybox = Persist(RenderSettings.skybox, saved);
        EditorSceneManager.MarkSceneDirty(SceneManager.GetActiveScene());
        EditorSceneManager.SaveScene(SceneManager.GetActiveScene(), ScenePath);
        EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(ScenePath, true) };
        AssetDatabase.SaveAssets();
        if (SceneView.lastActiveSceneView)
            SceneView.lastActiveSceneView.LookAt(new Vector3(0, 3, 10), Quaternion.Euler(22, 12, 0), 38);
        Debug.Log("Chengdu scene generated and saved: " + ScenePath);
    }

    static Material Persist(Material material, Dictionary<string, Material> saved)
    {
        if (AssetDatabase.Contains(material)) return material;
        string key = material.name.Replace('/', '_');
        if (saved.TryGetValue(key, out Material cached)) return cached;
        string path = "Assets/Generated/Materials/" + key + ".mat";
        Material existing = AssetDatabase.LoadAssetAtPath<Material>(path);
        if (existing) { EditorUtility.CopySerialized(material, existing); EditorUtility.SetDirty(existing); }
        else { existing = material; AssetDatabase.CreateAsset(existing, path); }
        saved.Add(key, existing);
        return existing;
    }

    [MenuItem("Chengdu/Capture game view to PNG")]
    public static void Capture()
    {
        Camera camera = Camera.main;
        if (!camera) { Debug.LogError("Generate the street scene first."); return; }
        string path = EditorUtility.SaveFilePanel("Save street image", "", "Chengdu.png", "png");
        if (string.IsNullOrEmpty(path)) return;
        RenderTexture previous = camera.targetTexture;
        RenderTexture previousActive = RenderTexture.active;
        RenderTexture target = RenderTexture.GetTemporary(1920, 1080, 24, RenderTextureFormat.ARGB32);
        Texture2D image = new Texture2D(1920, 1080, TextureFormat.RGB24, false);
        try
        {
            camera.targetTexture = target; camera.Render(); RenderTexture.active = target;
            image.ReadPixels(new Rect(0, 0, 1920, 1080), 0, 0); image.Apply();
            File.WriteAllBytes(path, image.EncodeToPNG());
        }
        finally
        {
            camera.targetTexture = previous; RenderTexture.active = previousActive;
            RenderTexture.ReleaseTemporary(target); Object.DestroyImmediate(image);
        }
        Debug.Log("Saved street image: " + path);
    }
}
