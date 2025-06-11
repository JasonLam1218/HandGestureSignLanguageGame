using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class MainMenuUI : MonoBehaviour
{
    public Button startButton;
    public Button settingsButton;
    public Button quitButton;

    [Header("Scene Names")]
    public string zoneSelectionSceneName = "ZoneSelection";

    private void Start()
    {
        startButton.onClick.AddListener(OnStartButtonClicked);
        settingsButton.onClick.AddListener(OnSettingsButtonClicked);
        quitButton.onClick.AddListener(OnQuitButtonClicked);
    }

    private void OnStartButtonClicked()
    {
        Debug.Log("Start Button Clicked!");
        SceneManager.LoadScene(zoneSelectionSceneName);
    }

    private void OnSettingsButtonClicked()
    {
        Debug.Log("Settings Button Clicked!");
        // TODO: Implement settings panel
    }

    private void OnQuitButtonClicked()
    {
        Debug.Log("Quit Button Clicked!");
#if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
#else
        Application.Quit();
#endif
    }
} 