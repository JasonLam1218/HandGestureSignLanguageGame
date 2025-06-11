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

        // Find a suitable webcam
        WebCamDevice frontCam = WebCamTexture.devices[0]; // Default to first available
        foreach (var camDevice in WebCamTexture.devices)
        {
            if (camDevice.isFrontFacing)
            {
                frontCam = camDevice;
                break;
            }
        }

        webcamTexture = new WebCamTexture(frontCam.name, requestedWidth, requestedHeight, requestedFPS);
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