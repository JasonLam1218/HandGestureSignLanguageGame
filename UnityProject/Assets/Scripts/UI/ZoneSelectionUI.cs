using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections.Generic;

public class ZoneSelectionUI : MonoBehaviour
{
    [Header("UI Elements")]
    public GameObject zoneButtonPrefab;
    public Transform zoneButtonParent;
    public Button backButton;

    private void Start()
    {
        backButton.onClick.AddListener(OnBackButtonClicked);
        GenerateZoneButtons();
    }

    private void GenerateZoneButtons()
    {
        // Clear existing buttons if any
        foreach (Transform child in zoneButtonParent)
        {
            Destroy(child.gameObject);
        }

        if (ZoneManager.Instance == null)
        {
            Debug.LogError("ZoneManager not found! Make sure it exists in the scene.");
            return;
        }

        List<ZoneManager.Zone> zones = ZoneManager.Instance.zones;

        for (int i = 0; i < zones.Count; i++)
        {
            ZoneManager.Zone zone = zones[i];
            GameObject buttonGO = Instantiate(zoneButtonPrefab, zoneButtonParent);
            buttonGO.name = $"ZoneButton_{zone.zoneName}";

            Button button = buttonGO.GetComponent<Button>();
            TextMeshProUGUI buttonText = buttonGO.GetComponentInChildren<TextMeshProUGUI>();

            if (buttonText != null)
            {
                buttonText.text = zone.zoneName;
            }

            int zoneIndex = i; // Capture current index for the lambda
            button.onClick.AddListener(() => OnZoneButtonClicked(zoneIndex));
        }
    }

    private void OnZoneButtonClicked(int zoneIndex)
    {
        Debug.Log($"Zone {zoneIndex} selected!");
        if (ZoneManager.Instance != null)
        {
            ZoneManager.Instance.SelectZone(zoneIndex);
        }
    }

    private void OnBackButtonClicked()
    {
        Debug.Log("Back Button Clicked!");
        UnityEngine.SceneManagement.SceneManager.LoadScene("MainMenu");
    }
} 