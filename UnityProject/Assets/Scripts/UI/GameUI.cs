using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class GameUI : MonoBehaviour
{
    [Header("UI Elements")]
    public TextMeshProUGUI monsterText;
    public TextMeshProUGUI feedbackText;
    public Slider healthBar;
    public Button pauseButton;

    private void Start()
    {
        pauseButton.onClick.AddListener(OnPauseButtonClicked);
        UpdateHealthBar(1.0f); // Initialize health bar to full
        UpdateFeedbackText(""); // Clear feedback initially
    }

    public void UpdateMonsterText(string gestureName)
    {
        if (monsterText != null)
        {
            monsterText.text = $"Show: {gestureName}";
        }
    }

    public void UpdateFeedbackText(string message, Color color = default)
    {
        if (feedbackText != null)
        {
            feedbackText.text = message;
            if (color != default) // Apply color if provided
            {
                feedbackText.color = color;
            }
            // TODO: Implement fading effect for feedback text
        }
    }

    public void UpdateHealthBar(float normalizedHealth)
    {
        if (healthBar != null)
        {
            healthBar.value = normalizedHealth;
        }
    }

    private void OnPauseButtonClicked()
    {
        Debug.Log("Pause Button Clicked!");
        GameManager.Instance.PauseGame();
        // TODO: Show pause menu UI
    }

    // Call this from LevelManager when gesture is correct
    public void ShowCorrectFeedback()
    {
        UpdateFeedbackText("CORRECT!", Color.green);
    }

    // Call this from LevelManager when gesture is incorrect
    public void ShowIncorrectFeedback()
    {
        UpdateFeedbackText("TRY AGAIN!", Color.red);
    }

    // Call this from LevelManager when time runs out
    public void ShowTimeoutFeedback()
    {
        UpdateFeedbackText("TIME OUT!", Color.yellow);
    }
} 