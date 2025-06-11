using UnityEngine;
using System.Collections.Generic;

public class MonsterSpawner : MonoBehaviour
{
    [Header("Monster Prefabs")]
    public List<GameObject> monsterPrefabs; // Assign different monster prefabs in Inspector

    [Header("Spawn Settings")]
    public Transform spawnPoint; // Where monsters will appear
    public float spawnDelay = 1.0f;

    private GameObject currentMonster;

    public GameObject SpawnMonster(string monsterType)
    {
        if (currentMonster != null)
        {
            Destroy(currentMonster); // Destroy previous monster if exists
        }

        GameObject monsterToSpawn = GetMonsterPrefab(monsterType);
        if (monsterToSpawn == null)
        {
            Debug.LogError($"Monster prefab for type '{monsterType}' not found.");
            return null;
        }

        currentMonster = Instantiate(monsterToSpawn, spawnPoint.position, spawnPoint.rotation);
        Monster monsterComponent = currentMonster.GetComponent<Monster>();
        if (monsterComponent != null)
        {
            monsterComponent.SetRequiredGesture(monsterType); // Set the required gesture for the monster
        }
        Debug.Log($"Spawned monster: {monsterType}");
        return currentMonster;
    }

    private GameObject GetMonsterPrefab(string monsterType)
    {
        // A simple way to get a prefab by name. In a real game, you might use a dictionary
        // or a more robust asset management system.
        foreach (GameObject prefab in monsterPrefabs)
        {
            if (prefab.name.Equals(monsterType, System.StringComparison.OrdinalIgnoreCase))
            {
                return prefab;
            }
        }
        // Fallback if specific monster not found
        if (monsterPrefabs.Count > 0)
        {
            return monsterPrefabs[0]; // Return the first one as a default
        }
        return null;
    }

    public void DespawnCurrentMonster()
    {
        if (currentMonster != null)
        {
            Destroy(currentMonster);
            currentMonster = null;
            Debug.Log("Current monster despawned.");
        }
    }
} 