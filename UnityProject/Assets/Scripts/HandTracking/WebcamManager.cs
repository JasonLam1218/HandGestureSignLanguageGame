using UnityEngine;
using System;

public class WebcamManager : MonoBehaviour
{
    public static WebcamManager Instance { get; private set; }

    [Header("Webcam Settings")]
    public int requestedWidth = 640;
    public int requestedHeight = 480;
    public int requestedFPS = 30;

    private WebCamTexture webcamTexture;
    private bool isWebcamReady = false;

    // Event to notify when webcam texture is updated
    public event Action<WebCamTexture> OnWebcamTextureUpdated;

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

    private void Start()
    {
        InitializeWebcam();
    }

    private void InitializeWebcam()
    {
        WebCamDevice[] devices = WebCamTexture.devices;
        if (devices.Length == 0)
        {
            Debug.LogError("No webcam found!");
            isWebcamReady = false;
            return;
        }

        WebCamDevice selectedCam = devices[0]; // Default to the first available camera
        bool camFound = false;

        // 1. Try to find a specific built-in macOS camera (e.g., MacBook's camera)
        string[] macBuiltInCameraNames = {"FaceTime HD Camera", "iSight Camera", "Built-in iSight", "Apple Camera"};

        foreach (var camDevice in devices)
        {
            foreach (string name in macBuiltInCameraNames)
            {
                if (camDevice.name.Contains(name))
                {
                    selectedCam = camDevice;
                    camFound = true;
                    Debug.Log($"Selected built-in Mac camera: {selectedCam.name}");
                    break; // Found a built-in Mac camera, stop searching
                }
            }
            if (camFound) break;
        }

        // 2. If no specific Mac camera found, try to find any front-facing camera (original logic)
        if (!camFound)
        {
            foreach (var camDevice in devices)
            {
                if (camDevice.isFrontFacing)
                {
                    selectedCam = camDevice;
                    camFound = true;
                    Debug.Log($"Selected front-facing camera (fallback): {selectedCam.name}");
                    break;
                }
            }
        }
        
        // 3. If still no suitable camera, use the default (first available device)
        if (!camFound && devices.Length > 0)
        {
             Debug.Log($"No specific built-in or front-facing camera found, using default: {selectedCam.name}");
        }
        else if (!camFound && devices.Length == 0)
        {
            Debug.LogError("No camera devices available to select.");
            isWebcamReady = false;
            return;
        }

        webcamTexture = new WebCamTexture(selectedCam.name, requestedWidth, requestedHeight, requestedFPS);
        webcamTexture.Play();

        if (webcamTexture.isPlaying)
        {
            isWebcamReady = true;
            Debug.Log($"Webcam initialized: {webcamTexture.deviceName} ({webcamTexture.width}x{webcamTexture.height}@{webcamTexture.requestedFPS}fps)");
        }
        else
        {
            Debug.LogError("Failed to start webcam.");
            isWebcamReady = false;
        }
    }

    private void Update()
    {
        if (isWebcamReady && webcamTexture.isPlaying)
        {
            // Notify listeners that the webcam texture has updated
            OnWebcamTextureUpdated?.Invoke(webcamTexture);
        }
    }

    public WebCamTexture GetWebcamTexture()
    {
        return webcamTexture;
    }

    public bool IsWebcamReady()
    {
        return isWebcamReady;
    }

    private void OnApplicationQuit()
    {
        if (webcamTexture != null && webcamTexture.isPlaying)
        {
            webcamTexture.Stop();
            WebCamTexture.Destroy(webcamTexture);
        }
    }
} 