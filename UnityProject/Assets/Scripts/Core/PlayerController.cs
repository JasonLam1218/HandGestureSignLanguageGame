using UnityEngine;

public class PlayerController : MonoBehaviour
{
    [Header("Player Settings")]
    public float moveSpeed = 5.0f;

    private Rigidbody rb;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
        if (rb == null)
        {
            Debug.LogWarning("Rigidbody not found on PlayerController. Adding one.");
            rb = gameObject.AddComponent<Rigidbody>();
        }
        rb.useGravity = false; // Player movement will be controlled manually
    }

    private void Update()
    {
        // Example: Basic keyboard input for movement
        float moveHorizontal = Input.GetAxis("Horizontal");
        float moveVertical = Input.GetAxis("Vertical");

        Vector3 movement = new Vector3(moveHorizontal, 0.0f, moveVertical);
        rb.velocity = movement * moveSpeed;

        // TODO: Integrate with UI/Touch input for zone selection movement
    }

    private void OnTriggerEnter(Collider other)
    {
        // Example: Collision with a zone gate
        if (other.CompareTag("ZoneGate"))
        {
            Debug.Log("Player entered a Zone Gate!");
            // TODO: Trigger zone selection logic or scene transition
        }
        // TODO: Handle collision with monsters or other game elements
    }

    public void MoveToZone(Vector3 targetPosition)
    {
        // TODO: Implement smooth movement to a selected zone in ZoneSelection scene
        transform.position = targetPosition; // Instant teleport for now
    }
} 