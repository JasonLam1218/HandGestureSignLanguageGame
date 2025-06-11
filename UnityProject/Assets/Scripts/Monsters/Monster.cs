using UnityEngine;

public class Monster : MonoBehaviour
{
    [Header("Monster Settings")]
    public string requiredGesture; // The gesture needed to defeat this monster
    public float health = 100f;

    [Header("References")]
    public Animator monsterAnimator;

    private void Awake()
    {
        if (monsterAnimator == null)
        {
            monsterAnimator = GetComponent<Animator>();
        }
    }

    public void TakeDamage(float amount)
    {
        health -= amount;
        if (health <= 0)
        {
            Defeat();
        }
        // TODO: Update UI (e.g., monster health bar)
    }

    public void Defeat()
    {
        Debug.Log($"Monster {gameObject.name} defeated!");
        // TODO: Play defeat animation, sound, and trigger destruction or fading
        gameObject.SetActive(false); // For now, simply deactivate
    }

    public void SetRequiredGesture(string gesture)
    {
        requiredGesture = gesture;
        Debug.Log($"Monster {gameObject.name} now requires gesture: {requiredGesture}");
        // TODO: Update monster visual/text to show required gesture
    }

    // Example: Method to trigger attack animation
    public void Attack()
    {
        if (monsterAnimator != null)
        {
            monsterAnimator.SetTrigger("Attack");
        }
    }

    // Example: Method to trigger idle animation
    public void Idle()
    {
        if (monsterAnimator != null)
        {
            monsterAnimator.SetTrigger("Idle");
        }
    }
} 