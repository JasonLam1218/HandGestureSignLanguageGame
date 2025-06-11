using UnityEngine;
using UnityEngine.SceneManagement;
using System.Collections;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    [Header("Game Settings")]
    public int currentLevel = 1;
    public int currentZone = 0;
    public bool isGamePaused = false;

    [Header("References")]
    public GameObject playerPrefab;
    public Transform playerSpawnPoint;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void Start()
    {
        InitializeGame();
    }

    private void InitializeGame()
    {
        // Initialize game state
        currentLevel = 1;
        currentZone = 0;
        isGamePaused = false;

        // Spawn player if needed
        if (playerPrefab != null && playerSpawnPoint != null)
        {
            Instantiate(playerPrefab, playerSpawnPoint.position, playerSpawnPoint.rotation);
        }
    }

    public void LoadLevel(int levelIndex)
    {
        StartCoroutine(LoadLevelAsync(levelIndex));
    }

    private IEnumerator LoadLevelAsync(int levelIndex)
    {
        AsyncOperation asyncLoad = SceneManager.LoadSceneAsync(levelIndex);
        
        while (!asyncLoad.isDone)
        {
            // Update loading progress
            float progress = Mathf.Clamp01(asyncLoad.progress / 0.9f);
            Debug.Log($"Loading progress: {progress * 100}%");
            yield return null;
        }
    }

    public void PauseGame()
    {
        isGamePaused = true;
        Time.timeScale = 0f;
    }

    public void ResumeGame()
    {
        isGamePaused = false;
        Time.timeScale = 1f;
    }

    public void GameOver()
    {
        // Handle game over logic
        Debug.Log("Game Over!");
        // TODO: Implement game over UI and restart logic
    }

    public void LevelComplete()
    {
        // Handle level completion
        Debug.Log($"Level {currentLevel} Complete!");
        currentLevel++;
        // TODO: Implement level completion UI and next level loading
    }

    public void ChangeZone(int zoneIndex)
    {
        currentZone = zoneIndex;
        // TODO: Implement zone change logic
    }
} 