using UnityEngine;
using UnityEngine.SceneManagement;
using System.Collections.Generic;

public class ZoneManager : MonoBehaviour
{
    public static ZoneManager Instance { get; private set; }

    [System.Serializable]
    public class Zone
    {
        public string zoneName;
        public int zoneIndex;
        public string sceneName; // Scene to load for this zone
        public List<string> gestureCategories; // E.g., "Letters", "Numbers", "Greetings"
        public List<string> monstersInZone; // Specific monsters or gestures for this zone
    }

    public List<Zone> zones;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            // We don't destroy on load if this is the only manager between scenes
            // For now, let's assume it's created and managed per scene or by GameManager
        }
        else
        {
            Destroy(gameObject);
        }
    }

    public void SelectZone(int zoneIndex)
    {
        if (zoneIndex >= 0 && zoneIndex < zones.Count)
        {
            Zone selectedZone = zones[zoneIndex];
            Debug.Log($"Selected Zone: {selectedZone.zoneName}");
            GameManager.Instance.currentZone = selectedZone.zoneIndex; // Update GameManager
            
            // For now, directly load the game level scene for simplicity
            // In a more complex setup, ZoneManager would coordinate with LevelManager
            GameManager.Instance.LoadLevel(SceneManager.GetSceneByName(selectedZone.sceneName).buildIndex);
            
            // TODO: Pass relevant zone data (e.g., gesture categories, monster list) to LevelManager
        }
        else
        {
            Debug.LogError($"Invalid Zone Index: {zoneIndex}");
        }
    }

    // Method to get a zone by its index
    public Zone GetZone(int zoneIndex)
    {
        if (zoneIndex >= 0 && zoneIndex < zones.Count)
        {
            return zones[zoneIndex];
        }
        return null;
    }

    // Method to get a zone by its name
    public Zone GetZoneByName(string name)
    {
        return zones.Find(zone => zone.zoneName.Equals(name, System.StringComparison.OrdinalIgnoreCase));
    }
} 