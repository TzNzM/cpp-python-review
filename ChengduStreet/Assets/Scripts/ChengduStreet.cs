using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

// All dimensions are metres. The street is an original stylized composition.
public sealed class ChengduStreet : MonoBehaviour
{
    public const string RootName = "Chengdu · 银杏茶街";
    readonly Dictionary<string, Material> palette = new Dictionary<string, Material>();
    Transform root;
    System.Random random;

    void Start() { if (!GameObject.Find(RootName)) Build(); }
    float R(float a, float b) { return Mathf.Lerp(a, b, (float)random.NextDouble()); }
    Material Mat(string name, string hex, float smoothness = .2f, float emission = 0)
    {
        if (palette.TryGetValue(name, out Material found)) return found;
        ColorUtility.TryParseHtmlString(hex, out Color color);
        Material mat = new Material(Shader.Find("Standard")) { name = name, color = color };
        mat.SetFloat("_Glossiness", smoothness);
        if (emission > 0) { mat.EnableKeyword("_EMISSION"); mat.SetColor("_EmissionColor", color * emission); }
        palette.Add(name, mat);
        return mat;
    }
    GameObject Shape(string name, PrimitiveType kind, Vector3 pos, Vector3 scale, Material mat, Transform parent = null)
    {
        GameObject o = GameObject.CreatePrimitive(kind);
        o.name = name;
        o.transform.SetParent(parent ? parent : root, false);
        o.transform.localPosition = pos;
        o.transform.localScale = scale;
        o.GetComponent<Renderer>().sharedMaterial = mat;
        Collider col = o.GetComponent<Collider>();
        if (Application.isPlaying) Destroy(col); else DestroyImmediate(col);
        return o;
    }
    GameObject Box(string n, Vector3 p, Vector3 s, Material m, Transform t = null) { return Shape(n, PrimitiveType.Cube, p, s, m, t); }
    GameObject Ball(string n, Vector3 p, Vector3 s, Material m, Transform t = null) { return Shape(n, PrimitiveType.Sphere, p, s, m, t); }
    GameObject Cylinder(string n, Vector3 p, float radius, float height, Material m, Transform t = null) { return Shape(n, PrimitiveType.Cylinder, p, new Vector3(radius * 2, height / 2, radius * 2), m, t); }
    Transform Group(string name, Vector3 p, float yaw = 0)
    {
        Transform t = new GameObject(name).transform;
        t.SetParent(root, false); t.localPosition = p; t.localRotation = Quaternion.Euler(0, yaw, 0); return t;
    }
    void Beam(string name, Vector3 a, Vector3 b, float radius, Material mat, Transform t = null)
    {
        GameObject o = Cylinder(name, (a + b) / 2, radius, Vector3.Distance(a, b), mat, t);
        o.transform.localRotation = Quaternion.FromToRotation(Vector3.up, b - a);
    }
    void Sign(string resource, Vector3 p, Vector2 size, Transform parent)
    {
        Texture2D texture = Resources.Load<Texture2D>("Signs/" + resource);
        if (!texture) { Debug.LogWarning("Missing sign: " + resource); return; }
        Material m = new Material(Shader.Find("Unlit/Texture")) { name = "Sign_" + resource, mainTexture = texture };
        Shape(resource, PrimitiveType.Quad, p, new Vector3(size.x, size.y, 1), m, parent);
    }

    public void Build()
    {
        GameObject old = GameObject.Find(RootName);
        if (old) { if (Application.isPlaying) { old.SetActive(false); Destroy(old); } else DestroyImmediate(old); }
        palette.Clear(); random = new System.Random(20260907);
        root = new GameObject(RootName).transform;
        Material asphalt = Mat("Wet graphite", "#39484B", .65f);
        Material stone = Mat("Warm stone", "#A59E88");
        Material dark = Mat("Ink", "#203337");
        Material wood = Mat("Tea house timber", "#53352C");
        Material ivory = Mat("Ivory", "#EADCC0");
        Material red = Mat("Chilli red", "#BB3B2D");
        Material gold = Mat("Brass", "#DAAF60", .5f);
        Box("City foundation", new Vector3(0, -.38f, 12), new Vector3(72, .5f, 96), dark);
        Box("Boulevard", new Vector3(0, -.07f, 10), new Vector3(13, .16f, 86), asphalt);
        for (int side = -1; side <= 1; side += 2)
        {
            Box("Stone pavement", new Vector3(side * 10, .06f, 8), new Vector3(7, .3f, 80), stone);
            for (int z = -31; z < 48; z += 2)
            {
                Box("Kerbstone", new Vector3(side * 6.65f, .17f, z), new Vector3(.3f, .32f, 1.94f), ivory);
                Box("Paving seam", new Vector3(side * 10, .216f, z), new Vector3(6.5f, .009f, .025f), Mat("Grout", "#7E7E72"));
            }
            Box("Cycle lane", new Vector3(side * 5.25f, .025f, 10), new Vector3(1.75f, .015f, 83), Mat("Cycle jade", "#507E77"));
            Box("Lane edge", new Vector3(side * 4.3f, .035f, 10), new Vector3(.1f, .012f, 83), ivory);
            for (int z = -23; z < 45; z += 12) { Tree(new Vector3(side * 9.4f, .23f, z)); Lamp(new Vector3(side * 7.2f, .25f, z + 5)); }
        }
        for (int z = -29; z < 48; z += 6) Box("Centre dash", new Vector3(0, .025f, z), new Vector3(.12f, .016f, 2.8f), gold);
        for (int x = -5; x <= 5; x += 2) Box("Zebra crossing", new Vector3(x, .04f, -14), new Vector3(1.1f, .018f, 4.5f), ivory);
        string[] shops = { "tea", "hotpot", "noodles", "books", "coffee", "market", "tea", "hotpot" };
        for (int i = 0; i < 4; i++)
        {
            Shop(new Vector3(-15, .23f, -13 + i * 14), -90, shops[i], i);
            Shop(new Vector3(15, .23f, -13 + i * 14), 90, shops[i + 4], i + 4);
        }
        for (int i = 0; i < 16; i++)
        {
            float x = (i % 2 == 0 ? -1 : 1) * R(23, 33), z = -18 + (i / 2) * 10;
            float h = R(13, 29), width = R(5, 8);
            Material facade = Mat("Tower " + (i % 3), new[] { "#637A7D", "#81908B", "#51676D" }[i % 3], .6f);
            Box("Modern Chengdu skyline", new Vector3(x, h / 2, z), new Vector3(width, h, 7), facade);
            for (float y = 3; y < h; y += 2.3f)
                Box("Skyline floor band", new Vector3(x, y, z - 3.53f), new Vector3(width - .4f, .65f, .08f), Mat("Skyline glass", "#BBC1AA", .75f));
        }
        // A fictional landmark tower provides a focal point beyond the street.
        Cylinder("Distant observation tower", new Vector3(6, 19, 63), .9f, 38, Mat("Tower concrete", "#84908A"));
        Ball("Observation deck", new Vector3(6, 32, 63), new Vector3(7, 2.3f, 7), gold);
        Cylinder("Tower antenna", new Vector3(6, 39, 63), .13f, 10, dark);
        Panda(new Vector3(10.3f, .23f, -22));
        TeaTable(new Vector3(-10.4f, .23f, -12)); TeaTable(new Vector3(-10.4f, .23f, -8));
        for (int i = 0; i < 7; i++) Bicycle(new Vector3(7.9f, .23f, 4 + i * 1.2f));
        Car(new Vector3(-2.2f, .05f, 9), 0, Mat("Taxi teal", "#298E8B", .6f), true);
        Car(new Vector3(2.2f, .05f, 30), 180, ivory, false);
        for (int i = 0; i < 14; i++) Person(new Vector3((i % 2 == 0 ? -1 : 1) * R(7.7f, 11), .23f, R(-20, 42)), i);
        Transform gateway = Group("Street sign", new Vector3(-6.9f, .2f, -19), 25);
        Cylinder("Signpost", new Vector3(0, 1.8f, 0), .06f, 3.6f, dark, gateway);
        Box("Road name backing", new Vector3(0, 3.25f, 0), new Vector3(2.8f, .8f, .12f), dark, gateway);
        Sign("street", new Vector3(0, 3.25f, -.065f), new Vector2(2.7f, .7f), gateway);
        SetupLighting();
        Transform cameraRig = new GameObject("Street Camera").transform;
        cameraRig.SetParent(root); cameraRig.position = new Vector3(-1.8f, 5.3f, -30);
        cameraRig.LookAt(new Vector3(0, 3.7f, 13));
        Camera camera = cameraRig.gameObject.AddComponent<Camera>(); camera.tag = "MainCamera";
        camera.fieldOfView = 59; camera.nearClipPlane = .1f; camera.farClipPlane = 230; camera.allowHDR = true;
        cameraRig.gameObject.AddComponent<AudioListener>(); cameraRig.gameObject.AddComponent<StreetCamera>();
    }

    void Shop(Vector3 position, float yaw, string sign, int index)
    {
        Transform t = Group("Shop · " + sign, position, yaw);
        Material wall = Mat("Plaster " + index % 3, new[] { "#CBBFA5", "#A8AAA0", "#C2B398" }[index % 3]);
        Material timber = palette["Tea house timber"], ink = palette["Ink"], red = palette["Chilli red"];
        Material glass = Mat("Warm windows", "#F4CA83", .45f, .25f);
        Box("Two-storey plaster", new Vector3(0, 3.3f, 1.8f), new Vector3(12.8f, 6.6f, 6), wall, t);
        Box("Brick plinth", new Vector3(0, .4f, -1.24f), new Vector3(12.8f, .8f, .15f), ink, t);
        for (int x = -5; x <= 5; x += 2)
        {
            Box("Timber column", new Vector3(x, 3.3f, -1.36f), new Vector3(.15f, 6.6f, .23f), timber, t);
            Box("Ground floor glass", new Vector3(x, 1.75f, -1.29f), new Vector3(1.65f, 2.4f, .1f), glass, t);
            Box("Upper window", new Vector3(x, 5, -1.29f), new Vector3(1.4f, 1.6f, .1f), glass, t);
            for (int j = -1; j <= 1; j++) Box("Window lattice", new Vector3(x + j * .43f, 5, -1.4f), new Vector3(.06f, 1.7f, .06f), timber, t);
            Box("Window crossbar", new Vector3(x, 5, -1.42f), new Vector3(1.5f, .07f, .06f), timber, t);
        }
        Box("Signboard frame", new Vector3(0, 3.38f, -1.54f), new Vector3(8.6f, 1.03f, .26f), timber, t);
        Sign(sign, new Vector3(0, 3.38f, -1.68f), new Vector2(8.3f, .8f), t);
        for (int floor = 0; floor < 2; floor++)
        {
            float y = floor == 0 ? 4.04f : 6.75f;
            for (int half = -1; half <= 1; half += 2)
            {
                GameObject roof = Box("Grey tiled roof", new Vector3(0, y + .22f, 1.7f + half * 2), new Vector3(13.9f, .18f, 4.5f), ink, t);
                roof.transform.localRotation = Quaternion.Euler(half * 13, 0, 0);
                for (float x = -6.8f; x <= 6.8f; x += .44f)
                    Beam("Tile ridge", new Vector3(x, y + .73f, 1.7f), new Vector3(x, y - .24f, 1.7f + half * 4.3f), .045f, Mat("Tile edges", "#596665"), t);
            }
            Box("Roof ridge", new Vector3(0, y + .79f, 1.7f), new Vector3(14, .21f, .24f), ink, t);
        }
        for (int x = -5; x <= 5; x += 5) Lantern(new Vector3(x, 2.72f, -2.25f), t);
        Box("Shop threshold", new Vector3(0, .06f, -1.85f), new Vector3(12.6f, .12f, 1.1f), palette["Warm stone"], t);
    }
    void Lantern(Vector3 p, Transform t)
    {
        Material glow = Mat("Lantern silk", "#E76435", .25f, .5f), gold = palette["Brass"];
        Ball("Red lantern", p, new Vector3(.55f, .66f, .55f), glow, t);
        Cylinder("Lantern cap", p + Vector3.up * .32f, .16f, .065f, gold, t);
        Cylinder("Lantern tassel", p - Vector3.up * .48f, .025f, .3f, gold, t);
        Beam("Lantern cord", p + Vector3.up * .33f, p + Vector3.up * .8f, .013f, palette["Ink"], t);
    }
    void Tree(Vector3 p)
    {
        Transform t = Group("Golden ginkgo", p);
        Material bark = Mat("Ginkgo bark", "#685947"), leaf = Mat("Ginkgo gold", "#E5BC49"), leafLight = Mat("Ginkgo light", "#F3D56C");
        Box("Tree planter", new Vector3(0, .12f, 0), new Vector3(1.55f, .24f, 1.55f), palette["Ink"], t);
        Cylinder("Trunk", new Vector3(0, 2.2f, 0), .14f, 4.4f, bark, t);
        for (int i = 0; i < 7; i++)
        {
            Vector3 crown = new Vector3(R(-1.5f, 1.5f), R(4.2f, 6.3f), R(-1.3f, 1.3f));
            Beam("Branch", new Vector3(0, 2.5f, 0), crown, .065f, bark, t);
            Ball("Ginkgo crown", crown, new Vector3(R(2, 3.2f), R(1.6f, 2.5f), R(2, 3)), i % 2 == 0 ? leaf : leafLight, t);
        }
        for (int i = 0; i < 18; i++)
        {
            GameObject fallen = Box("Fallen leaf", new Vector3(R(-2, 2), .02f, R(-2, 2)), new Vector3(.1f, .008f, .16f), leaf, t);
            fallen.transform.localRotation = Quaternion.Euler(0, R(0, 360), 0);
        }
    }
    void Lamp(Vector3 p)
    {
        Transform t = Group("Street lantern", p); Material dark = palette["Ink"];
        Cylinder("Post", new Vector3(0, 2.15f, 0), .055f, 4.3f, dark, t);
        Box("Cross arm", new Vector3(0, 4.3f, 0), new Vector3(1.1f, .07f, .07f), dark, t);
        Box("Lamp glow", new Vector3(0, 4, 0), new Vector3(.38f, .5f, .38f), Mat("Lamp light", "#FFDA95", .3f, 1), t);
        Box("Lamp roof", new Vector3(0, 4.31f, 0), new Vector3(.7f, .12f, .7f), dark, t);
        GameObject light = new GameObject("Warm pool of light"); light.transform.SetParent(t, false); light.transform.localPosition = new Vector3(0, 3.6f, 0);
        Light l = light.AddComponent<Light>(); l.type = LightType.Point; l.color = new Color(1, .66f, .3f); l.intensity = 1.5f; l.range = 7; l.shadows = LightShadows.None;
    }
    void TeaTable(Vector3 p)
    {
        Transform t = Group("Sidewalk tea seating", p); Material wood = palette["Tea house timber"], white = palette["Ivory"];
        Cylinder("Round tea table", new Vector3(0, .75f, 0), .65f, .1f, wood, t);
        Cylinder("Table leg", new Vector3(0, .38f, 0), .12f, .75f, wood, t);
        for (int s = -1; s <= 1; s += 2)
        {
            Box("Bamboo chair seat", new Vector3(s, .4f, 0), new Vector3(.5f, .09f, .5f), palette["Brass"], t);
            Box("Bamboo chair back", new Vector3(s * 1.23f, .72f, 0), new Vector3(.06f, .65f, .5f), palette["Brass"], t);
            for (int j = -1; j <= 1; j += 2) for (int k = -1; k <= 1; k += 2)
                Cylinder("Chair leg", new Vector3(s + j * .19f, .2f, k * .19f), .024f, .4f, wood, t);
            Cylinder("Gaiwan cup", new Vector3(s * .27f, .86f, 0), .08f, .1f, white, t);
            Cylinder("Gaiwan lid", new Vector3(s * .27f, .93f, 0), .095f, .025f, white, t);
        }
        Ball("Teapot", new Vector3(0, .9f, .25f), new Vector3(.23f, .2f, .23f), white, t);
    }
    void Panda(Vector3 p)
    {
        Transform t = Group("Panda public art", p, 28); Material black = palette["Ink"], white = palette["Ivory"];
        Cylinder("Panda plinth", new Vector3(0, .16f, 0), 1.2f, .32f, palette["Warm stone"], t);
        Ball("Panda body", new Vector3(0, 1.05f, 0), new Vector3(1.45f, 1.55f, 1.1f), white, t);
        Ball("Panda head", new Vector3(0, 2.13f, -.12f), new Vector3(1.45f, 1.22f, 1.1f), white, t);
        for (int s = -1; s <= 1; s += 2)
        {
            Ball("Ear", new Vector3(s * .52f, 2.66f, -.08f), Vector3.one * .46f, black, t);
            GameObject eye = Ball("Eye patch", new Vector3(s * .3f, 2.18f, -.6f), new Vector3(.31f, .43f, .1f), black, t); eye.transform.localRotation = Quaternion.Euler(0, 0, s * -22);
            Ball("Eye glint", new Vector3(s * .28f, 2.22f, -.657f), Vector3.one * .07f, white, t);
            Ball("Foot", new Vector3(s * .46f, .55f, -.42f), new Vector3(.59f, .49f, .7f), black, t);
            Ball("Arm", new Vector3(s * .71f, 1.3f, -.1f), new Vector3(.42f, .83f, .5f), black, t);
        }
        Ball("Nose", new Vector3(0, 1.98f, -.69f), new Vector3(.23f, .14f, .13f), black, t);
    }
    void Bicycle(Vector3 p)
    {
        Transform t = Group("Shared bicycle", p, 15); Material teal = Mat("Bicycle turquoise", "#39BEB0"), dark = palette["Ink"];
        for (int s = -1; s <= 1; s += 2)
        {
            GameObject wheel = Cylinder("Wheel", new Vector3(0, .34f, s * .52f), .32f, .06f, dark, t); wheel.transform.localRotation = Quaternion.Euler(0, 0, 90);
            GameObject hub = Cylinder("Wheel inset", new Vector3(0, .34f, s * .52f), .24f, .069f, palette["Warm stone"], t); hub.transform.localRotation = Quaternion.Euler(0, 0, 90);
            Beam("Frame", new Vector3(0, .34f, s * .52f), new Vector3(0, .78f, 0), .035f, teal, t);
        }
        Beam("Top tube", new Vector3(0, .78f, -.15f), new Vector3(0, .78f, .48f), .04f, teal, t);
        Beam("Handle stem", new Vector3(0, .34f, .52f), new Vector3(0, 1.02f, .44f), .025f, dark, t);
        Box("Handlebar", new Vector3(0, 1.02f, .44f), new Vector3(.5f, .05f, .05f), dark, t);
        Box("Saddle", new Vector3(0, .85f, -.15f), new Vector3(.25f, .06f, .3f), dark, t);
    }
    void Car(Vector3 p, float yaw, Material paint, bool taxi)
    {
        Transform t = Group(taxi ? "Chengdu taxi" : "Electric car", p, yaw);
        Box("Body", new Vector3(0, .65f, 0), new Vector3(1.8f, .65f, 4), paint, t);
        Box("Cabin", new Vector3(0, 1.14f, -.1f), new Vector3(1.6f, .6f, 2.05f), Mat("Car glass", "#294B58", .9f), t);
        Box("Roof", new Vector3(0, 1.49f, -.1f), new Vector3(1.62f, .1f, 2.1f), paint, t);
        for (int x = -1; x <= 1; x += 2) for (int z = -1; z <= 1; z += 2)
        {
            GameObject wheel = Cylinder("Tyre", new Vector3(x * .91f, .4f, z * 1.25f), .36f, .16f, palette["Ink"], t); wheel.transform.localRotation = Quaternion.Euler(0, 0, 90);
            Box("Car light", new Vector3(x * .62f, .73f, z * 2.01f), new Vector3(.4f, .17f, .05f), z == 1 ? palette["Ivory"] : palette["Chilli red"], t);
        }
        if (taxi) Box("Taxi roof sign", new Vector3(0, 1.68f, 0), new Vector3(.6f, .25f, .3f), palette["Brass"], t);
    }
    void Person(Vector3 p, int i)
    {
        Transform t = Group("Strolling pedestrian", p, R(0, 360));
        Material clothes = Mat("Outfit " + i % 4, new[] { "#517C78", "#C3794B", "#D7C59F", "#796274" }[i % 4]), dark = palette["Ink"];
        Shape("Coat", PrimitiveType.Capsule, new Vector3(0, 1.03f, 0), new Vector3(.42f, .42f, .3f), clothes, t);
        Ball("Head", new Vector3(0, 1.59f, 0), Vector3.one * .3f, Mat("Skin", "#C79877"), t);
        for (int s = -1; s <= 1; s += 2)
        {
            Beam("Leg", new Vector3(s * .1f, .78f, 0), new Vector3(s * .13f, .13f, s * .1f), .07f, dark, t);
            Beam("Arm", new Vector3(s * .22f, 1.25f, 0), new Vector3(s * .29f, .83f, .05f), .065f, clothes, t);
        }
    }
    void SetupLighting()
    {
        RenderSettings.ambientMode = AmbientMode.Trilight;
        RenderSettings.ambientSkyColor = new Color(.62f, .70f, .72f);
        RenderSettings.ambientEquatorColor = new Color(.53f, .49f, .4f);
        RenderSettings.ambientGroundColor = new Color(.23f, .28f, .29f);
        RenderSettings.fog = true; RenderSettings.fogMode = FogMode.ExponentialSquared;
        RenderSettings.fogColor = new Color(.68f, .75f, .74f); RenderSettings.fogDensity = .011f;
        Material sky = new Material(Shader.Find("Skybox/Procedural")) { name = "Chengdu evening sky" };
        sky.SetColor("_SkyTint", new Color(.57f, .65f, .69f)); sky.SetFloat("_AtmosphereThickness", 1.3f); sky.SetFloat("_Exposure", 1.1f);
        RenderSettings.skybox = sky;
        GameObject sun = new GameObject("Late afternoon sun"); sun.transform.SetParent(root); sun.transform.rotation = Quaternion.Euler(24, -38, 0);
        Light l = sun.AddComponent<Light>(); l.type = LightType.Directional; l.color = new Color(1, .79f, .54f); l.intensity = 1.25f;
        l.shadows = LightShadows.Soft; l.shadowStrength = .8f; RenderSettings.sun = l;
        QualitySettings.shadowDistance = 110; QualitySettings.shadows = ShadowQuality.All;
        QualitySettings.shadowResolution = ShadowResolution.High; QualitySettings.antiAliasing = 4; QualitySettings.pixelLightCount = 4;
    }
}
