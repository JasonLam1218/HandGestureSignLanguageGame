using UnityEngine;
using System.Collections.Generic;

public class LevelManager : MonoBehaviour
{
    public static LevelManager Instance { get; private set; }

    [Header("Level Settings")]
    public List<string> monsterQueue; // List of monsters for the current level
    public int currentMonsterIndex = 0;
    public float gestureMatchTimeLimit = 5.0f; // Time limit to match gesture

    [Header("References")]
    public MonsterSpawner monsterSpawner;
    public HandGestureDetector gestureDetector;
    public GameUI gameUI;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void OnEnable()
    {
        if (gestureDetector != null)
        {
            gestureDetector.OnGestureDetected += HandleGestureDetected;
        }
    }

    private void OnDisable()
    {
        if (gestureDetector != null)
        {
            gestureDetector.OnGestureDetected -= HandleGestureDetected;
        }
    }

    public void StartLevel(List<string> monsters)
    {
        monsterQueue = new List<string>(monsters);
        currentMonsterIndex = 0;
        SpawnNextMonster();
        // TODO: Start level timer if any
    }

    private void SpawnNextMonster()
    {
        if (currentMonsterIndex < monsterQueue.Count)
        {
            string monsterType = monsterQueue[currentMonsterIndex];
            monsterSpawner.SpawnMonster(monsterType); // Assumes MonsterSpawner handles actual monster prefab creation
            gameUI.UpdateMonsterText(monsterType); // Display the required gesture
            // TODO: Start countdown for gesture match
        }
        else
        {
            Debug.Log("All monsters defeated! Level Complete.");
            GameManager.Instance.LevelComplete();
        }
    }

    private void HandleGestureDetected(string detectedGesture)
    {
        Debug.Log($"Detected gesture: {detectedGesture}");
        if (currentMonsterIndex < monsterQueue.Count)
        {
            string requiredGesture = monsterQueue[currentMonsterIndex];
            if (detectedGesture.Equals(requiredGesture, System.StringComparison.OrdinalIgnoreCase))
            {
                Debug.Log("Correct gesture! Monster defeated.");
                // TODO: Play monster defeat animation/sound
                currentMonsterIndex++;
                SpawnNextMonster();
            }
            else
            {
                Debug.Log("Incorrect gesture. Try again.");
                // TODO: Provide feedback to user (e.g., shake monster, error sound)
            }
        }
    }

    // TODO: Implement timer for gesture match failure
    // public void GestureTimeOut()
    // {
    //     Debug.Log("Time out! Gesture not matched.");
    //     GameManager.Instance.GameOver(); // Or some other penalty
    // }
} 