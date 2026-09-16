using UnityEngine;

public sealed class StreetCamera : MonoBehaviour
{
    public float speed = 7f;
    Vector3 home;
    Quaternion homeRotation;
    float yaw, pitch;
    bool orbit;
    void Start() { home = transform.position; homeRotation = transform.rotation; SyncAngles(); }
    void SyncAngles() { yaw = transform.eulerAngles.y; pitch = Mathf.DeltaAngle(0, transform.eulerAngles.x); }
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Tab)) orbit = !orbit;
        if (Input.GetKeyDown(KeyCode.Escape)) { orbit = false; Cursor.lockState = CursorLockMode.None; Cursor.visible = true; }
        if (Input.GetKeyDown(KeyCode.R)) { orbit = false; transform.SetPositionAndRotation(home, homeRotation); SyncAngles(); }
        if (orbit)
        {
            float t = Time.time * .075f;
            transform.position = new Vector3(Mathf.Sin(t) * 32, 18, 10 - Mathf.Cos(t) * 40);
            transform.LookAt(new Vector3(0, 3, 12));
            SyncAngles();
            return;
        }
        if (Input.GetMouseButton(1))
        {
            yaw += Input.GetAxis("Mouse X") * 2;
            pitch = Mathf.Clamp(pitch - Input.GetAxis("Mouse Y") * 2, -85, 85);
            transform.rotation = Quaternion.Euler(pitch, yaw, 0);
        }
        Vector3 move = Vector3.zero;
        if (Input.GetKey(KeyCode.W)) move += transform.forward;
        if (Input.GetKey(KeyCode.S)) move -= transform.forward;
        if (Input.GetKey(KeyCode.A)) move -= transform.right;
        if (Input.GetKey(KeyCode.D)) move += transform.right;
        if (Input.GetKey(KeyCode.E)) move += Vector3.up;
        if (Input.GetKey(KeyCode.Q)) move -= Vector3.up;
        transform.position += Vector3.ClampMagnitude(move, 1) * speed * (Input.GetKey(KeyCode.LeftShift) ? 2.5f : 1) * Time.deltaTime;
        Vector3 p = transform.position;
        p.y = Mathf.Clamp(p.y, 1.1f, 65);
        transform.position = p;
    }
    void OnGUI()
    {
        GUI.color = new Color(.05f, .10f, .12f, .86f);
        GUI.DrawTexture(new Rect(22, 22, 325, 89), Texture2D.whiteTexture);
        GUI.color = new Color(1, .85f, .53f);
        GUI.Label(new Rect(38, 32, 300, 24), "C H E N G D U   /   GOLDEN HOUR");
        GUI.color = Color.white;
        GUI.Label(new Rect(38, 57, 310, 24), "WASD move  |  RMB look  |  Q / E down / up");
        GUI.Label(new Rect(38, 79, 310, 24), "Shift fast  |  Tab orbit  |  R reset");
    }
}
