using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using TMPro;

public class LevelCompleteUI : MonoBehaviour
{
    [Header("UI Elements")]
    public TextMeshProUGUI levelCompleteText;
    public Button nextLevelButton;
    public Button returnToZoneSelectionButton;

    [Header("Scene Names")]
    public string zoneSelectionSceneName = "ZoneSelection";

    private void Start()
    {
        nextLevelButton.onClick.AddListener(OnNextLevelButtonClicked);
        returnToZoneSelectionButton.onClick.AddListener(OnReturnToZoneSelectionButtonClicked);
    }

    public void ShowLevelComplete(int levelNumber)
    {
        gameObject.SetActive(true);
        if (levelCompleteText != null)
        {
            levelCompleteText.text = $"Level {levelNumber} Complete!";
        }
        // TODO: Check if there is a next level in the current zone
        // If no more levels, hide nextLevelButton or change its text
    }

    public void HideLevelComplete()
    {
        gameObject.SetActive(false);
    }

    private void OnNextLevelButtonClicked()
    {
        Debug.Log("Next Level Button Clicked!");
        // GameManager.Instance.LoadNextLevel(); // Assuming GameManager handles loading next level
        // For now, let's just reload the current game scene for testing
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

    private void OnReturnToZoneSelectionButtonClicked()
    {
        Debug.Log("Return to Zone Selection Button Clicked!");
        SceneManager.LoadScene(zoneSelectionSceneName);
    }
} 